all_data = rbind(rain_data, no_rain_data)
all_data <- mutate(all_data, rain=factor(rain, labels=c("no", "yes")))

ggplot(all_data, aes(x=ENTRIESn_hourly, fill=rain)) + 
  geom_histogram(alpha=0.2, position="identity", binwidth = 500) +
  xlab("hourly entries") +
  ggtitle("entry counts for a sample of 100 rain and non-rain entries")
ggsave(filename = "histogram_entries_rain_no_rain.png", width = 8, height = 4)
