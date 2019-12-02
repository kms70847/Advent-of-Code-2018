import re
import collections

def time_range(start, end):
    hour, minute = map(int,start.split(":"))
    end_hour, end_minute = map(int,end.split(":"))
    while hour != end_hour or minute != end_minute:
        yield (hour, minute)
        if minute == 59:
            minute = 0
            if hour == 23:
                hour = 0
            else:
                hour += 1
        else:
            minute += 1

events = []
with open("input") as file:
    for line in file:
        m = re.match(r"\[1518-(\d{2}-\d{2}) (\d{2}:\d{2})] (falls asleep|wakes up|Guard #(\d+) begins shift)", line)
        events.append(dict(zip("date time type id".split(), m.groups())))

events.sort(key=lambda d: (d["date"], d["time"]))

cur_guard = None
sleep_date = None
sleep_time = None
chart = {}
sleep_totals = collections.Counter()
for event in events:
    if event["type"].endswith("begins shift"):
        cur_guard = event["id"]
    elif event["type"] == "falls asleep":
        sleep_date = event["date"]
        sleep_time = event["time"] 
    elif event["type"] == "wakes up":
        for hour, minute in time_range(sleep_time, event["time"]):
            chart[sleep_date, hour, minute] = cur_guard
            sleep_totals[cur_guard] += 1



sleepiest = sleep_totals.most_common(1)[0][0]
sleeps_by_minute = collections.Counter()
for (date, hour, minute), g in chart.items():
    if g == sleepiest:
        sleeps_by_minute[minute] += 1

sleepiest_minute = int(sleeps_by_minute.most_common(1)[0][0])
print(int(sleepiest) * sleepiest_minute)



sleeps_by_guard_and_minute = collections.Counter()
for (date, hour, minute), g in chart.items():
    sleeps_by_guard_and_minute[g, minute] += 1

g, minute = sleeps_by_guard_and_minute.most_common(1)[0][0]
print(int(g)*minute)