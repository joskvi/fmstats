
from db import Database
import pandas as pd
from datetime import datetime


class ListeningHistory:

    def __init__(self, db_path):

        with Database(db_path) as database:
            self._listens = pd.DataFrame(database.query('select * from listens;'),
                                columns=['ts', 'track', 'album', 'artist'])
        self._listens.ts = self._listens.ts.apply(lambda ts: datetime.strptime(ts, '%Y-%m-%d %H:%M:%S'))

    def get_top_per_month(self, grouping_limit, grouping_key='artist'):
        ''' Returns a dataframe with top listens per month '''

        listens_stat = self._listens.copy()

        # Append a column with appropriate time values
        listens_stat['ts_interval'] = listens_stat.ts.apply(lambda ts: ts.strftime('%Y%m'))

        # Count listens per time internval and grouping key and rank them
        listens_stat = listens_stat.groupby(['ts_interval', grouping_key]).ts.agg(['count']).reset_index()
        listens_stat = listens_stat.sort_values(by=['ts_interval', 'count'], ascending=False)
        listens_stat['rank_no'] = listens_stat.groupby(['ts_interval']).cumcount()+1

        # Split the ranked list into top and botton based on the given grouping_limit
        # The groupings in the bottom are then aggregated to a single listening count per time interval
        listens_stat_high = listens_stat[listens_stat.rank_no <= grouping_limit]
        listens_stat_low = listens_stat[listens_stat.rank_no > grouping_limit]
        listens_stat_low = pd.DataFrame(listens_stat_low.groupby('ts_interval')['count'].sum()).reset_index()
        listens_stat_low[grouping_key] = 'Other'

        # Append the aggregated bottom to the top again, and return the dataframe
        listens_stat = listens_stat_high.append(listens_stat_low, sort=False)
        return listens_stat[['ts_interval', grouping_key, 'count']]


if __name__ == "__main__":
    
    history = ListeningHistory('database.db')
    print(history)

    print(history.get_top_per_month(5, grouping_key='album'))