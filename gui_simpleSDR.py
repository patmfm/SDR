import simplesoapy
import numpy as np
import PySimpleGUI as sg 
import tkinter as tk   


file_path_car_up = "/home/patmfm/Desktop/RC_car/carup.raw"
file_path_car_down = "/home/patmfm/Desktop/RC_car/cardown.raw"
file_path_car_up_left = "/home/patmfm/Desktop/RC_car/car_up_left.raw"
file_path_car_up_right = "/home/patmfm/Desktop/RC_car/car_up_right.raw"
file_path_car_down_left = "/home/patmfm/Desktop/RC_car/car_down_left.raw"
file_path_car_down_right = "/home/patmfm/Desktop/RC_car/car_down_right.raw"

sdr = simplesoapy.SoapyDevice("hackrf")
sample_rate = 2e6  # 2 MSPS
sdr.sample_rate = sample_rate
sdr.freq = 50019e3  # Frequency in Hz
sdr.gain = 30  # Gain in dB

data_car_up = np.fromfile(file_path_car_up, dtype=np.complex64)  # Adjust dtype to match your format
data_car_down = np.fromfile(file_path_car_down, dtype=np.complex64)
data_car_up_left = np.fromfile(file_path_car_up_left, dtype=np.complex64)
data_car_up_right = np.fromfile(file_path_car_up_right, dtype=np.complex64)
data_car_down_left = np.fromfile(file_path_car_down_left, dtype=np.complex64)
data_car_down_right = np.fromfile(file_path_car_down_right, dtype=np.complex64)


chunk_size = 1024

tx_stream = sdr.stream
sdr.start_stream(tx_stream)


def send_up_in_chunks():
    for i in range(0, len(data_car_up), chunk_size):
        chunk = data_car_up[i:i + chunk_size]
        sdr.write(chunk)
def send_down_in_chunks():
    for i in range(0, len(data_car_down), chunk_size):
        chunk = data_car_down[i:i + chunk_size]
        tx_stream.write(chunk)
def send_up_left_in_chunks():
    for i in range(0, len(data_car_up_left), chunk_size):
        chunk = data_car_up_left[i:i + chunk_size]
        tx_stream.write(chunk)
def send_up_right_in_chunks():
    for i in range(0, len(data_car_up_right), chunk_size):
        chunk = data_car_up_right[i:i + chunk_size]
        tx_stream.write(chunk)
def send_down_left_in_chunks():
    for i in range(0, len(data_car_down_left), chunk_size):
        chunk = data_car_down_left[i:i + chunk_size]
        tx_stream.write(chunk)
def send_down_right_in_chunks():
    for i in range(0, len(data_car_down_right), chunk_size):
        chunk = data_car_down_right[i:i + chunk_size]
        tx_stream.write(chunk)


root = tk.Tk()
go_up = tk.Button(root, text="UP", command=send_up_in_chunks)
go_down = tk.Button(root, text="DOWN", command=send_down_in_chunks)
go_up_left = tk.Button(root, text="UP LEFT", command=send_up_left_in_chunks)
go_up_right = tk.Button(root, text="UP RIGHT", command=send_up_right_in_chunks)
go_down_left = tk.Button(root, text="DOWN LEFT", command=send_down_left_in_chunks)
go_down_right = tk.Button(root, text="DOWN RIGHT", command=send_down_right_in_chunks)
go_up.pack()
go_down.pack()
go_up_left.pack()
go_up_right.pack()
go_down_left.pack()
go_down_right.pack()
root.mainloop()
sdr.stop_stream(tx_stream)
sdr.close(tx_stream)