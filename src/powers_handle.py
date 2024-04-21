def get_pair_avrg(lst: list):
    processed_list = []
    iterations = int(len(lst) / 2)
    for i in range(iterations):
        avrg = (lst[i] + lst[i-(i+1)]) / 2
        avrg = round(avrg, 3)
        processed_list.append(avrg)

    return processed_list


def process_lists(dictionary: dict):
    processed_data = {}

    for key, lst in dictionary.items():
        first_list = lst[:3] + lst[-3:]
        second_list = lst[3:-3]

        first_list = get_pair_avrg(first_list)
        second_list = get_pair_avrg(second_list)

        processed_data[key] = [first_list, second_list]

    print(processed_data)


powers = {
    '30_0.20': [0.06, 0.09, 0.11, 0.15, 0.17, 0.19,
                0.19, 0.18, 0.15, 0.11, 0.07, 0.05],
    '45_0.20': [0.06, 0.09, 0.11, 0.15, 0.16, 0.17,
                0.17, 0.17, 0.15, 0.11, 0.08, 0.06],
    '60_0.20': [0.06, 0.09, 0.11, 0.13, 0.14, 0.15,
                0.15, 0.16, 0.14, 0.11, 0.08, 0.06],
    '30_0.36': [0.09, 0.15, 0.18, 0.26, 0.29, 0.31,
                0.32, 0.31, 0.25, 0.18, 0.12, 0.09],
    '45_0.36': [0.1, 0.15, 0.19, 0.24, 0.27, 0.28,
                0.29, 0.29, 0.25, 0.18, 0.13, 0.09],
    '60_0.36': [0.11, 0.15, 0.18, 0.22, 0.24, 0.25,
                0.25, 0.26, 0.23, 0.18, 0.13, 0.1],
    '30_0.52': [0.19, 0.29, 0.37, 0.51, 0.58, 0.63,
                0.64, 0.61, 0.5, 0.35, 0.24, 0.17],
    '45_0.52': [0.20, 0.31, 0.37, 0.49, 0.54, 0.57,
                0.58, 0.58, 0.50, 0.37, 0.26, 0.19],
    '60_0.52': [0.21, 0.31, 0.35, 0.45, 0.47, 0.49,
                0.51, 0.52, 0.47, 0.36, 0.26, 0.20],
}

process_lists(powers)
