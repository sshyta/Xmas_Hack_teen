import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_data(file_name, data_folder='data', delimiter=';'):
    file_path = os.path.join(data_folder, file_name)
    return pd.read_csv(file_path, delimiter=delimiter)

def load_geo_data(file_name, data_folder='data', delimiter=';'):
    df = load_data(file_name, data_folder, delimiter)
    df['geometry'] = gpd.GeoSeries.from_wkt(df['geom'])
    return gpd.GeoDataFrame(df)

# Загрузка данных
wifi_logs = load_data('wifi_logs.csv')
road_network = load_geo_data('road_network.csv')
wifi_routers = load_geo_data('wifi_routers.csv')

# Пример анализа данных
for name, data in [('Wi-Fi Logs', wifi_logs), ('Road Network', road_network), ('Wi-Fi Routers', wifi_routers)]:
    print(f"\n{name}:")
    print(data.head())

# Пример визуализации
road_network.plot(figsize=(10, 10))
plt.title('Сеть дорог')
plt.show()

wifi_routers.plot(figsize=(10, 10), marker='o', color='blue', markersize=50, alpha=0.5)
plt.title('Расположение Wi-Fi роутеров')
plt.xlabel('Долгота')
plt.ylabel('Широта')
plt.show()

# Загрузка данных из файла wifi_logs.csv
wifi_logs = load_data('wifi_logs.csv', delimiter=';')
wifi_logs['tm'] = pd.to_datetime(wifi_logs['tm'], utc=True)

# Создание нового столбца 'hour' для анализа по часам
wifi_logs['hour'] = wifi_logs['tm'].dt.hour
wifi_logs['week'] = wifi_logs['tm'].dt.strftime('%Y-%m-%d')

# Группировка данных по часам, роутерам отправителям и роутерам получателям
router_hourly_counts = wifi_logs.groupby(['hour', 'router_mac', 'router_id']).size().reset_index(name='count')

# Построение графика изменения дорожно-транспортной ситуации с течением времени
plt.figure(figsize=(12, 8))
sns.lineplot(x='hour', y='count', hue='router_mac', data=router_hourly_counts)
plt.title('Изменение дорожно-транспортной ситуации с течением времени')
plt.xlabel('Час дня')
plt.ylabel('Количество перемещений')
plt.legend(title='Router MAC', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Создание нового столбца 'week' для анализа по неделям
wifi_logs['week'] = wifi_logs['tm'].dt.strftime('%Y-%U')

# Группировка данных по неделям, роутерам отправителям и роутерам получателям
router_weekly_counts = wifi_logs.groupby(['week', 'router_mac', 'router_id']).size().reset_index(name='count')

# Построение графика изменения дорожно-транспортной ситуации с течением времени (по неделям)
plt.figure(figsize=(12, 8))
sns.lineplot(x='week', y='count', hue='router_mac', data=router_weekly_counts)
plt.title('Изменение дорожно-транспортной ситуации с течением времени (по неделям)')
plt.xlabel('Неделя')
plt.ylabel('Количество перемещений')
plt.xticks(rotation=45, ha='right')  # Повернуть метки по оси X для лучшей читаемости
plt.legend(title='Router MAC', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
