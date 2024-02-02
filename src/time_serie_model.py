import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def arima_model(X_train : pd.DataFrame, X_test : pd.DataFrame, arima_order, exog_variables : list[str] = None):
    '''Forecasting arima to predict new observations at long term
    
    Parameters
    ---------

    X_train : DataFrame
        Training df
    X_test : DataFrame
        Test df
    arima_order : (int, int, int)
        Order (p, d, q)
    exog_variables : list[str]
        Possible exogeneous variables
    
    Return
    ------

    X_test : df with predicted values 
    '''
    X_test_res = X_test.copy()

    arima_model = ARIMA(endog = X_train["daily_pct_variation"],
                            exog = X_train[exog_variables] if exog_variables is not None else None,
                            order = arima_order)
    model_fit = arima_model.fit()
    forecast = model_fit.get_forecast(steps = len(X_test_res),
                                      exog = X_test_res[exog_variables] if exog_variables is not None else None, 
                                    alpha = 0.05)
    predicted_values = forecast.predicted_mean
    conf_int = forecast.conf_int()

    X_test_res["predicted_values"] = predicted_values.values
    X_test_res["predicted_values_upper"] = conf_int["upper daily_pct_variation"].values
    X_test_res["predicted_values_lower"] = conf_int["lower daily_pct_variation"].values

    return X_test_res





def rolling_arima_model(X_train : pd.DataFrame, X_test : pd.DataFrame, arima_order, exog_variables : list[str]):
    '''Rolling forecasting arima to predict new observations
    
    Parameters
    ---------

    X_train : DataFrame
        Training df
    X_test : DataFrame
        Test df
    arima_order : (int, int, int)
        Order (p, d, q)
    exog_variables : list[str]
        Possible exogeneous variables
    
    Return
    ------

    X_test : df with predicted values 
    '''
    X_test_res = X_test.copy()
    history = list(X_train["daily_pct_variation"].values)
    exog_train_value = (
        list(X_train[exog_variables].values) if exog_variables is not None else []
    )
    test_data = list(X_test_res["daily_pct_variation"].values)
    exog_test_value = (
        list(X_test_res[exog_variables].values) if exog_variables is not None else []
    )
    predicted_values = []
    upper_conf = []
    lower_conf = []

    for time_point in range(len(X_test_res)):
        model = ARIMA(endog= history,
                            exog = exog_train_value if exog_variables is not None else None,
                            order=arima_order)
        
        model_fit = model.fit()
        output = model_fit.get_forecast(step = 1,
                                        exog=exog_test_value[time_point] if exog_variables is not None else None
                                    )
        
        output_predicted_values = output.predicted_mean[0]
        conf_int = output.conf_int()[0]
        predicted_values.append(output_predicted_values)
        lower_conf.append(conf_int[0])
        upper_conf.append(conf_int[1])

        true_test_value = test_data[time_point]

        if exog_variables is not None:
            exog_train_value.append(exog_test_value[time_point])
        history.append(true_test_value)

    # Add the predicted values to the test dataset 
    X_test_res["predicted_values"] = predicted_values
    X_test_res["predicted_values_upper"] = upper_conf
    X_test_res["predicted_values_lower"] = lower_conf

    return X_test_res
