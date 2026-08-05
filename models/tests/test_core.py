import pytest
import numpy as np
import torch
import torch.nn as nn

# Импортируем ваши модули из папки models
# Примечание: после установки через `pip install -e .` импорты будут работать именно так
from rephysics.models.ptolemy_core import PtolemyFFTCore
from rephysics.models.void_map import DigitalVoidProcessor
from rephysics.models.caloric_descent_optimizer import CaloricVoidDescent

@pytest.fixture
def synthetic_data():
    """Фикстура для создания зашумленного циклического сигнала с аномалией (лакуной)."""
    np.random.seed(42)
    t = np.linspace(0, 10, 200)
    # Истинный периодический закон природы
    y_true = np.sin(2 * np.pi * 0.2 * t)
    # Искусственная архивная "ошибка" (интеллектуальный вакуум) в середине датасета
    y_archival = np.sin(2 * np.pi * 0.2 * t) + np.random.normal(0, 0.1, 200)
    y_archival[80:120] += 3.0  # Локальный провал/всплеск архивной модели
    return t, y_true, y_archival

def test_ptolemy_fft_core_generation(synthetic_data):
    """Тест Слоя 2: Проверяем, что PtolemyFFTCore корректно строит суррогатную траекторию."""
    t, y_true, _ = synthetic_data
    
    # Инициализируем и обучаем Птолемея
    ptolemy = PtolemyFFTCore(max_epicycles=3)
    ptolemy.fit_archival_orbits(t, y_true)
    
    # Генерируем траекторию эпициклов
    trajectory = ptolemy.generate_surrogate_trajectory(t)
    
    assert trajectory.shape == t.shape, "Размерность выходящей траектории должна совпадать со временем"
    assert ptolemy.deferent_radius is not None, "Базовый деферент должен быть рассчитан"
    assert len(ptolemy.epicycles_params) <= 3, "Количество эпициклов не должно превышать max_epicycles"

def test_digital_void_processor_mask(synthetic_data):
    """Тест Слоя 3: Проверяем, что Метод Цифровых Пустот успешно находит аномалии."""
    t, y_true, y_archival = synthetic_data
    
    processor = DigitalVoidProcessor(threshold_tau=1.5)
    void_landscape = processor.fit_void_landscape(y_true, y_archival, t)
    invariants = processor.extract_topological_invariants()
    graph = processor.build_deficit_graph(invariants)
    
    assert void_landscape.shape == y_true.shape, "Карта пустот должна повторять размерность данных"
    assert invariants["critical_nodes_count"] > 0, "Процессор должен обнаружить зону искусственной ошибки (3.0)"
    assert "nodes" in graph and "edges" in graph, "Граф дефицита должен содержать узлы и ребра"

def test_caloric_descent_optimization():
    """Тест Слоя 4а: Проверяем работоспособность термодинамического шага оптимизатора."""
    # Создаем простейшую модель ИИ
    model = nn.Linear(10, 1)
    optimizer = CaloricVoidDescent(model.parameters(), lr=0.1, caloric_capacity=1.2)
    
    # Имитируем маску цифровых пустот от процессора
    fake_void_mask = torch.ones(10) * 2.5
    
    # Прямой и обратный проход PyTorch
    inputs = torch.randn(1, 10)
    target = torch.tensor([[0.5]])
    loss_fn = nn.MSELoss()
    
    output = model(inputs)
    loss = loss_fn(output, target)
    loss.backward()
    
    # Проверяем, что шаг выполняется без падения тензоров
    try:
        optimizer.step(void_mask_tensor=fake_void_mask)
        step_passed = True
    except Exception as e:
        step_passed = False
        print(f"Ошибка шага оптимизатора: {e}")
        
    assert step_passed is True, "Оптимизатор CaloricVoidDescent должен успешно выполнять шаг step()"
