#!/usr/bin/env python3

import epw
import matplotlib.pyplot as plt

sub_dict = {
        ("Zone", "ZONE1", "Ceiling Height"): [15., 20.],
        ("Material", "BETON 18CM", "Conductivity"): [0.5, 0.3],
        ("Material", "BETON 20CM", "Conductivity"): [0.8, 0.2]
    }

df_list = epw.core.sub_run(epw.data.idf_cube_path(),
                           weather_file_path=epw.data.weather_san_francisco_tmy_path(),
                           sub_dict=sub_dict)

print(df_list)

for df in df_list:
    df['DistrictHeating:Facility [J](Hourly)'].plot(figsize=(20, 8))

plt.show()