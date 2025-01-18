import SoapySDR
import numpy as np
import time

# Load the recorded IQ data
file_path_car_up = "/home/patmfm/Desktop/RC_car/carup.raw"
file_path_car_down = "/home/patmfm/Desktop/RC_car/cardown.raw"
file_path_car_up_left = "/home/patmfm/Desktop/RC_car/car_up_left.raw"
file_path_car_up_right = "/home/patmfm/Desktop/RC_car/car_up_right.raw"
file_path_car_down_left = "/home/patmfm/Desktop/RC_car/car_down_left.raw"
file_path_car_down_right = "/home/patmfm/Desktop/RC_car/car_down_right.raw"

# Total playback duration in seconds
up_runtime = 1  # Replace with desired running time
down_runtime = 1 
up_left_runtime = 1 
up_right_runtime = 1 
down_left_runtime = 1 
down_right_runtime = 1  

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
data_car_up = np.fromfile(file_path_car_up, dtype=np.complex64)  # Adjust dtype to match your format
data_car_down = np.fromfile(file_path_car_down, dtype=np.complex64)
data_car_up_left = np.fromfile(file_path_car_up_left, dtype=np.complex64)
data_car_up_right = np.fromfile(file_path_car_up_right, dtype=np.complex64)
data_car_down_left = np.fromfile(file_path_car_down_left, dtype=np.complex64)
data_car_down_right = np.fromfile(file_path_car_down_right, dtype=np.complex64)


# Set up the SDR stream
chunk_size = 1024
try:
    tx_stream = sdr.setupStream(SoapySDR.SOAPY_SDR_TX, SoapySDR.SOAPY_SDR_CF32)
    sdr.activateStream(tx_stream)

    # Track playback time
    start_time = time.time()

    # Stream the data in chunks until runtime is exceeded
    while time.time() - start_time < up_runtime:
        for i in range(0, len(data_car_up), chunk_size):
            chunk = data_car_up[i:i + chunk_size]
            sdr.writeStream(tx_stream, [chunk], len(chunk))
    while time.time() - start_time < down_runtime:
        for i in range(0, len(data_car_down), chunk_size):
            chunk = data_car_down[i:i + chunk_size]
            sdr.writeStream(tx_stream, [chunk], len(chunk))
    while time.time() - start_time < up_left_runtime:
        for i in range(0, len(data_car_up_left), chunk_size):
            chunk = data_car_up_left[i:i + chunk_size]
            sdr.writeStream(tx_stream, [chunk], len(chunk))
    while time.time() - start_time < up_right_runtime:
        for i in range(0, len(data_car_up_right), chunk_size):
            chunk = data_car_up_right[i:i + chunk_size]
            sdr.writeStream(tx_stream, [chunk], len(chunk))
    while time.time() - start_time < down_left_runtime:
        for i in range(0, len(data_car_down_left), chunk_size):
            chunk = data_car_down_left[i:i + chunk_size]
            sdr.writeStream(tx_stream, [chunk], len(chunk))
    while time.time() - start_time < down_right_runtime:
        for i in range(0, len(data_car_down_right), chunk_size):
            chunk = data_car_down_right[i:i + chunk_size]
            sdr.writeStream(tx_stream, [chunk], len(chunk))  

    
finally:
    # Deactivate and clean up the stream
    sdr.deactivateStream(tx_stream)
    sdr.closeStream(tx_stream)

