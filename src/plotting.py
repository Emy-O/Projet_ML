import plotly.graph_objects as go




def plot_predicted_value(X_train, X_test):
    '''Function to plot the predicted value of the Arima forecasting'''
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=X_train["Date"], y=X_train["daily_pct_variation"], name='STOX X50 index',
                            line=dict(color='royalblue', width=1.5)))

    fig.add_trace(go.Scatter(x=X_test["Date"], y=X_test["daily_pct_variation"], name='STOX X50 index real value',
                            line=dict(color='royalblue', width=3, dash = "dash")))


    fig.add_trace(go.Scatter(x=X_test["Date"], y=X_test["predicted_values"], name='STOX X50 index predicted',
                            line=dict(color='purple', width=1.5)))

    # Confidence interval 
    fig.add_trace(go.Scatter(x=X_test["Date"], y=X_test["predicted_values_upper"], 
        line=dict(color='rgba(0,100,80,0.2)'),
        fill='tonexty',
        name='Confidence Interval upper'
    ))

    fig.add_trace(go.Scatter(x=X_test["Date"], y=X_test["predicted_values_lower"],  
        line=dict(color='rgba(0,100,80,0.2)'),
        fill='tonexty',
        name='Confidence Interval upper' 
    ))

    fig.update_layout(title='Impact of the ECB press conferences dates on the STOXX50 index',
                    xaxis_title='Date',
                    yaxis_title='STOXX50')
    fig.show()

