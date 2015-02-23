from sklearn import datasets, linear_model
import pandas


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

regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(turnstile_data_train[features], turnstile_data_train['ENTRIESn_hourly'])

print '%-20s: %s' % ("Intercept", regr.intercept_)
for a, b in zip(features, regr.coef_):
    print '%-20s: %s' % (a, b)

print('Variance score: %.2f' % regr.score(turnstile_data_test[features], turnstile_data_test['ENTRIESn_hourly']))

