# -- encoding:utf-8 --
"""
Create by ibf on 2018/11/20
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.externals import joblib
from sklearn.utils import shuffle

np.random.seed(28)

if __name__ == '__main__':
    # flag为True表示模型训练，flag为False表示基于训练好的模型对数据做一个预测
    flag = True
    model_file_path = './models/03_tree.pkl'

    # 1. 读取数据，形成DataFrame
    file_path = '../datas/boston_housing.data'
    df = pd.read_csv(file_path, header=None)
    # 提取数据
    data = np.empty(shape=(len(df), 14))
    for idx, value in enumerate(df.values):
        value = value[0]
        values = value.split(" ")
        values = filter(lambda v: v != '', values)
        data[idx] = list(values)
    data = data.astype(np.float32)
    print(data)
    print(data.shape)

    if flag:
        # 2. 数据的分割
        x, y = np.split(data, (13,), axis=1)
        y = y.ravel()
        print("样本数据量:%d, 特征个数:%d" % x.shape)
        print("目标属性样本数据量:%d" % y.shape[0])

        # 3. 数据的划分
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=14)
        print("训练数据特征属性形状:{}, 测试数据特征形状:{}".format(x_train.shape, x_test.shape))

        # 4. 特征工程

        # 5. 模型的构建
        algo = DecisionTreeRegressor(max_depth=5)

        # 6. 模型训练
        algo.fit(x_train, y_train)

        # 7. 模型效果评估
        train_pred = algo.predict(x_train)
        test_pred = algo.predict(x_test)
        print("训练数据的MSE评估指标:{}".format(mean_squared_error(y_train, train_pred)))
        print("测试数据的MSE评估指标:{}".format(mean_squared_error(y_test, test_pred)))
        print("训练数据的R2评估指标:{}".format(r2_score(y_train, train_pred)))
        print("测试数据的R2评估指标:{}".format(r2_score(y_test, test_pred)))
        print("训练数据的RMSE评估指标:{}".format(np.sqrt(mean_squared_error(y_train, train_pred))))
        print("测试数据的RMSE评估指标:{}".format(np.sqrt(mean_squared_error(y_test, test_pred))))

        # 8. 模型保存/持久化
        joblib.dump(algo, model_file_path)
    else:
        # 1. 加载模型
        algo = joblib.load(model_file_path)
        # 2. 使用模型对输入数据做一个预测
        data = shuffle(data)
        data = data[:10]
        y_pred = algo.predict(data[:, :13])
        print("预测的R2指标为:{}".format(r2_score(data[:, 13], y_pred)))
        print("实际值:\n{}".format(data[:, 13]))
        print("预测值:\n{}".format(y_pred))
