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

# Пример визуализации
fig, axes = plt.subplots(2, 1, figsize=(12, 16))

# Первый график - изменение дорожно-транспортной ситуации по часам
router_hourly_counts = wifi_logs.groupby(['hour', 'router_mac', 'router_id']).size().reset_index(name='count')
sns.lineplot(x='hour', y='count', hue='router_mac', data=router_hourly_counts, ax=axes[0])
axes[0].set_title('Изменение дорожно-транспортной ситуации по часам')
axes[0].set_xlabel('Час дня')
axes[0].set_ylabel('Количество перемещений')
axes[0].legend(title='Router MAC', bbox_to_anchor=(1.05, 1), loc='upper left')

# Второй график - изменение дорожно-транспортной ситуации по неделям
wifi_logs['week'] = wifi_logs['tm'].dt.strftime('%Y-%U')
router_weekly_counts = wifi_logs.groupby(['week', 'router_mac', 'router_id']).size().reset_index(name='count')
sns.lineplot(x='week', y='count', hue='router_mac', data=router_weekly_counts, ax=axes[1])
axes[1].set_title('Изменение дорожно-транспортной ситуации по неделям')
axes[1].set_xlabel('Неделя')
axes[1].set_ylabel('Количество перемещений')
axes[1].legend(title='Router MAC', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
