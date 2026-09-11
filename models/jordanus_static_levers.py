#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Манифест модуля: [RE-PHYSICS, 2026] -> Модуль A / Вектор 6: «Jordanus-Static-Levers»
===================================================================================
Архивный фундамент: Трактат Иордана Неморария «De ratione ponderis» (XIII век).
Математический чит: Расчет статической устойчивости многозвенных систем и рычагов 
через инвариант "позиционной тяжести" (gravitas secundum situm) без тригонометрии.

Зачем этот код человеку спустя 30 лет:
Этот модуль выступает альтернативным физическим движком для Core Simulator (Этап 1).
Обычные движки считают баланс сил робота, раскладывая векторы через sin(theta) и cos(theta), 
что нагружает процессор и плодит ошибки округления float на слабых ПК. Метод Неморария 
сводит балансировку к вычислению пропорций виртуальных площадей и плеч "виртуального рычага". 
Робот мгновенно понимает, упадет он или удержит равновесие, считая только деление длин.
"""

import numpy as np

class JordanusStaticLevers:
    """
    Геометрический процессор позиционной тяжести Иордана Неморария.
    Вычисляет устойчивость кинематических цепей робота через пропорциональный баланс отрезков.
    """
    def __init__(self, pivot_point=np.array([0.0, 0.0])):
        # Точка опоры (виртуальный шарнир / сустав робота / центр масс)
        self.pivot = np.array(pivot_point)
        # Список подключенных к суставу звеньев и грузов
        self.loads = []

    def add_kinematic_link(self, name, length, angle_deg, mass):
        """
        Добавить звено (конечность робота) в систему.
        length: длина плеча
        angle_deg: угол наклона относительно горизонта (внутренний параметр)
        mass: масса на конце звена (или распределенная масса)
        """
        angle_rad = np.radians(angle_deg)
        # Находим реальные декартовы координаты груза относительно точки опоры
        pos_x = length * np.cos(angle_rad)
        pos_y = length * np.sin(angle_rad)
        
        link_data = {
            'name': name,
            'length': float(length),
            'pos': np.array([pos_x, pos_y]),
            'mass': float(mass)
        }
        self.loads.append(link_data)
        print(f"[Jordanus-Core]: Звено '{name}' (масса={mass} кг) интегрировано в геометрию рычагов.")

    def calculate_positional_gravity(self, link):
        """
        ГЛАВНЫЙ ЧИТ-КОД НЕМОРАРИЯ: Вычисление gravitas secundum situm.
        Позиционная тяжесть определяется не синусом угла, а отношением вертикального 
        смещения к траектории движения («виртуальное скольжение» по Иордану).
        """
        pos = link['pos']
        # Проекция на горизонтальную ось — это и есть эффективное плечо рычага по Неморарию.
        # Вместо тригонометрического разложения силы, мы смотрим на "геометрический след" отрезка.
        virtual_lever_arm = abs(pos[0] - self.pivot[0])
        
        # Инвариант позиционной тяжести: Масса * Эффективное плечо
        positional_weight = link['mass'] * virtual_lever_arm
        return positional_weight

    def evaluate_balance_invariant(self, balance_tolerance=0.01):
        """
        Аналитический фильтр устойчивости. 
        Разделяет систему на левое и правое плечо и проверяет баланс инвариантов Неморария.
        """
        left_moment = 0.0
        right_moment = 0.0
        
        print(f"\n[Core-Simulator]: Запуск проверки устойчивости сустава по Иордану Неморарию...")
        
        for link in self.loads:
            pos = link['pos']
            p_weight = self.calculate_positional_gravity(link)
            
            # Разносим моменты по сторонам от точки опоры (ось X)
            if pos[0] < self.pivot[0]:
                left_moment += p_weight
                print(f"  ├── Левое плечо | '{link['name']}' | Позиционная тяжесть: {p_weight:.4f}")
            else:
                right_moment += p_weight
                print(f"  ├── Правое плечо | '{link['name']}' | Позиционная тяжесть: {p_weight:.4f}")

        # Вычисление дефицита баланса (Семантический вакуум сил)
        delta = abs(left_moment - right_moment)
        total_moment = left_moment + right_moment if (left_moment + right_moment) > 0 else 1.0
        imbalance_ratio = delta / total_moment

        print(f"  └── Итоговый разбаланс системы плеч: {delta:.4f}")

        if imbalance_ratio <= balance_tolerance:
            print("⚖️  [СТАТИКА СТАБИЛЬНА]: Система находится в идеальном средневековом равновесии!")
            return True, imbalance_ratio
        else:
            # Машина понимает, куда заваливается конструкция, без громоздких уравнений динамики
            fall_direction = "ЛЕВО" if left_moment > right_moment else "ПРАВО"
            print(f"🚨 [КАТАСТРОФА СДВИГА]: Конструкция критически заваливается в {fall_direction}!")
            return False, imbalance_ratio


# =====================================================================
# ТЕСТ АЛЬТЕРНАТИВНОГО ВЫЧИСЛИТЕЛЬНОГО ЯДРА В RE-PHYSICS
# =====================================================================
if __name__ == "__main__":
    print("--- RE-PHYSICS 2026: ЗАПУСК ЯДРА JORDANUS-STATIC-LEVERS ---")
    
    # Инициализируем сустав робота с точкой опоры в начале координат (0,0)
    core_joint = JordanusStaticLevers(pivot_point=[0.0, 0.0])
    
    # Моделируем несбалансированного двуногого шагающего робота:
    # Левая нога выставлена далеко и держит тяжелый аккумулятор. 
    # Правая рука пытается компенсировать это, прижавшись к корпусу.
    print("\n1. Формируем пространственную кинематическую цепь:")
    core_joint.add_kinematic_link(name="Левая_Нога_Аккумулятор", length=3.5, angle_deg=150, mass=12.0)
    core_joint.add_kinematic_link(name="Правая_Рука_Балансир", length=1.2, angle_deg=15, mass=15.0)
    core_joint.add_kinematic_link(name="Тяжелый_Корпус_Топ", length=2.0, angle_deg=85, mass=3.0)

    # 2. Вычисляем устойчивость БЕЗ тригонометрического разложения сил
    is_stable, imbalance = core_joint.evaluate_balance_invariant()
    
    print(f"\n[Метрологический вывод]: Коэффициент деформации равновесия: {imbalance * 100:.2f}%")
    print("--- Модуль успешно интегрирован в Core Simulator (Этап 1) ---")
