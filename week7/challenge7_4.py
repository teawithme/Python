# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt

def Temperature():
    df_temperature = pd.read_csv('GlobalSurfaceTemperature.csv')
    df_gas = pd.read_csv('GreenhouseGas.csv')
    df_co2 = pd.read_csv('CO2ppm.csv')
    
    df_t = df_temperature[df_temperature.iloc[:, [1, 2, 3]].notnull().index]
    df_g = df_gas[df_gas.notnull()]
    df_co2 = df_co2[df_co2.notnull()]
    print(df_t)
    #print(df_t.isnull().sum())
    print(df_gas.isnull().sum())
    print(df_co2.isnull().sum())
    
if __name__ == '__main__':
    Temperature()
