# FOC File Tools

Scripts for converting `.foc` binary EEG files.

## File format

- Binary file, 248-byte header (skip it)
- Data = float32 values, little-endian (`<f`)
- Multi-channel, interleaved (sample1_ch1, sample1_ch2, sample2_ch1, ...)

## `foc_to_edf.py`
Converts `.foc` → `.edf` (EEG standard format). Highly optimized using NumPy vectorization for instant loading and cleaning.

- Reads raw floats, replaces NaN/Inf with 0.0 in a single vectorized pass.
- Splits interleaved data natively in C-memory space by `N_CHANNELS`.
- Writes EDF with `pyedflib`.

### Download Requirements
```Requirements
numpy
matplotlib
pyedflib
mne
pandas
