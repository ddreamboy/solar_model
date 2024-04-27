import csv


def dict_to_csv(data: dict, filename: str) -> None:
    # Записываем данные в CSV файл
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Записываем заголовки (ключи словаря)
        writer.writerow(data.keys())

        # Записываем данные (значения словаря)
        writer.writerows(zip(*data.values()))


x1 = 5.02  # инсоляция
x2 = 0.36  # площадь рабочей поверхности панели, м2
x3 = 45  # оптимальный угол наклона исходя из широты местности
a = 0.001  # шаг

data = {
    'x1': [],
    'x2': [],
    'x3': [],
    'dx1': [],
    'dx2': [],
    'dx3': [],
    'y': [],
}

for i in range(100):
    if x1 <= 9:
        y = -20.8 - 6.42*x1 + 342.4*x2 + 93.793*x1*x2 - 0.31*x1*x3 + 1.557*x3

        dx1 = -6.42 + 93.793 * x2 - 0.31 * x3
        dx2 = 342.4 + 93.793 * x1
        dx3 = -0.31 * x1 + 1.557

        data['x1'].append(round(x1, 2))
        data['x2'].append(round(x2, 2))
        data['x3'].append(round(x3, 2))
        data['dx1'].append(round(dx1, 2))
        data['dx2'].append(round(dx2, 2))
        data['dx3'].append(round(dx3, 2))
        data['y'].append(round(y, 2))

        x1 = x1 + a * dx1
        x2 = x2 + a * dx2
        x3 = x3 + a * dx3
    else:
        break

for key, value in data.items():
    print("{0}: {1}".format(key, value))

dict_to_csv(data, 'box_wilson_grad.csv')
