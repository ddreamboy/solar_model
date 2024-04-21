numbers = [2.13, 3.31, 4.77, 6.67, 7.65, 8.11,
           7.65, 6.86, 5.27, 3.61, 2.37, 1.8
           ]

avrg = sum(numbers) / len(numbers)
delta_min = avrg - min(numbers)
delta_max = max(numbers) - avrg
x = 0 - (delta_min - delta_max)
delta = (delta_min + delta_max + x) / 2

print(round(avrg, 2))
print(round(delta, 2))
