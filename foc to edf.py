import argparse
import os
import numpy as np
import pyedflib

def convert_foc_to_edf(input_file, output_file, header_size=248, n_channels=2, sfreq=256):
    # 1. Read everything at once with NumPy (Lightning Fast)
    with open(input_file, "rb") as f:
        f.seek(header_size)
        raw_data = np.fromfile(f, dtype=np.float32)
        
    print(f"Loaded {len(raw_data)} samples")

    # 2. Vectorized cleaning: Replace NaNs and Infs with 0.0
    raw_data = np.nan_to_num(raw_data, nan=0.0, posinf=0.0, neginf=0.0)

    # 3. Trim for even channel splitting
    usable = len(raw_data) - (len(raw_data) % n_channels)
    raw_data = raw_data[:usable]

    # 4. Reshape and transpose to separate channels natively
    signals = raw_data.reshape(-1, n_channels).T.astype(np.float64)

    # 5. Build EDF headers
    channel_info = [{"label": f"CH{ch+1}", "dimension": "uV", 
                     "sample_frequency": sfreq, "physical_min": -100.0, 
                     "physical_max": 100.0, "digital_min": -32768, 
                     "digital_max": 32767, "transducer": "", "prefilter": ""} 
                    for ch in range(n_channels)]

    # 6. Write EDF
    writer = pyedflib.EdfWriter(output_file, n_channels, file_type=pyedflib.FILETYPE_EDFPLUS)
    writer.setSignalHeaders(channel_info)
    writer.writeSamples(signals)
    writer.close()
    
    print(f"EDF successfully written: {output_file}")

if __name__ == "__main__":
    # Setup for terminal usage
    parser = argparse.ArgumentParser(description="Convert .foc files to .edf format.")
    parser.add_argument("input", help="Input .foc file path")
    parser.add_argument("-o", "--output", default="output.edf", help="Output .edf file path")
    parser.add_argument("-c", "--channels", type=int, default=2, help="Number of channels")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found.")
    else:
        convert_foc_to_edf(args.input, args.output, n_channels=args.channels)
