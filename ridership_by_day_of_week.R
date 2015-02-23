turnstile_data_by_date <- ddply(turnstile_data, .(date, day_week), summarise, total_entries_k=sum(entries/1000))
turnstile_data_by_day_of_week <- ddply(turnstile_data_by_date, .(day_week), summarise, total_entries_k=mean(total_entries_k))
turnstile_data_by_day_of_week$day_week <- turnstile_data_by_day_of_week$day_week+1

plot(total_entries_k ~ day_week, data = turnstile_data_by_day_of_week)
fit <- lm(total_entries_k ~ day_week + I(day_week^2), data = turnstile_data_by_day_of_week)
fit_line = predict(fit, turnstile_data_by_day_of_week["day_week"])
lines(fit_line)