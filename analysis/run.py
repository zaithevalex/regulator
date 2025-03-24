import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


class LinearCurve:
    def __init__(self, start_t, end_t, start_n):
        self.x0 = start_t
        self.x1 = end_t
        self.y0 = start_n
        self.y1 = start_n

    def k(self):
        return (self.y1 - self.y0) / (self.x1 - self.x0)

    def b(self):
        return self.y0 - ((self.y1 - self.y0) * self.x0) / (self.x1 - self.x0)

class PieceLinearCurve:
    def __init__(self, linearCurves, amountPoints):
        maxlength = linearCurves[0].x1 - linearCurves[0].x0
        for i in range(len(linearCurves)):
            if linearCurves[i].x1 - linearCurves[i].x0 > maxlength:
                maxlength = linearCurves[i].x1 - linearCurves[i].x0

        self.times = []
        self.events = []

        start = 0
        for i in range(len(linearCurves)):
            interval = np.linspace(linearCurves[i].x0, linearCurves[i].x1, int(np.round((linearCurves[i].x1 - linearCurves[i].x0) * amountPoints / maxlength)))
            for p in range(len(interval)):
                self.times.append(interval[p])

            events = linearCurve(linearCurves[i].k(), linearCurves[i].b(), self.times[start:len(self.times)])
            for p in range(len(events)):
                self.events.append(events[p])

            start = len(self.times)

    def selfConvolve(self, shift):
        if shift >= len(self.events):
            shift = len(self.events) - 1

        events = []
        for i in range(len(self.events)):
            max = 0
            for j in range(0, shift, 1):
                if i + j < len(self.events):
                    if self.events[i + j] + self.events[j] > max:
                        max = self.events[i + j] + self.events[j]
                else:
                    if self.events[len(self.events)-1] + self.events[j] > max:
                        max = self.events[len(self.events)-1] + self.events[j]

            events.append(max)

        return events

    def selfMinPlusConvolve(self, s):
        events = []
        for i in range(len(self.events)):
            min = self.events[i] + self.events[0]
            for j in range(0, i, 1):
                if self.events[i - j] + self.events[j] < min:
                    min = self.events[i - j] + self.events[j]

            events.append(min)

        return events

    # def selfSubAddClosure(self):


def linearCurve(k, b, x):
    return k * np.float64(x) + b

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

linearCurves = []
for i in range(num_segments):
    start = breakpoints[i]
    end = breakpoints[i + 1] + 1

    x_segment = np_time[start:end].reshape(-1, 1)
    y_segment = np_numbers[start:end]

    model = LinearRegression().fit(x_segment, y_segment)
    predicted_y[start:end] = model.predict(x_segment)

    if end >= len(np_time):
        break

    linearCurves.append(LinearCurve(
        np_time[start],
        np_time[end],
                    np_numbers[start]
                    ))

linearCurves.append(LinearCurve(
    np_time[breakpoints[num_segments]],
    np_time[breakpoints[num_segments]],
    np_numbers[breakpoints[num_segments]]
))

for i in range(len(linearCurves)-1):
    linearCurves[i].x1 = linearCurves[i+1].x0
    linearCurves[i].y1 = linearCurves[i+1].y0

    if linearCurves[i].y0 > linearCurves[i].y1:
        linearCurves[i].y1 = linearCurves[i].y0

p = PieceLinearCurve(linearCurves, 1000)

plt.scatter(np_time, np_numbers, color='green', label='Dataset', alpha=0.5)
plt.plot(p.times, p.events, color='blue', label='Linear Regression')
plt.plot(p.times, p.selfConvolve(500), color='orange', label='Self-Convolution')
plt.plot(p.times, p.selfMinPlusConvolve(10), color='red', label='Self-MinPlusConvolution')

plt.xlabel('t, unixtime(ms)')
plt.ylabel('y(t)')
plt.legend()
plt.show()