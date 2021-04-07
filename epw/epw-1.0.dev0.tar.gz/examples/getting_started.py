#!/usr/bin/env python3

import epw
import matplotlib.pyplot as plt

sub_dict = {("Material", "BETON 20CM", "Conductivity"): 9.99}

df = epw.core.sub_run(epw.data.idf_cube_path(),
                      weather_file_path=epw.data.weather_san_francisco_tmy_path(),
                      sub_dict=sub_dict)

df.plot()
plt.show()