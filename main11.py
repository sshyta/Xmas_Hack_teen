import os
import time
from pathlib import Path

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from geopandas import GeoDataFrame


def load_data(file_name, data_folder='data', delimiter=';'):
    print(data_folder, file_name)
    file_path = os.path.join(data_folder, file_name)
    return pd.read_csv(file_path, delimiter=delimiter)


def load_geo_data(file_name, data_folder='data', delimiter=';'):
    df = load_data(file_name, data_folder, delimiter)
    df['geometry'] = gpd.GeoSeries.from_wkt(df['geom'])
    return gpd.GeoDataFrame(df)


# Загрузка данных


def show_road_network(road_network: GeoDataFrame):
    # Пример визуализации
    print(1)
    road_network.plot(figsize=(10, 10), legend=True)
    print(2)
    plt.title('Сеть дорог')
    print(3)
    plt.show()


# show_road_network(load_geo_data('road_network.csv'))


def show_wifi_routers(wifi_routers: GeoDataFrame):
    wifi_routers.plot(figsize=(10, 10), marker='o', color='blue', markersize=50, alpha=0.5)
    print(5)
    plt.title('Расположение Wi-Fi роутеров')
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    print(6)
    plt.show()
    print(7)


# show_wifi_routers(load_geo_data('wifi_routers.csv'))


def show_wifi_logs(wifi_logs: GeoDataFrame):
    # Загрузка данных из файла wifi_logs.csv
    wifi_logs['tm'] = pd.to_datetime(wifi_logs['tm'], utc=True)
    print(8)

    # Создание нового столбца 'hour' для анализа по часам
    wifi_logs['hour'] = wifi_logs['tm'].dt.hour
    print(9)
    wifi_logs['week'] = wifi_logs['tm'].dt.strftime('%Y-%m-%d')
    print(10)

    # Группировка данных по часам, роутерам отправителям и роутерам получателям
    router_hourly_counts = wifi_logs.groupby(['hour', 'router_mac', 'router_id']).size().reset_index(name='count')
    print(11)

    # Построение графика изменения дорожно-транспортной ситуации с течением времени
    plt.figure(figsize=(12, 8))
    print(12)
    sns.lineplot(x='hour', y='count', hue='router_mac', data=router_hourly_counts)
    print(13)
    plt.title('Изменение дорожно-транспортной ситуации с течением времени')
    print(14)
    plt.xlabel('Час дня')
    plt.ylabel('Количество перемещений')
    plt.legend(title='Router MAC', bbox_to_anchor=(1.05, 1), loc='upper left')
    print(15)
    plt.show()
    print(16)


# show_wifi_logs(load_data('wifi_logs.csv'))

def show_wifi_week(wifi_logs: GeoDataFrame):
    # wifi_logs = load_data('wifi_logs.csv')
    wifi_logs['tm'] = pd.to_datetime(wifi_logs['tm'], utc=True)
    print(8)
    print(dir(wifi_logs['tm'].dt))
    # Создание нового столбца 'hour' для анализа по часам
    wifi_logs['hour'] = wifi_logs['tm'].dt.hour
    print(9)
    wifi_logs['week'] = wifi_logs['tm'].dt.isocalendar().week

    print(17)

    # Группировка данных по неделям, роутерам отправителям и роутерам получателям
    router_weekly_counts = wifi_logs.groupby(['week', 'router_mac', 'router_id']).size().reset_index(name='count')
    print(18)

    # Построение графика изменения дорожно-транспортной ситуации с течением времени (по неделям)
    plt.figure()
    sns.lineplot(x='week', y='count', hue='router_mac', data=router_weekly_counts)
    plt.title('Изменение дорожно-транспортной ситуации с течением времени (по неделям)')
    plt.xlabel('Неделя')
    plt.ylabel('Количество перемещений')
    plt.xticks(rotation=45, ha='right')  # Повернуть метки по оси X для лучшей читаемости
    plt.legend(title='Router MAC', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()


def read_files(path):
    files = [file for file in Path(path).glob("*.csv")][:7]
    return pd.concat([load_data(file, data_folder='')
                      for file in files],
                     ignore_index=True)



# show_wifi_week(read_files("./data/logs"))
