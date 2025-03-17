import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

with open('./dataset/x.txt', 'r') as file:
    lines = file.readlines()

times = []
numbers = []

i = 1
for line in lines:
    times.extend(int(num) for num in line.strip().split() if num)

for i in range(0, len(times), 1):
    numbers.append(i+1)

np_times = np.array(times)
np_numbers = np.array(numbers)

spline = CubicSpline(numbers, times)
spline_numbers = np.linspace(np_numbers.min(), np_numbers.max(), 100)
spline_times = spline(spline_numbers)

plt.figure(figsize=(8,5))
plt.plot(np_numbers, np_times, 'o', label='before')
plt.plot(spline_numbers, spline_times, label='spline')

plt.xlabel("t")
plt.ylabel("x(t)")
plt.show()