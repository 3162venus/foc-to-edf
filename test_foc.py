import numpy as np
import matplotlib.pyplot as plt
import os

filename = "STP.1.2-corr 1.foc"
HEADER_SIZE = 248

size = os.path.getsize(filename)
n_floats = (size - HEADER_SIZE) // 4

with open(filename, "rb") as f:
    f.seek(HEADER_SIZE)
    values = np.fromfile(f, dtype="<f4", count=n_floats)

print("min:", values.min(), "max:", values.max())
print("samples:", len(values))

plt.plot(values)
plt.show()