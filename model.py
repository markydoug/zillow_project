import pandas as pd
import numpy as np

import sklearn.metrics as metric
from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor
from sklearn.preprocessing import PolynomialFeatures

def regression_models(X_train, y_train, X_validate, y_validate):
    y_pred_mean = y_train.mean()
    y_pred_median = y_train.median()

    train_predictions = pd.DataFrame(y_train)
    validate_predictions = pd.DataFrame(y_validate)

    # create the metric_df as a blank dataframe
    metric_df = pd.DataFrame() 

    lm = LinearRegression(normalize=True)
    lm.fit(X_train, y_train)
    train_predictions['home_value_pred_lm'] = lm.predict(X_train)
    # predict validate
    validate_predictions['home_value_pred_lm'] = lm.predict(X_validate)


    return metric_df

def make_metric_df(y_train, y_train_pred, y_validate, y_validate_pred, model_name, metric_df):
    if metric_df.size ==0:
        metric_df = pd.DataFrame(data=[
            {
                'model': model_name, 
                f'RMSE_train': metric.mean_squared_error(
                    y_train,
                    y_train_pred[model_name]) ** .5,
                f'r^2_train': metric.explained_variance_score(
                    y_train,
                    y_train_pred[model_name]),
                f'RMSE_validate': metric.mean_squared_error(
                    y_validate,
                    y_validate_pred[model_name]) ** .5,
                f'r^2_validate': metric.explained_variance_score(
                    y_validate,
                    y_validate_pred[model_name])
            }])
        return metric_df
    else:
        return metric_df.append(
            {
                'model': model_name, 
                f'RMSE_train': metric.mean_squared_error(
                    y_train,
                    y_train_pred[model_name]) ** .5,
                f'r^2_train': metric.explained_variance_score(
                    y_train,
                    y_train_pred[model_name]),
                f'RMSE_validate': metric.mean_squared_error(
                    y_validate,
                    y_validate_pred[model_name]) ** .5,
                f'r^2_validate': metric.explained_variance_score(
                    y_validate,
                    y_validate_pred[model_name])
            }, ignore_index=True)