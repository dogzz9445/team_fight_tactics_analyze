from datetime import datetime, timedelta

def week_analyze_time_duration(start_date: datetime, end_date: datetime):
    analyze_date = start_date + timedelta(days=1)
    while not analyze_date > end_date:
        yield analyze_date - timedelta(days=7), analyze_date
        analyze_date = analyze_date + timedelta(days=1)
