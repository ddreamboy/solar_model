import csv


def dict_to_csv(data: dict, filename: str) -> None:
    # Записываем данные в CSV файл
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Записываем заголовки (ключи словаря)
        writer.writerow(data.keys())

        # Записываем данные (значения словаря)
        writer.writerows(zip(*data.values()))


# y = -20,8 - 6,42x1 + 342,4x2 + 93,793x1x2 - 0,31x1x3 + 1,557x3
b = {
    'b0': -20.8,
    'bx1': -6.42,
    'bx2': 342.4,
    'bx3': 1.557,
    'bx1x2': 93.793,
    'bx1x3': -0.31
}

x1 = 5.02  # инсоляция
delta_x1 = 3.09
x1_min = round(x1 - delta_x1, 2)
x1_max = round(x1 + delta_x1, 2)

x2 = 0.36  # площадь рабочей поверхности панели, м2
delta_x2 = 0.16
x2_min = round(x2 - delta_x2, 2)
x2_max = round(x2 + delta_x2, 2)

x3 = 45  # оптимальный угол наклона исходя из широты местности
delta_x3 = 15
x3_min = round(x3 - delta_x3, 2)
x3_max = round(x3 + delta_x3, 2)

xj = {
    'bx1': x1,
    'bx2': x2,
    'bx3': x3,
    'bx1x2': round(x1 * x2 + delta_x1 * delta_x2, 2),
    'bx1x3': round(x1 * x3 + delta_x1 * delta_x3, 2)
}

xi = {
    'bx1': delta_x1,
    'bx2': delta_x2,
    'bx3': delta_x3,
    'bx1x2': round(abs(xj['bx1x2'] - x1_min * x2_min), 2),
    'bx1x3': round(abs(xj['bx1x3'] - x1_min * x3_min), 2)
}

bdx = {}
for key, value in xi.items():
    bdx.update(
        {
            key: round(value * b[key], 2)
        }
    )

step_bdx = {}
for key, value in bdx.items():
    step_bdx.update(
        {
            key: round(value / 10, 2)
        }
    )

bi = {}
for key, value in b.items():
    if key != 'b0':
        bi.update(
            {
                key: value
            }
        )

variable_data = {
    'xj': list(xj.values()),
    'xi': list(xi.values()),
    'bi': list(bi.values()),
    'bidxi': list(bdx.values()),
    'step bidxi': list(step_bdx.values())
}

dict_to_csv(variable_data, 'box_start_data.csv')

data = {}
for key, value in xj.items():
    data.update(
        {
            key: [value]
        }
    )

data.update(
    {
        'y': [0]
    }
)

# y = -20,8 - 6,42x1 + 342,4x2 + 93,793x1x2 - 0,31x1x3 + 1,557x3

for i in range(8):
    y = b['b0']
    for key, value in data.items():
        if key != 'y':
            x = round(data[key][-1] - step_bdx[key], 2)
            data[key].append(x)
            y += b[key] * x
    data['y'].append(round(y, 2))

dict_to_csv(data, 'box_end_data.csv')
