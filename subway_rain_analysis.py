"""
Performs an analysis on MTA turnstile data to see if there's a statistically
significant difference in ridership between days with rain and without rain.
"""
import copy
import pandas
import random
import scipy
from scipy import stats

turnstile_data = pandas.read_csv('turnstile_weather_v2.csv')
turnstile_data['DATEn'] = pandas.to_datetime(turnstile_data['DATEn'])

# Generate a map of unique unit, day of week and hour combinations and their 
# index in the turnstile data.
mp = {}
# TODO(laixer): There's probably a way to do this in pandas without iterating.
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
while len(rain_rows) < 100:
    rand = random.randint(0, len(mp) - 1)
    key_at_rand = mp.keys()[rand]
    
    if not mp[key_at_rand]['rain'] or not mp[key_at_rand]['norain']:
        print("Delete %s" % (key_at_rand))
        del mp[key_at_rand]
        continue
    # pick a random entry with rain for given key
    rand_rain_idx = random.randint(0, len(mp[key_at_rand]['rain']) - 1)
    rain_df_row = mp[key_at_rand]['rain'].pop(rand_rain_idx)
    # pick a random entry with no rain for same key.
    rand_nonrain_idx = random.randint(0, len(mp[key_at_rand]['norain']) - 1)
    nonrain_df_row = mp[key_at_rand]['norain'].pop(rand_nonrain_idx)
    rain_rows.append(rain_df_row)
    non_rain_rows.append(nonrain_df_row)

# Extract just the rows we selected.
rain_data = turnstile_data.iloc[rain_rows]
norain_data = turnstile_data.iloc[non_rain_rows]

U, p = scipy.stats.mannwhitneyu(
norain_data["ENTRIESn_hourly"], rain_data["ENTRIESn_hourly"])
print("Rain data mean: %s" % (rain_data['ENTRIESn_hourly'].mean()))
print("No rain data mean: %s" % (norain_data['ENTRIESn_hourly'].mean()))
print("U: %s" % (U))
print("p: %s" % (p))
