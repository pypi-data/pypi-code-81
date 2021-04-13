import os
from datetime import datetime
from thanetwffapi.query.SGQuery import SGQuery

class TestSGQuery:
    def test_read_df(self):

        # Arrange
        local_path = os.path.abspath(os.path.join(__file__, "../../resources"))
        file = 'A02-20170823-191000-192000.txt'

        df = SGQuery() \
            .using_db(local_path) \
            .with_name(file) \
            .with_channels(1, 3, 5, 7) \
            .query_files() \
            .correct_channels_microstrain() \
            .correct_timestamp() \
            .to_df()

        # Act
        timestamp_0 = datetime.strptime('2017-08-23 19:10:02.064000', '%Y-%m-%d %H:%M:%S.%f')

        # Assert
        assert (df.head().index[0]) == (timestamp_0)
