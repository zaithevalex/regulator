import matplotlib
import matplotlib.pyplot as plt

with open('./dataset/x.txt', 'r') as file:
    lines = file.readlines()

times = []
numbers = []

i = 1
for line in lines:
    times.extend(int(num) for num in line.strip().split() if num)

for i in range(0, len(times), 1):
    numbers.append(i+1)

plt.scatter(numbers, times, c='blue')
plt.show()