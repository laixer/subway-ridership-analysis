# turnstile_data_by_date <- ddply(turnstile_data, .(date, day_week), summarise, total_entries_k=sum(entries/1000))
# turnstile_data_by_day_of_week <- ddply(turnstile_data_by_date, .(day_week), summarise, total_entries_k=mean(total_entries_k))
# turnstile_data_by_day_of_week$day_week <- turnstile_data_by_day_of_week$day_week+1

turnstile_data_by_hour <- ddply(turnstile_data, .(date, day_of_week, hour), summarise, total_entries_k=sum(entries/1000))
turnstile_data_by_hour <- ddply(turnstile_data_by_hour, .(hour), summarise, total_entries_k=mean(total_entries_k))
turnstile_data_by_hour <- mutate(turnstile_data_by_hour, hour = as.numeric(hour))

plot(total_entries_k ~ hour, data = turnstile_data_by_hour)
fit <- lm(total_entries_k ~ hour + I(hour^2)+I(hour^3), data = turnstile_data_by_hour)
fit_line = predict(fit, turnstile_data_by_hour["hour"])
lines(fit_line)