#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Манифест модуля: [RE-PHYSICS, 2026] -> Модуль G / Вектор 4.1: «Kepler-Harmonic-Shock-Generator»
===========================================================================================
Архивный фундамент: Иоганн Кеплер (Harmonices Mundi, 1619) + Методология Семантического Вакуума.
Прикладной метод: Генеративный дизайн метаматериалов на базе слепого "Электрического Шок-Фильтра".

Зачем этот код человеку спустя 30 лет:
Этот модуль генерирует элементарные 3D-ячейки кристаллических метаматериалов (Almaz, Rubin, Sera).
Вместо уравнений Шрёдингера стабильность решетки проверяется через ее "акустическую созвучность".
Расстояния между примесными атомами переводятся в математические пропорции хорд планет. 
Если решетка "фальшивит" (содержит лакуны, дефекты, нестабильные углы) — алгоритм имитирует 
мгновенный электрический шок (штрафной вольтаж), отжигающий и уничтожающий бракованную структуру.
"""

import numpy as np

class KeplerHarmonicShockGenerator:
    """
    Генератор аномальных метаматериалов, управляемый кеплеровскими резонансами 
    и штрафным электрическим вольтажом Шок-Фильтра.
    """
    def __init__(self):
        # Базовая матрица планетных хорд Кеплера (соотношения афелий/перигелий)
        self.kepler_chords = {
            'Saturn':  2.05 / 1.75,   # ~ 1.171
            'Jupiter': 6.30 / 5.50,   # ~ 1.145
            'Mars':    38.18 / 26.23, # ~ 1.455 (Хаотичный, рваный шаг)
            'Earth':   59.13 / 57.17, # ~ 1.034
            'Venus':   96.25 / 94.83, # ~ 1.015
            'Mercury': 384.00 / 164.00 # ~ 2.341 (Максимальный эксцентриситет)
        }
        # Компоненты синтезируемого метаматериала
        self.atom_types = ['C_Almaz', 'Al_Rubin', 'S_Sera']

    def generate_random_lattice(self, num_atoms=8, box_size=5.0):
        """Создание первичного хаотичного облака атомов в 3D-пространстве."""
        lattice = []
        for _ in range(num_atoms):
            atom = {
                'type': np.random.choice(self.atom_types),
                'pos': np.random.uniform(0, box_size, size=3) # Координаты X, Y, Z
            }
            lattice.append(atom)
        return lattice

    def calculate_shock_voltage(self, lattice, resonance_threshold=0.08):
        """
        ЭЛЕКТРИЧЕСКИЙ ШОК-ФИЛЬТР (Слепая селекция).
        Превращает геометрические пропорции решетки в штрафной вольтаж.
        """
        total_voltage_penalty = 0.0
        num_atoms = len(lattice)
        checked_pairs = 0

        # Сканируем межсоседские расстояния во всей 3D-ячейке
        for i in range(num_atoms):
            for j in range(i + 1, num_atoms):
                pos_i = lattice[i]['pos']
                pos_j = lattice[j]['pos']
                
                # Физическое евклидово расстояние между узлами решетки
                distance = np.linalg.norm(pos_i - pos_j)
                if distance < 0.5: # Защита от коллапса (ядерного перекрытия атомов)
                    total_voltage_penalty += 500.0  # Экстремальный шоковый удар
                    continue

                # Ищем третью точку, чтобы построить пропорцию двух плеч решетки (аналог хорды)
                for k in range(num_atoms):
                    if k == i or k == j: 
                        continue
                    pos_k = lattice[k]['pos']
                    distance_alt = np.linalg.norm(pos_i - pos_k)
                    
                    if distance_alt == 0: 
                        continue
                        
                    # Математический чит: Пропорция длин двух связей решетки
                    ratio = max(distance, distance_alt) / min(distance, distance_alt)
                    checked_pairs += 1

                    # Проверяем, "звучит" ли эта пропорция по Кеплеру
                    harmonic_match = False
                    for planet, ideal_ratio in self.kepler_chords.items():
                        if abs(ratio - ideal_ratio) < resonance_threshold:
                            harmonic_match = True
                            break # Узел попал в планетную гармонию!

                    # Если пропорция узлов фальшивит — решетка получает электрический удар
                    if not harmonic_match:
                        # Штрафной вольтаж пропорционален степени "фальши" (удаленности от гармонии)
                        total_voltage_penalty += 15.5
                        
        # Нормируем штраф, если пары были проверены
        return total_voltage_penalty / (checked_pairs + 1)

    def mutate_lattice(self, lattice, mutation_rate=0.2, box_size=5.0):
        """Случайная микро-деформация координат под воздействием теплового отжига."""
        mutated_lattice = []
        for atom in lattice:
            new_pos = atom['pos'] + np.random.normal(0, mutation_rate, size=3)
            # Удерживаем атомы внутри виртуального куба симуляции
            new_pos = np.clip(new_pos, 0, box_size)
            mutated_lattice.append({'type': atom['type'], 'pos': new_pos})
        return mutated_lattice

    def evolve_perfect_material(self, generations=500, num_atoms=10, box_size=4.0):
        """Цикл слепой эволюции метаматериала под ударами Шок-Фильтра."""
        print(f"[Kepler-Shock-Engine]: Запуск синтеза. Целевое число атомов: {num_atoms}")
        
        # Шаг 1: Рождаем хаотичную структуру
        best_lattice = self.generate_random_lattice(num_atoms, box_size)
        best_voltage = self.calculate_shock_voltage(best_lattice)
        
        print(f"  └─► Начальный штрафной вольтаж хаоса: {best_voltage:.2f} В")

        # Эволюционный отжиг решетки
        for gen in range(generations):
            # Создаем мутацию (деформацию под током)
            candidate_lattice = self.mutate_lattice(best_lattice, mutation_rate=0.15, box_size=box_size)
            candidate_voltage = self.calculate_shock_voltage(candidate_lattice)

            # Если мутация снизила вольтаж (решетка стала чище звучать по Кеплеру) — закрепляем её
            if candidate_voltage < best_voltage:
                best_lattice = candidate_lattice
                best_voltage = candidate_voltage

            # Логируем прогресс отсечения дефектов на лету
            if gen % 100 == 0:
                print(f"  ⚡ [Поколение {gen:04d}]: Текущий вольтаж ошибок: {best_voltage:.4f} В")
                
            # Если вольтаж упал до критического минимума — структура стабильна
            if best_voltage < 0.5:
                print(f"🔥 Гармония достигнута на шаге {gen}! Идеальная квазирешетка выращена.")
                break

        print(f"\n[Синтез завершен]: Итоговый штрафной вольтаж: {best_voltage:.4f} В")
        return best_lattice


# =====================================================================
# ТЕСТ ГЕНЕРАТОРА МЕТАМАТЕРИАЛОВ В СРЕДЕ RE-PHYSICS
# =====================================================================
if __name__ == "__main__":
    print("--- RE-PHYSICS 2026: МОДУЛЬ KEPLER-HARMONIC-SHOCK-GENERATOR ---")
    
    # Запускаем генератор метаматериала вслепую
    generator = KeplerHarmonicShockGenerator()
    
    # Выращиваем кристаллическую структуру из 8 примесных узлов (Almaz + Rubin + Sera)
    perfect_crystal = generator.evolve_perfect_material(generations=400, num_atoms=8, box_size=3.5)
    
    print("\n📐 Сгенерированная матрица устойчивых координат атомов:")
    for idx, atom in enumerate(perfect_crystal):
        print(f" Атом #{idx} | Тип: {atom['type']} | Позиция: [{atom['pos'][0]:.3f}, {atom['pos'][1]:.3f}, {atom['pos'][2]:.3f}]")
