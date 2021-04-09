# coding:utf-8

"""Stb-tester Python API: Automated GUI Testing for Set-Top Boxes.

Copyright © 2013-2020 Stb-tester.com Ltd. All rights reserved.
"""

import stbt_core  # open source APIs
from stbt_core import *

# The following APIs are not open source, and they require the Stb-tester Node
# hardware to run. This file contains stubs for local installation, to allow
# IDE linting & autocompletion.
__all__ = stbt_core.__all__ + [
    "audio_chunks",
    "AudioChunk",
    "BadSyncPattern",
    "detect_pages",
    "find_selection_from_background",
    "FIRST_FRAME_TIME",
    "get_rms_volume",
    "measure_av_sync",
    "play_audio_file",
    "prometheus",
    "stop_job",
    "TEST_PACK_ROOT",
    "VolumeChangeDirection",
    "VolumeChangeTimeout",
    "wait_for_volume_change",
]


from collections import namedtuple

import numpy
from enum import IntEnum
from _stbt.imgutils import _frame_repr

from . import prometheus


FIRST_FRAME_TIME = None
TEST_PACK_ROOT = None


# pylint: disable=redefined-outer-name,unused-argument


def _raise_premium(api_name):
    raise NotImplementedError(
        "`stbt.%s` is a premium API only available to customers of "
        "Stb-tester.com Ltd. It requires *Stb-tester Node* hardware to run. "
        "See https://stb-tester.com for details on products and pricing. "
        "If you are receiving this error on the *Stb-tester Node* hardware "
        "contact support@stb-tester.com for help" % api_name)


class AudioChunk(numpy.ndarray):
    """A sequence of audio samples.

    An ``AudioChunk`` object is what you get from `audio_chunks`. It is a
    subclass of `numpy.ndarray`. An ``AudioChunk`` is a 1-D array containing
    audio samples in 32-bit floating point format (`numpy.float32`) between
    -1.0 and 1.0.

    In addition to the members inherited from `numpy.ndarray`, ``AudioChunk``
    defines the following attributes:

    :ivar float time: The wall-clock time of the first audio sample in this
        chunk, as number of seconds since the unix epoch
        (1970-01-01T00:00:00Z). This is the same format used by the Python
        standard library function `time.time`.

    :ivar int rate: Number of samples per second. This will typically be 48000.

    :ivar float duration: The duration of this audio chunk in seconds.

    :ivar float end_time: ``time`` + ``duration``.

    ``AudioChunk`` supports slicing using Python's ``[x:y]`` syntax, so the
    above attributes will be updated appropriately on the returned slice.
    """
    def __new__(cls, array, dtype=None, order=None, time=None, rate=48000):
        _raise_premium("AudioChunk")

    def __array_finalize__(self, obj):
        if obj is not None:
            _raise_premium("AudioChunk")

    @property
    def time(self):
        _raise_premium("AudioChunk.time")
        return 0.

    @property
    def duration(self):
        _raise_premium("AudioChunk.duration")
        return 0.

    @property
    def rate(self):
        _raise_premium("AudioChunk.rate")
        return 0

    @property
    def end_time(self):
        _raise_premium("AudioChunk.end_time")
        return 0.


def audio_chunks(time_index=None, _dut=None):
    """Low-level API to get raw audio samples.

    ``audio_chunks`` returns an iterator of `AudioChunk` objects. Each one
    contains 100ms to 5s of mono audio samples (see `AudioChunk` for the data
    format).

    ``audio_chunks`` keeps a buffer of 10s of audio samples. ``time_index``
    allows the caller to access these old samples. If you read from the
    returned iterator too slowly you may miss some samples. The returned
    iterator will skip these old samples and silently re-sync you at -10s. You
    can detect this situation by comparing the ``.end_time`` of the previous
    chunk to the ``.time`` of the current one.

    :type time_index: int or float
    :param time_index:
        Time from which audio samples should be yielded.  This is an epoch time
        compatible with ``time.time()``. Defaults to the current time as given
        by ``time.time()``.

    :return: An iterator yielding `AudioChunk` objects
    :rtype: Iterator[AudioChunk]
    """
    _raise_premium("audio_chunks")
    return iter([AudioChunk((4800,), dtype=numpy.float32)])


def get_rms_volume(duration_secs=3, stream=None):
    """Calculate the average `RMS`_ volume of the audio over the given duration.

    For example, to check that your mute button works::

        stbt.press('KEY_MUTE')
        time.sleep(1)  # <- give it some time to take effect
        assert get_rms_volume().amplitude < 0.001  # -60 dB

    :type duration_secs: int or float
    :param duration_secs: The window over which you should average, in seconds.
        Defaults to 3s in accordance with short-term loudness from the EBU TECH
        3341 specification.

    :type stream: Iterator[AudioChunk]
    :param stream: Audio stream to measure. Defaults to ``audio_chunks()``.

    :raises ZeroDivisionError: If ``duration_secs`` is shorter than one sample
        or ``stream`` contains no samples.

    :returns:
        An object with the following attributes:

        * **amplitude** (*float*) – The RMS amplitude over the specified
          window. This is a value between 0.0 (absolute silence) and 1.0 (a
          full-range square wave).

        * **time** (*float*) – The start of the window, as number of seconds
          since the unix epoch (1970-01-01T00:00Z). This is compatible with
          ``time.time()`` and ``stbt.Frame.time``.

        * **duration_secs** (*float*) – The window size, in seconds. Typically
          this will be the same as passed into ``get_rms_volume()``.

    .. _RMS: https://en.wikipedia.org/wiki/Root_mean_square
    """
    _raise_premium("get_rms_volume")
    return _RmsVolumeResult(0.0, 0.0, 0.0)


_RmsVolumeResult = namedtuple('RmsVolumeResult', 'time duration_secs amplitude')


class VolumeChangeDirection(IntEnum):
    LOUDER = 1
    QUIETER = -1

    # For nicer formatting of `wait_for_volume_change` signature in generated
    # API documentation:
    def __repr__(self):
        return str(self)


class VolumeChangeTimeout(AssertionError):
    pass


def wait_for_volume_change(
        direction=VolumeChangeDirection.LOUDER, stream=None,
        window_size_secs=0., threshold_db=0., noise_floor=0.0, timeout_secs=0.):

    """Wait for changes in the RMS audio volume.

    This can be used to listen for the start of content, or for bleeps and
    bloops when navigating the UI. It returns after the first significant
    volume change. This function tries hard to give accurate timestamps for
    when the volume changed. It works best for sudden changes like a beep.

    This function detects changes in volume using a rolling window. The RMS
    volume is calculated over a rolling window of size ``window_size_secs``.
    For every sample this function compares the RMS volume in the window
    preceeding the sample, to the RMS volume in the window following the
    sample. The ratio of the two volumes determines whether the volume change
    is significant or not.

    Example: Measure the latency of the mute button::

        keypress = stbt.press('KEY_MUTE')
        quiet = wait_for_volume_change(
            direction=VolumeChangeDirection.QUIETER,
            stream=audio_chunks(time_index=keypress.start_time))
        print "MUTE latency: %0.3f s" % (quiet.time - keypress.start_time)

    Example: Measure A/V sync between "beep.png" being displayed and a beep
    being heard::

        video = wait_for_match("beep.png")
        audio = wait_for_volume_change(
            stream=audio_chunks(time_index=video.time - 0.5),
            window_size_secs=0.01)
        print "a/v sync: %i ms" % (video.time - audio.time) * 1000

    :type direction: VolumeChangeDirection
    :param direction: Whether we should wait for the volume to increase or
        decrease. Defaults to ``VolumeChangeDirection.LOUDER``.

    :type stream: Iterator returned by `audio_chunks`
    :param stream: Audio stream to listen to. Defaults to `audio_chunks()`.
        Postcondition: the stream will be positioned at the time of the volume
        change.

    :type window_size_secs: int
    :param window_size_secs: The time over which the RMS volume should be
        averaged. Defaults to 0.4 (400ms) in accordance with momentary loudness
        from the EBU TECH 3341 specification. Decrease this if you want to
        detect bleeps shorter than 400ms duration.

    :type threshold_db: float
    :param threshold_db: This controls sensitivity to volume changes. A volume
        change is considered significant if the ratio between the volume before
        and the volume afterwards is greater than ``threshold_db``. With
        ``threshold_db=10`` (the default) and
        ``direction=VolumeChangeDirection.LOUDER`` the RMS volume must increase
        by 10 dB (a factor of 3.16 in amplitude). With
        ``direction=VolumeChangeDirection.QUIETER`` the RMS volume must fall by
        10 dB.

    :type noise_floor_amplitude: float
    :param noise_floor_amplitude: This is used to avoid `ZeroDivisionError`
        exceptions.  The change from an amplitude of 0 to 0.1 is ∞ dB.
        This isn't very practical to deal with so we consider 0 amplitude to be
        this non-zero ``noise_floor_amplitude`` instead. It defaults to ~0.0003
        (-70dBov). Increase this value if there is some sort of background
        noise that you want to ignore.

    :type timeout_secs: float
    :param timeout_secs: Timeout in seconds. If no significant volume change is
        found within this time, `VolumeChangeTimeout` will be raised and your
        test will fail.

    :raises VolumeChangeTimeout: If no volume change is detected before
        ``timeout_secs``.

    :returns:
        An object with the following attributes:

        * **direction** (`VolumeChangeDirection`) – This will be either
          ``VolumeChangeDirection.LOUDER`` or ``VolumeChangeDirection.QUIETER``
          as given to ``wait_for_volume_change``.
        * **rms_before** (see `get_rms_volume`) – The RMS volume averaged over
          the window immediately before the volume change. Use
          ``result.rms_before.amplitude`` to get the RMS amplitude as a float.
        * **rms_after** (see `get_rms_volume`) – The RMS volume averaged over
          the window immediately after the volume change.
        * **difference_db** (*float*) – Ratio between ``rms_after`` and
          ``rms_before``, in decibels.
        * **difference_amplitude** (*float*) – Absolute difference between the
          ``rms_after`` and ``rms_before``. This is a number in the range -1.0
          to +1.0.
        * **time** (*float*) – The time of the volume change, as number of
          seconds since the unix epoch (1970-01-01T00:00:00Z). This is the same
          format used by the Python standard library function ``time.time()``
          and ``stbt.Frame.time``.
        * **window_size_secs** (*float*) – The size of the window over which
          the volume was averaged, in seconds.
    """
    _raise_premium("wait_for_volume_change")
    return _VolumeChangeResult(VolumeChangeDirection.LOUDER,
                               _RmsVolumeResult(0.0, 0.0, 0.0),
                               _RmsVolumeResult(0.0, 0.0, 0.0),
                               0.0, 0.0, 0.0, 0.)


_VolumeChangeResult = namedtuple(
    '_VolumeChangeResult',
    "direction rms_before rms_after difference_db difference_amplitude time "
    "window_size_secs")


def play_audio_file(filename):
    """Play an audio file through the Stb-tester Node's "audio out" jack.

    Useful for testing integration of your device with Alexa or Google Home.

    :param str filename:
      The audio file to play (for example a WAV or MP3 file committed to
      your test-pack).

      Filenames should be relative paths. This uses the same path lookup
      algorithm as `stbt.load_image`.
    """
    _raise_premium("play_audio_file")
    return None


_AVSyncResult = namedtuple(
    "_AVSyncResult",
    "offset type time duration_secs rate drift drift_p_value samples "
    "undetectable acceptable")


def measure_av_sync(duration_secs=60, start_timeout_secs=10,
                    frames=None, audiostream=None):

    """
    Measures the offset between audio and video.

    This function requires a reference video to be played on the device under
    test.  The caller is responsible for playing this video.  This function will
    wait until a known A/V sync video is playing and then measure the A/V
    offset.  Typically an A/V sync test will look like this::

        play_av_sync_video()
        result = stbt.measure_av_sync()
        assert result.acceptable

    Where ``play_av_sync_video`` is a function implemented by you, specific to
    your device-under-test.

    ``measure_av_sync`` supports the following reference videos:

    * `Apple HTTP Live Streaming Examples <https://developer.apple.com/streaming/examples/>`__
        * `AppleBipBop16x9 <https://developer.apple.com/streaming/examples/basic-stream-osx-ios5.html>`__
        * `AppleBipBop4x3 <https://developer.apple.com/streaming/examples/basic-stream-osx-ios4-3.html>`__
        * `AppleBipBopAdvanced <https://developer.apple.com/streaming/examples/advanced-stream-fmp4.html>`__
    * Contact us for support for other reference videos.

    :type duration_secs: float
    :param duration_secs: Duration over which A/V sync measurements should be
        taken.  It is not an error if the video ends before `duration_secs`
        worth of samples has been collected.  In this case `measure_av_sync`
        will return with the samples it collected before the video ended.  You
        can check `result.duration_secs` to detect this situation.

    :type start_timeout_secs: float
    :param start_timeout_secs: Number of seconds to wait for the A/V sync
        video to start.  If a known video is not detected within this period
        this function will raise `stbt.BadSyncPattern`.

    :raises BadSyncPattern: Raised if we didn't recognise a playing A/V sync
        video within ``start_timeout_secs`` or if the detected video is paused.

    :rtype: AVSyncResult
    :return: Statistics regarding A/V sync.  See `AVSyncResult` for more
        details.
    """

    _raise_premium("measure_av_sync")

    return _AVSyncResult(
        0.0, "", 0.0, 0.0, 0.0, 0.0, 0.0,
        numpy.array([], dtype=[
            ('video_time', 'f8'),
            ('audio_time', 'f8'),
            ('video_rate', 'f4')]),
        False, False)


class BadSyncPattern(RuntimeError):
    pass


class FindSelectionFromBackgroundResult(object):
    def __init__(self, matched, region, mask_region, image, frame):
        self.matched = matched
        self.region = region
        self.mask_region = mask_region
        self.image = image
        self.frame = frame

    def __bool__(self):
        return self.matched

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        return (
            "FindSelectionFromBackgroundResult(matched=%r, region=%r, "
            "mask_region=%r, image=%s, frame=%s)" % (
                self.matched,
                self.region,
                self.mask_region,
                _frame_repr(self.image),
                _frame_repr(self.frame)))


def find_selection_from_background(
        image, max_size, min_size=None, frame=None, mask=Region.ALL,
        threshold=25, erode=True):

    """Checks whether ``frame`` matches ``image``, calculating the region
    where there are any differences. The region where ``frame`` doesn't match
    the image is assumed to be the selection. This allows us to simultaneously
    detect the presence of a screen (used to implement a `stbt.FrameObject`
    class's ``is_visible`` property) as well as finding the selection.

    For example, to find the selection of an on-screen keyboard, ``image``
    would be a screenshot of the keyboard without any selection. You may need
    to construct this screenshot artificially in an image editor by merging two
    different screenshots.

    Unlike `stbt.match`, ``image`` must be the same size as ``frame``.

    :type image: str or `numpy.ndarray`
    :param image:
      The background to match against. It can be the filename of a PNG file on
      disk, or a numpy array containing the pixel data in 8-bit BGR format.
      If it has an alpha channel, any transparent pixels are masked out (that
      is, the alpha channel is ANDed with ``mask``). This image must be the
      same size as ``frame``.

    :type max_size: tuple of 2 ints ``(width, height)``
    :param max_size:
      The maximum size of the differing region. If the differences between
      ``image`` and ``frame`` are larger than this in either dimension, the
      function will return a falsey result.

    :type min_size: tuple of 2 ints ``(width, height)``
    :param min_size:
      The minimum size of the differing region (optional). If the differences
      between ``image`` and ``frame`` are smaller than this in either
      dimension, the function will return a falsey result.

    :type frame: `stbt.Frame` or `numpy.ndarray`
    :param frame:
      If this is specified it is used as the video frame to search in;
      otherwise a new frame is grabbed from the device-under-test. This is an
      image in OpenCV format (for example as returned by `stbt.frames` and
      `stbt.get_frame`).

    :type mask: `stbt.Region` or `numpy.ndarray`
    :param mask:
      Specifies an area within the image to check. If it's a numpy array
      (image) it should be a single-channel black-and-white image where black
      pixels are masked out (ignored).

    :type threshold: int
    :param threshold:
      Threshold for differences between ``image`` and ``frame`` for it to be
      considered a difference. This is a colour distance between pixels in
      ``image`` and ``frame``. 0 means the colours have to match exactly. 255
      would mean that even white (255, 255, 255) would match black (0, 0, 0).

    :param bool erode:
      By default we pass the thresholded differences through an erosion
      algorithm to remove noise or small anti-aliasing differences. If your
      selection is a single line less than 3 pixels wide, set this to False.

    :returns:
      An object that will evaluate to true if ``image`` and ``frame`` matched
      with a difference smaller than ``max_size``. The object has the following
      attributes:

      * **matched** (*bool*) – True if the image and the frame matched with a
        difference smaller than ``max_size``.
      * **region** (`stbt.Region`) – The bounding box that contains the
        selection (that is, the differences between ``image`` and ``frame``).
      * **mask_region** (`stbt.Region`) – The region of the frame that was
        analysed, as given in the function's ``mask`` parameter.
      * **image** (`stbt.Image`) – The reference image given to
        ``find_selection_from_background``.
      * **frame** (`stbt.Frame`) – The video-frame that was analysed.

    Added in v32.
    """
    _raise_premium("find_selection_from_background")
    return FindSelectionFromBackgroundResult(True, Region.ALL, mask, image,
                                             frame)


def detect_pages(frame=None, candidates=None, test_pack_root=""):
    """Find Page Objects that match the given frame.

    This function tries each of the Page Objects defined in your test-pack
    (that is, subclasses of `stbt.FrameObject`) and returns an instance of
    each Page Object that is visible (according to the object's ``is_visible``
    property).

    This is a Python `generator`_ that yields 1 Page Object at a time. If your
    code only consumes the first object (like in the example below),
    ``detect_pages`` will try each Page Object class until it finds a match,
    yield it to your code, and then it won't waste time trying other Page
    Object classes::

        page = next(stbt.detect_pages())

    To get all the matching pages you can iterate like this::

        for page in stbt.detect_pages():
            print(type(page))

    Or create a list like this::

        pages = list(stbt.detect_pages())

    :param stbt.Frame frame:
        The video frame to process; if not specified, a new frame is grabbed
        from the device-under-test by calling `stbt.get_frame`.

    :param Sequence[Type[stbt.FrameObject]] candidates:
        The Page Object classes to try. Note that this is a list of the classes
        themselves, not instances of those classes. If ``candidates`` isn't
        specified, ``detect_pages`` will use static analysis to find all of the
        Page Objects defined in your test-pack.

    :param str test_pack_root:
        A subdirectory of your test-pack to search for Page Object definitions,
        used when ``candidates`` isn't specified. Defaults to the entire
        test-pack.

    :rtype: Iterator[stbt.FrameObject]
    :returns:
        An iterator of Page Object instances that match the given ``frame``.

    Added in v32.

    .. _generator: https://docs.python.org/3.6/tutorial/classes.html#generators
    """
    _raise_premium("detect_pages")
    return iter([FrameObject()])


def stop_job(reason=None):
    # type: (str) -> None

    """Stop this job after the current testcase exits.

    If you are running a job with multiple testcases, or a
    :ref:`soak-test <soak-testing>`, the job will stop when the current
    testcase exits. Any remaining testcases (that you specified when you
    started the job) will not be run.

    :param str reason: Optional message that will be logged.

    Added in Stb-tester v31.
    """
    _raise_premium("stop_job")
