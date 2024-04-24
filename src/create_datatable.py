import csv


def generate_combinations(list_1, list_2, list_3):
    combinations = []
    for i in list_1:
        for k in list_2:
            for j in list_3:
                combinations.append((i, k, j))
    return combinations


def logical_view(values, min_values, max_values):
    logic = []
    for items in values:
        row = []
        for value in items:
            if value in min_values:
                row.append(-1)
            elif value in max_values:
                row.append(1)
        logic.append(row)
    return logic


def add_logical_operations(values):
    logic = []
    for x in values:
        x1x2 = x[0] * x[1]
        x2x3 = x[1] * x[2]
        x1x3 = x[0] * x[2]
        x1x2x3 = x[0] * x[1] * x[2]

        logic.append(
            [
                x[0], x[1], x[2],
                x1x2, x2x3, x1x3,
                x1x2x3
            ]
            )
    return logic


def set_outputs(all_outputs: dict, values_list):
    global x1_min, x1_max
    outputs = []

    for values in values_list:
        if values[0] == x1_min:
            out_list: list = all_outputs[f'{values[2]}_{values[1]}'][0]
            avrg_out_list = sum(out_list) / len(out_list)
            avrg_out_list = int(avrg_out_list)
            out_list.append(avrg_out_list)
            outputs.append(out_list)
        elif values[0] == x1_max:
            out_list: list = all_outputs[f'{values[2]}_{values[1]}'][1]
            avrg_out_list = sum(out_list) / len(out_list)
            avrg_out_list = int(avrg_out_list)
            out_list.append(avrg_out_list)
            outputs.append(out_list)
    return outputs


def create_final_table(logic, ouputs):
    table = []
    for i in range(len(logic)):
        row = []
        for k in logic[i]:
            # if k == -1:
            #     row.append('-')
            # if k == 1:
            #     row.append('+')
            row.append(k)

        for j in ouputs[i]:
            row.append(j)

        table.append(row)

    return table


def write_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["x1", "x2", "x3",
                            "x1x2", "x2x3", "x1x3",
                            "x1x2x3",
                            "y1", "y2", "y3",
                            "y"])
        csvwriter.writerows(data)


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


# powers = {
#     '30_0.2': [[0.055, 0.07, 0.08], [0.15, 0.16, 0.17]],
#     '60_0.2': [[0.06, 0.075, 0.085], [0.135, 0.14, 0.145]],
#     '30_0.52': [[0.18, 0.23, 0.27], [0.505, 0.54, 0.565]],
#     '60_0.52': [[0.205, 0.255, 0.275], [0.46, 0.47, 0.48]]
#     }

powers = {
    '30_0.2': [[0.045, 0.067, 0.078], [0.15, 0.16, 0.17]],
    '60_0.2': [[0.06, 0.075, 0.085], [0.135, 0.14, 0.145]],
    '30_0.52': [[0.18, 0.23, 0.27], [0.505, 0.54, 0.565]],
    '60_0.52': [[0.205, 0.255, 0.275], [0.46, 0.47, 0.48]]
    }

for key, value in powers.items():
    for i in range(len(powers[key])):
        for k in range(len(powers[key][i])):
            powers[key][i][k] = int(powers[key][i][k] * 10**3)

print(powers)


x1_list = [x1_min, x1_max]
x2_list = [x2_min, x2_max]
x3_list = [x3_min, x3_max]

x_min = [x1_min, x2_min, x3_min]
x_max = [x1_max, x2_max, x3_max]

print(x_min)
print(x_max)

X_values = generate_combinations(x1_list, x2_list, x3_list)
X_logic = logical_view(X_values, x_min, x_max)
X_all_logic = add_logical_operations(X_logic)
process_outputs = set_outputs(powers, X_values)
final_table = create_final_table(X_all_logic, process_outputs)

write_data_to_csv(final_table, r"E:\Python\solar_data\data\data.csv")
