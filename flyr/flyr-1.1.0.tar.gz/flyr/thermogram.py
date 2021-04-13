from math import sqrt, exp, fsum
from typing import Optional, Dict, Any, Union

import numpy as np
from PIL import Image
from nptyping import Array

import flyr.palettes as palettes


class FlyrThermogram:
    # Required members variables required to be set
    __thermal = None  # type: Array[int, ..., ..., ...]
    __metadata = None  # type: Dict[str, Union[float, int]]
    __optical = None  # type: Optional[Array[int, ..., ..., 3]]

    # Derivative member variables that are calculated when necessary and stored
    # prevent double calculation.
    __kelvin = None  # type: Optional[Array[float, ..., ...]]
    __celsius = None  # type: Optional[Array[float, ..., ...]]

    def __init__(
        self,
        thermal: Array[np.int64, ..., ...],
        metadata: Dict[str, Any],
        optical: Optional[Array[np.uint8, ..., ..., 3]] = None,
    ):
        """ Initialize a new instance of this class. The raw thermal data and
            the accompanying metadata to correctly interpret this data are
            required.

            Parameters
            ----------
            thermal : Array[np.int64, ..., ...]
                A 2D numpy array of 64 bit integers. This is the raw thermal
                data as it is stored in the FLIR file. Order is [H, W].
            metadata : Dict[str, Any]
                A dictionary with physical parameters to interpret the raw
                thermal data.
            optical : Array[np.uint8, ..., ..., 3]
                A 3D numpy array of 8 bit integers, in the order of [H, W, C].
                This should be a 'normal' photo (RGB) of the same scene as
                thermogram.
        """
        self.__thermal = thermal  # Raw thermal data
        self.__optical = optical  # Optical (RGB) photo in the thermogram
        self.__metadata = metadata

    def render(
        self,
        min_v: float = 0.0,
        max_v: float = 1.0,
        mode: str = "percentiles",  # or percentiles | span
        palette: str = "grayscale",
    ) -> Array[np.uint8, ..., ..., 3]:
        """ Renders the thermogram to RGB with the given settings.

            First the thermogram is normalized using the given interval and
            mode. Then the palette is used to translate the values to colors.

            Parameters
            ----------
            min_v: float. Is `0.0` by default.
                All values below this value will be clipped to this value,
                although the exact behaviour depends on the `mode`.
                    When `mode='minmax'`, the `min_v` (and `max_v`) values
                function directly as the thresholds to which the thermogram is
                clipped.
                    When mode='percentiles'` (default), then `min_v` and `max_v`
                are interpreted as percentiles. First the values for those
                percentiles are retrieved which are then used to clip the
                thermogram as described when `mode='minmax'`.
            max_v: float. Is `100.0` by default.
                See the `min_v` for details on how it is interpreted.
            mode: str. Options are 'percentiles' (default) and 'minmax'.
                The mode variable decides the normalization method and
                influences how `min_v` and `max_v` are used.
            palette: str. Is `'grayscale'` by default.
                The name of the color palette to use. Currently only grayscale
                and jet are supported.

            Returns
            -------
            Array[np.uint8, ..., ..., ...]
                A three dimensional array of integers between 0 and 255,
                representing an RGB render of the thermogram. Order is
                [H, W, C].
        """
        assert min_v < max_v
        normalizer = {  # Functions defined below
            "minmax": norm_minmax,
            "percentiles": norm_percentiles,
        }
        assert mode in normalizer.keys()
        assert palette == "grayscale" or palette in palettes.palettes

        normalized = normalizer[mode](min_v, max_v, self.kelvin)
        if palette == "grayscale":
            # Strategy for grayscale is very different from when using a map
            rendered = (normalized * 255).astype(np.uint8)
            outshape = rendered.shape + (3,)
            repeated = np.broadcast_to(rendered[..., None], outshape)
            return np.clip(repeated, 0, 255)  # return grayscale
        return palettes.map_colors(normalized, palette)  # return with color map

    def render_pil(self, **kwargs) -> Image:
        """ Renders the thermogram, but returns a pillow Image object. See
            `render()` for documentation on the parameters and other details.

            Returns
            -------
            PIL.Image
                A pillow Image of the rendered thermogram.
        """
        return Image.fromarray(self.render(**kwargs))

    @property
    def kelvin(self) -> Array[np.float64, ..., ...]:
        """ A property method that returns the thermogram's temperature in
            kelvin (K).

            Returns
            -------
            Array[np.float64, ..., ...]
                A 2D array of numpy float values in kelvin. Order is [H, W].
        """
        return self.__raw_to_kelvin(**self.__metadata)  # type: ignore

    @property
    def celsius(self) -> Array[np.float64, ..., ...]:
        """ A property method that returns the thermogram's temperature in
            degrees celsius (°C).

            Returns
            -------
            Array[np.float64, ..., ...]
                A 2D array of numpy float values in celsius. Order is [H, W].
        """
        return self.kelvin - 273.15

    @property
    def optical(self) -> Optional[Array[np.uint8, ..., ..., 3]]:
        """ Returns the thermogram's embedded photo.

            Returns
            -------
            Array[np.uint8, ..., ..., 3]
                A 3D array of 8 bit integers containing the RGB photo
                embedded within the FLIR thermogram.  Order is [H, W, C].
        """
        return self.__optical

    @property
    def metadata(self) -> Dict[str, Union[float, int]]:
        return self.__metadata.copy()

    def adjust_metadata(self, **kwargs: Union[float, int]):
        """ Updates the physical metadata used to calculate the kelvin / celsius values
            based on the raw thermal data.

            This can be used to calculate kelvin/celsius values with different settings
            than the ones embedded in the thermogram itself during capture.

            This method does not check the given parameters. Wrong parameters names or
            values will be accepted without exceptions being raised. These exceptions will
            only occur when `kelvin` or `celsius` is accessed.

            # Parameters
            emissivity: float
            object_distance: float
            atmospheric_temperature: float
            ir_window_temperature: float
            ir_window_transmission: float
            reflected_apparent_temperature: float
            relative_humidity: float
            planck_r1: float
            planck_r2: float
            planck_b: float
            planck_f: int
            planck_o: int
            atmospheric_trans_alpha1: float
            atmospheric_trans_alpha2: float
            atmospheric_trans_beta1: float
            atmospheric_trans_beta2: float
            atmospheric_trans_x: float
        """
        self.__metadata.update(kwargs)

    def __raw_to_kelvin(
        self,
        emissivity: float = 1.0,
        object_distance: float = 1.0,
        atmospheric_temperature: float = 293.15,
        ir_window_temperature: float = 293.15,
        ir_window_transmission: float = 1.0,
        reflected_apparent_temperature: float = 293.15,
        relative_humidity: float = 0.5,
        planck_r1: float = 21106.77,
        planck_r2: float = 0.012545258,
        planck_b: float = 1501.0,
        planck_f: int = 1,
        planck_o: int = -7340,
        atmospheric_trans_alpha1: float = 0.006569,
        atmospheric_trans_alpha2: float = 0.01262,
        atmospheric_trans_beta1: float = -0.002276,
        atmospheric_trans_beta2: float = -0.00667,
        atmospheric_trans_x: float = 1.9,
    ) -> Array[np.float64, ..., ...]:
        """ Use the details camera info metadata to translate the raw
            temperatures to °Kelvin.

            The method is expected to be called with the `metadata` member
            variable as its key words arguments, e.g.
            `__raw_to_kelvin(**self.camera_info)`. Missing values are filled
            with the parameters' default values.

            Parameters
            ----------
            emissivity : float
            object_distance : float
                Unit is meters
            atmospheric_temperature : float
                Unit is Kelvin
            ir_window_temperature : float
                Unit is Kelvin
            ir_window_transmission : float
                Unit is Kelvin
            reflected_apparent_temperature : float
                Unit is Kelvin
            relative_humidity : float
                Value in 0 and 1
            planck_r1 : float
            planck_r2 : float
            planck_b : float
            planck_f : float
            planck_o : int
            atmospheric_trans_alpha1 : float
            atmospheric_trans_alpha2 : float
            atmospheric_trans_beta1 : float
            atmospheric_trans_beta2 : float
            atmospheric_trans_x : float

            Returns
            -------
            Array[np.float64, ..., ...]
                An array of float64 values in kelvin.
        """
        # Transmission through window (calibrated)
        emiss_wind = 1 - ir_window_transmission
        refl_wind = 0

        # Transmission through the air
        water = relative_humidity * exp(
            1.5587
            + 0.06939 * (atmospheric_temperature - 273.15)
            - 0.00027816 * (atmospheric_temperature - 273.17) ** 2
            + 0.00000068455 * (atmospheric_temperature - 273.15) ** 3
        )

        def calc_atmos(alpha, beta):
            term1 = -sqrt(object_distance / 2)
            term2 = alpha + beta * sqrt(water)
            return exp(term1 * term2)

        atmos1 = calc_atmos(atmospheric_trans_alpha1, atmospheric_trans_beta1)
        atmos2 = calc_atmos(atmospheric_trans_alpha2, atmospheric_trans_beta2)
        tau1 = atmospheric_trans_x * atmos1 + (1 - atmospheric_trans_x) * atmos2
        tau2 = atmospheric_trans_x * atmos1 + (1 - atmospheric_trans_x) * atmos2

        # Radiance from the environment
        def plancked(t):
            planck_tmp = planck_r2 * (exp(planck_b / t) - planck_f)
            return planck_r1 / planck_tmp - planck_o

        raw_refl1 = plancked(reflected_apparent_temperature)
        raw_refl1_attn = (1 - emissivity) / emissivity * raw_refl1

        raw_atm1 = plancked(atmospheric_temperature)
        raw_atm1_attn = (1 - tau1) / emissivity / tau1 * raw_atm1

        term3 = emissivity * tau1 * ir_window_transmission
        raw_wind = plancked(ir_window_temperature)
        raw_wind_attn = emiss_wind / term3 * raw_wind

        raw_refl2 = plancked(reflected_apparent_temperature)
        raw_refl2_attn = refl_wind / term3 * raw_refl2

        raw_atm2 = plancked(atmospheric_temperature)
        raw_atm2_attn = (1 - tau2) / term3 / tau2 * raw_atm2

        subtraction = fsum(
            [
                raw_atm1_attn,
                raw_atm2_attn,
                raw_wind_attn,
                raw_refl1_attn,
                raw_refl2_attn,
            ]
        )

        raw_obj = self.__thermal.astype(np.float64)
        raw_obj /= emissivity * tau1 * ir_window_transmission * tau2
        raw_obj -= subtraction

        # Temperature from radiance
        raw_obj += planck_o
        raw_obj *= planck_r2
        planck_term = planck_r1 / raw_obj + planck_f
        return planck_b / np.log(planck_term)


def norm_minmax(
    min_t: float, max_t: float, thermal: Array[float, ..., ...]
) -> Array[float, ..., ...]:
    assert min_t < max_t
    thermal = np.clip(thermal, min_t, max_t)
    thermal = (thermal - min_t) / (max_t - min_t)
    return thermal


def norm_percentiles(
    min_p: float, max_p: float, thermal: Array[np.float64, ..., ...]
) -> Array[np.float64, ..., ...]:
    """ Normalizes the given thermal array using the values at the given minimum
        and maximum percentiles.

        Parameters
        ----------
        min_p: float
            Value between 0 and 1 that is lower than `max_p`. Indicates the
            percentile from which to take the minimum normalization value.
        max_p: float
            Value between 0 and 1 that is greater than `min_p`. Indicates the
            percentile from which to take the maximum normalization value.
        thermal: Array[np.float64, ..., ...]
            Array to normalize.

        Returns
        -------
        Array[np.float64, ..., ...]
            The normalized array, all np.float64 values between 0 and 1.
    """
    assert 0.0 <= min_p < max_p <= 1.0
    return norm_minmax(
        np.percentile(thermal, int(min_p * 100)),
        np.percentile(thermal, int(max_p * 100)),
        thermal,
    )
