import numpy as np

# ==============================================================================
# МОДУЛЬ: Emission-Optics-Trap (Вектор 3 + Метод F фреймворка RE-PHYSICS)
# ЭПИСТЕМЕ: Согласно Платону, свет — это лучи, исходящие из наблюдателя (экстрамиссия).
# Мы используем эту ложную оптику для расчета читерского поглощения света кристалом.
# Мы пускаем "лучи Платона" снаружи внутрь матрицы 2D-ландшафта потерь.
# Алмаз (C) и Рубин (Al) работают как идеальные зеркала, а Сера (S) — как черная дыра.
# Наша цель — заставить компьютер так расставить атомы Серы, чтобы входящий луч 
# бесконечно отражался от Алмаза и полностью поглотился Серой, не выйдя наружу.
# ==============================================================================

class EmissionOpticsSimulator:
    def __init__(self, size=8):
        self.size = size
        # Оптические свойства элементов для Лучей Платона:
        # 'C' и 'Al' отражают лучи, 'S' (Сера) — поглощает флюид света
        self.optical_properties = {
            'C':  {'type': 'reflect', 'efficiency': 1.0},
            'Al': {'type': 'reflect', 'efficiency': 0.8},
            'S':  {'type': 'absorb',  'efficiency': 0.95}
        }

    def simulate_plato_rays(self, crystal_grid, ray_entry_y):
        """
        Реализует Спектрально-волновое детектирование провалов и Метод Цифровых Пустот.
        crystal_grid: матрица 8x8, заполненная типами атомов ('C', 'Al', 'S')
        ray_entry_y: координата Y, куда вонзается входящий луч Платона
        """
        # Начальная позиция луча (входит слева: x=0, y=ray_entry_y)
        pos_x = 0
        pos_y = ray_entry_y
        
        # Направление луча: [dx, dy] (изначально летит строго вправо)
        direction = np.array([1, 0])
        
        shock_voltage = 0.0
        light_absorbed = 0.0
        ray_energy = 100.0 # Начальная энергия платоновского луча
        steps = 0
        
        # Трассировка луча Платона (максимум 50 шагов внутри ловушки)
        while 0 <= pos_x < self.size and 0 <= pos_y < self.size and ray_energy > 5.0 and steps < 50:
            atom = crystal_grid[pos_x][pos_y]
            prop = self.optical_properties[atom]
            
            if prop['type'] == 'absorb':
                # 🎉 ЧИТЕРСКИЙ БОНУС: Сера поглощает энергию луча!
                absorbed = ray_energy * prop['efficiency']
                light_absorbed += absorbed
                ray_energy -= absorbed
                # Отскок от поглотителя (хаотичное изменение направления)
                direction = -direction 
                
            elif prop['type'] == 'reflect':
                # Алмаз/Рубин зеркально отражают луч. Меняем вектор направления (X или Y)
                if abs(direction[0]) > 0:
                    direction[0] = -direction[0] # Отскок по горизонтали
                else:
                    direction[1] = -direction[1] # Отскок по вертикали
                
                ray_energy *= prop['efficiency'] # Небольшие потери энергии при отражении
                
            # Двигаем луч на следующий шаг
            pos_x += direction[0]
            pos_y += direction[1]
            steps += 1

        # ⚡️ НАШ УДАР ТОКОМ (Функция штрафа RE-PHYSICS)
        # Если луч вылетел обратно наружу (ray_energy > 5) — кристалл "бликует", ловушка сломана!
        # Шарахаем компьютер током пропорционально оставшейся энергии луча
        if ray_energy > 5.0:
            shock_voltage += ray_energy * 450 # Жесткий разряд за упущенный свет!
            
        # Если луч зациклился и сделал 50 шагов, но ничего не поглотилось — это тоже баг
        if steps >= 50 and light_absorbed < 10.0:
            shock_voltage += 2000.0
            
        # Бонус за тотальное поглощение (снижает штрафной баланс)
        shock_voltage -= light_absorbed * 15
        shock_voltage = max(0.0, shock_voltage)
        
        return shock_voltage, light_absorbed, steps

# ==============================================================================
# ОПТИМИЗАТОР ПЛАТОНОВСКИХ ЛОВУШЕК (Эволюционное ядро)
# ==============================================================================
if __name__ == "__main__":
    print("💎 RE-PHYSICS: Запуск Вектора 3 (Платоновская Оптика / Emission-Optics)")
    print("🧪 Цель: Найти фрактальный мотив Серы для 100% поглощения луча света\n")
    
    size = 8
    simulator = EmissionOpticsSimulator(size=size)
    
    # Создаем базовую матрицу: всё заполнено прочным Алмазом ('C')
    best_grid = None
    min_shock = float('inf')
    max_absorption = 0.0
    
    # 5000 итераций интуитивного нащупывания
    for step in range(1, 5001):
        # Компьютер берет алмазную сетку
        test_grid = np.full((size, size), 'C', dtype=object)
        
        # И случайно "впаивает" туда несколько атомов Серы ('S') и Рубина ('Al')
        for _ in range(12): # 12 случайных примесей
            rx, ry = np.random.randint(0, size), np.random.randint(0, size)
            test_grid[rx][ry] = np.random.choice(['S', 'Al'], p=[0.7, 0.3])
            
        # Пускаем луч Платона в координату Y = 3
        shock, absorption, path_steps = simulator.simulate_plato_rays(test_grid, ray_entry_y=3)
        
        # Селекция: если шоковый вольтаж меньше — фиксируем читерскую оптическую ловушку
        if shock < min_shock:
            min_shock = shock
            best_grid = test_grid
            max_absorption = absorption
            print(f"Шаг {step}: Световая ловушка перестроилась! Ток: {shock:.1f} V | Поглощено: {absorption:.1f}% | Шагов луча: {path_steps}")
            
            if min_shock == 0:
                print("\n🎉 БЕЗУПРЕЧНЫЙ МОТИВ НАЙДЕН! Луч полностью заперт во фрактале.")
                break
                
    print("\n🎉 Результат оптимизации Вектора 3!")
    print(f"Финальный пробой тока: {min_shock:.2f} V")
    print(f"Процент удержания света внутри минерала: {max_absorption:.2f}%")
    print("\nФрактальная карта решетки (C - Алмаз, Al - Рубин, S - Сера):")
    for row in best_grid:
        print(" ".join(row))
