# USB-C microphones for Android: a market sample

A sample of well-reviewed products as of 2026-11-06, not a complete list. The data, with a source for each
claim, is in [`data/products.csv`](../data/products.csv).

## The baseline

Every product is checked against two rules:

1. It reaches the phone with a male USB-C plug as supplied, with no adapter.
2. There is evidence that it works on Android.

Run the check with `scripts/validate_products.py`. A product that fails stays on the list, so the reason is
on record.

Android evidence is graded, strongest first:

| Grade | Meaning |
| --- | --- |
| `tested-here` | Tested for this dataset (see `data/results.csv`) |
| `manufacturer-stated` | The maker says it works on Android, which is a claim, not a test |
| `independent-report` | A review or buyer reports it working |
| `unverified` | No evidence found |

## Passing products

| Use | Product | Evidence | Approx. USD | Stated frequency response |
| --- | --- | --- | --- | --- |
| Dictation | Yealink BH70 | Tested here | Not found | Measured: about 8 kHz |
| Dictation | Poly Blackwire 3320 | Manufacturer | $57 | 100 Hz to 10 kHz |
| Dictation | Jabra Evolve2 30 SE | Manufacturer | $94 | Not published |
| Dictation | EPOS ADAPT 160 USB II | Manufacturer, "device dependent" | $79 | 100 Hz to 8 kHz |
| Podcast | Shure MV7+ | Manufacturer, Android 12 or later | $279 | 50 Hz to 16 kHz |
| Podcast | Rode PodMic USB | Manufacturer | Not found | Not found |
| Podcast | Audio-Technica ATR2100x-USB | Buyer reports | $79 | 50 Hz to 15 kHz |

Prices are approximate, some are undated, and none is a live price or a claim about stock.

## Reading this list

- **Dictation headsets have little independent data.** Reviews are scarce, and Android support mostly rests on
  what manufacturers say. Only the Poly and Jabra name mobile use clearly.
- **A headset's stated range doesn't show what it records.** Both headsets tested here deliver 48 kHz files
  with no speech above about 8 kHz, and no office headset publishes its real mic bandwidth. That is fine for
  dictation. For voice cloning or podcasting, measure it first.
- **Check the box contents.** Several good mics fail only because they ship with a USB-A cable. A USB-C to USB-C
  cable may fix that, but it hasn't been tested here.
- **Not every Android phone will work.** Shure and Jabra both warn about this.
