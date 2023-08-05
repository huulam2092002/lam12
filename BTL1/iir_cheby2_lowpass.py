# import required modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math
from scipy.signal import iirfilter, freqz, butter, tf2zpk, dimpulse, dlti, buttord, sosfreqz, sosfiltfilt, sos2zpk,cheby2, cheb2ord, unit_impulse, sosfilt
from scipy.io.wavfile import write



# sampling frequency
fs = 1000
# pass band frequency
wp = 150

# stop band frequency
ws = 300

# pass band ripple
gpass = 0.5

# stop band attenuation
gstop = 50

# Bậc của bộ lọc
# Hàm tìm bậc bé nhất của bộ lọc:
ord, wn = cheb2ord(wp, ws, gpass, gstop, False, fs)
print('Bac cua bo loc la ',ord)
print('Tan so cat ', wn)       


# Thiết kế bộ lọc IIR
sos = iirfilter(ord, wn, rp=None, rs=gstop, btype='low', analog=False, ftype='cheby2', output='sos', fs=fs)
b1, a1 = cheby2(ord, rs=gstop, Wn=wn , btype='low' ,  analog=False, output='ba', fs=fs )
print('So phep tinh nhan la ', len(b1) + len(a1))

# Vẽ đáp ứng biên độ
w, h = sosfreqz(sos, fs=fs)
#plt.subplot(2, 2, 2)
plt.plot(w, 20 * np.log10(abs(h)))
plt.xlim(0, fs/2)
plt.title('IIR Chebyshev II filter frequency response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
#plt.margins(0, 0.01, y = 0.01)
plt.grid( which='both', axis='both')
plt.axhline(-50, color='red', ls='--', label = '-50 dB')
plt.legend(loc='best')
plt.axhline(-0.5, color='green', ls='--', label = '-0.5 dB')
plt.legend(loc='best')
plt.axvline(150, color='orange', label = '150 Hz')
plt.legend(loc='best')
plt.axvline(300, color='blue', label ='300 Hz')
plt.legend(loc='best')
plt.show()

# Vẽ giản đồ cực và zero
z, p, k = sos2zpk(sos)
#plt.subplot(2, 2, 1)
plt.plot(np.real(z), np.imag(z), 'ob', markerfacecolor='none')
plt.plot(np.real(p), np.imag(p), 'xr')
plt.legend(['Zeros', 'Poles'], loc=2)
plt.title('Pole / Zero Plot')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.grid()
plt.show()
       
# Đáp ứng của 100 trọng số đầu tiên
x1= unit_impulse(100)
y_sos = sosfilt(sos, x1)
tt = np.arange(0,100)
plt.plot(tt, y_sos, linewidth=1)
markerline, stemlines, baseline = plt.stem(tt, y_sos)
plt.setp(stemlines, 'linewidth', 1)
plt.grid()
plt.xlabel('Impulse reponse [100]')
plt.ylabel('Amplitude')
plt.show()

 #cac tin hieu vao
f1 = 180  # Frequency of 1st signal
f2 = 400  # Frequency of 2nd signal

# Generate the time vector of 1 sec duration
t = np.linspace(0, 1,1000)  # Generate 1000 samples in 1 sec

# Generate the signal containing f1 and f2
sig = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
       
 # Display the signal
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t, sig)
ax1.set_title('Tin hieu truoc khi loc')
ax1.axis([0, 1, -2, 2])

       
# Áp bộ lọc vào tín hiệu

# Lọc theo một chiều (one-dimension)
#y = sosfilt(sos, sig, 0)

# Lọc tiến lùi (Forward-backward filtering)
y = sosfiltfilt(sos, sig, 0)
# Display the output signal
ax2.plot(t, y)
ax2.set_title('Sau khi loc')
ax2.axis([0, 1, -2, 2])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()



