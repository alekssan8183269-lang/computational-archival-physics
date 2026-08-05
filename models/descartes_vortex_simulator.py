# =====================================================================
# 4. 3D-ВИЗУАЛИЗАЦИЯ ДЛЯ МОДУЛЯ D (ДЕКАРТ / ВИХРИ)
# =====================================================================
print("[Графика]: Рендеринг 3D-водоворота Декарта...")
vortex_sim = DescartesVortexSimulator(num_particles=300, vortex_strength=30.0)

# Делаем симуляцию и собираем точки во времени (Ось Z будет шагами времени)
x_vortex_history = []
y_vortex_history = []
z_vortex_time = []

for t_step in range(50):
    vortex_sim.update_vortex_motion(dt=0.1)
    x_c, y_c, _ = clean_vortices_to_orbits(vortex_sim.r, vortex_sim.phi)
    
    x_vortex_history.extend(x_c)
    y_vortex_history.extend(y_c)
    z_vortex_time.extend([t_step] * len(x_c))

fig4 = go.Figure(data=[go.Scatter3d(
    x=x_vortex_history, y=y_vortex_history, z=z_vortex_time,
    mode='markers',
    marker=dict(size=2, color=z_vortex_time, colorscale='Plasma', opacity=0.6)
)])

fig4.update_layout(title="Модуль D: 3D-Траектория Космического Водоворота Декарта (Вращайте спираль!)",
                  scene=dict(xaxis_title='Пространство X', yaxis_title='Пространство Y', zaxis_title='Эволюция времени (t)'),
                  template="plotly_dark")
fig4.write_html("descartes_3d_vortex.html")
print("[Успех]: Файл descartes_3d_vortex.html успешно создан.")
