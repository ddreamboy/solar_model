from math import sqrt
import pandas as pd


df = pd.read_csv(r'C:\WorkSpace\PythonProjects\solar_model\data\data.csv')
x_values = ["x1", "x2", "x3", "x1x2", "x2x3", "x1x3", "x1x2x3"]
y_values = ['y1', 'y2', 'y3']
y_avrg = df['y']


# РАСЧЕТ КОЭФФИЦИЕНТОВ
b = {
    'b0': y_avrg.sum() / 8
}

for x in x_values:
    bx = (df[x] * y_avrg).sum()
    bx = bx / 8
    bx = round(bx, 3)

    b.update({
        f'b{x}': bx
    })

    b_equal = f'b{x} = ('
    for x_value, y_value in zip(df[x], y_avrg):
        result = x_value * y_value

        if result > 0:
            b_equal += ' + '
            b_equal += str(result)
        elif result < 0:
            b_equal += ' - '
            b_equal += str(abs(result))

    b_equal += f') / 8 = {bx}'

    print(b_equal)


# Уравнение регрессии после расчета коэффициентов
equal = f"y = {b['b0']}"

for key, value in b.items():
    if value > 0 and key != 'b0':
        equal += ' + '
        equal += str(value)
        equal += key.replace('b', '')
    elif value < 0 and key != 'b0':
        equal += ' - '
        equal += str(abs(value))
        equal += key.replace('b', '')

print(equal)


# РАСЧЕТ ДИСПЕРСИИ
dispersion = {}

# отклонение от среднего
for y in y_values:
    dev_from_mean = abs(df[y] - y_avrg)
    dispersion.update(
        {
            f'|{y}-y|': dev_from_mean
        }
    )

# квадраты отклонений
for y in y_values:
    squared_devs = dispersion[f'|{y}-y|']**2
    dispersion.update(
        {
            f'({y}-y)^2': squared_devs
        }
    )

# сумма квадратов отклонений
sum_squared_devs = pd.Series([0]*8)
for y in y_values:
    sum_squared_devs += dispersion[f'({y}-y)^2']
dispersion.update(
    {
        'SUM(yuk-y)^2': sum_squared_devs
    }
)

# дисперсия
dispersion_func = dispersion['SUM(yuk-y)^2'] / 2
dispersion.update(
    {
        '*s^2(yuk)': dispersion_func.astype(int)
    }
)

# дисперсия воспроизводимости
s2_yk = int(dispersion['*s^2(yuk)'].sum() / 8)

# среднеквадратичное отклонение выходной функции
# для всей совокупности результатов
s2_y = round(s2_yk / 3, 2)

# среднеквадратичное отклонение для коэффициентов
# уравнения регрессии
s2_bi = round(s2_y / 8, 2)
s_bi = round(sqrt(s2_bi), 2)

# определение числа Стьюдента
q = 0.05  # уровень значимости
f = 16  # число степеней свободы
t = 2.12  # число Стьюдента

# проверка значимости коэффициентов
e = round(t * s_bi, 2)

for key, value in dispersion.items():
    print(key, value.to_list())
print('s2_yk =', s2_yk)
print('s2_y =', s2_y)
print('s2_bi =', s2_bi)
print('s_bi =', s_bi)
print('e =', e)

# сравнение коэффициентов с условие bi >= e
sign = 'Значимые коэффициенты:'
non_sign = 'Незначимые коэффициенты:'
non_sign_coeffs = []
b_sign = b.copy()

for key, value in b_sign.items():
    if abs(value) >= e:
        sign += f'\n{key} = {value}'
    else:
        non_sign += f'\n{key} = {value}'
        non_sign_coeffs.append(key)

for item, value in enumerate(non_sign_coeffs):
    b_sign.pop(value)
    non_sign_coeffs[item] = value.replace('b', '')

print(sign)
print(non_sign)

# Уравнение регрессии после проверки значимости
equal = f"y = {b['b0']}"

for key, value in b_sign.items():
    if value > 0 and key != 'b0':
        equal += ' + '
        equal += str(value)
        equal += key.replace('b', '')
    elif value < 0 and key != 'b0':
        equal += ' - '
        equal += str(abs(value))
        equal += key.replace('b', '')

print(equal)

y_ = pd.Series([0]*8)
for x in x_values:
    if x not in non_sign_coeffs:
        y_ += df[x] * b_sign[f'b{x}']
y_: pd.Series = b_sign['b0'] + y_
print('y_ :', y_.to_list())

y_y_: pd.Series = abs(y_avrg - y_)
print('y-y_:', y_y_.to_list())

y_y_2: pd.Series = round(y_y_**2, 2)
print('(y-y_)^2:', y_y_2.to_list())

# дисперсия адекватности
SUM_y_y_2 = round(y_y_2.sum(), 2)
print('SUM(y-y_)^2 =', SUM_y_y_2)

# критерий Фишера
F = round(SUM_y_y_2 / s2_y, 2)
f1 = 3  # изначальное кол-во b минус оставшееся
f2 = 16
Ft = 5.29  # табличное значение критерия
print('Критерий Фишера F =', F, ', табличный', Ft)

if F < Ft:
    print('Расчетное значение ниже, следовательно полученное уравнение',
          'адекватно описывает исследуемый процесс')
    

x1 = 5.02  # инсоляция
delta_x1 = 3.09

x2 = 0.36  # площадь рабочей поверхности панели, м2
delta_x2 = 0.16

x3 = 45  # оптимальный угол наклона исходя из широты местности
delta_x3 = 15

x1_fiz_1 = 1 / delta_x1
x1_fiz_2 = -(x1 / delta_x1)

physic_coeffs = {
    'x1': [1 / delta_x1, -(x1 / delta_x1)],
    'x2': [1 / delta_x2, -(x2 / delta_x2)],
    'x3': [1 / delta_x3, -(x3 / delta_x3)]
}
for key, value in physic_coeffs.items():
    physic_coeffs[key][0] = round(value[0], 4)
    physic_coeffs[key][1] = round(value[1], 4)

calculate = {}
for key, value in b_sign.items():
    if key != 'b0':
        calculate.update(
            {
                key: [value, value]
            }
        )
    
for key, value in physic_coeffs.items():
    for item in calculate.keys():
        if key in item:
            calculate[item][0] *= value[0]
            calculate[item][1] *= value[1]

for key, value in calculate.items():
    calculate[key][0] = round(value[0], 4)
    calculate[key][1] = round(value[1], 4)

print(physic_coeffs)
print(calculate)

result_calculate = {}
b0 = b_sign['b0']
for key, value in calculate.items():
    print(b0, value[1], b0 + value[1])
    b0 += value[1]
    result_calculate.update(
            {
                'b0': b0,
                key: value[0]
            }
        )
result_calculate['b0'] = round(b0, 4)
print(result_calculate)

equal = f"y = {result_calculate['b0']}"

for key, value in result_calculate.items():
    if value > 0 and key != 'b0':
        equal += ' + '
        equal += str(value)
        equal += key.replace('b', '')
    elif value < 0 and key != 'b0':
        equal += ' - '
        equal += str(abs(value))
        equal += key.replace('b', '')

print(equal)