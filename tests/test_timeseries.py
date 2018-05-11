import unittest
from datetime import datetime, timedelta

import sys
sys.path.append(r"../..")
from daymetpy import daymet_timeseries

class TimeseriesTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_ornl_df(self):
        ornl_lat, ornl_long = 35.9313167, -84.3104124
        df = daymet_timeseries(lon=ornl_long, lat=ornl_lat, start_year=2012, end_year=2012)

        self.assertTrue(df.year.count() == 365)
        self.assertTrue("tmax" in df.columns)
        self.assertTrue("tmin" in df.columns)
        self.assertTrue("prcp" in df.columns)

    def test_out_of_bounds(self):
        london_lat, london_long = 51.5072, 0.1275
        with self.assertRaises(NameError):
            df = daymet_timeseries(lon=london_long, lat=london_lat, start_year=2012, end_year=2012)


if __name__ == '__main__':
    unittest.main()
