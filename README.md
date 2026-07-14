# FOC File Tools

Scripts for reading and converting `.foc` binary EEG files.

## File format

- Binary file, 248-byte header (skip it)
- Data = float32 values, little-endian (`<f`)
- Multi-channel, interleaved (sample1_ch1, sample1_ch2, sample2_ch1, ...)

## Files

### `test_foc.py`
Quick look at raw data. Loads all floats, prints min/max/count, plots full signal.

Run first to sanity-check file.

### `guess_channels.py`
Tries channel counts (2, 4, 8, 16, 32, 64). Reshapes data per guess, prints std dev per channel.

Use to figure out N_CHANNELS. Look for stable, non-zero std devs.

### `foc_to_edf.py`
Converts `.foc` → `.edf` (EEG standard format).

- Reads floats, replaces NaN/Inf with 0
- Splits interleaved data by `N_CHANNELS`
- Writes EDF with `pyedflib`

Set `N_CHANNELS` and `SFREQ` (sampling rate) before running — get these from `guess_channels.py` and file metadata.

### `_run_the_edf_file_.py`
Loads converted `.edf`, prints channel info (names, sample rate, duration), builds dataframe, plots first 10s.

## Workflow

1. `test_foc.py` — check data looks sane
2. `guess_channels.py` — find channel count
3. Edit `foc_to_edf.py` config, run it
4. `_run_the_edf_file_.py` — verify EDF output

## Requirements

```
numpy
matplotlib
pyedflib
mne
pandas
```

## Open questions

- N_CHANNELS = 2 is a guess. Confirm with `guess_channels.py`.
- SFREQ = 256 is a guess. Confirm from device docs/header.
- Physical min/max (-100/100 uV) — adjust if values exceed range.
