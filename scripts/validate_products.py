#!/usr/bin/env python3
"""Check products in data/products.csv against the baseline for a USB mic on Android.

    scripts/validate_products.py [data/products.csv]

Baseline, every product:
  1. Reaches the phone with a male USB-C plug as supplied, with no adapter.
  2. Android support has evidence: tested here, stated by the manufacturer, or independently reported.

A product can be listed without passing, so a known failure stays on record. Exits 1 if a row is malformed.
"""
import csv
import sys

USE_CASES = {"dictation", "podcast"}
USB_C_PLUG = {"usb-c-fixed", "usb-c-detachable", "usb-c-cable-type-unknown"}
CONNECTORS = USB_C_PLUG | {"usb-c-unconfirmed", "usb-c-adapter-needed", "usb-a-only"}
EVIDENCE = {"tested-here", "manufacturer-stated", "independent-report", "unverified"}
REQUIRED = ["product", "use_case", "connector", "android_evidence", "android_source", "approx_price_usd", "price_source", "price_date"]


def problems(row):
    """What is malformed in a row: a missing field or an unknown value."""
    out = [f"missing {k}" for k in REQUIRED if not row.get(k, "").strip()]
    for field, allowed in (("use_case", USE_CASES), ("connector", CONNECTORS), ("android_evidence", EVIDENCE)):
        value = row.get(field, "").strip()
        if value and value not in allowed:
            out.append(f"{field} is {value!r}, expected one of {sorted(allowed)}")
    return out


def baseline_failures(row):
    """Why a well-formed row misses the baseline."""
    out = []
    if row["connector"] not in USB_C_PLUG:
        out.append("no male USB-C plug as supplied")
    if row["android_evidence"] == "unverified":
        out.append("no evidence of Android support")
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/products.csv"
    rows = list(csv.DictReader(open(path, newline="")))
    malformed = 0
    for row in rows:
        name = row.get("product") or "(no name)"
        bad = problems(row)
        if bad:
            malformed += 1
            print(f"MALFORMED  {name}: {'; '.join(bad)}")
            continue
        fails = baseline_failures(row)
        print(f"{'FAIL' if fails else 'PASS'}  {row['use_case']:9s} {row['android_evidence']:19s} {name}" + (f": {'; '.join(fails)}" if fails else ""))
    print(f"{len(rows)} products, {malformed} malformed")
    return 1 if malformed else 0


if __name__ == "__main__":
    sys.exit(main())
