import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

class LinearCurve:
    def __init__(self, times_pair, numbers_pair):
        self.k = (numbers_pair[1] - numbers_pair[0]) / (times_pair[1] - times_pair[0])
        self.b = numbers_pair[0] - ((numbers_pair[1] - numbers_pair[0]) * times_pair[0] / (times_pair[1] - times_pair[0]))

with open('./dataset/y.txt', 'r') as file:
    lines = file.readlines()

def f(x):
    return 0.0008146067415730337 * x -1419203668.1544664

times = []
numbers = []
for line in lines:
    times.extend(int(num) for num in line.strip().split() if num)

for i in range(0, len(times), 1):
    numbers.append(i+1)

np_time = np.array(times)
np_numbers = np.array(numbers)

num_segments = 15
breakpoints = np.linspace(0, len(np_time) - 1, num_segments + 1).astype(int)
predicted_y = np.zeros_like(np_numbers)

linearCurves = []
for i in range(num_segments):
    start = breakpoints[i] + 1
    end = breakpoints[i + 1] + 1
    linearCurves.append(LinearCurve(
        [np_time[start-1], np_time[end-1]],
        [np_numbers[start-1], np_numbers[end-1]]
    ))

    x_segment = np_time[start:end].reshape(-1, 1)
    y_segment = np_numbers[start:end]

    model = LinearRegression().fit(x_segment, y_segment)
    predicted_y[start:end] = model.predict(x_segment)

print('LINEAR CURVES:')
print(linearCurves[1].k, linearCurves[1].b)

plt.subplot(1, 2, 1)
plt.scatter(np_time, np_numbers, color='green', label='Data', alpha=0.5)
plt.plot(np_time, predicted_y, color='red', label='Piecewise linear approximation')
plt.plot(np_time, f(np_time), color='blue')
plt.xlabel('t, unixtime(ms)')
plt.ylabel('y(t)')
plt.legend()

plt.show()