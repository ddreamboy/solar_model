from solar_data_handler import DataHandler
import matplotlib.pyplot as plt
import numpy as np


def draw_data_compar(y1, y2, y_label='кВт*ч / м²'):
    months = ["Янв", "Фев", "Мар",
              "Апр", "Май", "Июн",
              "Июл", "Авг", "Сен",
              "Окт", "Ноя", "Дек"
              ]
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots()
    ax.plot(months, y1, c='red', alpha=0.5, label='Краснодарский край',
            linewidth=3, marker='o')
    ax.plot(months, y2, c='blue', alpha=0.5, label='Ленинградская область',
            linewidth=3, marker='o')
    plt.fill_between(months, y1, y2, facecolor='blue', alpha=0.1)
    plt.xlabel('', fontsize='24')
    plt.ylabel(y_label, fontsize='24')
    plt.tick_params(axis='both', which='major', labelsize=24)
    plt.legend(fontsize='24')
    # plt.show()


def get_diff_percent(array_1, array_2):
    array_1 = np.array(array_1)
    array_2 = np.array(array_2)
    percent_diff = ((array_1 - array_2) / array_2) * 100
    avrg_percent_diff = np.mean(percent_diff)
    return round(avrg_percent_diff, 2)


krasnodar_data = DataHandler('data/krasnodarskiy_krai.csv')
lenobl_data = DataHandler('data/len_oblast.csv')

parameter = 'CLRSKY_SFC_SW_DWN'
year = 2020
krasnodar_avrg = krasnodar_data.get_avrg_values_monthly(parameter,
                                                        year)
lenobl_avrg = lenobl_data.get_avrg_values_monthly(parameter,
                                                  year)
diff_percent = get_diff_percent(krasnodar_avrg, lenobl_avrg)

print(f'Краснодарский край: {krasnodar_avrg}')
print(f'Ленинградская область: {lenobl_avrg}')
print(f'Разница: {diff_percent}% или в {diff_percent/100+1} раза')

draw_data_compar(krasnodar_avrg, lenobl_avrg, 'м/с')
