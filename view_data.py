import numpy as np
import matplotlib.pyplot as plt

# Load the raw IQ data file
file_path = "/home/patmfm/Desktop/RC_car/car_down_left.raw"
iq_data = np.fromfile(file_path, dtype=np.complex64)

# # Plot the magnitude of the IQ data
# plt.figure(figsize=(10, 5))
# plt.plot(np.abs(iq_data), label="Signal")
# plt.ylim(bottom=0, top=np.max(np.abs(iq_data)) * 1.2)
# plt.title("Signal Magnitude Over Time")
# plt.xlabel("Sample Index")
# plt.ylabel("Magnitude")
# plt.legend()
# plt.show()


# Define a magnitude threshold
threshold = 0.05  # Adjust based on your signal characteristics

# Create a mask for data above the threshold
signal_mask = np.abs(iq_data) > threshold

# Extract the signal using the mask
filtered_signal = iq_data[signal_mask]

# Save the filtered data to a new file
filtered_file_path = "/home/patmfm/Desktop/RC_car/filtered_down_left_signal.raw"
filtered_signal.tofile(filtered_file_path)

print(f"Filtered signal saved to {filtered_file_path}")

