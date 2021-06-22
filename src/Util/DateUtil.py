from datetime import datetime, timedelta

def week_analyze_time_duration(start_date: datetime, end_date: datetime):
    analyze_date = start_date + timedelta(days=1)
    while not analyze_date > end_date:
        yield analyze_date - timedelta(days=7), analyze_date
        analyze_date = analyze_date + timedelta(days=1)

def duration_datetime(self, start_time, end_time, period_delta):
    previous_time = start_time
    current_time = start_time + period_delta
    while not current_time > end_time:
        yield previous_time, current_time
        previous_time = current_time
        current_time = current_time + period_delta
