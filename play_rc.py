import SoapySDR
import numpy as np
import time

# Load the recorded IQ data
file_paths = {
    "car_up": "/home/patmfm/Desktop/RC_car/carup.raw",
    "car_down": "/home/patmfm/Desktop/RC_car/cardown.raw",
    "car_up_left": "/home/patmfm/Desktop/RC_car/car_up_left.raw",
    "car_up_right": "/home/patmfm/Desktop/RC_car/car_up_right.raw",
    "car_down_left": "/home/patmfm/Desktop/RC_car/car_down_left.raw",
    "car_down_right": "/home/patmfm/Desktop/RC_car/car_down_right.raw",
}

# Total playback durations in seconds for each action
runtimes = {
    "car_up": 1,
    "car_down": 1,
    "car_up_left": 1,
    "car_up_right": 1,
    "car_down_left": 1,
    "car_down_right": 1,
}

# Initialize SDR
try:
    sdr = SoapySDR.Device({"driver": "hackrf"})  # Replace with your SDR's driver
except Exception as e:
    print(f"Error initializing SDR: {e}")
    exit(1)

# Set SDR parameters
sample_rate = 2e6  # 2 MSPS
sdr.setSampleRate(SoapySDR.SOAPY_SDR_TX, 0, sample_rate)
sdr.setFrequency(SoapySDR.SOAPY_SDR_TX, 0, 50019e3)  # Frequency in Hz
sdr.setGain(SoapySDR.SOAPY_SDR_TX, 0, 30)  # Gain in dB

# Read the data
data = {}
try:
    for key, file_path in file_paths.items():
        data[key] = np.fromfile(file_path, dtype=np.complex64)  # Adjust dtype to match your format
        if data[key].size == 0:
            print(f"Error: No data found in file {file_path}.")
            exit(1)
except Exception as e:
    print(f"Error reading data file: {e}")
    exit(1)

# Set up the SDR stream
chunk_size = 1024
try:
    tx_stream = sdr.setupStream(SoapySDR.SOAPY_SDR_TX, SoapySDR.SOAPY_SDR_CF32)
    sdr.activateStream(tx_stream)

    # Play each action for its defined runtime
    for action, runtime in runtimes.items():
        start_time = time.time()  # Independent start time for each action
        print(f"Playing {action} for {runtime} seconds...")
        while time.time() - start_time < runtime:
            for i in range(0, len(data[action]), chunk_size):
                chunk = data[action][i:i + chunk_size]
                sdr.writeStream(tx_stream, [chunk], len(chunk))
                # Break early if runtime exceeded
                if time.time() - start_time >= runtime:
                    break

finally:
    # Deactivate and clean up the stream
    sdr.deactivateStream(tx_stream)
    sdr.closeStream(tx_stream)


