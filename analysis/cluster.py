import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Генерация примера данных (возрастающая функция)
np.random.seed(0)
x = np.sort(np.random.rand(500))  # 500 точек в диапазоне [0, 1]
y = np.sin(2 * np.pi * x) + 0.5 * x + 0.1 * np.random.normal(size=x.shape)  # Пример возрастающей функции с шумом

# Функция для кусочной линейной аппроксимации
def piecewise_linear_fit(x, y, num_segments):
    segment_length = len(x) // num_segments
    segments = []

    for i in range(num_segments):
        start_index = i * segment_length
        end_index = (i + 1) * segment_length if (i < num_segments - 1) else len(x)

        # Получаем сегмент данных
        x_segment = x[start_index:end_index].reshape(-1, 1)
        y_segment = y[start_index:end_index]

        # Линейная регрессия
        model = LinearRegression()
        model.fit(x_segment, y_segment)

        # Сохраняем коэффициенты
        segments.append((model.coef_[0], model.intercept_, x_segment))

    # Проверка и коррекция наклонов для обеспечения строго возрастающей функции
    for i in range(1, len(segments)):
        if segments[i][0] <= segments[i-1][0]:  # Если наклон не увеличивается
            segments[i] = (segments[i-1][0] + 1e-5, segments[i][1], segments[i][2])  # Увеличиваем наклон

    return segments

# Количество сегментов
num_segments = 5
segments = piecewise_linear_fit(x, y, num_segments)

# Визуализация
plt.scatter(x, y, color='blue', label='Данные', alpha=0.5)

for slope, intercept, x_segment in segments:
    x_line = np.linspace(x_segment[0], x_segment[-1], 100)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line, color='red')

plt.title('Кусочная линейная аппроксимация (возрастающая функция)')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
