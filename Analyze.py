from datetime import datetime, timedelta

from lolchess.model.analyzed import Analyzed

from .src.Util.DateUtil import week_analyze_time_duration,
from .src.Analyzer import Analyzer

if __name__ == '__main__':
    analyzer = Analyzer()

    analyze_start_date = datetime(2021, 5, 27, 0, 0, 0)
    analyze_end_date = datetime(2021, 5, 29, 0, 0, 0)

    for s_date, e_date in week_analyze_time_duration(analyze_start_date, analyze_end_date):
        version = 1
        analyze_period = 6
        target_date = e_date - timedelta(days=1)

        print('Analyzing: ' + target_date.strftime('%Y-%m-%d'))
        analyzer.read_data(s_date, e_date, 100)

        json_result = analyzer.cluster_tft_matches(s_date, e_date, 6)
        
        # product
        ana = Analyzed(version = version, 
                        analyze_period = analyze_period, 
                        target_start_date=s_date, 
                        target_end_date=e_date,
                        target_date=target_date,
                        json_result=json_result)
        
        analyzer.postgres_db_manager.session.add(ana)
        analyzer.postgres_db_manager.session.commit()