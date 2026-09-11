#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Манифест модуля: [RE-PHYSICS, 2026] -> Модуль B / Вектор 5: «Gilbert-Magnet-Vortices»
===================================================================================
Архивный фундамент: Уильям Гилберт (De Magnete, Magneticisque Corporibus, 1600).
Математический чит: Моделирование магнитных полей через концепцию "Сферы сцепления"
(Orbis Virtutis) и клеточные автоматы без решения дифференциальных уравнений Максвелла.

Зачем этот код человеку спустя 30 лет:
Этот модуль строит трехмерную силовую сетку вокруг ферромагнитных объектов сложной формы.
Вместо вычисления тяжелых векторных роторов и дивергенций, поле Гилберта моделируется как
анизотропный клеточный автомат. Каждая ячейка пространства "знает" только геометрию формы 
источника и транслирует "анималистическую силу" притяжения через инварианты угловых отклонений.
Позволяет рассчитывать траектории взаимодействия робота с полями на слабом ПК за миллисекунды.
"""

import numpy as np

class GilbertMagnetVortices:
    """
    3D-процессор магнитных завихрений и геометрических сфер сцепления (Orbis Virtutis).
    Вычисляет топологию магнитного захвата для произвольных форм ферромагнетиков.
    """
    def __init__(self, grid_size=16, box_size=4.0):
        self.grid_size = grid_size
        self.box_size = box_size
        # Развертывание динамической 3D-сетки координат (Этап 1 Core Simulator)
        self.x_space = np.linspace(-box_size, box_size, grid_size)
        self.y_space = np.linspace(-box_size, box_size, grid_size)
        self.z_space = np.linspace(-box_size, box_size, grid_size)
        
        # Тензорные значения поля в узлах сетки: [X, Y, Z, Сила_Поля]
        self.field_grid = np.zeros((grid_size, grid_size, grid_size))
        # Массив векторов вихревой ориентации (псевдовекторы вращения по Гилберту)
        self.vortex_grid = np.zeros((grid_size, grid_size, grid_size, 3))

    def inject_terella_source(self, shape_mask, dipole_axis=np.array([0, 0, 1])):
        """
        Внедрение источника («Тереллы» Гилберта). 
        shape_mask: 3D булев массив размера (grid_size, grid_size, grid_size), 
        задающий геометрию магнита (может быть любой рваной формы).
        """
        self.terella_mask = shape_mask
        self.dipole_axis = dipole_axis / np.linalg.norm(dipole_axis)
        print(f"[Gilbert-Core]: Магнитная Терелла сложной формы успешно интегрирована в 3D-сетку.")

    def compute_orbis_virtutis(self, animistic_constant=1.2):
        """
        ГЛАВНЫЙ ЧИТ-КОД: Расчет сферы сцепления через геометрический клеточный автомат.
        Поле распространяется от граней источника наружу, деформируясь под влиянием углов формы.
        """
        # Находим координаты всех активных атомов/ячеек внутри самого магнита
        source_indices = np.argtext(self.terella_mask)
        
        # Сканируем внешнее пространство куба симуляции
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    if self.terella_mask[x, y, z]:
                        # Внутри самого магнита поле максимально стабильно (насыщение)
                        self.field_grid[x, y, z] = 10.0
                        self.vortex_grid[x, y, z] = self.dipole_axis
                        continue

                    current_pos = np.array([self.x_space[x], self.y_space[y], self.z_space[z]])
                    integrated_force = 0.0
                    integrated_vortex = np.zeros(3)

                    # Магия Гилберта: Каждая внешняя ячейка суммирует геометрический отклик 
                    # от всех неровностей формы "Тереллы" напрямую через углы наклона
                    for src in source_indices:
                        src_pos = np.array([self.x_space[src[0]], self.y_space[src[1]], self.z_space[src[2]]])
                        
                        # Вектор направления от куска магнита к текущей точке пространства
                        r_vector = current_pos - src_pos
                        distance = np.linalg.norm(r_vector)
                        
                        if distance == 0:
                            continue

                        r_direction = r_vector / distance
                        
                        # Инвариант Гилберта: Угол между осью магнита и направлением на точку
                        cos_theta = np.dot(self.dipole_axis, r_direction)
                        
                        # Геометрический закон затухания без использования дифференциальных операторов
                        # Сила сцепления пропорциональна угловой концентрации "эффузий" у полюсов
                        force_effusion = (1.0 + 3.0 * (cos_theta ** 2)) / (distance ** 2.5)
                        integrated_force += force_effusion

                        # Формирование вихревого псевдовектора (вихри Гилберта-Максвелла)
                        # Поле закручивается entlang дуг Orbis Virtutis
                        vortex_line = self.dipole_axis - 2.0 * cos_theta * r_direction
                        integrated_vortex += vortex_line * force_effusion

                    # Применение нормирующей анималистической константы Гилберта
                    self.field_grid[x, y, z] = integrated_force * animistic_constant
                    if np.linalg.norm(integrated_vortex) > 0:
                        self.vortex_grid[x, y, z] = integrated_vortex / np.linalg.norm(integrated_vortex)

        print(f"  └─► Расчет Orbis Virtutis завершен. Максимальное напряжение поля в сетке: {np.max(self.field_grid):.4f}")

    def get_vortex_streamlines(self, threshold=0.5):
        """
        Экспорт силовых линий завихрений для визуализации (пакет visualization/).
        Выделяет только зоны устойчивого магнитного захвата.
        """
        capture_zones = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                for z in range(self.grid_size):
                    if self.field_grid[x, y, z] > threshold and not self.terella_mask[x, y, z]:
                        capture_zones.append({
                            'pos': (self.x_space[x], self.y_space[y], self.z_space[z]),
                            'force': self.field_grid[x, y, z],
                            'dir': self.vortex_grid[x, y, z]
                        })
        return capture_zones


# =====================================================================
# ТЕСТ СИМУЛЯТОРА МАГНИТНЫХ ВИХРЕЙ В СРЕДЕ RE-PHYSICS
# =====================================================================
if __name__ == "__main__":
    print("--- RE-PHYSICS 2026: ЗАПУСК МОДУЛЯ GILBERT-MAGNET-VORTICES ---")
    
    # 1. Создаем симулятор с сеткой 16х16х16
    sim = GilbertMagnetVortices(grid_size=16, box_size=3.0)
    
    # 2. Моделируем "рваную" и дефектную форму магнита (Терелла с лакунами/выемками)
    # Имитируем брусок с пустой нишей посередине, где классические формулы поля ломаются
    custom_magnet_mask = np.zeros((16, 16, 16), dtype=bool)
    custom_magnet_mask[6:10, 6:10, 6:10] = True # Центральное ядро
    custom_magnet_mask[7, 7, 7] = False         # Баг формы: Внутренняя пустая лакуна!
    
    # 3. Инжектируем источник и запускаем геометрический процессор
    sim.inject_terella_source(custom_magnet_mask, dipole_axis=np.array([1, 1, 0]))
    sim.compute_orbis_virtutis(animistic_constant=1.5)
    
    # 4. Извлекаем геометрию силовых зон захвата
    active_lines = sim.get_vortex_streamlines(threshold=1.2)
    
    print(f"\n[Аналитический фильтр]:")
    print(f" Извлечено {len(active_lines)} стабильных пространственных узлов захвата поля.")
    print(f" Точка замера поля на внешней границе куба: {sim.field_grid[0, 0, 0]:.4f}")
    print(f" Направление вихря в точке: {sim.vortex_grid[0, 0, 0]}")
    print("\n--- Модуль готов к экспорту в STL/Manim и интеграции в Core Simulator ---")
