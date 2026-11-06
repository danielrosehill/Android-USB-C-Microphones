# Recording from a USB mic on unrooted Android

Can you use a USB-C mic on an unrooted phone reliably, and which apps can prove what they captured? Researched
2026-11-06 from Android documentation, store pages and manuals. **No app here has been tested for this dataset.**

## Short answer

Recording works without root, and apps need no special access. The catch is that Android makes no firm promise
about which mic an app gets or the format it records in. An app has to check both during the take, and few
recording apps show you the result.

## What Android does

- **Support:** Android detects USB audio devices and routes to them automatically, with no USB-specific audio
  API. [AOSP](https://source.android.com/docs/core/audio/usb) lists 8 to 48 kHz and 16, 24 or 32-bit PCM, in
  mono or stereo.
- **Permission:** the normal route needs `RECORD_AUDIO`. We tested this on the phone in this dataset and no
  other permission was involved.
- **Choosing the mic:** [`setPreferredDevice`](https://developer.android.com/reference/android/media/AudioRecord)
  is a request, and the docs don't promise it will be honoured.
- **Confirming the mic:** `getRoutedDevice()` works while recording, and
  [`AudioRecordingConfiguration`](https://developer.android.com/reference/android/media/AudioRecordingConfiguration)
  reports the device in use.
- **Format:** Android may resample. In `AudioRecordingConfiguration`, `getClientFormat()` is what the app asked
  for and `getFormat()` is what the device records. [Oboe](https://github.com/google/oboe/blob/main/docs/FullGuide.md)
  also warns that requested settings aren't guaranteed, and 24-bit needs API 31.
- **Processing:** the
  [`UNPROCESSED`](https://developer.android.com/reference/android/media/MediaRecorder.AudioSource) source
  behaves like the default if the phone doesn't support it. `VOICE_RECOGNITION` must ship with effects off by
  default. We found nothing confirming how `UNPROCESSED` behaves on a USB input.
- **Bit-perfect mode:** Android 14's [bit-perfect mixer](https://developer.android.com/reference/android/media/AudioMixerAttributes)
  is for playback. We found no recording equivalent.

## Two ways to capture

| | Android's audio stack | The app's own USB driver |
| --- | --- | --- |
| Access | Any app with mic access | The app talks to the mic through the USB host API, with a USB permission prompt |
| Format | Android decides, so check it | The app controls it directly, which is the appeal |
| Sharing | Normal | Only that app can use the mic |
| Example | Hebrish, most recorders | USB Audio Recorder PRO |

## What we saw on a real phone

On a OnePlus Nord 3 with Android 16, a training app using Android's stack recorded 460 takes from the Jabra and
59 from the Yealink. Android reported the right device each time, capturing at 48 kHz with processing off.

Two findings:

- **The input's label can mislead.** In that app, picking "Speakerphone" or "Headset earpiece" opened inputs with
  those names while Android kept routing to the USB headset. Ask Android what is really in use.
- **A 48 kHz file doesn't mean 48 kHz audio.** Both headsets stopped at about 8 kHz. No app setting can restore
  what the mic never captured.

## Apps

Store details are from Google Play on 2026-11-06. "Verifies the mic" means how far the app shows it is
using the USB mic: **documented** by the developer, **reported** by users, or **not found**.

| App | Updated | Price | Formats | Own USB driver | Verifies the mic |
| --- | --- | --- | --- | --- | --- |
| [USB Microphone Recorder](https://play.google.com/store/apps/details?id=com.majinsoft.usbmicrophonerecorder) | Jun 2026 | $7.99 | Up to 192 kHz, 16-bit or 32-bit float, WAV, RAW, AAC | Not stated | Documented, and the mic's name is saved in WAV files |
| [USB Audio Recorder PRO](https://play.google.com/store/apps/details?id=com.extreamsd.usbaudiorecorderpro) | Oct 2026 | $5.99 | Up to 384 kHz, 16 to 32-bit, WAV, FLAC, OGG, AIFF | Yes | Documented for USB use, but not how it shows the device |
| [Audio Evolution Mobile](https://play.google.com/store/apps/details?id=com.extreamsd.aemobile) | Nov 2026 | $11.99, driver extra | Whatever the device supports | Yes, as a paid add-on | Driver documented, verification not found |
| [RØDE Reporter](https://play.google.com/store/apps/details?id=com.rode.reporter) | Aug 2026 | Free | Up to 48 kHz, 24-bit, WAV, MP3 | Not found | Documented connection indicator, RØDE mics only |
| [ShurePlus MOTIV](https://play.google.com/store/apps/details?id=com.shure.motiv) | Oct 2026 | Free | Up to 96 kHz, 24-bit, WAV (third-party manual, 2021) | Not found | Reported, needs Android 12 or later |
| [n-Track Studio](https://play.google.com/store/apps/details?id=com.ntrack.studio.demo) | Nov 2026 | Free demo, Pro $29.99 | Up to 192 kHz, 16 to 32-bit | Not found | Not found |
| [RecForge II](https://play.google.com/store/apps/details?id=dje073.android.modernrecforge) | Oct 2026 | Free, Pro $4.49 | 8 to 48 kHz, 16-bit, many formats | Not found | Not found |
| [Open Camera](https://play.google.com/store/apps/details?id=net.sourceforge.opencamera) (video) | May 2026 | Free | Not documented | No | Reported, mixed results |

Dolby On, Easy Voice Recorder, Hi-Q and Voice Recorder Pro have no documented USB mic verification. Dolby On also
adds its own effects, so it isn't raw capture. Auphonic's app was last updated in 2017.

## Where to start

1. **USB Microphone Recorder:** the only app whose manual says it lists the mic in use, saves its name in the
   file and offers only what the mic supports. It's from a small developer.
2. **USB Audio Recorder PRO:** its own driver offers the most direct control of format, but only that app can use
   the mic.
3. **RØDE Reporter:** the first-party choice if you have a RØDE USB-C mic.

Whichever you use, check one take yourself. Read the rate and bit depth from the file, confirm the mic's name,
and look at a spectrogram to see how far up the audio really goes.
