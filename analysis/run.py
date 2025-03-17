import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

with open('./dataset/y.txt', 'r') as file:
    lines = file.readlines()

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

steps = []
for i in range(num_segments):
    start = breakpoints[i] + 1
    end = breakpoints[i + 1] + 1

    for j in range(end - start):
        steps.append(i)

    x_segment = np_time[start:end].reshape(-1, 1)
    y_segment = np_numbers[start:end]

    model = LinearRegression().fit(x_segment, y_segment)
    predicted_y[start:end] = model.predict(x_segment)

steps.append(steps[len(steps)-1])

plt.subplot(1, 2, 1)
plt.scatter(np_time, np_numbers, color='green', label='Data', alpha=0.5)
plt.plot(np_time, predicted_y, color='red', label='Piecewise linear approximation')
plt.xlabel('t, unixtime(ms)')
plt.ylabel('y(t)')
plt.legend()

plt.subplot(1, 2, 2)
plt.step(np_time, steps, color='blue')
plt.xlabel('t, unixtime(ms)')
plt.ylabel('step')
plt.legend()

plt.show()