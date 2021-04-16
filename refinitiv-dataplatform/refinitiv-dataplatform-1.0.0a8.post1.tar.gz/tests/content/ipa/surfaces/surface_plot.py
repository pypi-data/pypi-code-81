# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

from conftest import open_platform_session
from refinitiv.dataplatform.content import ipa


def convert_DateString_to_float(date_string_array):
    import datetime
    import matplotlib.dates as dates

    date_float_array = []
    for date_string in date_string_array:
        date_string = str(date_string)
        try:
            date_float = dates.date2num(datetime.datetime.strptime(date_string, '%Y-%m-%d'))
            date_float_array.append(date_float)
        except ValueError:
            date_float = dates.date2num(datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ'))
            date_float_array.append(date_float)
    return date_float_array


open_platform_session()

response = ipa.surface.Surfaces().get_surface(
    universe=[
        ipa.surface.eti.Definition(
            tag="1",
            instrument_code="BNPP.PA@RIC",
            calculation_params=ipa.surface.eti.CalculationParams(
                price_side=ipa.enum_types.PriceSide.MID,
                volatility_model=ipa.enum_types.VolatilityModel.SVI,
                x_axis=ipa.enum_types.Axis.DATE,
                y_axis=ipa.enum_types.Axis.STRIKE,
                ),
            layout=ipa.surface.SurfaceOutput(
                format=ipa.enum_types.Format.MATRIX,
                y_point_count=10
                ),
            )
        ],
    outputs=[ipa.surface.Surfaces.Outputs.DATA]
    )

data = response.data

curve = data.surface.get_curve("2020-15-10", ipa.enum_types.Axis.X)
point = data.surface.get_point("2020-15-10", 38.25)

X, Y, Z = data.surface.get_axis()
Y = [convert_DateString_to_float(y) for y in Y]
fig = plt.figure(figsize=[15, 10])

ax = plt.axes(projection='3d')
ax.set_xlabel('moneyness')
ax.set_ylabel('time to expiry')
ax.set_zlabel('volatilities')

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
plt.show()
