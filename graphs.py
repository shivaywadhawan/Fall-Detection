import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

def make_graphs(filename, id):
    data = pd.read_csv("528_rows_1.csv")
    data = data[data["id"] == id]
    accel = data.iloc[:, 0:3]

    # plot acceleration
    plt.plot(accel)
    plt.title(f"{filename} acceleration (xyz) (fs = 60)")
    plt.ylabel("acceleration (m/s^2)")
    plt.xlabel("time (t = 6s)")
    plt.legend(['z_accel', 'y_accel', 'x_accel'])
    # plt.savefig(f'./figures/acceleration_{filename}.png')
    plt.show()
    plt.clf()

    # take magnitude
    mag = np.linalg.norm(accel, axis=1)

    # plot acceleration magnitude
    plt.plot(mag)
    plt.title(f"{filename} acceleration (magnitude) (fs = 60)")
    plt.ylabel("acceleration (m/s^2)")
    plt.xlabel("time (t = 6s)")
    # plt.savefig(f'./figures/acceleration_{filename}.png')
    plt.show()
    plt.clf()

    # take fft for spectrogram
    x = np.array(accel.iloc[:, 0])
    f, t, Sxx = scipy.signal.spectrogram(x, fs=60, nperseg=10, noverlap=6)

    # plot acceleration spectrogram
    plt.pcolormesh(t, f, Sxx)
    plt.title(f'Spectrogram of {filename} x acceleration (fs = 60)')
    plt.ylabel("freq (Hz)")
    plt.xlabel("time (t = 6s)")
    # plt.savefig(f'./figures/acceleration_spectro_{filename}.png')
    plt.show()
    plt.clf()

    # gyroscope data
    gyro = data.iloc[:, 3:6]

    # plot angular acceleration
    plt.plot(gyro)
    plt.title(f"{filename} angular acceleration (fs = 60)")
    plt.ylabel("angular acceleration (degree/s)")
    plt.xlabel("time (t = 6s)")
    plt.legend(['z_accel', 'y_accel', 'x_accel'])
    # plt.savefig(f'./figures/gyro_{filename}.png')
    plt.show()
    plt.clf()

    # take fft for spectrogram
    x = np.array(gyro.iloc[:, 0])
    f, t, Sxx = scipy.signal.spectrogram(x, fs=60, nperseg=10, noverlap=6)

    # plot angular acceleration spectrogram
    plt.pcolormesh(t, f, Sxx)
    plt.title(f'Spectrogram of {filename} x angular acceleration (fs = 60)')
    plt.ylabel("freq (Hz)")
    plt.xlabel("time (t = 6s)")
    # plt.savefig(f'./figures/gyro_spectro_{filename}.png')
    plt.show()
    plt.clf()


make_graphs("forward", 1)
# make_graphs("backward", 2)
# make_graphs("left", 3)
# make_graphs("right", 4)
