import pandas
import numpy as np

def day_of_week_to_string(day_of_week):
    if day_of_week == 0:
        return "Monday"
    elif day_of_week == 1:
        return "Tuesday"
    elif day_of_week == 2:
        return "Wednesday"
    elif day_of_week == 3:
        return "Thursday"
    elif day_of_week == 4:
        return "Friday"
    elif day_of_week == 5:
        return "Saturday"
    elif day_of_week == 6:
        return "Sunday"
    

turnstile_data = pandas.read_csv('turnstile_weather_v2.csv')
turnstile_data['DATEn'] = pandas.to_datetime(turnstile_data['DATEn'])
turnstile_data['day_week'] = turnstile_data['day_week'].apply(day_of_week_to_string)
turnstile_data.describe()
msk = np.random.rand(len(turnstile_data)) < 0.8
