# Android USB-C Microphones

A small open dataset on how USB microphones behave when plugged into Android phones: which phone, which
mic, whether it was connected directly or through an adapter, and whether the connection held.

USB mics need no special app permission on Android. Android's own USB audio support lists them as normal
inputs, so any app with microphone access can use them. Whether the link stays up is another matter, and
that is what this records.

## Results

| Date | Phone | Mic | Connection | Recognised | Observed | Drops that reconnected within 2 s | Stability |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-06 | OnePlus Nord 3, Android 16 | Jabra Evolve 30 II (`0b0e:0314`) | Adapter: USB-C to USB-A female | Yes | 89 min | 12 | Flaky from the start |
| 2026-11-06 | OnePlus Nord 3, Android 16 | Yealink BH70 (`6993:b21a`) | Direct: Baseus USB-C cable | Yes | 16.5 min | 0 | Stable, confirmed by the tester |

The Jabra's connections had a median length of 30.5 seconds and the shortest lasted 8 seconds. Two long
ones lasted 24 and 34 minutes. It worked as a mic between drops. The test does not show whether the
adapter, the cable or the phone's power output causes them, because the two tests differ in both mic and
connection.

Both mics deliver audio at 48 kHz, but neither carries speech above about 8 kHz. That limit is in the
headsets, not in Android or the app: no processing was switched on and the phone captured at 48 kHz. They
suit speech recognition well. For work that needs the full band, such as voice cloning, they carry no more
detail than a 16 kHz recording.

## Files

- `data/results.csv`: one row per test. This is the dataset.
- `data/sessions/<test_id>.csv`: one row per USB connection in a test.
- `scripts/usb_sessions.py`: builds a sessions file from the phone's USB log.

## Add a test

1. Plug in the mic and use it normally for at least 30 minutes.
2. Save the sessions, using the USB ID shown by `adb shell dumpsys usb`:

   ```bash
   adb shell dumpsys usb | scripts/usb_sessions.py --id 0b0e:0314 > data/sessions/<test_id>.csv
   ```

   Android keeps only the last 32 USB events, so do this soon after the test.
3. Read the name and type Android gives the mic:

   ```bash
   adb shell dumpsys media.audio_policy | sed -n '/Available input devices/,/Available output/p'
   ```

4. Add a row to `data/results.csv`.

## Fields in `results.csv`

| Field | Meaning |
| --- | --- |
| `connection` | `direct`, `adapter` or `unconfirmed` |
| `adapter` | The adapter used, if any |
| `android_product_name` | The mic's name as Android reports it |
| `android_input_type` | Android's device type, such as `usb_headset` or `usb_device` |
| `recognised_as_input` | Android listed it as a mic |
| `records_in_app` | An app recorded from it |
| `observed_seconds` | From the first connection to the last event logged |
| `connections` | USB connections in that time |
| `quick_reconnects` | Connections that came back within 2 seconds of a drop, which a person unplugging is unlikely to cause |
| `capture_rate_hz` | The rate Android captured at |
| `audio_band_limit_hz` | Where the speech energy stops, measured from recordings |
| `stability` | The tester's summary |

A disconnect with a longer gap may just be someone unplugging the mic, so it isn't counted as a drop.

## Licence

CC BY 4.0, see `LICENSE`.
