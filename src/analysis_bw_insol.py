import pandas as pd


insolation = [
    2.13, 3.31, 4.77, 6.67, 7.65, 8.11,
    7.65, 6.86, 5.27, 3.61, 2.37, 1.8
    ]

avrg_insol = round(sum(insolation) / len(insolation), 2)


df = pd.read_csv(r'.\data\box_wilson_insolation.csv')
y_specific: pd.DataFrame = df['y'] / (df['x2'] / df['x2_origin'])
df['y_specific'] = y_specific.round(2)

df.to_csv(r'.\data\updated_box_wilson_insolation.csv', index=False)


df = pd.read_csv(r'.\data\updated_box_wilson_insolation.csv')
delta_insolation = 0.2
is_optimal = df['x1'].apply((lambda x: avrg_insol - delta_insolation <
                             x < avrg_insol + delta_insolation))
df['is_optimal'] = is_optimal

df.to_csv(r'.\data\updated_box_wilson_insolation.csv', index=False)


df = pd.read_csv(r'.\data\updated_box_wilson_insolation.csv')
df = df.loc[df['is_optimal'] == True]

df.to_csv(r'.\data\optimal_box_wilson_insolation.csv', index=False)


df = pd.read_csv(r'.\data\optimal_box_wilson_insolation.csv')

df['efficiency_factor'] = ((df['y_specific'] * df['x2_origin']) /
                           (df['x1'] * df['x2']))
df['efficiency_factor'] = df['efficiency_factor'].round(4)
df['normalized_values'] = ((df['efficiency_factor'] -
                            df['efficiency_factor'].min()) /
                           (df['efficiency_factor'].max() -
                            df['efficiency_factor'].min()))
df['normalized_values'] = df['normalized_values'].round(4)

for column_name in ['dx1', 'dx2', 'dx3', 'is_optimal']:
    del df[column_name]
df.to_csv(r'.\data\optimal_box_wilson_insolation.csv', index=False)


df = pd.read_csv(r'.\data\updated_box_wilson_insolation.csv')
months = [
    'Янв', 'Фев', 'Март',
    'Апр', 'Май', 'Июнь',
    'Июль', 'Авг', 'Сент',
    'Окт', 'Нояб', 'Дек'
    ]

dfs = []

for month in months:
    df_copy = df.loc[df['Месяц'] == month].copy()
    df_copy['efficiency_factor'] = ((df_copy['y_specific']) /
                                    (df_copy['x1'] * df_copy['x2']))
    df_copy['efficiency_factor'] = df_copy['efficiency_factor'].round(4)
    df_copy['normalized_values'] = ((df_copy['efficiency_factor'] -
                                     df_copy['efficiency_factor'].min()) /
                                    (df_copy['efficiency_factor'].max() -
                                     df_copy['efficiency_factor'].min()))
    df_copy['normalized_values'] = df_copy['normalized_values'].round(4)
    df_copy = df_copy.loc[df_copy['normalized_values'] == 1.0]
    dfs.append(df_copy)

combined_df = pd.concat(dfs, ignore_index=True)
for column_name in ['dx1', 'dx2', 'dx3',
                    'is_optimal', 'normalized_values', 'x2_origin']:
    del combined_df[column_name]
combined_df.to_csv(r'.\data\by_month_box_wilson_insolation.csv', index=False)
