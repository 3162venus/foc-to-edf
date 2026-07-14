import struct
import numpy as np

filename = "STP.1.2-corr 1.foc"

values = []

with open(filename, "rb") as f:
    f.seek(248)

    for _ in range(200000):
        chunk = f.read(4)

        if len(chunk) < 4:
            break

        values.append(struct.unpack("<f", chunk)[0])

values = np.array(values)

for channels in [2, 4, 8, 16, 32, 64]:
    usable = len(values) - (len(values) % channels)

    data = values[:usable].reshape(-1, channels)

    stds = data.std(axis=0)

    print(f"\n{channels} channels")
    print(stds[:10])