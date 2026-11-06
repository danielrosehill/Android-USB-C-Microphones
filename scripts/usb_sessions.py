#!/usr/bin/env python3
"""Turn the phone's USB connection log into one CSV row per connection.

    adb shell dumpsys usb | scripts/usb_sessions.py [--id 0b0e:0314] > data/sessions/<test>.csv

A summary goes to stderr. Android keeps only the last 32 connect and disconnect events, so run this
soon after a test. Times are the laptop's local time zone, so pass TZ if it differs from the phone's.
"""
import argparse
import csv
import datetime as dt
import re
import statistics
import sys

QUICK_SECONDS = 2  # a return this fast is the link dropping, not someone unplugging

EVENT = re.compile(
    r"device_address=(\S+)\s+mode=(-?\d+)\s+timestamp=(\d+)"
    r"(?:\s+manufacturer=(\d+)\s+product=(\d+)(?:\s+is_headset=\{\s+in=(\w+)\s+out=(\w+))?)?"
)


def sessions(text):
    """Pairs each connect (mode 0) with the next disconnect (mode -1) at the same address."""
    events = sorted(set(EVENT.findall(text)), key=lambda e: int(e[2]))
    live, done = {}, []
    for address, mode, ts, vendor, product, has_in, has_out in events:
        seconds = int(ts) / 1000
        if mode == "0":
            live[address] = {
                "usb_id": f"{int(vendor):04x}:{int(product):04x}",
                "start": seconds,
                "end": None,
                "input": has_in,
                "output": has_out,
            }
            done.append(live[address])
        elif address in live:
            live.pop(address)["end"] = seconds
    return done


def stamp(seconds):
    return dt.datetime.fromtimestamp(seconds).astimezone().isoformat(timespec="seconds")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", help="keep one device, as vendor:product in hex")
    args = ap.parse_args()
    rows = [s for s in sessions(sys.stdin.read()) if not args.id or s["usb_id"] == args.id]

    out = csv.writer(sys.stdout, lineterminator="\n")
    out.writerow(["usb_id", "connected", "disconnected", "seconds", "gap_before_seconds", "android_input", "android_output"])
    gaps, durations = [], []
    previous_end = None
    for s in rows:
        length = None if s["end"] is None else round(s["end"] - s["start"])
        gap = None if previous_end is None else round(s["start"] - previous_end)
        out.writerow([s["usb_id"], stamp(s["start"]), "" if s["end"] is None else stamp(s["end"]),
                      "" if length is None else length, "" if gap is None else gap, s["input"], s["output"]])
        if gap is not None:
            gaps.append(gap)
        if length is not None:
            durations.append(length)
        previous_end = s["end"]

    quick = sum(g <= QUICK_SECONDS for g in gaps)
    median = statistics.median(durations) if durations else "n/a"
    print(f"connections={len(rows)} ended={len(durations)} quick_reconnects={quick} median_seconds={median}", file=sys.stderr)


if __name__ == "__main__":
    main()
