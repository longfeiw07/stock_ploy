# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import load_model

#Setting the random seed to a fixed number
import random
random.seed(42)

class NeuralNetworks():
    def __init__(self):
        pass
    def GetDatas(self):
        dataset = pd.read_csv('resource/eastmoney.csv')
        dataset = dataset[['净买额占总成交比', '净买额占总成交比', '换手率', '流通市值(亿)', '上榜后1日', '上榜后2日']]
        dataset = dataset.dropna()
        x = dataset.iloc[:, :4]
        y = dataset.iloc[:, 4:]
        # print('x: ', x, 'y: ', y)
        #Splitting the dataset
        split = int(len(dataset)*0.8)
        X_train, X_test, y_train, y_test = x[:split], x[split:], y[:split], y[split:]
        #数据标准化
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        return X_train, X_test, y_train, y_test
    def NeuralNetwork(self):
        X_train, X_test,y_train, y_test = self.GetDatas()
        #一、定义网络
        classifier = Sequential()
        classifier.add(Dense(units = 4, kernel_initializer = 'uniform', activation = 'relu', input_dim = X_train.shape[1]))
        classifier.add(Dense(units = 2, kernel_initializer = 'uniform', activation = 'relu'))
        # classifier.add(LSTM(units = 50, return_sequences = True, input_shape=(None, 4)))
        # classifier.add(Dropout(0.2))
        # classifier.add(LSTM(units = 50, return_sequences = True))
        # classifier.add(Dropout(0.2))
        # classifier.add(LSTM(units = 50))
        # classifier.add(Dropout(0.2))
        # classifier.add(Dense(units = 2, kernel_initializer = 'uniform', activation = 'relu'))
        # y_train = np.array(y_train)
        # X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
        # X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
        #二、编译网络
        classifier.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])
        #三、训练网络  fit_generator
        print('X_train: ', X_train, 'y_train: ', y_train)
        classifier.fit(X_train, y_train, batch_size = 10, epochs = 100)
        #四、评价网络
        loss, accuracy = classifier.evaluate(X_test, y_test)
        print("loss: ", loss, "accuracy: ", accuracy)
        #五、进行预测
        y_pred = classifier.predict(X_test)
        print("y_pred: ", y_pred)
        #六、保存模型
        # classifier.save('resource/my_model.h5')
        #七、加载模型
        # classifier = load_model('resource/my_model.h5')







