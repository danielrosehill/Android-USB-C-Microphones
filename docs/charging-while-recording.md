# Using a USB mic while charging the phone

Can a hub on a phone's only USB-C port run a mic and charge the phone at full speed? Researched 2026-11-06.
**Nothing here has been tested for this dataset yet.**

## Short answer

Yes on some phones, no on others, and expect slower charging. A hub with a charging input is a real setup, but
it needs the phone to act as USB host while receiving power, which not every phone does. Phones with their own
fast-charging system will probably fall back to a much slower standard rate. No source tested this exact setup,
so treat each phone and hub as unknown until it's tried.

## Why it depends on the phone

USB-C treats data and power as separate roles. To use a mic the phone must be the data host. To charge, it must
take power at the same time. The [Linux USB-C interface](https://android.googlesource.com/kernel/common/+/ec03510e0a778/Documentation/ABI/testing/sysfs-class-typec)
that Android uses reports the two separately, but we found no source saying Android phones in general support
this combination.

User reports differ:

- A [Fairphone 3 owner](https://forum.fairphone.com/t/using-usb-headphones-via-a-usb-c-hub/78649) found USB audio
  failed with a powered hub, and worked unpowered, but then the phone didn't register as charging.
- [Plugable support](https://support.plugable.com/t/is-there-a-way-to-power-android-phone-samsung-galaxy-at-the-same-time-as-using-this-adapter/17621)
  says some phones allow only one function on the port at a time.
- In a [Digirig thread](https://forum.digirig.net/t/digirig-lite-1-2-not-recognized-on-google-pixel-8/4125?page=2)
  on a USB audio device, a hub helped on some Pixels and failed on a Pixel 9 and a Samsung S24 Ultra.

The OnePlus Nord 3 tested here reports a dual-role port (`supported_modes=dual`). With nothing attached,
`can_change_data_role` and `can_change_power_role` read false. That doesn't settle whether it can do both at once.

## What charging speed to expect

| | Figure | Source |
| --- | --- | --- |
| Nord 3 with its own 80W SUPERVOOC charger | 95% in 30 minutes | [Pokde review](https://pokde.net/review/oneplus-nord-3-review) |
| OnePlus 10 Pro: own charger, 5 to 100% | About 37 minutes | [Digital Trends](https://www.digitaltrends.com/mobile/oneplus-10-pro-super-vooc-vs-usb-pd-charging-review) |
| OnePlus 10 Pro: 100W third-party USB PD charger | 1 hour 30 minutes | Same |
| Recent OnePlus phones on USB PD | Roughly 18 to 27 W (secondary sources) | [Smartprix](https://www.smartprix.com/bytes/from-warp-to-supervooc-did-oneplus-downgrade-charger-quality/) |

- **SUPERVOOC through a hub:** not confirmed anywhere. It relies on a handshake between phone, charger and cable,
  so plan on USB PD speed at best.
- **The Nord 3's own USB PD rate:** not found. Measure it with a USB power meter.
- **Hub overhead:** hubs keep some power for themselves, commonly 10 to 15 W.
- **Worst case:** one [Pixel user](https://m.androidcentral.com/best-2-1-usb-type-c-adapter-googles-pixel-2)
  reported only 5 V at 1.5 A through a hub.

## Options

| Setup | Why | Evidence |
| --- | --- | --- |
| Mic or receiver with its own USB-C charging port, such as the [Hollyland LARK A1 USB-C receiver](https://www.bhphotovideo.com/c/product/1895900-REG/hollyland_hl_lark_a1_usb_c_receiver_gray_lark_a1_wireless_receiver.html/overview) | No hub, one less thing to negotiate | Seller claims only |
| USB-C hub with PD input and a separate data port, such as the Anker 332 or Satechi USB-C Hub Mobile | Works with any USB mic | Laptop hubs. No test with a phone and mic found |
| Wired mic on battery power, phone charged between sessions | Nothing extra to fail | The setup tested in `data/results.csv` |

On a hub, plug the mic into a data port. A hub's [PD port may be charging-only](https://www.lention.com/blogs/news/usb-microphone-not-working-through-usbc-hub).

The Shure MV7+ documents pass-through charging only for iOS.

## Audio risks

- **Hum or whine:** USB power and audio can share a ground path, and charger noise can become audible.
  [Ulanzi's guide](https://www.ulanzi.com/blogs/knowledges/camera-audio-buzzing-power-bank-fix) suggests comparing
  a recording on battery with one on charge. Keep the power cable away from the mic cable.
- **Dropouts:** a hub that resets disconnects everything on it at once. We found no Android report of a mic
  dropping this way, or of overheating, so both are open questions.

## Test plan

If a hub is added to this dataset, record:

1. Whether the mic appears as an input with the charger connected, and in which plug order.
2. Charging power with a USB power meter, during a take.
3. Whether a take survives plugging in and removing the charger.
4. Noise floor on charge against battery.
5. Connection stability over 30 minutes, logged with `scripts/usb_sessions.py`.
