import numpy as np
import matplotlib.pyplot as plt

# Генерация данных

# Построение прямоугольной кривой (ступенчатой функции)
plt.step([0, 1, 2, 3, 4, 5], [0, 1, 1, 1, 2, 2], where='post', label='Прямоугольная кривая', color='blue')
# Настройка графика
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Прямоугольная кривая (ступенчатая функция)')
plt.legend()
plt.grid()
plt.show()