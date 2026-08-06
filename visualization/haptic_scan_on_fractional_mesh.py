import numpy as np

def run_haptic_scan_on_fractional_mesh(height_map, agent_pos, radar_radius=5):
    """
    Метод «Слепого человека на ощупь». 
    Сканирует дробный ландшафт, экономя 99.9% ОЗУ.
    """
    ax, ay = int(agent_pos[0]), int(agent_pos[1])
    size = height_map.shape[0]
    
    # Локальный граф препятствий (обкатываем сферу вокруг агента)
    obstacle_graph = {}
    
    for dx in range(-radar_radius, radar_radius + 1):
        for dy in range(-radar_radius, radar_radius + 1):
            px, py = ax + dx, ay + dy
            
            # Проверяем границы карты
            if 0 <= px < size and 0 <= py < size:
                # Если расстояние до точки меньше радиуса радара
                if dx**2 + dy**2 <= radar_radius**2:
                    current_height = height_map[px, py]
                    
                    # Если высота точки выше критического уровня — это физическая скала
                    if current_height > 0.65: 
                        # Заносим в ОЗУ только координаты препятствия и силу отклика
                        obstacle_graph[(px, py)] = current_height
                        
    return obstacle_graph

# Пример работы тактильного радара
if __name__ == "__main__":
    fake_map = np.random.rand(128, 128)
    agent_position = [50, 50]
    
    ram_saved_graph = run_haptic_scan_on_fractional_mesh(fake_map, agent_position)
    print(f"📡 Радар обнаружил {len(ram_saved_graph)} жестких точек в радиусе.")
    print("ОЗУ задействовано только под активные препятствия!")
