import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from sklearn.linear_model import LinearRegression

with open('./dataset/y.txt', 'r') as file:
    lines = file.readlines()

times = []
numbers = []

i = 1
for line in lines:
    times.extend(int(num) for num in line.strip().split() if num)

for i in range(0, len(times), 1):
    numbers.append(i+1)

x = np.array(times)
y = np.array(numbers)

# np_times = np.array(times)
# np_numbers = np.array(numbers)
#
# linear_spline = interp1d(np_numbers, np_times, kind='linear')
# spline_numbers = np.linspace(np_numbers.min(), np_numbers.max(), len(numbers))
# spline_times = linear_spline(spline_numbers)
#
# plt.figure(figsize=(8,5))
# plt.plot(np_numbers, np_times, 'o', label='before')
# plt.plot(spline_numbers, spline_times, label='spline')
#
# plt.xlabel("t")
# plt.ylabel("y(t)")
# plt.show()

num_segments = 15
breakpoints = np.linspace(0, len(x)-1, num_segments + 1).astype(int)

segments = []
for i in range(num_segments):
    start = breakpoints[i]
    end = breakpoints[i + 1] + 1
    x_segment = x[start:end].reshape(-1, 1)
    y_segment = y[start:end]

    # Линейная регрессия
    model = LinearRegression().fit(x_segment, y_segment)
    segments.append((model.coef_[0], model.intercept_))


plt.scatter(x, y, color='blue', label='Данные')
for i in range(num_segments):
    m, b = segments[i]
    plt.plot(x[breakpoints[i]:breakpoints[i + 1] + 1],
             m * x[breakpoints[i]:breakpoints[i + 1] + 1] + b,
             color='red')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Кусочная линейная аппроксимация для возрастающей кривой')
plt.legend()
plt.show()