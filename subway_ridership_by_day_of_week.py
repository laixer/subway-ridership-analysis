from ggplot import *

turnstile_data_by_date = turnstile_data[['day_week', 'ENTRIESn_hourly']].groupby(['day_week'], as_index=False).sum()
print(ggplot(turnstile_data_by_date, aes(x='day_week', y='ENTRIESn_hourly')) +
    geom_point() +
    geom_line() +
    xlab('date') +
    ylab('total entries') +
    ggtitle('total entries by day of week'))

# 6 - sunday