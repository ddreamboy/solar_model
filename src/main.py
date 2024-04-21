import matplotlib.pyplot as plt


kk = [1.95, 3.1, 4.64, 6.51, 7.52, 7.97, 7.55, 6.65, 5.06, 3.34, 2.15, 1.59]
lenob = [0.49, 1.47, 3.28, 5.52, 7.23, 7.94, 7.2, 5.67, 3.61, 1.72, 0.69, 0.27]
months = ["Янв", "Фев", "Мар",
          "Апр", "Май", "Июн",
          "Июл", "Авг", "Сен",
          "Окт", "Ноя", "Дек"
          ]

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots()
ax.plot(months, kk, c='red', alpha=0.5, label='Краснодарский край',
        linewidth=3)
ax.plot(months, lenob, c='blue', alpha=0.5, label='Лен. область',
        linewidth=3)
plt.fill_between(months, kk, lenob, facecolor='blue', alpha=0.1)
plt.xlabel('', fontsize='24')
plt.ylabel('кВт*ч / м²', fontsize='16')
plt.tick_params(axis='both', which='major', labelsize=16)
plt.legend(fontsize='16')
plt.show()
