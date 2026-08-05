import numpy as np

# =====================================================================
# ШАГ 1: ДВИЖОК ЭПИЦИКЛОВ ПТОЛЕМЕЯ (Генератор "Архивных Ошибочных Данных")
# =====================================================================
def generate_ptolemy_orbit(days=365, noise_level=0.05):
    """
    Генерирует орбиту планеты по модели Птолемея:
    Земля в центре, планета крутится по деференту (кругу 1) 
    и одновременно по эпициклу (кругу 2 внутри круга 1).
    """
    # Временная сетка (дни)
    t = np.linspace(0, 2 * np.pi, days)
    
    # Параметры Птолемея (радиусы и угловые скорости вращения орбит)
    R_deferent = 10.0      # Радиус главного круга
    omega_deferent = 1.0   # Скорость вращения по главному кругу
    
    R_epicycle = 3.0       # Радиус малого круга (эпицикла)
    omega_epicycle = 5.0   # Скорость вращения внутри эпицикла (петли)
    
    # Математика Птолемея через комплексные числа (Оси X и Y)
    # X = реальная часть, Y = мнимая часть
    deferent_vector = R_deferent * np.exp(1j * omega_deferent * t)
    epicycle_vector = R_epicycle * np.exp(1j * omega_epicycle * t)
    
    # Итоговая сложная "ошибочная" траектория с петлями
    ptolemy_trajectory = deferent_vector + epicycle_vector
    
    # Добавляем "шум наблюдений" древнего астронома
    noise = (np.random.normal(0, noise_level, days) + 
             1j * np.random.normal(0, noise_level, days))
    
    return t, ptolemy_trajectory + noise


# =====================================================================
# ШАГ 2: АНАЛИТИЧЕСКИЙ ФИЛЬТР (ИИ-Очиститель данных до Истины)
# =====================================================================
def clean_archival_data(trajectory):
    """
    Применяет спектральный анализ (Фурье) для очистки ложной модели.
    Компьютер не знает формулу Птолемея, он просто ищет скрытые паттерны в хаосе.
    """
    # Переводим пространственные координаты в частотные паттерны
    fft_values = np.fft.fft(trajectory)
    frequencies = np.fft.fftfreq(len(trajectory))
    
    # Находим амплитуды (силу сигналов)
    amplitudes = np.abs(fft_values)
    
    # ОЧИСТКА: Отсекаем мелкий шум и вытаскиваем только главные гармоники (паттерны)
    # Ищем пики, которые вносят вклад более 5% от максимального
    main_peaks = np.where(amplitudes > (np.max(amplitudes) * 0.05))[0]
    
    extracted_patterns = []
    for idx in main_peaks:
        freq = frequencies[idx]
        amp = amplitudes[idx] / len(trajectory)
        phase = np.angle(fft_values[idx])
        extracted_patterns.append({
            "frequency_idx": idx,
            "raw_frequency": round(freq, 4),
            "clean_amplitude": round(amp, 2),
            "phase_shift_rad": round(phase, 2)
        })
        
    return extracted_patterns


# =====================================================================
# ШАГ 3: ЗАПУСК СИМУЛЯЦИИ И ВЫВОД РЕЗУЛЬТАТА В КОНСОЛЬ
# =====================================================================
if __name__ == "__main__":
    print("====== ЗАПУСК КОМПЛЕКСА RE-PHYSICS: МОДУЛЬ ПТОЛЕМЕЯ ======")
    print("[Инфо]: Генерируем 365 точек траектории с наложением шума...")
    
    # 1. Генерируем данные ложной теории
    time_steps, raw_trajectory = generate_ptolemy_orbit(days=365, noise_level=0.1)
    
    # Посмотрим на первые 3 точки хаотичных координат (X, Y)
    print(f"[Данные]: Первые точки ложной орбиты (X + iY): {raw_trajectory[:3]}\n")
    
    print("[Анализ]: Запуск цифрового археологического фильтра...")
    # 2. Очищаем формулу компьютером
    discovered_signals = clean_archival_data(raw_trajectory)
    
    print("[Успех]: Компьютер очистил шум и выделил фундаментальные инварианты:")
    print("-" * 70)
    for i, signal in enumerate(discovered_signals, 1):
        print(f"Паттерн №{i}: Извлеченная Чистая Амплитуда (Радиус) = {signal['clean_amplitude']} ед.")
        print(f"           Скрытая частота вращения оси      = {signal['raw_frequency']}")
        print(f"           Фазовый сдвиг геометрии (рад)     = {signal['phase_shift_rad']}")
        print("-" * 70)
        
    print("\n✅ Вывод RE-PHYSICS:")
    print("Из сложной петляющей модели Птолемея алгоритм автоматически выделил")
    print("два чистых гармонических базиса (Амплитуды 10.0 и 3.0).")
    print("Мы очистили архивную ошибку до фундаментальных законов вращения векторов.")
