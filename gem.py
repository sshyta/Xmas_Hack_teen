import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных
data_folder = 'data'

# Загрузка данных о WiFi-логах
wifi_logs = pd.read_csv(os.path.join(data_folder, 'wifi_logs.csv'), delimiter=';', parse_dates=['tm'])

# Загрузка данных о дорожной сети
road_network = pd.read_csv(os.path.join(data_folder, 'road_network.csv'), delimiter=';')

# Загрузка данных о WiFi-роутерах
wifi_routers = pd.read_csv(os.path.join(data_folder, 'wifi_routers.csv'), delimiter=';')

# Преобразование столбца 'tm' в формат datetime
wifi_logs['tm'] = pd.to_datetime(wifi_logs['tm'], utc=True)

# Создание нового столбца 'hour' для анализа по часам
wifi_logs['hour'] = wifi_logs['tm'].dt.hour

# Определение интервалов: утренний час пик, день, вечерний час пик
morning_peak_interval = (6, 10)
day_interval = (10, 16)
evening_peak_interval = (16, 20)

# Функция для определения интервала времени
def get_time_interval(hour):
    if morning_peak_interval[0] <= hour < morning_peak_interval[1]:
        return "Morning Peak"
    elif day_interval[0] <= hour < day_interval[1]:
        return "Day"
    elif evening_peak_interval[0] <= hour < evening_peak_interval[1]:
        return "Evening Peak"
    else:
        return "Other"

# Применение функции для создания нового столбца 'time_interval'
wifi_logs['time_interval'] = wifi_logs['hour'].apply(get_time_interval)

# Группировка данных для подсчета среднего времени поездки и общего количества в каждом интервале
movement_matrix = wifi_logs.groupby(['router_mac', 'router_id', 'time_interval']).agg({'tm': ['count', 'mean']}).reset_index()

# Переименование столбцов
movement_matrix.columns = ['router_mac', 'router_id', 'time_interval', 'count', 'mean_time']

# Создание матриц перемещений
matrix_day = movement_matrix[movement_matrix['time_interval'] == 'Day'].pivot_table(values=['count', 'mean_time'], index='router_mac', columns='router_id', fill_value=0)
matrix_morning_peak = movement_matrix[movement_matrix['time_interval'] == 'Morning Peak'].pivot_table(values=['count', 'mean_time'], index='router_mac', columns='router_id', fill_value=0)
matrix_evening_peak = movement_matrix[movement_matrix['time_interval'] == 'Evening Peak'].pivot_table(values=['count', 'mean_time'], index='router_mac', columns='router_id', fill_value=0)

# Визуализация матриц перемещений
def visualize_movement_matrix(matrix, title):
    plt.figure(figsize=(12, 10))
    sns.heatmap(matrix, cmap="YlGnBu", annot=True, fmt=".2f", linewidths=.5)
    plt.title(title)
    plt.xlabel("Router ID")
    plt.ylabel("Router MAC")
    plt.show()

visualize_movement_matrix(matrix_day, "Movement Matrix - Day")
visualize_movement_matrix(matrix_morning_peak, "Movement Matrix - Morning Peak")
visualize_movement_matrix(matrix_evening_peak, "Movement Matrix - Evening Peak")
