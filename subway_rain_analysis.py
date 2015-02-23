import copy
import pandas
import random
import scipy
from scipy import stats

turnstile_data = pandas.read_csv('turnstile_weather_v2.csv')
turnstile_data['DATEn'] = pandas.to_datetime(turnstile_data['DATEn'])


mp = {}
for i, row in turnstile_data.iterrows():
    key = "%s-%s-%s" % (row.UNIT, row.day_week, row.hour)
    if key not in mp:
        mp[key] = {'rain': [], 'norain': []}
    if row.rain:
        mp[key]['rain'].append(i)
    else:
        mp[key]['norain'].append(i)

random.seed(12348612)
rain_rows = []
non_rain_rows = []    
mp2 = copy.deepcopy(mp)
while len(rain_rows) < 100:
    rand = random.randint(0, len(mp2) - 1)
    key_at_rand = mp2.keys()[rand]
    
    # pick a random entry with rain for given key
    if not mp2[key_at_rand]['rain'] or not mp2[key_at_rand]['norain']:
        print("Delete %s" % (key_at_rand))
        del mp2[key_at_rand]
        continue
    rand_rain_idx = random.randint(0, len(mp2[key_at_rand]['rain']) - 1)
    rain_df_row = mp2[key_at_rand]['rain'].pop(rand_rain_idx)
    rand_nonrain_idx = random.randint(0, len(mp2[key_at_rand]['norain']) - 1)
    nonrain_df_row = mp2[key_at_rand]['norain'].pop(rand_nonrain_idx)
    rain_rows.append(rain_df_row)
    non_rain_rows.append(nonrain_df_row)
    #row_at_rand = turnstile_data.iloc()
    # pick random entry with rain

rain_data = turnstile_data.iloc[rain_rows]
norain_data = turnstile_data.iloc[non_rain_rows]

#U, p = scipy.stats.mannwhitneyu(rain_data["ENTRIESn_hourly"], norain_data["ENTRIESn_hourly"])
U, p = scipy.stats.mannwhitneyu(norain_data["ENTRIESn_hourly"], rain_data["ENTRIESn_hourly"])
print("Rain data mean: %s" % (rain_data['ENTRIESn_hourly'].mean()))
print("No rain data mean: %s" % (norain_data['ENTRIESn_hourly'].mean()))
print("U: %s" % (U))
print("p: %s" % (p))
