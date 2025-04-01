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

class MinPlusAlgebra:
    def ConvertToDataSet(self, linearCurves=[], amountPoints=0):
        times, events = [], []
        if len(linearCurves) == 0 or amountPoints == 0:
            return None, None

        maxlength = linearCurves[0].x1 - linearCurves[0].x0
        for i in range(len(linearCurves)):
            if linearCurves[i].x1 - linearCurves[i].x0 > maxlength:
                maxlength = linearCurves[i].x1 - linearCurves[i].x0

        start = 0
        for i in range(len(linearCurves)):
            interval = np.linspace(linearCurves[i].x0, linearCurves[i].x1, int(np.round((linearCurves[i].x1 - linearCurves[i].x0) * amountPoints / maxlength)))
            for p in range(len(interval)):
                times.append(interval[p])

            events = linearCurve(linearCurves[i].k(), linearCurves[i].b(), times[start:len(times)])
            for p in range(len(events)):
                events.append(events[p])

            start = len(times)

        return times, events

    def convolve(self, events_f, events_g):
        events = []
        for i in range(len(events_f)):
            tmp = []
            for j in range(i + 1):
                if j == 0:
                    tmp.append(events_f[i - j])
                else:
                    tmp.append(events_f[i - j] + events_g[j])
            events.append(min(tmp))

        return times, events

    def MinPlusConvolution1(self, f, g, times):
        if len(times) == 0:
            return None, None

        events_f = np.array([f(x) for x in times])
        events_g = np.array([g(x) for x in times])

        return self.convolve(events_f, events_g)

    def MinPlusConvolution2(self, events_f, events_g, times):
        if len(times) == 0:
            return None, None

        return self.convolve(events_f, events_g)

    def MinPlusDeconvolution(self, f, g, times):
        if len(times) == 0:
            return None, None

        events = []
        left = times[0]
        delta = (times[len(times) - 1] - left) / len(times)
        while left <= times[len(times) - 1]:
            tmp = [0] * len(times)

            if left <= 0:
                internal = 0.0
                internalCounter = 0
                while internal <= times[len(times) - 1]:
                    tmp[internalCounter] = f(left + internal) - g(internal)
                    internalCounter += 1
                    internal += delta
            else:
                internal = 0.0
                internalCounter = 0
                while internal <= times[len(times) - 1] - left:
                    tmp[internalCounter] = f(left + internal) - g(internal)
                    internalCounter += 1
                    internal += delta

            events.append(max(tmp))
            left += delta

        return np.linspace(times[0], times[len(times) - 1], len(events)), events

    def SelfSubAddClosure1(self, f, times, amountConvolutions):
        events_f = np.array([f(x) for x in times])
        for _ in range(amountConvolutions):
            _, events_f = self.convolve(events_f, events_f)

        return np.linspace(times[0], times[len(times) - 1], len(events_f)), events_f

    def SelfSubAddClosure2(self, events, times, amountConvolutions):
        for _ in range(amountConvolutions):
            _, events = self.convolve(events, events)

        return np.linspace(times[0], times[len(times) - 1], len(events)), events

    def AddConst1(self, f, times, const):
        f_events = np.array([(f(x) + const) for x in times])
        return np.linspace(times[0], times[len(times) - 1], len(f_events)), f_events

    def AddConst2(self, events, times, const):
        for i in range(len(events)):
            events[i] += const

        return np.linspace(times[0], times[len(times) - 1], len(events)), events

def betaLinearCurve(R, T, x):
    if x <= T:
        return 0

    return R * (x - T)

def linearCurve(k, b, x):
    return k * np.float64(x) + b

# def testCurve1(x):
#     if x < 3:
#         return 0
#     elif x >= 3 and x <= 5:
#         return (x - 3)
#     elif x >= 5 and x <= 12:
#         return 2
#
#     return 7 + 0.5 * (x - 12)
#
# def testCurve2(x):
#     if x <= 0:
#         return 1
#     elif x >= 0 and x < 2:
#         return 1 + x
#     elif x >= 2 and x <= 20.15:
#         return 3 + 0.25 * (x - 2)
#
#     return 15
#
# def testCurve1(x):
#     return x*x*x*x
#
# def testCurve2(x):
#     if x < 3:
#         return 0
#     elif x >= 3 and x < 10:
#         return (x - 3)
#
#     return 7 + 0.5 * (x - 10)

def alpha_in(x):
    return 2 * x + 3

def alpha_out(x):
    return x + 20

def beta(x):
    if x < 2:
        return 0
    return 3 * (x - 2)

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

# plt.plot(np.linspace(-20, 40, 1000), np.array([testCurve1(x) for x in np.linspace(-20, 40, 1000)]), color='blue', label='default linear curve')
# plt.plot(np.linspace(-20, 40, 1000), np.array([testCurve2(x) for x in np.linspace(-20, 40, 1000)]), color='green', label='serv curve')
# plt.plot(servCurve.times, piecewiseCurve.selfSubAddClosure(1), color='green', label='convolution')

# times, events = MinPlusAlgebra().MinPlusDeconvolution(testCurve1, testCurve2, np.linspace(-20, 50, 1401))
# plt.plot(times, events, color='red', label='Deconvolution')

# times, events = MinPlusAlgebra().MinPlusConvolution(testCurve1, testCurve2, np.linspace(0, 40, 1000))
# plt.plot(times, events, color='orange', label='Convolution')

# plt.plot(np.linspace(0, 100, 1000), np.array([testCurve1(x) for x in np.linspace(0, 100, 1000)]), color='blue', label='default linear curve')

# test_events = np.array([testCurve1(x) for x in np.linspace(0, 100, 1000)])
# times, events = MinPlusAlgebra().SelfSubAddClosure(testCurve1, np.linspace(0, 100, 1000), 2)
# plt.plot(times, events)

times = np.linspace(0, 100, 100)
alpha_in_events = np.array([alpha_in(x) for x in times])
alpha_out_events = np.array([alpha_out(x) for x in times])
beta_events = np.array([beta(x) for x in times])

plt.plot(times, alpha_in_events, color='red', label='alpha_in')
plt.plot(times, alpha_out_events, color='blue', label='alpha_out')
plt.plot(times, beta_events, color='green', label='beta')

times, events1 = MinPlusAlgebra().AddConst1(beta, times, 10)
plt.plot(times, events1, color='cyan', label='beta + 10')

times, events2 = MinPlusAlgebra().SelfSubAddClosure2(events1, times, 2)
# plt.plot(times, events2, color='black', label='sub-add closure')

times, events3 = MinPlusAlgebra().MinPlusConvolution2(events1, events2, times)
plt.plot(times, events3, color='orange', label='beta wfc')

plt.xlim(0)
plt.xlabel('t, unixtime(ms)')
plt.ylabel('y(t)')
plt.legend()
plt.show()