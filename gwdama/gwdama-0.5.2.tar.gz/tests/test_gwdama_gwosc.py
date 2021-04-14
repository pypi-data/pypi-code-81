# This file tests the reading capabilities
# using gwosc datasets

import unittest
from os import getcwd, path 
import sys
from pandas import read_csv
from pandas.testing import assert_frame_equal
from gwdama.io import GwDataManager

class TestDama(unittest.TestCase):
    """
    Class to test if the output af a simple data acquisition with gwdama performs as expected
    """

    def setUp(self):
        """
        This method will be called before the test and reads the existing reference DataFrame
        """
        df_name = "glitch_sample.csv"
        script_path = path.join(getcwd(), path.dirname(sys.argv[0]))
        data_dir = path.join(path.dirname(script_path),"..","data")
        
        try:
            ref_df = read_csv(path.join(data_dir, df_name))
        except IOError:
            print(f"Cannot access the reference glitch Dataframe at {data_dir}")      
        # Store the reference DataFrame
        self.ref_df = ref_df
      
        gl_csv = "glitch_sample_list_L1_O2.csv"
        try:
            gl_df = read_csv(path.join(data_dir, gl_csv))
        except IOError:
            print(f"Cannot access glitch specs Dataframe at {data_dir}")
        
        ifo = gl_df['ifo'].unique()[0]

        # Instance GwDataManager class
        gldama = GwDataManager("test_glitch_gwosc")

        # Import glitches data
        for n, t0_gps in enumerate(gl_df['GPStime']):
            t1=t0_gps-.5
            t2=t0_gps+.5
            gldama.read_gwdata(t1, t2, ifo=ifo, dts_key=f"Gltich_{n+1}")
        
        # Convert to DataFrame and store
        self.test_df = gldama.to_DataFrame()
   
    def test_dama(self):
        """
        Test that the reference DataFrame in data is equal to the acquired one
        """
        #foo = pd.DataFrame()
        assert_frame_equal(self.ref_df, self.test_df)

if __name__ == '__main__':
    unittest.main()          