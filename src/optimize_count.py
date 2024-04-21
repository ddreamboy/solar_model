from pulp import LpProblem, LpVariable, LpMinimize
from solar_data_handler import DataHandler
import random


def map_value(value, min, max):
    return round(0 + (1 - 0) * ((value - min) / (max - min)), 2)


# Данные
C_solar_panel = 5410  # Стоимость одной солнечной панели (у.е.)
C_wind_generator = 19166  # Стоимость одного ветрогенератора (у.е.)
E_solar_panel = 100
R_w_g = 0.6

E_consumption = [round(random.uniform(9, 11), 2) for _ in range(12)]

krasnodar_data = DataHandler('data/krasnodarskiy_krai.csv')

parameter = 'CLRSKY_SFC_SW_DWN'
year = 2020
krasnodar_ins = krasnodar_data.get_avrg_values_monthly(parameter,
                                                       year)
krasnodar_ins_min = min(krasnodar_ins)
krasnodar_ins_max = max(krasnodar_ins)

parameter = 'WS50M'
year = 2020
krasnodar_ws = krasnodar_data.get_avrg_values_monthly(parameter,
                                                      year)
krasnodar_ws_min = min(krasnodar_ws)
krasnodar_ws_max = max(krasnodar_ws)

solar_count = []
wind_count = []
total_coast = []
solar_E = []
wind_E = []
solar_maps = []
wind_maps = []

for i in range(len(E_consumption)):
    insolation_map = map_value(krasnodar_ins[i],
                               0,
                               krasnodar_ins_max
                               )
    wind_speed_map = map_value(krasnodar_ws[i],
                               0,
                               krasnodar_ws_max
                               )
    E_solar_panel_per_day = round((krasnodar_ins[i] * E_solar_panel *
                                   10**(-3) * 0.9),
                                  2)
    E_wind_generator_per_day = round((3.14 * R_w_g**2 * 0.4 *
                                      ((1.2 * krasnodar_ws[i]**3)/2) *
                                      10**(-3)), 2)

    # Создание модели оптимизации
    model = LpProblem(name="Optimal Energy Sources", sense=LpMinimize)

    # Определение переменных решения
    solar_panels = LpVariable(name="solar_panels", lowBound=0,
                              cat='Integer')
    wind_generators = LpVariable(name="wind_generators", lowBound=0,
                                 cat='Integer')

    # Добавление целевой функции (стоимость установки)
    model += C_solar_panel * solar_panels + C_wind_generator * wind_generators, "Total Cost"

    # Вычисление энергии, производимой за день
    E_solar_panel_total = E_solar_panel_per_day * insolation_map * solar_panels
    E_wind_generator_total = (E_wind_generator_per_day * wind_speed_map *
                              wind_generators)

    # Добавление ограничения на производство энергии
    model += E_solar_panel_total + E_wind_generator_total >= E_consumption[i], "Energy Production"

    # Решение задачи оптимизации
    model.solve()

    # # Вывод результатов
    # print('Потребление:', E_consumption[i])
    # print('Солнце:', E_solar_panel_per_day, krasnodar_ins[i])
    # print('Ветер:', E_wind_generator_per_day, krasnodar_ws[i])
    # print("Оптимальное кол-во солнечных панелей:", int(solar_panels.value()))
    # print("Оптимальное кол-во ветрогенераторов:", int(wind_generators.value()))
    # print("Минимальная стоимость:", round(model.objective.value(), 2), "у.е.")

    solar_count.append(int(solar_panels.value()))
    wind_count.append(int(wind_generators.value()))
    total_coast.append(round(model.objective.value(), 2))
    solar_E.append(E_solar_panel_per_day)
    wind_E.append(E_wind_generator_per_day)
    solar_maps.append(insolation_map)
    wind_maps.append(wind_speed_map)


months = ["Янв", "Фев", "Мар",
          "Апр", "Май", "Июн",
          "Июл", "Авг", "Сен",
          "Окт", "Ноя", "Дек"
          ]

print('Месяц:', months)
print('Потребление:', E_consumption)
print('Инсоляция:', krasnodar_ins)
print('Скорость ветра:', krasnodar_ws)
print('Приведенная инсоляция:', solar_maps)
print('Приведенная скорость ветра:', wind_maps)
print('Производство от Солнца:', solar_E)
print('Производство от ветра:', wind_E)
print('Кол-во солнечных панелей:', solar_count)
print('Кол-во ветрогенераторов:', wind_count)
print('Общая стоимость:', total_coast)
