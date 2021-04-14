"""
A collection of reference ISP algorithms.
"""

import time                  # built-in library
import warnings              # built-in library
from typing import Tuple     # built-in library
from typing import Sized     # built-in library
from typing import Iterable  # built-in library
from typing import Optional  # built-in library
from typing import Callable  # built-in library
import numpy as np           # pip install numpy
import colorio               # pip install colorio
import cv2                   # pip install opencv-python


class Algorithms:
    """
    A collection of ISP algorithms. See help(rawpipe) for documentation.
    """

    def __init__(self, verbose=False):
        """
        Initialize self. If verbose is True, progress information will be printed
        to stdout.
        """
        self.verbose = verbose

    def clip(self, frame: np.ndarray, lo: float = 0.0, hi: float = 1.0) -> np.ndarray:
        """
        Clip all pixels in the given frame to [lo, hi]. The frame may be in either
        RGB or raw format.
        """
        t0 = time.time()
        frame_out = np.clip(frame, lo, hi)
        self._vprint(f"{_elapsed(t0)} - clipping from {self._minmax(frame)} to [{lo:.2f}, {hi:.2f}]")
        return frame_out

    def bayer_split(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split the given Bayer frame into four single-color frames.
        """
        # pylint: disable=no-self-use
        ch1 = frame[0::2, 0::2]
        ch2 = frame[0::2, 1::2]
        ch3 = frame[1::2, 0::2]
        ch4 = frame[1::2, 1::2]
        return ch1, ch2, ch3, ch4

    def bayer_combine(self,
                      ch1: np.ndarray,
                      ch2: np.ndarray,
                      ch3: np.ndarray,
                      ch4: np.ndarray) -> np.ndarray:
        """
        Interleave the given Bayer channels into a complete frame.
        """
        # pylint: disable=no-self-use
        frame = np.zeros(np.array(ch1.shape) * 2, dtype=ch1.dtype)
        frame[0::2, 0::2] = ch1
        frame[0::2, 1::2] = ch2
        frame[1::2, 0::2] = ch3
        frame[1::2, 1::2] = ch4
        return frame

    def downsample(self, frame: np.ndarray, iterations: int = 1) -> np.ndarray:
        """
        Downsample the given RGB/Bayer frame by a factor of two in both directions,
        that is, to a quarter of its original size. This is repeated a given number
        of iterations. If iterations is zero, the frame is returned untouched. See
        resize() for arbitrary resizing with proper interpolation in RGB domain.
        """
        if iterations >= 1:
            t0 = time.time()
            orgh, orgw = frame.shape[:2]
            if frame.ndim == 3:  # RGB mode
                mode = "RGB"
                frame = frame[::2*iterations, ::2*iterations]
            if frame.ndim == 2:  # Bayer mode
                mode = "Bayer"
                for _ in range(iterations):
                    ch1, ch2, ch3, ch4 = self.bayer_split(frame)
                    ch1 = ch1[::2, ::2]
                    ch2 = ch2[::2, ::2]
                    ch3 = ch3[::2, ::2]
                    ch4 = ch4[::2, ::2]
                    frame = self.bayer_combine(ch1, ch2, ch3, ch4)
            imgh, imgw = frame.shape[:2]
            factor = f"{2**iterations} x {2**iterations}"
            self._vprint(f"{_elapsed(t0)} - {mode} downsampling [{factor}] from {orgw} x {orgh} to {imgw} x {imgh}")
        return frame

    def resize(self, frame: np.ndarray, target_width: int, target_height: int) -> np.ndarray:
        """
        Resize the given RGB frame to the given target width and height using Lanczos
        interpolation. If target width and height are the same as current width and
        height, the frame is returned untouched.
        """
        t0 = time.time()
        orgh, orgw = frame.shape[:2]
        dsth, dstw = int(target_height), int(target_width)
        if (dstw, dsth) != (orgw, orgh):
            frame = cv2.resize(frame, (dstw, dsth), cv2.INTER_LANCZOS4)
            dsth, dstw = frame.shape[:2]
            self._vprint(f"{_elapsed(t0)} - resizing [Lanczos] from {orgw} x {orgh} to {dstw} x {dsth}")
        return frame

    def subtract(self, frame: np.ndarray, blacklevels: Iterable) -> np.ndarray:
        """
        Subtract per-channel black levels from the given frame, but do not linearize.
        For demosaiced RGB frames, blacklevels must contain three values; for raw Bayer
        frames, four values are required. The caller is responsible for making sure
        that the per-channel levels are in the same Bayer order as the frame itself.
        """
        t0 = time.time()
        levels = np.array(blacklevels)
        if frame.ndim == 3:  # already demosaiced
            assert levels.size == 3, levels
            frame = np.maximum(frame, levels)
            frame = frame - levels
        else:  # raw Bayer
            assert levels.size == 4, levels
            rggb = list(self.bayer_split(frame))
            rggb = [np.maximum(ch, level) - level for ch, level in zip(rggb, levels)]
            frame = self.bayer_combine(*rggb)
        self._vprint(f"{_elapsed(t0)} - subtracting black levels {levels}: range = {self._minmax(frame)}")
        return frame

    def linearize(self,
                  frame: np.ndarray,
                  blacklevel: float = None,
                  whitelevel: float = None,
                  num_clipped: int = 1000) -> np.ndarray:
        """
        Linearize the given frame such that pixels are first clipped to the range
        [BL, WL] and then remapped to [0, 1], where BL and WL are the given black
        level and white level, respectively. If blacklevel is None, it is taken to
        be the Nth smallest pixel value within the frame, where N = num_clipped+1.
        A missing whitelevel is similarly estimated as the Nth largest pixel value.
        This algorithm is format-agnostic, although it's typically applied on raw
        sensor data.
        """
        if blacklevel is None:
            t0 = time.time()
            percentile = num_clipped / frame.size * 100.0
            blacklevel = np.percentile(frame, percentile)
            self._vprint(f"{_elapsed(t0)} - estimating black level: {percentile:5.2f}th percentile = {blacklevel:.2f}")
        if whitelevel is None:
            t0 = time.time()
            percentile = (1.0 - num_clipped / frame.size) * 100.0
            whitelevel = np.percentile(frame, percentile)
            self._vprint(f"{_elapsed(t0)} - estimating white level: {percentile:5.2f}th percentile = {whitelevel:.2f}")
        if (blacklevel, whitelevel) != (0, 1):
            frame = self.clip(frame, blacklevel, whitelevel)
            t0 = time.time()
            frame -= blacklevel
            frame /= whitelevel - blacklevel
            self._vprint(f"{_elapsed(t0)} - linearizing from [{blacklevel:.2f}, {whitelevel:.2f}] to [0, 1]")
        return frame

    def demosaic(self,
                 frame: np.ndarray,
                 bayer_pattern: str,
                 downsample: bool = False) -> np.ndarray:
        """
        Demosaic the given sensor raw frame using the Edge Aware Demosaicing (EAD)
        algorithm. Bayer order must be specified by the caller, and must be "RGGB",
        "GBRG", "BGGR", or "GRBG". The frame must be in floating-point format with
        all pixel values in the [0, 1] range.

        If the 'downsample' flag is True, RGB values are picked from the raw Bayer
        pattern as-is, without any interpolation other than averaging the greens.
        This reduces the size of the image by a factor of 2 x 2. In 'downsample'
        mode, pixel values need not be in [0, 1] range.
        """
        t0 = time.time()
        if not downsample:
            assert np.all((frame >= 0.0) * (frame <= 1.0)), "demosaic() requires pixel values in range [0, 1]"
            bayer_to_cv2 = {"RGGB": cv2.COLOR_BAYER_BG2RGB_EA,
                            "GBRG": cv2.COLOR_BAYER_GR2RGB_EA,
                            "BGGR": cv2.COLOR_BAYER_RG2RGB_EA,
                            "GRBG": cv2.COLOR_BAYER_GB2RGB_EA}
            frame = (frame * 65535).astype(np.uint16)
            frame = cv2.cvtColor(frame, bayer_to_cv2[bayer_pattern.upper()])
            frame = frame / 65535.0
            method = "EAD"
        else:
            channels = self.bayer_split(frame)
            bayer_to_index = {"RGGB": [0, 1, 2, 3],
                              "GBRG": [2, 0, 3, 1],
                              "BGGR": [3, 1, 2, 0],
                              "GRBG": [1, 0, 3, 2]}
            indices = bayer_to_index[bayer_pattern.upper()]
            r = channels[indices[0]]
            g = (channels[indices[1]] + channels[indices[2]]) / 2.0
            b = channels[indices[3]]
            frame = np.dstack((r, g, b))
            method = "downsample"
        self._vprint(f"{_elapsed(t0)} - demosaicing [{method}, {bayer_pattern}]: range = {self._minmax(frame)}")
        return frame

    def lsc(self, frame: np.ndarray, lscmap: np.ndarray) -> np.ndarray:
        """
        Multiply the given RGB/raw frame by the given lens shading correction (LSC)
        map. If the frame is in Bayer raw format, the LSC map must have the same
        size and Bayer order as the frame; otherwise, results will be unpredictable.
        In case of an RGB frame, the LSC map is automatically rescaled to match the
        frame. Also, the LSC map may be grayscale to correct vignetting only, or RGB
        to correct vignetting and/or color shading. If lscmap is None, the frame is
        returned untouched.
        """
        if lscmap is not None:
            t0 = time.time()
            imgh, imgw = frame.shape[:2]
            lsch, lscw = lscmap.shape[:2]
            need_resize = lscmap.shape[:2] != frame.shape[:2]
            if need_resize:
                xgrid = np.linspace(0, lscw - 1, imgw)
                ygrid = np.linspace(0, lsch - 1, imgh)
                mgrid = np.dstack(np.meshgrid(xgrid, ygrid, indexing="xy"))
                numthreads = cv2.getNumThreads()
                cv2.setNumThreads(0)  # work-around for OpenCV 4.1.2 deadlock
                lscmap = cv2.remap(lscmap, mgrid.astype(np.float32), None, cv2.INTER_LINEAR)
                cv2.setNumThreads(numthreads)
            if lscmap.ndim < frame.ndim:
                lscmap = np.atleast_3d(lscmap)  # {RGB, monochrome} => RGB
            frame = frame * lscmap
            with np.printoptions(formatter={'float': lambda x: f"{x:.3f}"}):
                if lscmap.ndim == 3:  # RGB
                    gains = np.amax(lscmap, axis=(0, 1))
                if lscmap.ndim == 2:  # assume Bayer raw, ignore grayscale
                    gains = np.array([np.amax(c) for c in self.bayer_split(lscmap)])
                self._vprint(f"{_elapsed(t0)} - applying LSC with max gains {gains}: range = {self._minmax(frame)}")
        return frame

    def wb(self, frame: np.ndarray, gains: Sized) -> np.ndarray:
        """
        Multiply the RGB channels of the given frame by the given white balance
        coefficients. If there are only two coefficients instead of three, they
        are applied on the R and B channels. If gains is None, the frame is
        returned untouched.
        """
        if gains is not None:
            t0 = time.time()
            gains = np.array(gains)
            gains = np.insert(gains, 1, 1.0) if len(gains) == 2 else gains
            frame = frame * gains
            with np.printoptions(formatter={'float': lambda x: f"{x:.3f}"}):
                self._vprint(f"{_elapsed(t0)} - applying WB gains {gains}: range = {self._minmax(frame)}")
        return frame

    def ccm(self, frame: np.ndarray, matrix: np.ndarray, clip=True) -> np.ndarray:
        """
        Apply the given color correction matrix on the given RGB frame. If the
        'clip' flag is True, input colors are clipped to [0, 1] to avoid "pink
        sky" artifacts caused by the combination of clipped highlights and
        less-than-1.0 coefficients in the CCM. No attempt is made at gamut
        mapping or highlight recovery. If matrix is None, the frame is returned
        untouched.
        """
        if matrix is not None:
            if clip:
                frame = self.clip(frame, 0, 1)
            t0 = time.time()
            frame = frame @ matrix.T
            with np.printoptions(formatter={'float': lambda x: f"{x:.2f}"}):
                sums = f"with column sums {np.sum(matrix, axis=0).T}"
                self._vprint(f"{_elapsed(t0)} - applying CCM {sums}: range = {self._minmax(frame)}")
        return frame

    def tonemap(self, frame: np.ndarray, mode: str = "Reinhard") -> np.ndarray:
        """
        Apply Reinhard tonemapping on the given RGB frame, compressing the range
        [0, N] to [0, 1]. Negative values are clipped to zero. This algorithm is
        format-agnostic. If mode is not "Reinhard", the frame is returned untouched.
        """
        if mode is not None:
            if mode == "Reinhard":
                frame = self.clip(frame, 0, np.inf)
                t0 = time.time()
                frame = frame.astype(np.float32)  # can't handle float64
                algo = cv2.createTonemapReinhard(gamma=1.0, intensity=0.0, light_adapt=0.0, color_adapt=0.0)
                frame = algo.process(frame)
                self._vprint(f"{_elapsed(t0)} - tonemapping [{mode}]: range = {self._minmax(frame)}")
        return frame

    def chroma_denoise(self,
                       frame: np.ndarray,
                       strength: int = 6,
                       winsize: int = 17) -> np.ndarray:
        """
        Apply non-local means denoising (Buades et al. 2011) on the given RGB frame.
        Input colors are clipped to [0, 1] prior to denoising. Increasing the values
        of filter strength and search window size make the denoising more aggressive
        and more time-consuming. If strength is 0, the frame is returned untouched.
        """
        if strength > 0:
            maxval, dtype = (255, np.uint8)  # OpenCV denoising can't handle 16-bit color
            frame = self.clip(frame * maxval + 0.5, 0, maxval)
            t0 = time.time()
            frame = frame.astype(dtype)
            frame = cv2.fastNlMeansDenoisingColored(frame, h=0, hColor=strength, searchWindowSize=winsize)
            frame = frame.astype(np.float32) / maxval
            self._vprint(f"{_elapsed(t0)} - chroma denoising [s={strength:.2f}, w={winsize}]: range = {self._minmax(frame)}")
        return frame

    def saturate(self,
                 frame: np.ndarray,
                 booster: Optional[Callable[[np.ndarray], np.ndarray]]) -> np.ndarray:
        """
        Apply the caller-provided boost function on the given RGB frame. The input
        frame is converted to HSL color space and the S channel given as the sole
        input to the boost function. Input RGB colors are clipped to [0, 1] before
        converting to HSL. If booster is None, the frame is returned untouched.

        Example:
          img = pipe.saturate(img, lambda x: x ** 0.75)
        """
        if booster is not None:
            t0 = time.time()
            hsl = _transform_srgb_to_hsl(frame)  # HSL is in planar form
            hsl[1] = booster(hsl[1])  # saturation boost
            hsl[1] = np.clip(hsl[1], 0, 1)  # may be -eps or 1+eps
            frame = _transform_hsl_to_srgb(hsl)  # RGB back in interleaved form
            self._vprint(f"{_elapsed(t0)} - applying HSL saturation boost: range = {self._minmax(frame)}")
        return frame

    def gamma(self,
              frame: np.ndarray,
              mode: str = "sRGB",
              lut: np.ndarray = None) -> np.ndarray:
        """
        Apply rec709 or sRGB gamma or a custom tone curve on the given frame.
        Input colors are clipped to [0, 1] to avoid any arithmetic exceptions.
        In "LUT" mode, the frame is quantized to match the number of entries N
        in the look-up table; for example, if N=64, the output frame will have
        6-bit colors (and severe banding). This algorithm is format-agnostic.
        If mode is None, the frame is returned untouched.
        """
        if mode is not None:
            realmode = mode
            frame = self.clip(frame, 0, 1)  # can't handle values outside of [0, 1]
            t0 = time.time()
            if realmode in ["sRGB", "rec709"]:
                bpp = 14
                maxval = 2 ** bpp - 1
                lut = np.linspace(0, 1, 2 ** bpp)
                mode = "LUT"
                if realmode == "sRGB":
                    srgb_lo = 12.92 * lut
                    srgb_hi = 1.055 * np.power(lut, 1.0/2.4) - 0.055
                    threshold_mask = (lut > 0.0031308)
                    lut = srgb_hi * threshold_mask + srgb_lo * (~threshold_mask)
                    lut = lut * maxval
                if realmode == "rec709":
                    srgb_lo = 4.5 * lut
                    srgb_hi = 1.099 * np.power(lut, 0.45) - 0.099
                    threshold_mask = (lut > 0.018)
                    lut = srgb_hi * threshold_mask + srgb_lo * (~threshold_mask)
                    lut = lut * maxval
            if mode == "LUT":
                assert lut is not None
                maxval = len(lut) - 1
                frame = self.quantize(frame, maxval)  # [0, 1] ==> [0, maxval]
                frame = lut[frame]                    # [0, maxval] ==> [0, maxval]
                frame = frame / maxval                # [0, maxval] ==> [0, 1]
            self._vprint(f"{_elapsed(t0)} - applying gamma curve [{realmode}]: range = {self._minmax(frame)}")
        return frame

    def quantize(self,
                 frame: np.ndarray,
                 maxval: int,
                 dtype: np.dtype = np.uint16) -> np.ndarray:
        """
        Clip the given frame to [0, 1], rescale it to [0, maxval], and convert
        it to the given dtype with proper rounding. This algorithm is format-
        agnostic.
        """
        t0 = time.time()
        frame = self.clip(frame * maxval + 0.5, 0, maxval)
        frame = frame.astype(dtype)
        self._vprint(f"{_elapsed(t0)} - quantizing from float [0, 1] to {np.dtype(dtype).name} [0, {maxval}]")
        return frame

    def _vprint(self, message: str, **kwargs):
        if self.verbose:
            print(message, **kwargs)

    def _minmax(self, frame: np.ndarray) -> str:
        if self.verbose:
            minmax_str = f"[{np.min(frame):.2f}, {np.max(frame):.2f}]"
            return minmax_str
        return ""


def _transform_srgb_to_hsl(frame: np.ndarray) -> np.ndarray:
    rgb = frame.swapaxes(-1, 0)  # (H, W, 3) ==> (3, W, H)
    rgb = np.clip(rgb, 0.001, 0.999)  # colorio.cs.HSL() can't handle 0.0 and 1.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        hsl = colorio.cs.HSL().from_rgb1(rgb)
        hsl = np.nan_to_num(hsl)
    return hsl


def _transform_hsl_to_srgb(frame: np.ndarray) -> np.ndarray:
    rgb = colorio.cs.HSL().to_rgb1(frame)
    rgb = rgb.swapaxes(-1, 0)  # (3, W, H) => (H, W, 3)
    rgb = np.ascontiguousarray(rgb)
    return rgb


def _elapsed(t0: float) -> str:
    elapsed = (time.time() - t0) * 1000
    elapsed_str = f"{elapsed:8.2f} ms"
    return elapsed_str
