import matplotlib.pyplot as plt
import numpy as np

def min_plus_convolution(f, g):
    """Compute the min-plus convolution of two functions f and g."""
    len_f = len(f)
    len_g = len(g)
    result_len = len_f + len_g - 1
    result = np.full(result_len, np.inf)  # Initialize with infinity

    for i in range(result_len):
        for j in range(len_g):
            if 0 <= i - j < len_f:
                result[i] = min(result[i], f[i - j] + g[j])

    return result

def min_plus_deconvolution(h, g):
    """Compute the min-plus deconvolution of h by g."""
    len_h = len(h)
    len_g = len(g)
    result = np.full(len_h, np.inf)  # Initialize with infinity

    for i in range(len_h):
        for j in range(len_g):
            if i - j >= 0:
                result[i] = min(result[i], h[i] - g[j])

    return result

# Example curves
x = np.linspace(0, 5, 5)
print(x)
f = np.array([1, 2, 3])  # Curve f
g = np.array([4, 5, 6])  # Curve g

# Compute min-plus convolution
h = min_plus_convolution(f, g)
print("Min-plus Convolution Result:", h)

# Compute min-plus deconvolution
deconvolved_result = min_plus_deconvolution(h, g)
print("Min-plus Deconvolution Result:", deconvolved_result)

# plt.plot(x, f, color='blue')
# plt.plot(x, g, color='red')
plt.plot(x, h, color='green')
plt.show()