# - *- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def co2_gdp_plot():
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname='Data')
    #df_country = pd.read_excel('ClimateChange.xlsx', sheetname='Country')
    #df_country = df_country['Country code']

    df_climate = df_climate.drop(['Country name', 'Series name', 'SCALE', 'Decimals'], axis=1)
    df_climate = df_climate[df_climate['Series code'].isin(['NY.GDP.MKTP.CD', 'EN.ATM.CO2E.KT'])]
    df_climate = df_climate.replace({'..': np.nan})
    df_climate = df_climate.dropna(thresh=3, axis=1)
    df_climate.iloc[:, 2:] = df_climate.iloc[:, 2:].fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_climate['sum'] = df_climate.iloc[:, 2:].sum(axis=1)
    
    df_co2 = df_climate[df_climate['Series code'] == 'EN.ATM.CO2E.KT']
    df_co2 = df_co2.rename(columns = {'sum': 'CO2-SUM'})
    #df_co2 = pd.merge(df_co2, df_country)
    df_co2['CO2-SUM'] = (df_co2['CO2-SUM'] - df_co2['CO2-SUM'].min())/(df_co2['CO2-SUM'].max() - df_co2['CO2-SUM'].min())
    #print(df_co2.head(5))
    
    df_gdp = df_climate[df_climate['Series code'] == 'NY.GDP.MKTP.CD']
    df_gdp = df_gdp.rename(columns = {'sum': 'GDP-SUM'})
    #df_gdp = pd.merge(df_gdp, df_country)
    df_gdp['GDP-SUM'] = (df_gdp['GDP-SUM'] - df_gdp['GDP-SUM'].min())/(df_gdp['GDP-SUM'].max() - df_gdp['GDP-SUM'].min())
    #print(df_gdp.head(5))
    
    df = pd.concat([df_co2, df_gdp], axis=1)
    print(df.head(5))
    co2 = df_co2[df_co2['Country code'] == 'CHN']['CO2-SUM'].iloc[0]
    gdp = df_gdp[df_gdp['Country code'] == 'CHN']['GDP-SUM'].iloc[0]
    china = [float("{0:.3f}".format(co2)), float("{0:.3f}".format(gdp))]
    #print(china)

    fig = plt.subplot()
    fig.set_title('GDP-CO2')
    fig.set_xlabel('Countries')
    fig.set_ylabel('Values')
    
    x = list(df_co2.index.values)
    y1 = df_co2['CO2-SUM']
    x = df_gdp['Country code']
    y1 = df_gdp['GDP-SUM']
    
    xticks = ['CHN', 'USA', 'GBR', 'FRA', 'RUS']
    #plt.xticks(x1, xticks)
    ax = plt.scatter(x, y1, 'b')

    #plt.plot(x2, y2, 'y')

    fig.legend()
    plt.show()

    return fig, china

if __name__ == '__main__':
    co2_gdp_plot()
