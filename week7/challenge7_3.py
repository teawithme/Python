# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates

def climate_plot():
    df_temperature = pd.read_excel('GlobalTemperature.xlsx')
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname='Data')
    
    df_climate = df_climate[df_climate['Series code'].isin(['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE'])]
    df_climate = df_climate.replace({'..': np.nan})
    df_climate = df_climate.dropna(thresh=7, axis=0)
    df_climate.iloc[:, 6:] = df_climate.iloc[:, 6:].fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_GHG = df_climate.iloc[:,6:27].sum()
    df_GHG = (df_GHG - df_GHG.min())/(df_GHG.max() - df_GHG.min())
    #print(df_climate.head(15))
    df_GHG.index = pd.to_datetime(df_GHG.index, format='%Y')
    df_GHG = df_GHG.to_frame(name = 'Total GHG')
    df_temperature['Date'] = pd.to_datetime(df_temperature['Date'])
    df_temperature = df_temperature.iloc[:, [0, 1, 4]]
    df_temperature = df_temperature.set_index('Date')
    df_t1 = df_temperature['1990':'2010']
    df_t3 = df_temperature.resample('Q').sum()
    df_t1 = df_t1.resample('AS').sum()
    #df_t3 = df_t1
    df_t1 = (df_t1 - df_t1.min())/(df_t1.max() - df_t1.min())
    #print(df_t1.head(15))
    df_t1 = pd.concat([df_GHG, df_t1], axis=1)
    df_t2 = df_t1
    df_t2.index = df_t2.index.year
    #print(df_t1.head(15))
    
    fig, axes = plt.subplots(nrows=2, ncols=2)
    
    ax1 = df_t1.plot(ax=axes[0, 0], kind='line')
    ax1.set(xlabel='Years', ylabel='Values')
    ax1.legend()
    
    ax2 = df_t2.plot(ax=axes[0, 1], kind='bar')
    ax2.set(xlabel='Years', ylabel='Values')
    #ax2.set_xticks(df_t1.index)
    #ax2.xaxis.set_major_formatter(dates.DateFormatter('%Y'))    
    ax2.legend()
    
    ax3 = df_t3.plot(ax=axes[1, 0], kind='area', legend=True)
    ax3.set(xlabel='Quarters', ylabel='Temperature')

    ax4 = df_t3.plot(ax=axes[1, 1], kind='kde', legend=True)
    ax4.set(xlabel='Values', ylabel='Values')

    plt.show()
    return fig

if __name__ == '__main__':
    climate_plot()
