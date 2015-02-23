import numpy as np
import pandas
import statsmodels.api as sm


turnstile_data = pandas.read_csv('turnstile_weather_v2.csv')
turnstile_data['DATEn'] = pandas.to_datetime(turnstile_data['DATEn'])
turnstile_data['day_week_p2'] = turnstile_data['day_week'].apply(lambda x: x**2)
turnstile_data['hour_p2'] = turnstile_data['hour'].apply(lambda x: x**2)
turnstile_data['hour_p3'] = turnstile_data['hour'].apply(lambda x: x**3)

def add_dummy_features(data, column, features):
    dummies = pandas.get_dummies(data[column], prefix=column)
    return data.join(dummies), features + list(dummies.columns)
 
features = ['day_week', 'day_week_p2', 'hour', 'hour_p2', 'hour_p3']
turnstile_data, features = add_dummy_features(turnstile_data, 'UNIT', features)

turnstile_data_train = turnstile_data[msk]
turnstile_data_test = turnstile_data[~msk]

dataframe = turnstile_data_train
features_data = dataframe[features]

# Values
values = dataframe['ENTRIESn_hourly']
m = len(values)

features_data['ones'] = np.ones(m) # Add a column of 1s (y intercept)
features_array = np.array(features_data)
values_array = np.array(values)

model = sm.OLS(values_array, features_array)
results = model.fit()
print("Params: %s" % (results.params))

test_data = turnstile_data_test[features]
test_data['ones'] = np.ones(turnstile_data_test.shape[0])
predictions = (np.matrix(test_data.values) * np.transpose(np.matrix(results.params)))

def compute_r_squared(data, predictions):
    r_squared = 1 - np.sum((data - predictions)**2)/np.sum((data-np.mean(data))**2)
    
    return r_squared
    
print("My variance score: %s" % (compute_r_squared(turnstile_data_test['ENTRIESn_hourly'].values, predictions.A1)))
