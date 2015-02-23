import numpy as np
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

def normalize_features(array):
   """
   Normalize the features in the data set.
   """
   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma

def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, 
    and the values for our thetas.
    
    This can be the same code as the compute_cost function in the lesson #3 exercises,
    but feel free to implement your own.
    """
    
    m = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    
    This can be the same gradient descent code as in the lesson #3 exercises,
    but feel free to implement your own.
    """
    
    m = len(values)
    cost_history = []

    for i in range(num_iterations):
        print("Iteration %s" % (i))
        theta = theta + (alpha/m)*np.dot(values - np.dot(features, theta), features)
        cost = compute_cost(features, values, theta)
        print("Cost is %s" % (cost))
        cost_history.append(cost)
    return theta, pandas.Series(cost_history)

dataframe = turnstile_data_train
features_data = dataframe[features]

# Values
values = dataframe['ENTRIESn_hourly']
m = len(values)

print("Normalizing features.")
features_data, mu, sigma = normalize_features(features_data)
features_data['ones'] = np.ones(m) # Add a column of 1s (y intercept)

features_array = np.array(features_data)
values_array = np.array(values)

alpha = 0.1
num_iterations = 75

print("Performing gradient descent.")
# Initialize theta, perform gradient descent
theta_gradient_descent = np.zeros(len(features_data.columns))
theta_gradient_descent, cost_history = gradient_descent(features_array, 
                                                        values_array, 
                                                        theta_gradient_descent, 
                                                        alpha, 
                                                        num_iterations)

test_data = (turnstile_data_test[features] - mu) / sigma
test_data['ones'] = np.ones(turnstile_data_test.shape[0])
predictions = (np.matrix(test_data.values) * np.transpose(np.matrix(theta_gradient_descent)))

def compute_r_squared(data, predictions):
    r_squared = 1 - np.sum((data - predictions)**2)/np.sum((data-np.mean(data))**2)
    
    return r_squared
    
print("My variance score: %s" % (compute_r_squared(turnstile_data_test['ENTRIESn_hourly'].values, predictions.A1)))
