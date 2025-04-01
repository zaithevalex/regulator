import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Пример данных
data_x = {'x': [1, 2, 3, 4, 5]}
data_y = {'y': [2, 3, 5, 7, 11]}  # Пример значений Y

# Создаем DataFrame
df_x = pd.DataFrame(data_x)
df_y = pd.DataFrame(data_y)

# Создаем интерполяционную функцию
interp_function = interp1d(df_x['x'], df_y['y'], fill_value="extrapolate")

# Функция для получения y по x
def y_function(x):
    return interp_function(x)

# Пример использования функции
x_values = np.array([1, 2, 3, 4, 5])  # Новые значения x
y_values = y_function(x_values)

print("Значения y для x =", x_values, ":", y_values)

# Визуализация
plt.scatter(df_x['x'], df_y['y'], color='red', label='Данные')
plt.plot(x_values, y_values, 'bo', label='Интерполированные точки')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Интерполяция данных')
plt.grid()
plt.show()