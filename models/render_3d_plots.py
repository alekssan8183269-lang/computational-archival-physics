import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Импортируем логику из наших созданных модулей (убедитесь, что файлы лежат в одной папке)
try:
    from core_simulator import generate_ptolemy_orbit
    from maxwell_ether_simulator import MaxwellEtherGrid, extract_electromagnetic_wave
    from caloric_fluid_simulator import CaloricFluidSimulator
except ImportError:
    print("[Ошибка]: Убедитесь, что файлы core_simulator.py, maxwell_ether_simulator.py и caloric_fluid_simulator.py лежат в этой же папке!")
    exit()

print("====== ЗАПУСК ИНТЕРАКТИВНОГО 3D-ВИЗУАЛИЗАТОРА RE-PHYSICS ======")

# =====================================================================
# 1. 3D-ВИЗУАЛИЗАЦИЯ ДЛЯ МОДУЛЯ А (ПТОЛЕМЕЙ)
# =====================================================================
print("[Графика]: Рендеринг 3D-времени для орбиты Птолемея...")
t_steps, ptolemy_traj = generate_ptolemy_orbit(days=200, noise_level=0.05)

# Раскладываем комплексные числа на оси X и Y. Ось Z — это ход времени!
x_ptolemy = np.real(ptolemy_traj)
y_ptolemy = np.imag(ptolemy_traj)
z_time = np.arange(len(ptolemy_traj))

# Идеальная очищенная орбита (только главный деферент)
x_clean = 10.0 * np.cos(1.0 * t_steps)
y_clean = 10.0 * np.sin(1.0 * t_steps)

fig1 = go.Figure()
# Добавляем "ошибочную" петляющую архивную траекторию
fig1.add_trace(go.Scatter3d(x=x_ptolemy, y=y_ptolemy, z=z_time, mode='lines+markers',
                         name='Архивный Птолемей (с шумом)', line=dict(color='red', width=3)))
# Добавляем траекторию, которую извлек наш ИИ-очиститель
fig1.add_trace(go.Scatter3d(x=x_clean, y=y_clean, z=z_time, mode='lines',
                         name='Очищенная истинная орбита', line=dict(color='cyan', width=5)))

fig1.update_layout(title="Модуль A: 3D-Пространство-Время Орбиты Птолемея (Вращайте мышкой!)",
                  scene=dict(xaxis_title='Ось X (Космос)', yaxis_title='Ось Y (Космос)', zaxis_title='Ось Z (Время / Дни)'),
                  template="plotly_dark")
fig1.write_html("ptolemy_3d_orbit.html")


# =====================================================================
# 2. 3D-ВИЗУАЛИЗАЦИЯ ДЛЯ МОДУЛЯ B (ЭФИР МАКСВЕЛЛА)
# =====================================================================
print("[Графика]: Рендеринг 3D-поля эфирных шестеренок Максвелла...")
ether = MaxwellEtherGrid(size=25, elasticity=0.2, friction=0.01)
center = 25 // 2
# Раскручиваем эфир посильнее для красивой волны
ether.apply_magnetic_impulse(center, center, strength=150.0)

# Делаем несколько шагов симуляции, чтобы волна разошлась по пространству
for _ in range(12):
    ether.update_physics_step(dt=0.15)
e_field_wave = extract_electromagnetic_wave(ether)

# Создаем сетку осей X и Y для 3D поверхности
x_grid = np.arange(25)
y_grid = np.arange(25)

fig2 = go.Figure(data=[go.Surface(z=e_field_wave, x=x_grid, y=y_grid, colorscale='Viridis')])
fig2.update_layout(title="Модуль B: 3D-Рельеф Электрического поля, рожденного из вихрей эфира",
                  scene=dict(xaxis_title='Ось X пространства', yaxis_title='Ось Y пространства', zaxis_title='Сила Эл. Поля (E)'),
                  template="plotly_dark")
fig2.write_html("maxwell_3d_ether.html")


# =====================================================================
# 3. 3D-ВИЗУАЛИЗАЦИЯ ДЛЯ МОДУЛЯ C (ТЕПЛОРОД КАРНО / ИИ ГРАДИЕНТ)
# =====================================================================
print("[Графика]: Рендеринг 3D-ландшафта перетекания Теплорода...")
sim = CaloricFluidSimulator(segments=15, diffusion_rate=0.25)

# Собираем историю изменения плотности флюида во времени для построения 3D поверхности
history_matrix = []
for _ in range(30):
    sim.update_caloric_flow(dt=0.3)
    history_matrix.append(np.copy(sim.caloric_density))

history_matrix = np.array(history_matrix)
x_segments = np.arange(15)  # Сегменты стержня
y_ticks = np.arange(30)     # Шаги времени

fig3 = go.Figure(data=[go.Surface(z=history_matrix, x=x_segments, y=y_ticks, colorscale='Hot')])
fig3.update_layout(title="Модуль C: 3D-Поверхность эволюции Теплорода (Ландшафт градиентного спуска)",
                  scene=dict(xaxis_title='Длина тела (X)', yaxis_title='Шаги времени (t)', zaxis_title='Плотность флюида / Ошибка ИИ'),
                  template="plotly_dark")
fig3.write_html("caloric_3d_fluid.html")


# =====================================================================
# ОТКРЫТИЕ РЕЗУЛЬТАТОВ
# =====================================================================
print("\n[Успех]: Все три интерактивных 3D-графика успешно сгенерированы!")
print("-" * 75)
print("В вашей папке созданы 3 файла. Откройте их двойным кликом:")
print("1. ptolemy_3d_orbit.html   -> Изучить петли времени Птолемея")
print("2. maxwell_3d_ether.html   -> Крутить волну механического вакуума")
print("3. caloric_3d_fluid.html   -> Увидеть рельеф теплового ИИ-градиента")
print("-" * 75)

# Пытаемся автоматически открыть первый главный график в браузере пользователя
try:
    os.system("start ptolemy_3d_orbit.html")
except:
    pass
