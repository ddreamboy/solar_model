import csv


def dict_to_csv(data: dict, filename: str) -> None:
    # Записываем данные в CSV файл
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Записываем заголовки (ключи словаря)
        writer.writerow(data.keys())

        # Записываем данные (значения словаря)
        writer.writerows(zip(*data.values()))


insolation = [
    [2.13, 'Янв'], [3.31, 'Фев'], [4.77, 'Март'], [6.67, 'Апр'], [7.65, 'Май'],
    [8.11, 'Июнь'], [7.65, 'Июль'], [6.86, 'Авг'], [5.27, 'Сент'],
    [3.61, 'Окт'], [2.37, 'Нояб'], [1.8, 'Дек']
    ]

insolation_values = [
    2.13, 3.31, 4.77, 6.67, 7.65, 8.11,
    7.65, 6.86, 5.27, 3.61, 2.37, 1.8
    ]

by_seasons_values = [
    [[30], insolation_values[5:8]],
    [[45], insolation_values[2:5] + insolation_values[8:-1]],
    [[60], insolation_values[:2] + insolation_values[-1:]],
]

by_seasons = [
    [[30], insolation[5:8]],
    [[45], insolation[2:5] + insolation[8:-1]],
    [[60], insolation[:2] + insolation[-1:]],
]

a = 0.001  # шаг

calc_result = {
    'Месяц': [],
    'x1': [],
    'x2': [],
    'x2_origin': [],
    'x3': [],
    'dx1': [],
    'dx2': [],
    'dx3': [],
    'y': [],
}

out_data = {}

for index, value in enumerate(by_seasons):
    # calc_result = {
    #     'x1': [],
    #     'x2': [],
    #     'x3': [],
    #     'dx1': [],
    #     'dx2': [],
    #     'dx3': [],
    #     'y': [],
    # }
    x3 = value[0][0]
    for insol_value in value[1]:
        for x2_origin in [0.2, 0.36, 0.52]:
            x1 = insol_value[0]
            x2 = x2_origin
            for i in range(100):
                if x1 <= max(by_seasons_values[index][1]):
                    y = ((-20.8 - 6.42*x1 + 342.4*x2) +
                         (93.793*x1*x2 - 0.31*x1*x3 + 1.557*x3))

                    dx1 = -6.42 + 93.793 * x2 - 0.31 * x3
                    dx2 = 342.4 + 93.793 * x1
                    dx3 = -0.31 * x1 + 1.557

                    calc_result['Месяц'].append(insol_value[1])
                    calc_result['x1'].append(round(x1, 2))
                    calc_result['x2'].append(round(x2, 2))
                    calc_result['x2_origin'].append(x2_origin)
                    calc_result['x3'].append(round(x3, 2))
                    calc_result['dx1'].append(round(dx1, 2))
                    calc_result['dx2'].append(round(dx2, 2))
                    calc_result['dx3'].append(round(dx3, 2))
                    calc_result['y'].append(round(y, 2))

                    x1 = x1 + a * dx1
                    x2 = x2 + a * dx2
                    x3 = x3 + a * dx3
                else:
                    continue
    out_data.update(
            {
                value[0][0]: calc_result
            }
        )

# for key, value in out_data.items():
#     print("{0}: {1}".format(key, value))

dict_to_csv(calc_result, './data/box_wilson_insolation.csv')
