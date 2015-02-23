library(lubridate)
library(ggplot2)
library(scales)
library(plyr)

#turnstile_data <- read.csv('turnstile_weather_v2.csv')
#turnstile_data <- mutate(turnstile_data, date = as.Date(mdy(DATEn)), day_of_week = weekdays(date), entries = ENTRIESn_hourly)
turnstile_data <- mutate(turnstile_data, 
                         day_of_week = factor(day_week, levels=0:6, 
                                              labels=c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"), 
                                              ordered = TRUE))

turnstile_data_by_date <- ddply(turnstile_data, .(date), summarise, total_entries_k=sum(entries/1000000))
ggplot(turnstile_data_by_date, aes(date, total_entries_k)) + 
  geom_point() + 
  geom_line() + 
  scale_x_date(breaks = date_breaks("week")) +
  xlab("Date") +
  ylab("total entries (millions)") +
  ggtitle("total entries by date") +
  ylim(0, NA)
ggsave(filename = "entries_by_date.png", width = 8, height = 4)

turnstile_data_by_date <- mutate(turnstile_data_by_date, day_of_week = factor(weekdays(date), levels=c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"), ordered = TRUE))
turnstile_data_by_day_of_week <- ddply(turnstile_data_by_date, .(day_of_week), summarise, total_entries_k=mean(total_entries_k))
ggplot(turnstile_data_by_day_of_week, aes(day_of_week, total_entries_k, group="d")) + 
  geom_point() + 
  geom_line() + 
  xlab("Day of week") +
  ylab("Average # entries (thousands)")

turnstile_data_by_hour <- ddply(turnstile_data, .(date, day_of_week, hour), summarise, total_entries_k=sum(entries/1000))
turnstile_data_by_hour <- ddply(turnstile_data_by_hour, .(day_of_week, hour), summarise, total_entries_k=mean(total_entries_k))
ggplot(turnstile_data_by_hour, aes(hour, total_entries_k, group="d")) + 
  facet_grid(. ~ day_of_week) +
  geom_point() + 
  geom_line() + 
  xlab("Hour") +
  ylab("# entries (thousands)")

turnstile_data_by_station <- ddply(turnstile_data, .(date, station), summarise, total_entries_k=sum(entries/1000))
avg_by_station <- ddply(turnstile_data_by_station, .(station), summarize, total_entries_k=mean(total_entries_k))
top_stations <- avg_by_station$station[order(avg_by_station$total_entries_k, decreasing = TRUE)[1:20]]
turnstile_data_top_station <- turnstile_data_by_station[turnstile_data_by_station$station %in% top_stations,]

ggplot(turnstile_data_top_station, aes(date, total_entries_k, group="d")) + 
  facet_wrap(~ station, ncol = 2) +
  geom_point() + 
  geom_line() + 
  scale_x_date(breaks = date_breaks("week")) +
  xlab("Hour") +
  ylab("# entries (thousands)")
ggsave(filename = "entries_by_station.png", width = 8, height = 16)

# group by date, hour, sum(entries)
# group by day_week, hour, mean(entries)
