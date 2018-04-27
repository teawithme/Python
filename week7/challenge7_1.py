# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def co2():
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname='Data')
    df_co2 = df_climate[df_climate['Series code'] == 'EN.ATM.CO2E.KT']
    df_co2 = df_co2.replace({'..': np.nan})
    df_co2 = df_co2.drop(['Country code', 'Series code', 'Series name', 'SCALE', 'Decimals'], axis=1)
    df_co2 = df_co2.dropna(axis=0, thresh=2)
    
    df_country = pd.read_excel('ClimateChange.xlsx', sheetname='Country')
    df = pd.merge(df_co2, df_country)
    df = df.set_index('Country name')
    df = df.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df = df.drop(['Country code', 'Capital city', 'Region', 'Lending category'], axis=1)
    col_list = list(df)
    col_list.remove('Income group')
    df['sum'] = df[col_list].sum(axis=1, numeric_only=True)
    #print(df)
    df1 = df[['Income group', 'sum']].groupby('Income group').sum()    
    df1.columns = ['Sum emissions']
    #print(df1.head(5))
    
    df3 = df[['Income group', 'sum']].groupby('Income group').max()
    df3.columns = ['Highest emissions']
    #print(df3.head(5))
    df2 = df[['Income group', 'sum']].groupby('Income group').idxmax()
    df2.columns = ['Highest emission country']
    #print(df2.head(5))
    df4 = df[['Income group', 'sum']].groupby('Income group').idxmin()
    df4.columns = ['Lowest emission country']
    #print(df4.head(5))

    df5 = df[['Income group', 'sum']].groupby('Income group').min()
    df5.columns = ['Lowest emissions']
    #print(df5.head(5))
    results = pd.concat([df1, df2, df3, df4, df5], axis=1)
    #print(results)
    return results

if __name__ == '__main__':
    co2()
