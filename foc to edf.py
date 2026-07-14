import struct
import math
import pyedflib
import numpy as np

# Input .foc file and output EDF name
FOC_FILE = "STP.1.2-corr 1.foc"
EDF_FILE = "converted file name.edf"

HEADER_SIZE = 248   # bytes to skip before data starts
N_CHANNELS = 2      # assumed channel count
SFREQ = 256         # assumed sampling rate (Hz)

values = []

# Read raw float32 values after header
with open(FOC_FILE, "rb") as f:
    f.seek(HEADER_SIZE)
    while True:
        chunk = f.read(4)
        if len(chunk) < 4:
            break
        v = struct.unpack("<f", chunk)[0]
        # replace corrupted values with 0
        if math.isnan(v) or math.isinf(v):
            v = 0.0
        values.append(v)

print("Loaded", len(values), "samples")

# Trim so values divide evenly across channels
usable = len(values) - (len(values) % N_CHANNELS)
values = values[:usable]

# Split interleaved data into separate channels
signals = []
for ch in range(N_CHANNELS):
    sig = np.array(values[ch::N_CHANNELS], dtype=np.float64)
    signals.append(sig)

# Build EDF channel headers
channel_info = []
for ch in range(N_CHANNELS):
    channel_info.append({
        "label": f"CH{ch+1}",
        "dimension": "uV",
        "sample_frequency": SFREQ,
        "physical_min": -100.0,
        "physical_max": 100.0,
        "digital_min": -32768,
        "digital_max": 32767,
        "transducer": "",
        "prefilter": ""
    })

# Write EDF file
writer = pyedflib.EdfWriter(
    EDF_FILE,
    N_CHANNELS,
    file_type=pyedflib.FILETYPE_EDFPLUS
)
writer.setSignalHeaders(channel_info)
writer.writeSamples(signals)
writer.close()

print("EDF written:", EDF_FILE)