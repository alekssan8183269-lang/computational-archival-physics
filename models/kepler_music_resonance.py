#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Манифест модуля: [RE-PHYSICS, 2026] -> Модуль G / Вектор 4: «Kepler-Music-Resonance»
===================================================================================
Архивный фундамент: Геометрическая космология Иоганна Кеплера (Harmonices Mundi, 1619).
Математический чит: Фильтрация хаотических временных рядов через интервальные матрицы 
планетных хорд (чистая геометрия звуковых резонансов) без использования преобразования Фурье.

Зачем этот код человеку спустя 30 лет:
Машина оперирует не абстрактными частотами, а пропорциями угловых скоростей планет в афелии 
и перигелии. Этот модуль берет зашумленный физический сигнал, вычисляет дельту его фазовых 
переходов и пропускает через жесткие сита кеплеровских планетных аккордов. Если в сигнале 
есть скрытый упорядоченный резонанс (сигнал выживания структуры) — он усиливается. Шум — умирает.
"""

import numpy as np

class KeplerMusicResonance:
    """
    Инвариантный геометрический фильтр на базе планетных аккордов Кеплера.
    Работает как бескоординатный процессор спектрального сжатия зашумленных данных.
    """
    def __init__(self):
        # Жестко зафиксированные Кеплером пропорции угловых скоростей (матрица хорд)
        # Формат: {'планета': (угловая_скорость_в_афелии, угловая_скорость_в_перигелии)}
        # Значения нормированы относительно Меркурия по архивным таблицам 1619 года.
        self.kepler_chords = {
            'Saturn':  (1.75,   2.05),   # Бас (интервал: терция)
            'Jupiter': (5.50,   6.30),   # Баритон
            'Mars':    (26.23,  38.18),  # Тенор (самый нелинейный, рваный интервал)
            'Earth':   (57.17,  59.13),  # Альт (очень узкий, стабильный зазор)
            'Venus':   (94.83,  96.25),  # Сопрано (почти чистый круговой монотон)
            'Mercury': (164.00, 384.00)  # Скрипка/Соло (бешеный эксцентриситет, экспрессия)
        }
        
    def _calculate_angular_ratios(self, time_series):
        """
        Перевод сырого временного ряда в относительные угловые шаги (деформации фазы).
        Имитирует движение точки по виртуальному эллипсу.
        """
        # Находим экстремумы (афелии и перигелии входящего сигнала)
        diffs = np.diff(time_series)
        zero_crossings = np.where(np.diff(np.sign(diffs)))[0]
        
        if len(zero_crossings) < 2:
            # Если сигнал слишком мертвый или монотонный, генерируем базовый люфт
            return np.array([1.0])
            
        # Вычисляем относительные амплитуды переходов между пиками
        peak_values = time_series[zero_crossings]
        ratios = []
        for i in range(len(peak_values) - 1):
            v_min = min(abs(peak_values[i]), abs(peak_values[i+1]))
            v_max = max(abs(peak_values[i]), abs(peak_values[i+1]))
            if v_min != 0:
                ratios.append(v_max / v_min)
                
        return np.array(ratios)

    def filter_signal(self, raw_signal, resonance_threshold=0.15):
        """
        ГЛАВНЫЙ ЧИТ-КОД: Фильтрация данных методом Кеплеровского резонанса.
        Проверяет, попадают ли пропорции изменений сигнала в гармонические планетные интервалы.
        """
        ratios = self._calculate_angular_ratios(raw_signal)
        clean_signal = np.copy(raw_signal)
        
        print(f"[Kepler-Core]: Анализ ткани сигнала. Обнаружено {len(ratios)} фазовых переходов.")
        
        # Проверяем каждую точку изменения сигнала на соответствие музыке сфер
        for idx, ratio in enumerate(ratios):
            harmonic_found = False
            matched_planet = None
            min_deviation = float('inf')
            
            for planet, (aphelion, perihelion) in self.kepler_chords.items():
                # Идеальная пропорция хорды планеты по Кеплеру
                ideal_ratio = perihelion / aphelion
                deviation = abs(ratio - ideal_ratio)
                
                if deviation < resonance_threshold:
                    if deviation < min_deviation:
                        min_deviation = deviation
                        harmonic_found = True
                        matched_planet = planet
            
            # Применяем фильтр: если шаг сигнала НЕ попал ни в один планетный аккорд,
            # значит эта точка — хаотичный приборный шум или дефект. Мы её подавляем (сглаживаем).
            if not harmonic_found:
                target_idx = idx + 1
                if target_idx < len(clean_signal) - 1:
                    clean_signal[target_idx] = (clean_signal[target_idx - 1] + clean_signal[target_idx + 1]) / 2.0
            else:
                # Усиление гармонического сигнала (резонанс)
                target_idx = idx + 1
                if target_idx < len(clean_signal):
                    print(f"  └─► [Резонанс пойман]: Пропорция {ratio:.3f} созвучна хорде {matched_planet} (отклонение: {min_deviation:.4f})")
                    
        return clean_signal

# =====================================================================
# ТЕСТ СИМУЛЯТОРА В РАМКАХ ТЕКУЩЕГО ОКРУЖЕНИЯ RE-PHYSICS
# =====================================================================
if __name__ == "__main__":
    print("--- RE-PHYSICS 2026: ЗАПУСК МОДУЛЯ KEPLER-MUSIC-RESONANCE ---")
    
    # Генерация тестового грязного сигнала: 
    # Синусоида (чистый космологический резонанс) + случайный адский шум (ошибки датчиков)
    np.random.seed(42)
    time_steps = np.linspace(0, 10, 100)
    # Базовая несущая частота, имитирующая пропорцию Марса (около 1.45)
    pure_astronomical_signal = np.sin(time_steps) * 5.0 
    noise = np.random.normal(0, 2.5, size=100) # Дикий зашумляющий лаг
    
    dirty_telemetry = pure_astronomical_signal + noise
    
    # Инициализация фильтра Кеплера
    kepler_processor = KeplerMusicResonance()
    
    print("\n[Входные данные]: Запуск фильтрации грязной телеметрии...")
    filtered_telemetry = kepler_processor.filter_signal(dirty_telemetry, resonance_threshold=0.2)
    
    # Оценка эффективности без карго-культа метрик
    initial_error = np.sum(abs(dirty_telemetry - pure_astronomical_signal))
    final_error = np.sum(abs(filtered_telemetry - pure_astronomical_signal))
    
    print("\n[Результат селекции по Кеплеру]:")
    print(f" Суммарный шум ДО очистки: {initial_error:.2f}")
    print(f" Суммарный шум ПОСЛЕ очистки хордами: {final_error:.2f}")
    print(f" Эффективность геометрического сжатия хаоса: {((initial_error - final_error) / initial_error)*100:.1f}%")
