import pandas as pd
import numpy as np
from keras.models import model_from_json
import pickle
import datetime


column_name = []
for i in range(1,51):
    column_name.append('var'+str(i))

scaler = pickle.load(open('scaler.pkl', 'rb'))



def scale_data(df,scaler):
    #scaler = pickle.load(open('scaler.pkl', 'rb'))
    print(df)
    df = scaler.transform(df)
    return df

def unscale_data(df, scaler):
    df = scaler.inverse_transform(df)
    return df


def convert(lis, dateval):
    #df = pd.DataFrame(lis)
    print(lis)
    print(dateval)
    df = pd.DataFrame(columns = ['dateval'])
    row = {'dateval':dateval}
    df = df.append(row,ignore_index=True)
    #df['dateval'] = dateval
    df['dateval'] = pd.to_datetime(df['dateval'],format='%d/%m/%Y')
    print("dtateasda")
    print(df)
    dataf = pd.DataFrame()
    dataf['weekday_0'] = (df.dateval.dt.weekday == 0) *1
    dataf['weekday_1'] = (df.dateval.dt.weekday == 1) *1
    dataf['weekday_2'] = (df.dateval.dt.weekday == 2) *1
    dataf['weekday_3'] = (df.dateval.dt.weekday == 3) *1
    dataf['weekday_4'] = (df.dateval.dt.weekday == 4) *1
    dataf['weekday_5'] = (df.dateval.dt.weekday == 5) *1
    dataf['weekday_6'] = (df.dateval.dt.weekday == 6) *1
    dataf['month_1'] = (df.dateval.dt.month == 1) *1
    dataf['month_2'] = (df.dateval.dt.month == 2) *1
    dataf['month_3'] = (df.dateval.dt.month == 3) *1
    dataf['month_4'] = (df.dateval.dt.month == 4) *1
    dataf['month_5'] = (df.dateval.dt.month == 5) *1
    dataf['month_6'] = (df.dateval.dt.month == 6) *1
    dataf['month_7'] = (df.dateval.dt.month == 7) *1
    dataf['month_8'] = (df.dateval.dt.month == 8) *1
    dataf['month_9'] = (df.dateval.dt.month == 9) *1
    dataf['month_10'] = (df.dateval.dt.month == 10) *1
    dataf['month_11'] = (df.dateval.dt.month == 11) *1
    dataf['month_12'] = (df.dateval.dt.month == 12) *1
    #print(column_name)
    print(dataf['month_7'])
    print(dataf)
    #li = []
    #li.append(lis)
    #print(li)
    #lis = pd.DataFrame(li)
    #print(lis.shape)
    #row = [0] * len(lis)
    #print(row)
    #l = []
    #l.append(lis)
    #l.append(row)
    lis = np.array(lis)
    lis = lis.reshape(1,-1)
    print(lis)
    #print(lis)
    df = scale_data(lis,scaler)
    print(df)
    print(df.shape)
    df = pd.DataFrame(df,columns=column_name)
    print(df)
    print(df.shape)
    dataf = pd.concat([dataf, df], axis=1)
    print(dataf)
    return dataf

def predict_val(model, dataf):
    test_X = dataf.values
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    print(test_X.shape)
    yhat = model.predict(test_X)
    yhat = unscale_data(yhat,scaler)
    return yhat


def convertDate(da):
    da =str(da)
    da = da.split('-')
    new = da[2]+'/'+da[1]+'/'+da[0]
    return new

def weekdata(lis):
    #print(lis)
    dateval = lis[0]
    print(dateval)
    lis = lis[1:]
    print(lis)
    dateval = datetime.datetime.strptime(dateval,'%d-%m-%Y').date()
    dateval = convertDate(dateval)
    print("date:", dateval)
    day1 = convert(lis, dateval)
    print(day1.shape)
    #pred_val = []
    df = predict_val(loaded_model,day1)
    #pred_val.append(df)
    df = pd.DataFrame(df)
    #dateval = datetime.datetime.strptime(dateval,'%d-%m-%Y').date()
    for i in range(6):
        print('hello')
        dateval = datetime.datetime.strptime(dateval,'%d/%m/%Y').date()
        dateval += datetime.timedelta(days = 1)
        dateval = convertDate(dateval)
        print(dateval)
        print(df)
        day1 = convert(df.iloc[-1,:],dateval)
        df1 = predict_val(loaded_model, day1)
        df1 = pd.DataFrame(df1)
        df = df.append(df1, ignore_index=True)
        #df = pd.concat(df,df1, axis = 0)
    print(df)
    sum_df = df.sum(axis=0)
    print(sum_df)


def load_main():
    
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    global loaded_model 
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
 
    # evaluate loaded model on test data
    loaded_model.compile(loss='mean_absolute_error', optimizer='adam')
load_main()