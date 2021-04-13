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


DIR = dirname(realpath(nanoscope.__file__))
EXAMPLES_FILE_PATH = join(DIR, "Example Nanoscope Files")
FORCE_FN = join(EXAMPLES_FILE_PATH, "Force.spm")
FORCE_HOLD_FN = join(EXAMPLES_FILE_PATH, "ForceHold.spm")
FORCE_HOLD_SWEEP_FN = join(EXAMPLES_FILE_PATH, "ForceHoldSweep.spm")
FV_FN = join(EXAMPLES_FILE_PATH, "FV.spm")
FV_HOLD_FN = join(EXAMPLES_FILE_PATH, "FVHold.spm")
PEAKFORCE_FN = join(EXAMPLES_FILE_PATH, "PeakForce.pfc")
HSDC_FN = join(EXAMPLES_FILE_PATH, "HSDC.hsdc")
IMAGE_FN = join(EXAMPLES_FILE_PATH, "Image.spm")
SCRIPT_FN = join(EXAMPLES_FILE_PATH, "Script.spm")
SCRIPT_MODULATION_FN = join(EXAMPLES_FILE_PATH, "ScriptModulation.spm")
NANODRIVE_FLT_FN = join(EXAMPLES_FILE_PATH, "NanoDrive.flt")
SECM_APPROACH_FN = join(EXAMPLES_FILE_PATH, "SECMApproach.spm")
TIPBIAS_FIXED = join(EXAMPLES_FILE_PATH, "ScriptTipBiasFixed.spm")
TIPBIAS_SWEEP = join(EXAMPLES_FILE_PATH, "ScriptTipBiasSweep.spm")


def run_example(n):
    """Provide examples of how to use the Python Module (Nanoscope)
    to retrieve, display and process data from Nanoscope Data Files.

    Run: run_example(n)

        n   Filetype            Description
        --  --------            -----------
         1  Force File          Display force curves - time, z, and
                                    separation
         2  Force Hold Data     Display Force curve and Hold data
         3  Force Volume File   Display FV image and curves - time and
                                    separation
         4  Force Volume File   Display defl and height sensor vs time,
                                    and Force curves for separation
                                    on/off using height and height
                                    sensor
         5  Force Volume        Display FV Image, Hold curves (multiple
                Hold Data           channels), and Force curves using
                                    height and height sensor
         6  PeakForce Capture   Display PF image and curves - time and
                                    separation
         7  PeakForce Capture   Compute Modulus from every 100th curve
         8  HSDC (High Speed    Display HSDC Data vs. time - multiple
                Data Capture)       channels
         9  SPM Image           Display SPM Image, multiple channels
        10  Script File         Display all segments, multiple channels
                Example
        11  Script File         Display single segment, multiple
                Example             channels
        12  NanoDrive           Display a NanoDrive image
        13  SECM Approach File  Display SECM approach curve, mutliple
                                    channels
        14  General File        Display general file information
                Parameters
        15  Script File         Display script file information
                Parameters
    """

    plt.close("all")

    if n == 1:
        force_file_example()
    elif n == 2:
        force_hold_example()
    elif n == 3:
        force_volume_example_1()
    elif n == 4:
        force_volume_example_2()
    elif n == 5:
        force_volume_hold_example()
    elif n == 6:
        peakforce_capture_example_1()
    elif n == 7:
        peakforce_capture_example_2()
    elif n == 8:
        hsdc_example()
    elif n == 9:
        image_example()
    elif n == 10:
        script_example(True)
    elif n == 11:
        script_example(False)
    elif n == 12:
        nano_drive_example()
    elif n == 13:
        secm_approach_example()
    elif n == 14:
        get_general_parms_example()
    elif n == 15:
        get_script_parms_example()
    else:
        raise IndexError("No example for index {}.".format(n))


def force_file_example():
    print("Force File Example")
    # Select channel 1
    i_chan = 1

    # Open a force curve file
    with files.CurveFile(FORCE_FN) as file_:
        channel = file_[i_chan]
        # Display timed data of channel
        data, ax_properties = channel.create_force_time_plot(VOLTS)
        plt.plot(data.x, data.y)
        plt.gca().set(**ax_properties)
        plt.show()

        # Display F vs. Z plot of channel
        fz_plot, ax_properties = channel.create_force_z_plot(FORCE)
        plt.plot(fz_plot.trace.x, fz_plot.trace.y)
        plt.plot(fz_plot.retrace.x, fz_plot.retrace.y)
        plt.gca().set(**ax_properties)
        plt.show()

        # Display force separation curves
        fs_plot = channel.compute_separation(fz_plot, FORCE)
        plt.plot(fs_plot.trace.x, fs_plot.trace.y)
        plt.plot(fs_plot.retrace.x, fs_plot.retrace.y)

        # Display the contact region
        x_retrace = fs_plot.retrace.x
        y_retrace = fs_plot.retrace.y
        contact_point_index = find_contact_point(x_retrace, y_retrace)
        region_bottom, region_top = compute_contact_region_bounds(
            x_retrace, y_retrace, contact_point_index, 10, 90)
        ax_properties["title"] = "Force vs. Separation"
        plt.hlines((region_bottom, region_top), x_retrace[0], x_retrace[-1],
                   colors='m')

        plt.gca().set(**ax_properties)
        plt.show()

        # Calculate some values and display in command window
        [index_1, index_2] = compute_markers(x_retrace, y_retrace, region_top,
                                             region_bottom)
        k = exponential_fit(x_retrace, y_retrace, index_1, index_2,
                            contact_point_index)
        pr = file_.poisson_ratio
        tr = file_.tip_radius
        e = get_youngs_modulus(k, pr, tr)
        print("PR = {}".format(pr))
        print("TR = {} nm".format(tr))
        print("E = {} Pa".format(e))


def force_hold_example():
    print("Force Hold Example")
    # Select channel 0
    i_chan = 0

    # Open  a force curve file which contains a hold segment
    with files.HoldCurveFile(FORCE_HOLD_FN) as file_:
        channel = file_[i_chan]
        # Display timed data of channel
        ft_plot, ax_properties = channel.create_force_time_plot(METRIC)
        plt.plot(ft_plot.x, ft_plot.y)
        plt.gca().set(**ax_properties)
        plt.show()

        hold_plot, ax_properties = channel.create_force_hold_time_plot(METRIC)
        plt.plot(hold_plot.x, hold_plot.y)
        plt.gca().set(**ax_properties)
        plt.show()


def force_volume_example_1():
    print("Force Volume Example 1")

    # Open a force volume file
    with files.ForceVolumeFile(FV_FN) as file_:
        # Display Force volume image
        image_channel = file_.image_channel
        fv_image, ax_properties = image_channel.create_image(METRIC)
        plt.imshow(fv_image, **PLT_kwargs)
        spl = image_channel.samples_per_line
        lines = image_channel.number_of_lines

        # Note: the following makes the axes bigger
        markersize = 10
        plt.plot(0, 0, 's', markersize=markersize,
                 markeredgecolor='b', markerfacecolor='b',
                 scalex=False, scaley=False)  # bottom left
        plt.plot(lines-1, 0, 's', markersize=markersize,
                 markeredgecolor='c', markerfacecolor='c',
                 scalex=False, scaley=False)  # bottom right
        plt.plot(lines-1, spl-1, 's', markersize=markersize,
                 markeredgecolor='g', markerfacecolor='g',
                 scalex=False, scaley=False)  # top right
        plt.gca().set(**ax_properties)
        plt.show()

        # Display force curve against time for 3 corner pixels
        fc_channel = file_.force_curves_channel
        fv_pixels = fc_channel.number_of_force_curves

        # bottom left curve
        ft_plot_bl, ax_prop = fc_channel.create_force_time_plot(0, METRIC)
        plt.plot(ft_plot_bl.x, ft_plot_bl.y, "b-")
        # bottom right curve
        ft_plot_br, _ = fc_channel.create_force_time_plot(spl-1, METRIC)
        plt.plot(ft_plot_br.x, ft_plot_br.y, "c-")
        # top right curve
        ft_plot_tr, _ = fc_channel.create_force_time_plot(fv_pixels-1,
                                                          METRIC)
        plt.plot(ft_plot_tr.x, ft_plot_tr.y, "g-")
        plt.gca().set(**ax_prop)
        plt.show()

        # Display Force curves against distance (separation) for 3 corner pixels
        # bottom left pixel
        fz_plot_bl, ax_prop = fc_channel.create_force_z_plot(0, FORCE)
        fs_plot_bl = fc_channel.compute_separation(fz_plot_bl, FORCE)
        plt.plot(fs_plot_bl.trace.x, fs_plot_bl.trace.y, 'b-')
        plt.plot(fs_plot_bl.retrace.x, fs_plot_bl.retrace.y, 'r-')

        # bottom right pixel
        fz_plot_br, _ = fc_channel.create_force_z_plot(spl-1, FORCE)
        fs_plot_br = fc_channel.compute_separation(fz_plot_br, FORCE)
        plt.plot(fs_plot_br.trace.x, fs_plot_br.trace.y, 'c-')
        plt.plot(fs_plot_br.retrace.x, fs_plot_br.retrace.y, 'm-')

        # top right pixel
        fz_plot_tr, _ = fc_channel.create_force_z_plot(fv_pixels-1, FORCE)
        fs_plot_tr = fc_channel.compute_separation(fz_plot_tr, FORCE)
        plt.plot(fs_plot_tr.trace.x, fs_plot_tr.trace.y, 'g-')
        plt.plot(fs_plot_tr.retrace.x, fs_plot_tr.retrace.y, 'y-')

        ax_prop["title"] = ax_prop["title"].replace("Z", "Separation")
        plt.gca().set(**ax_prop)
        plt.show()


def force_volume_example_2():
    print("Force Volume Example 2")

    # Open a force volume file
    with files.ForceVolumeFile(FV_HOLD_FN) as file_:
        # This file has height sensor data

        # Display Force volume image
        fv_image, ax_properties = file_.image_channel.create_image(METRIC)
        plt.imshow(fv_image, **PLT_kwargs)

        plt.plot(0, 0, 's', markersize=30,
                 markeredgecolor='b', markerfacecolor='b',
                 scalex=False, scaley=False)  # bottom left

        plt.gca().set(**ax_properties)
        plt.show()

        # Display Force and Height Sensor against time (different y axes)
        # bottom left pixel
        defl_chan = file_[1]
        h_sens_chan = file_[2]
        defl_data, delf_ax_prop = defl_chan.create_force_time_plot(0, METRIC)
        h_sens_data, hs_ax_prop = h_sens_chan.create_force_time_plot(0, METRIC)

        plt.plot(defl_data.x, defl_data.y, "b-")
        plt.ylabel(delf_ax_prop["ylabel"], color="b")
        plt.xlabel(delf_ax_prop["xlabel"])
        plt.gca().twinx()  # Make twin axis sharing same x
        plt.plot(h_sens_data.x, h_sens_data.y, "r-")
        plt.ylabel(hs_ax_prop["ylabel"], color="r")
        plt.title("Channel vs. Time")
        plt.show()

        # Display Force curves against distance/separation for height and
        # height sensor, for bottom left pixel.
        fc_channel = file_.force_curves_channel

        # Force vs. height
        fz_plot, ax_prop = fc_channel.create_force_z_plot(0, METRIC)
        plt.plot(fz_plot.trace.x, fz_plot.trace.y, 'b-')
        plt.plot(fz_plot.retrace.x, fz_plot.retrace.y, 'r-')
        plt.gca().set(**ax_prop)
        plt.title("Force vs. Height")
        plt.show()

        # Force vs. separation
        fs_plot = fc_channel.compute_separation(fz_plot, METRIC)
        plt.plot(fs_plot.trace.x, fs_plot.trace.y, 'b-')
        plt.plot(fs_plot.retrace.x, fs_plot.retrace.y, 'r-')
        plt.gca().set(**ax_prop)
        plt.title("Force vs. Separation")
        plt.show()

        # Get height sensor data, and use it for x
        h_sens_data = h_sens_chan.get_force_curve_data(0, METRIC)
        plt.plot(h_sens_data.trace, fz_plot.trace.y, 'b-')
        plt.plot(h_sens_data.retrace, fz_plot.retrace.y, 'r-')
        plt.gca().set(**ax_prop)
        plt.title("Force vs. Height Sensor")
        plt.show()

        # Forve vs. separation, overwrite x
        fs_hs_plot = fc_channel.compute_separation(fz_plot, METRIC,
                                                   h_sens_data=h_sens_data)
        plt.plot(fs_hs_plot.trace.x, fs_hs_plot.trace.y, 'b-')
        plt.plot(fs_hs_plot.retrace.x, fs_hs_plot.retrace.y, 'r-')
        plt.gca().set(**ax_prop)
        plt.title("Force vs. Height Sensor Separation")
        plt.show()


def force_volume_hold_example():
    print("Force Volume with Hold Example")

    # Open a force volume file which contains hold segments
    with files.ForceVolumeHoldFile(FV_HOLD_FN) as file_:
        # Display Force volume image
        image_channel = file_.image_channel
        fv_image, ax_properties = image_channel.create_image(METRIC)
        plt.imshow(fv_image, **PLT_kwargs)
        spl = image_channel.samples_per_line
        lines = image_channel.number_of_lines

        # Note: the following makes the axes bigger
        markersize = 20
        plt.plot(0, 0, 's', markersize=markersize,
                 markeredgecolor='b', markerfacecolor='b',
                 scalex=False, scaley=False)  # bottom left
        plt.plot(lines-1, 0, 's', markersize=markersize,
                 markeredgecolor='c', markerfacecolor='c',
                 scalex=False, scaley=False)  # bottom right
        plt.plot(lines-1, spl-1, 's', markersize=markersize,
                 markeredgecolor='g', markerfacecolor='g',
                 scalex=False, scaley=False)  # top right
        plt.gca().set(**ax_properties)
        plt.show()

        # Display hold data for first 2 channels
        for channel in file_.force_curves_channels[:2]:
            # get hold data (metric units) for 3 corner points
            plot, ax_prop = channel.create_force_hold_time_plot(0, METRIC)
            plt.plot(plot.x, plot.y, 'b-')

            plot, _ = channel.create_force_hold_time_plot(spl-1, METRIC)
            plt.plot(plot.x, plot.y, 'c-')

            fv_pixels = channel.number_of_force_curves
            plot, _ = channel.create_force_hold_time_plot(fv_pixels-1, METRIC)
            plt.plot(plot.x, plot.y, 'g-')

            plt.gca().set(**ax_prop)
            plt.show()

        # Display Force curves against distance (separation)
        channel = file_.force_curves_channels[0]
        h_sens_chan = file_.height_sensor_channel

        # bottom left pixel
        fz_plot_bl, ax_prop = channel.create_force_z_plot(0, FORCE)
        fs_plot_bl = channel.compute_separation(fz_plot_bl, FORCE)
        plt.plot(fs_plot_bl.trace.x, fs_plot_bl.trace.y, 'b-')
        plt.plot(fs_plot_bl.retrace.x, fs_plot_bl.retrace.y, 'r-')

        # bottom right pixel
        fz_plot_br, _ = channel.create_force_z_plot(spl-1, FORCE)
        fs_plot_br = channel.compute_separation(fz_plot_br, FORCE)
        plt.plot(fs_plot_br.trace.x, fs_plot_br.trace.y, 'c-')
        plt.plot(fs_plot_br.retrace.x, fs_plot_br.retrace.y, 'm-')

        # top right pixel
        fz_plot_tr, _ = channel.create_force_z_plot(fv_pixels-1, FORCE)
        fs_plot_tr = channel.compute_separation(fz_plot_tr, FORCE)
        plt.plot(fs_plot_tr.trace.x, fs_plot_tr.trace.y, 'g-')
        plt.plot(fs_plot_tr.retrace.x, fs_plot_tr.retrace.y, 'y-')

        ax_prop["title"] = ax_prop["title"].replace("Z", "Separation")
        ax_prop["xlabel"] = ax_prop["xlabel"].replace("Z", "Height")
        plt.gca().set(**ax_prop)
        plt.show()

        # Display Force curves against distance (separation), from height sensor
        # bottom left pixel
        h_sens_data_bl = h_sens_chan.get_force_curve_data(0, METRIC)
        fs_hs_plot_bl = channel.compute_separation(fz_plot_bl, FORCE,
                                                   h_sens_data=h_sens_data_bl)
        plt.plot(fs_hs_plot_bl.trace.x, fs_hs_plot_bl.trace.y, 'b-')
        plt.plot(fs_hs_plot_bl.retrace.x, fs_hs_plot_bl.retrace.y, 'r-')

        # bottom right pixel
        h_sens_data_br = h_sens_chan.get_force_curve_data(spl-1, METRIC)
        fs_hs_plot_br = channel.compute_separation(fz_plot_br, FORCE,
                                                   h_sens_data=h_sens_data_br)
        plt.plot(fs_hs_plot_br.trace.x, fs_hs_plot_br.trace.y, 'c-')
        plt.plot(fs_hs_plot_br.retrace.x, fs_hs_plot_br.retrace.y, 'm-')

        # top right pixel
        h_sens_data_tr = h_sens_chan.get_force_curve_data(fv_pixels-1, METRIC)
        fs_hs_plot_tr = channel.compute_separation(fz_plot_tr, FORCE,
                                                   h_sens_data=h_sens_data_tr)
        plt.plot(fs_hs_plot_tr.trace.x, fs_hs_plot_tr.trace.y, 'g-')
        plt.plot(fs_hs_plot_tr.retrace.x, fs_hs_plot_tr.retrace.y, 'y-')

        ax_prop["xlabel"] = ax_prop["xlabel"].replace("Height",
                                                      "Height Sensor")
        plt.gca().set(**ax_prop)
        plt.show()


def peakforce_capture_example_1():
    print("PeakForce Capture Example 1")

    # Open a peak force capture file
    with files.PeakforceCaptureFile(PEAKFORCE_FN) as file_:
        # Display Peakforce image
        image_channel = file_.image_channel
        pf_image, ax_properties = image_channel.create_image(METRIC)
        plt.imshow(pf_image, **PLT_kwargs)
        spl = image_channel.samples_per_line
        lines = image_channel.number_of_lines

        # Note: the following makes the axes bigger
        markersize = 3
        plt.plot(0, 0, 's', markersize=markersize,
                 markeredgecolor='b', markerfacecolor='b',
                 scalex=False, scaley=False)  # bottom left
        plt.plot(lines//2-1, spl//2-1, 's', markersize=markersize,
                 markeredgecolor='c', markerfacecolor='c',
                 scalex=False, scaley=False)  # center
        plt.plot(lines-1, spl-1, 's', markersize=markersize,
                 markeredgecolor='g', markerfacecolor='g',
                 scalex=False, scaley=False)  # top right
        plt.gca().set(**ax_properties)
        plt.show()

        # Display Force curves against time
        fc_channel = file_.force_curves_channel
        fv_pixels = fc_channel.number_of_force_curves

        # bottom left curve
        ft_plot_bl, ax_prop = fc_channel.create_force_time_plot(0, METRIC)
        plt.plot(ft_plot_bl.x, ft_plot_bl.y, "b-")
        # center curve
        ft_plot_br, _ = fc_channel.create_force_time_plot(fv_pixels//2-1,
                                                          METRIC)
        plt.plot(ft_plot_br.x, ft_plot_br.y, "c-")
        # top right curve
        ft_plot_tr, _ = fc_channel.create_force_time_plot(fv_pixels-1,
                                                          METRIC)
        plt.plot(ft_plot_tr.x, ft_plot_tr.y, "g-")
        plt.gca().set(**ax_prop)
        plt.show()

        # Force curves against distance (separation)
        # bottom left pixel
        fz_plot_bl, ax_prop = fc_channel.create_force_z_plot(0, FORCE)
        fs_plot_bl = fc_channel.compute_separation(fz_plot_bl, FORCE)
        plt.plot(fs_plot_bl.trace.x, fs_plot_bl.trace.y, 'b-')
        plt.plot(fs_plot_bl.retrace.x, fs_plot_bl.retrace.y, 'r-')

        # bottom right pixel
        fz_plot_br, _ = fc_channel.create_force_z_plot(fv_pixels//2-1,
                                                       FORCE)
        fs_plot_bl = fc_channel.compute_separation(fz_plot_br, FORCE)
        plt.plot(fs_plot_bl.trace.x, fs_plot_bl.trace.y, 'c-')
        plt.plot(fs_plot_bl.retrace.x, fs_plot_bl.retrace.y, 'm-')

        # top right pixel
        fz_plot_tr, _ = fc_channel.create_force_z_plot(fv_pixels-1, FORCE)
        fs_plot_tr = fc_channel.compute_separation(fz_plot_tr, FORCE)
        plt.plot(fs_plot_tr.trace.x, fs_plot_tr.trace.y, 'g-')
        plt.plot(fs_plot_tr.retrace.x, fs_plot_tr.retrace.y, 'y-')
        plt.gca().set(**ax_prop)
        plt.show()


def peakforce_capture_example_2():
    print("PeakForce Capture Example 2")

    # Open a peak force capture file
    with files.PeakforceCaptureFile(PEAKFORCE_FN) as file_:
        fc_channel = file_.force_curves_channel
        number_of_curves = fc_channel.number_of_force_curves
        pr = file_.poisson_ratio
        tr = file_.tip_radius

        for i in range(0, number_of_curves, 100):
            plot, ax_prop = fc_channel.create_force_z_plot(i, METRIC)
            sep_plot = fc_channel.compute_separation(plot, METRIC)

            x_retrace, y_retrace = sep_plot.retrace
            contact_point_index = find_contact_point(x_retrace, y_retrace)
            region_bottom, region_top = compute_contact_region_bounds(
                x_retrace, y_retrace, contact_point_index, 10, 70)
            index_1, index_2 = compute_markers(x_retrace, y_retrace,
                                               region_top, region_bottom)
            k = exponential_fit(x_retrace, y_retrace, index_1, index_2,
                                contact_point_index)
            modulus = get_youngs_modulus(k, pr, tr)
            print("Curve # {}: Modulus = {}".format(i, modulus))


def hsdc_example():
    print("High Speed Data Capture Example")

    # Open a High Speed Data Capture file)
    with files.HSDCFile(HSDC_FN) as file_:
        # cycle through the channels (max 3)
        for channel in file_[:3]:
            plot, ax_properties = channel.create_HSDC_time_plot(METRIC)
            fig = plt.figure()
            fig_size = fig.get_size_inches()
            # resize fig to cope with HS data
            fig.set_size_inches((fig_size[0]*2.5, fig_size[1]), forward=True)
            plt.plot(plot.x, plot.y)
            plt.gca().set(**ax_properties)
            plt.show()


def image_example():
    print("Image Example")

    # Open an image file
    with files.ImageFile(IMAGE_FN) as file_:
        n_chan = len(file_)
        for channel in file_:
            image, ax_properties = channel.create_image(METRIC)
            aspect_ratio = channel.aspect_ratio

            # compute planefit coefficients and display on command line
            a, b, c, fit_type_str = channel.planefit_settings
            print("Chan #{}:".format(channel.i_chan))
            print("\tAspect Ratio = {},".format(aspect_ratio))
            print("\tPlaneFit Coeffs = ({}, {}, {})".format(a, b, c))

            plt.subplot(1, n_chan, channel.i_chan+1)
            plt.imshow(image, **PLT_kwargs)
            plt.gca().set(**ax_properties)
        plt.show()


def script_example(all_segs):
    print("Ramp Script Example")

    # Open a ramp script file
    with files.ScriptFile(SCRIPT_FN) as file_:
        n_segs = file_.segments_count
        segs_info = file_.segments_info

        # if not all_segs, arbitrarily plot seg 6 (index 5) (or last if fewer)
        i_seg = None if all_segs else min(5, n_segs)

        # cycle through the channels (max 3)
        for channel in file_[:3]:
            data = channel.get_script_segment_data(i_seg, METRIC)
            plt.plot(data.x, data.y)
            type_desc = channel.data_type_desc
            scale_unit = channel.get_scale_unit(METRIC)

            if all_segs:
                # Plot segment dividers
                y_min, y_max = plt.ylim()
                x_pos = 0
                for i in range(0, n_segs-1):
                    x_pos += segs_info[i].size
                    plt.axvline(x=data.x[x_pos], ymin=y_min, ymax=y_max,
                                color="r")
                title = "Script {} - {} Segments".format(type_desc, n_segs)
            else:
                title = 'Script {}, segment #{}: {}'.format(
                    type_desc, i_seg, segs_info[i_seg].description)

            ax = plt.gca()
            ax.set_title(title)
            ax.set_ylabel(u"{} ({})".format(type_desc,
                                            scale_unit))
            ax.set_xlabel("Time (s)")
            plt.show()

        if all_segs:
            for i in range(n_segs):
                print("Seg #{}: {}".format(i, segs_info[i].description))


def nano_drive_example():
    # Open a nanodrive file
    with files.NanoDriveFile(NANODRIVE_FLT_FN) as file_:
        channel = file_[0]
        image = channel.get_image_data(METRIC)
        size = channel.scan_size
        size_units = channel.scan_size_unit
        scale_units = channel.get_scale_unit(METRIC)
        spl = channel.samples_per_line
        lines = channel.number_of_lines

        x, y = np.meshgrid(np.linspace(0, size, spl),
                           np.linspace(0, size, lines))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(x, y, image, cmap="copper", linewidth=0)
        ax.autoscale(tight=True)
        ax.set_title("NanoDrive")
        ax.set_xlabel(u"x ({})".format(size_units))
        ax.set_ylabel(u"y ({})".format(size_units))
        ax.set_zlabel(u"data ({})".format(scale_units))
        plt.show()


def secm_approach_example():
    # Open a secm file
    with files.CurveFile(SECM_APPROACH_FN) as file_:
        # Get channels
        itip_chan = file_[0]  # Itip
        defl_chan = file_[1]  # Deflection

        # Itip vs Z
        iz_plot, ax_prop = itip_chan.create_force_z_plot(VOLTS)
        plt.plot(iz_plot.trace.x, iz_plot.trace.y)
        plt.plot(iz_plot.retrace.x, iz_plot.retrace.y)
        plt.gca().set(**ax_prop)
        plt.show()

        # Defl. vs Z
        fz_plot, ax_prop = defl_chan.create_force_z_plot(VOLTS)
        plt.plot(fz_plot.trace.x, fz_plot.trace.y)
        plt.plot(fz_plot.retrace.x, fz_plot.retrace.y)
        plt.gca().set(**ax_prop)
        plt.show()

        # Itip vs time
        it_data, ax_prop = itip_chan.create_force_time_plot(VOLTS)
        plt.plot(it_data.x, it_data.y)
        plt.gca().set(**ax_prop)
        plt.show()

        # Defl vs time
        ft_data, ax_prop = defl_chan.create_force_time_plot(VOLTS)
        plt.plot(ft_data.x, ft_data.y)
        plt.gca().set(**ax_prop)
        plt.show()


def get_general_parms_example():
    def print_general_file_parms(file_):
        print("k: {} N/m".format(file_.spring_constant))
        print("Tip radius: {} nm".format(file_.tip_radius))
        print("Half angle: {} rad".format(file_.half_angle))
        print("Poisson ratio: {}".format(file_.poisson_ratio))
        print(u"ZSens units: {}".format(file_.z_sens_units))
        print("Deflection sensitivity: {} {}".format(
            file_.defl_sens, file_.defl_sens_units))
        lim, lim2 = file_.defl_limits
        lim_units, lim2_units = file_.defl_limits_units
        print(u"Deflection limit: {} {}".format(lim, lim_units))
        print(u"Deflection limit LockIn3LSADC1: {} {}".format(
            lim2, lim2_units))
        for number, channel in enumerate(file_):
            print("Channel #{}: {}".format(number, channel.data_type_desc))

    def print_curve_parms(curve_channel):
        for metric in (False, True):
            print("Ramp Size: {} {}".format(
                curve_channel.get_ramp_size(metric),
                curve_channel.get_ramp_size_unit(metric)))

    def print_sweep_file_info(sweep_file_):
        type_desc = sweep_file_.force_sweep_type_desc
        print("Sweep type: {}".format(type_desc))
        if type_desc.lower() != "off":
            min_freq, max_freq = sweep_file_.force_sweep_freq_range
            print("Frequency Range: {} - {} Hz".format(min_freq, max_freq))
        info = sweep_file_.modulation_info
        mod = "Modulation type: {}".format(info.type_desc)
        amp = u"Amplitude: {} {}".format(info.amplitude,
                                         info.amplitude_units)
        freq = u"Frequency: {} {}".format(info.frequency,
                                          info.frequency_units)
        print(" | ".join((mod, amp, freq)))

    with files.CurveFile(FORCE_FN) as file_:
        print("\nForce Curve")
        print_general_file_parms(file_)
        print_curve_parms(file_[0])

    with files.ForceVolumeHoldFile(FV_HOLD_FN) as file_:
        print("\nForce Volume Hold")
        print_general_file_parms(file_)
        print(u"Scan Size: {:.2f} {}".format(
            file_[0].scan_size, file_[0].scan_size_unit))
        print_sweep_file_info(file_)

    with files.HoldCurveFile(FORCE_HOLD_SWEEP_FN) as file_:
        print("\nForce Hold Sweep")
        print_general_file_parms(file_)
        print_curve_parms(file_[0])
        print_sweep_file_info(file_)

    with files.ScriptFile(SCRIPT_FN) as file_:
        print("\nScript File")
        print_general_file_parms(file_)


def get_script_parms_example():
    with files.ScriptFile(SCRIPT_MODULATION_FN) as file_:
        print("")
        print(" N            Description  Type  Size    Duration    Period"
              "  Amplitude  Frequency  Phase Offset")
        print(" -            -----------  ----  ----    --------    ------"
              "  ---------  ---------  ------------")
        segs_info = file_.segments_info
        for i, info in enumerate(segs_info):
            general = "{:>2}  {:>21}  {:>4}  {:>4}".format(
                i, info.description, info.type, info.size)
            duration = u"{:>8.4f} {:<2}".format(info.duration,
                                                info.duration_units)
            period = u"{:>4} {:<1}".format(int(info.period), info.period_units)
            if not info.is_modulation:
                print("  ".join((general, duration, period)))
                continue
            if info.amplitude > 100:
                ampl = int(info.amplitude)
            else:
                ampl = info.amplitude
            amplitude = u"{:>6} {:<2}".format(ampl, info.amplitude_units)
            frequency = u"{:>6} {:<2}".format(info.frequency,
                                              info.frequency_units)
            phase_offset = u"{:>7} {:<2}".format(info.phase_offset,
                                                 info.phase_offset_units)
            print("  ".join((general, duration, period, amplitude, frequency,
                             phase_offset)))


def get_youngs_modulus(k, poisson_ratio, tip_radius):
    """Return the Young modulus, E, in MPa, using Hertz sphere model

    Hertz model:
        k = 4/3 * E/(1 - PR^2) * R^(1/2)
    """
    return (1 - poisson_ratio**2) * .75 * k / tip_radius**.5


def exponential_fit(x, y, index_1, index_2, contact_point_index):
    """Return k"""
    k = 0.
    start_index, end_index = np.sort((index_1, index_2))

    # add the contact point & contact region
    fit_x = np.concatenate(([x[contact_point_index]],
                            x[start_index:end_index]))
    fit_y = np.concatenate(([y[contact_point_index]],
                            y[start_index:end_index]))

    # transfer the data so x=0 is the first data point
    x0 = fit_x[0]
    x1 = fit_x[-1]
    scale = abs(x1 - x0)/(x1 - x0)

    # not flipped
    if fit_y[0] <= fit_y[-1]:
        y_min = fit_y[0]
        fit_x = (fit_x - x0) * scale
    else:  # flipped
        y_min = fit_y[-1]
        fit_x = (x1 - fit_x) * scale
    # get y in pN
    fit_y = (fit_y - y_min) * 1000
    # first guess, K = mean(F(x)/x^E)
    n = 0
    for i in range(len(fit_x)):
        if fit_x[i] > 0 and fit_y[i] >= 0:
            k += fit_y[i] / fit_x[i] ** 1.5
            n += 1
    if n > 0:
        k /= n
    return k


def compute_markers(x, y, region_top, region_bottom):
    """Output: index_1, index_2"""
    # if the x is increasing
    if x[0] < x[-1]:
        # index_1 refers to the first point bellow region top
        index_1 = min(np.where((y <= region_top))[0])
        # index_2 refers to the point before the first bellow region_bottom
        index_2 = min(np.where((y <= region_bottom))[0]) - 1
    else:  # x decreasing
        # index_1 refers to the last point bellow region top
        index_1 = max(np.where((y <= region_top))[0])
        # index_2 refers to the point faster the last bellow region_bottom
        index_2 = max(np.where((y <= region_bottom))[0]) + 1

    return index_1, index_2


def compute_contact_region_bounds(x, y, contact_point_index, min_force_percent,
                                  max_force_percent):
    """Compute the contact region

    Output:
        region_bottom, region_top
    """
    curve_end_index = -1 if x[0] > x[-1] else 0
    max_region = y[curve_end_index]
    min_region = y[contact_point_index]
    region_bottom = (max_region - min_region) * min_force_percent / 100. + \
        min_region
    region_top = (max_region - min_region) * max_force_percent / 100. + \
        min_region

    return region_bottom, region_top


def find_contact_point(x, y):
    """Return the index of the contact point

    Input: x and y data

    Here, the contact point is defined as the point the furthest below
    the line connecting the first and the last points of the curve.
    """
    slope = (y[-1] - y[0]) / (x[-1] - x[0])
    return np.argmin(y - slope * x)


def copy_examples_code(destination=None):
    """Save the python file containing the examples.

    The file is copied to the given destination path.
    If no destination is given, a file dialog will request one.
    """
    nanoscope.tools.copy_py_file(__file__, destination)


if __name__ == "__main__":
    for i in range(1, 16):
        print("")
        print(i)
        run_example(i)
