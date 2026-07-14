import mne
import pandas as pd

# Load EDF file converted from .foc
raw = mne.io.read_raw_edf("converted file name.edf", preload=True)

# Print basic recording info (channels, duration, sample rate)
print(raw)
print(raw.ch_names)
print(raw.info["sfreq"])      # sampling rate in Hz
print(raw.times[-1])          # total recording duration in seconds
print(raw.annotations)         # event markers, if any

# Extract raw signal data as numpy array (channels x samples)
data = raw.get_data()

# Convert sample indices to time in milliseconds
times_ms = raw.times * 1000

# Build table: time + amplitude per channel
df = pd.DataFrame({
    "Time_ms": times_ms,
    "negative num ch 1": data[0],
    "positive num ch 2": data[1]
})

# Show first 20 rows
print(df.head(20))

# Plot first 10 seconds of both channels
raw.plot(duration=10, n_channels=2, block=True)