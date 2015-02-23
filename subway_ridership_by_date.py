from ggplot import *

turnstile_data_by_date = turnstile_data[['DATEn', 'day_week', 'ENTRIESn_hourly']].groupby(['DATEn', 'day_week'], as_index=False).sum()
p = ggplot(turnstile_data_by_date, aes(x='DATEn', y='ENTRIESn_hourly')) + \
    geom_point() + \
    geom_line() + \
    scale_x_date(breaks=date_breaks('7 days'), labels = date_format("%Y-%m-%d")) + \
    xlab('date') + \
    ylab('total entries') + \
    ggtitle('total entries by date')
print(p)