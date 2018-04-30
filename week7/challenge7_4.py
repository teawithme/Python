# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import linear_model

def Temperature():
    df_temperature = pd.read_csv('GlobalSurfaceTemperature.csv')
    df_gas = pd.read_csv('GreenhouseGas.csv')
    df_co2 = pd.read_csv('CO2ppm.csv')
   
    df_temperature['Year'] = pd.to_datetime(df_temperature['Year'], format='%Y')
    df_temperature = df_temperature.set_index('Year')
    #df = df['1980':]
    
    df_gas['Year'] = pd.to_datetime(df_gas['Year'], format='%Y')
    df_gas = df_gas.set_index('Year')
    #df_gas = df_gas['1980':]

    df_co2['Year'] = pd.to_datetime(df_co2['Year'], format='%Y')
    df_co2 = df_co2.set_index('Year')
    
    df = pd.concat([df_temperature, df_gas, df_co2], axis=1)
    df = df['1980':] 
    df_train = df['1980':'2010']
    df_train_feature = df_train.iloc[:, 3:]
    df_train_target = df_train.iloc[:, 0:3]
    
    df_test_feature = df['2011':'2017'].iloc[:, 3:]
    df_test_feature = df_test_feature.fillna(method='ffill', axis=0).fillna(method='bfill', axis=0)
    
    model = linear_model.LinearRegression()
    model.fit(df_train_feature, df_train_target)
    df_test_target = model.predict(df_test_feature).round(3)
    #df_test_target_list = df_test_target.tolist()
    UpperPredict = df_test_target[:, 1].tolist()
    MedianPredict = df_test_target[:, 0].tolist()
    LowerPredict = df_test_target[:, 2].tolist()
    #print(df_test_target.shape)
    #print(type(UpperPredict))
    #print(UpperPredict)

    return UpperPredict, MedianPredict, LowerPredict
if __name__ == '__main__':
    Temperature()
