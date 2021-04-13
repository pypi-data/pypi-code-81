# -*- coding: utf-8 -*-
"""
Examples for the nanoscope analysis utilities.

Use the run_example function to get an insight on how to use the
package.
"""

import matplotlib.pyplot as plt
import nanoscope
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from os.path import dirname, realpath, join
from nanoscope import files
from nanoscope.constants import FORCE, METRIC, VOLTS, PLT_kwargs
from nanoscope.tools import script_tools as st


DIR = dirname(realpath(nanoscope.__file__))
EXAMPLES_FILE_PATH = join(DIR, "Example Nanoscope Files")
TIPBIAS_FIXED = join(EXAMPLES_FILE_PATH, "ScriptTipBiasFixed.spm")
TIPBIAS_SWEEP = join(EXAMPLES_FILE_PATH, "ScriptTipBiasSweep.spm")


def run_pfm_example(n):
    """Provide examples of how to use the Python Module (Nanoscope)
    to retrieve, display and process data from Nanoscope Data Files.

    Run: run_pfm_example(n)

        n   Filetype            Description
        --  --------            -----------
        1  PFM Script File     Display script file information for PFM script
                Parameters      with sweep modulation
        2  PFM Script File     Display script file information for PFM script
                Parameters      with fixed frequency modulation
    """

    plt.close("all")

    if n == 1:
        tip_bias_plot(TIPBIAS_FIXED)
        get_pfm_script_parms_example(TIPBIAS_FIXED)
    elif n == 2:
        tip_bias_plot(TIPBIAS_SWEEP)
        get_pfm_script_parms_example(TIPBIAS_SWEEP)
    else:
        raise IndexError("No example for index {}.".format(n))


def get_pfm_script_parms_example(scriptpath):
    """ Generates a table of parameters relevant for a PFM script
    """
    with files.ScriptFile(scriptpath) as file_:
        print("")
        print(" N Description            Type  Size   Duration   "
              "Tip Bias  Ramp  Type      Ramp Size Ramp Start Amplitude"
              "Frequency")
        print("-- ---------------------- ----- -----  ---------- "
              "--------  --------------- --------- ---------- --------- "
              "--------- ")
        segs_info = file_.segments_info
        for i, info in enumerate(segs_info):
            general = "{:>2}  {:>21}  {:>4}  {:>4}".format(
                i, info.description, info.type, info.size)
            duration = "{:>8.4f} {:<2}".format(info.duration,
                                               info.duration_units)

            tip_bias_blanked, tip_bias_units_blanked = st.blank_unitless(
                info.tip_bias, info.tip_bias_units)
            tip_bias = u"{:>4} {:<2}".format(
                tip_bias_blanked, tip_bias_units_blanked)

            ramp_type = u"{:>13}".format(info.ramp_type)

            ramp_size_blanked, ramp_size_units_blanked = st.blank_unitless(
                info.ramp_size, info.ramp_size_units)
            ramp_size = u"{:>6} {:>2}".format(
                ramp_size_blanked, ramp_size_units_blanked)

            ramp_start_blanked, ramp_start_units_blanked = st.blank_unitless(
                info.ramp_start, info.ramp_start_units)
            ramp_start = u"{:>5} {:>2}".format(
                ramp_start_blanked, ramp_start_units_blanked)

            amp_blanked, amp_units_blanked = st.blank_unitless(
                info.amplitude, info.amplitude_units)
            if amp_units_blanked == "":
                amplitude = u"{:>5}".format(amp_blanked)
                amplitude += u"{:>2}".format(amp_units_blanked)
            else:
                amplitude = u"{:>5}".format(amp_blanked)
                amplitude += u"{:>2}".format(amp_units_blanked.decode('utf8'))

            freq_blanked, freq_units_blanked = st.blank_unitless(
                info.frequency, info.frequency_units)
            if freq_units_blanked == "":
                frequency = u"{:>2}".format(freq_blanked)
                frequency += u"{:>4}".format(freq_units_blanked)
            else:
                frequency = u"{:>2}".format(freq_blanked)
                frequency += u"{:>4}".format(freq_units_blanked.decode('utf8'))

            print("  ".join((general, duration, tip_bias, ramp_type,
                             ramp_size, ramp_start, amplitude, frequency)))


def tip_bias_plot(scriptpath):
    with files.ScriptFile(scriptpath) as file_:
        segs_info = file_.segments_info
        num_segs = file_.segments_count

        for i, info in enumerate(segs_info):

            # if hold force with bias segment, plot tip bias
            if info.type == 11:
                plt.hlines(info.tip_bias, i, i+1, color="C0")

            # vertical dashed lines showing segment start/end
            plt.axvline(i, linestyle='--', color='grey')
        ax = plt.gca()

        ax.set_title("Script Tip Bias")
        ax.set_ylabel("Tip Bias (V)")
        ax.set_xlabel("Segment Number")

        plt.xticks(range(1, num_segs-1))
        plt.show()


if __name__ == "__main__":
    for i in range(1, 3):
        print("")
        print(i)
        run_pfm_example(i)
