import pandas as pd


class DataHandler():
    def __init__(self, filepath: str) -> None:
        self.df = pd.read_csv(filepath)

    def get_avrg_values_monthly(self, parameter: str, year=2020):
        # Отфильтровать строки, где значение столбца PARAMETER равно "PS"
        filtered_df = self.df[(self.df['PARAMETER'] == parameter)
                              & (self.df['YEAR'] == year)]

        # Выбрать только столбцы с месяцами
        months_df = filtered_df[['JAN', 'FEB', 'MAR',
                                 'APR', 'MAY', 'JUN',
                                 'JUL', 'AUG', 'SEP',
                                 'OCT', 'NOV', 'DEC']]

        # Вычислить среднее значение для каждого месяца
        monthly_mean = months_df.mean().tolist()
        formatted_values = [round(x, 2) for x in monthly_mean]

        return formatted_values
