import numpy as np

def fourier_series(t, a0, a, b):

    T = (t[-1] - t[0])
    sum = a0/2
    for i in range(len(a)):
        sum += a[i]*np.cos(2*np.pi*(i+1)*t/T) + b[i]*np.sin(2*np.pi*(i+1)*t/T)
    return sum

def fourier_coefficients(x, y, N_fourier=30):

    a0 = 0
    a = np.zeros(N_fourier)
    b = np.zeros(N_fourier)

    T = (x[-1] - x[0])

    for i in range(N_fourier):
        # trapz
        a0 += 2/T * np.trapz(y * np.cos(2*np.pi*(i+1)*x/T), x)
        a[i] = 2/T * np.trapz(y * np.cos(2*np.pi*(i+1)*x/T), x)
        b[i] = 2/T * np.trapz(y * np.sin(2*np.pi*(i+1)*x/T), x)

    return a0, a, b