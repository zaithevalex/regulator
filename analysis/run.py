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
    def __init__(self, linearCurves=[], amountPoints=0, times=None, events=None):
        if times is not None and events is not None:
            self.times = times
            self.events = events
            return

        if len(linearCurves) == 0 or amountPoints == 0:
            self.times = []
            self.events = []

            return

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

    def minPlusConvolution(self, events):
        result = []

        for i in range(len(self.events)):
            tmp = []
            for j in range(i + 1):
                if j == 0:
                    tmp.append(self.events[i - j])
                else:
                    tmp.append(self.events[i - j] + events[j])

            result.append(min(tmp))

        return result

    def minPlusDeconvolution(self, events):
        result = []
        for i in range(len(self.events)):
            tmp = []
            for j in range(len(self.events) - i):
                if j == 0:
                    tmp.append(self.events[i + j])
                else:
                    tmp.append(self.events[i + j] - events[j])

            result.append(max(tmp))
        return result

    def selfSubAddClosure(self, amountConvolutions):
        pieceLinearCurve = PieceLinearCurve([], 0)
        pieceLinearCurve.times = self.times
        pieceLinearCurve.events = self.events

        for _ in range(amountConvolutions):
            pieceLinearCurve.events = pieceLinearCurve.minPlusConvolution(pieceLinearCurve.events)

        return pieceLinearCurve.events

def betaLinearCurve(x, R, T):
    if x <= T:
        return 0

    return R * (x - T)

def linearCurve(k, b, x):
    return k * np.float64(x*x) + b

def testCurve1(x):
    if x < 2:
        return np.float64(x)

    return 2 + 0.25 * np.float64(x - 2)

def testCurve2(x):
    if x <= 3:
        return 1.5
    elif x > 3 and x <= 12:
        return 1 * (x - 3) + 1.5
    return 9 + 1.5


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

# p = PieceLinearCurve(linearCurves, 1000)

# shift to start of axis:
# p.times = p.times - p.times[0]
# np_time = np_time - np_time[0]

# betaServiceCurve = PieceLinearCurve(times=p.times, events=np.array([betaLinearCurve(t,  0.002, 50000) for t in p.times]))
# betaServiceCurve1 = PieceLinearCurve(times=p.times, events=np.array([betaLinearCurve(t, 0.002, 50000) for t in p.times]))
# betaServiceCurve1.events = betaServiceCurve1.events + np.float64(5)

# plt.scatter(np_time, np_numbers, color='green', label='Dataset', alpha=0.5)
# plt.plot(p.times, p.events, color='blue', label='Linear Regression')
# plt.plot(p.times, p.selfConvolve(500), color='orange', label='Self-Convolution')
# plt.plot(p.times, p.minPlusConvolve(p.events), color='red', label='Self-MinPlusConvolution')
# plt.plot(p.times, p.selfSubAddClosure(5), color='purple', label='Self-SubAddClosure')
# plt.plot(betaServiceCurve.times, betaServiceCurve.events , color='magenta', label='Beta')
# plt.plot(betaServiceCurve.times, betaServiceCurve.minPlusConvolve(betaServiceCurve1.selfSubAddClosure(5)), color='cyan', label='Beta-wfc')
#
piecewiseCurve = PieceLinearCurve(times=np.linspace(0, 20, 1000), events=linearCurve(0.5, 2, np.linspace(0, 20, 1000)))
servCurve = PieceLinearCurve(times=np.linspace(0, 20, 1000), events=np.array([betaLinearCurve(t,  3, 4) for t in np.linspace(0, 20, 1000)]))

# piecewiseCurve = PieceLinearCurve(times=np.linspace(0, 50, 1000), events=np.array([testCurve1(x) for x in np.linspace(0, 50, 1000)]))
# servCurve = PieceLinearCurve(times=np.linspace(0, 50, 1000), events=np.array([testCurve2(x) for x in np.linspace(0, 50, 1000)]))
plt.plot(piecewiseCurve.times, piecewiseCurve.events, color='red', label='default linear curve')
# plt.plot(servCurve.times, servCurve.events, color='blue', label='serv curve')
plt.plot(servCurve.times, piecewiseCurve.selfSubAddClosure(1), color='green', label='convolution')
plt.plot(servCurve.times, piecewiseCurve.selfSubAddClosure(2), color='green', label='convolution')
plt.plot(servCurve.times, piecewiseCurve.selfSubAddClosure(3), color='green', label='convolution')
plt.plot(servCurve.times, piecewiseCurve.selfSubAddClosure(4), color='green', label='convolution')
# plt.plot(piecewiseCurve.times, piecewiseCurve.minPlusDeconvolution(servCurve.events), color='cyan', label='convolution')

plt.xlabel('t, unixtime(ms)')
plt.ylabel('y(t)')
plt.legend()
plt.show()