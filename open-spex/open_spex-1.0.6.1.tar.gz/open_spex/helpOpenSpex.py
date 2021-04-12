HELPTEXT = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title></title>
<meta name="generator" content="HTML::TextToHTML v2.51"/>
</head>
<body>
<h1><a name="section_1">openSpex - a tool for radioxenon beta-gamma analysis</a></h1>
<p>Version 1.0.5- April 12, 2021
</p>
<h2><a name="section_1_1">General features</a></h2>

<p>openSpex is a basic analysis and display tool for radioxenon beta-gamma data on IMS-format (see IDC-ENG-SPC-103-Rev.7.3). 
The program can also be used to create, display, and analyse measurement- and measurement-set files, which contain data and analysis results for one or several beta-gamma radioxenon measurements. 
</p>
<p>The program is developed in Python3.7, and is available as open source under an MIT license (see the file LICENSE included in the distribuiton of this program, or in Help-&gt;About in the opneSpex menu). 
</p>
<p>Activity concentrations and related quantities are calculated based on the BGM (Beta-Gamma Matrix) method, which is described in 
</p>
<p>"A. Ringbom and A. Axelsson, A new method for analysis of beta-gamma radioxenon spectra, Appl. Rad. Isot., 156, Feb. 2020." <a href="https://doi.org/10.1016/j.apradiso.2019.108950">https://doi.org/10.1016/j.apradiso.2019.108950</a>
</p>
<p>Data stored as PHD-files on IMS -format is loaded either manually one file at the time, or by placing multiple files into two directories, one for sample- and gas background files, and one for the detector background files, respectively. Resulting measurements and analysis results, consisting of data obtained from two or more PHD-files, can be serialized and saved using the Python pickle (.pkl) format. This simplifies re-analysis of the measurements, as well as communication of samples and analysis results between different users. If multiple files are analyzed and saved in one go, pkl-files are sorted into a directory structure according to station code. This can be used as a basic database for raw- and analyzed data. 
</p>
<p>openSpex also offers some capability to analyze a measurement set, which is a collection of results from several measurements. In the same way as a measurement, a measurement set can be saved as a pkl-file. Selected data from a measurement set can also be saved in CVS-format, which can be opened in any spreadsheet tool.
</p>
<p>IMPORTANT NOTE: The pickle module is not secure. Only open pkl-files you trust.
</p>
<h2><a name="section_1_2">Installation</a></h2>

<p>Install the package using pip, preferably in a virtual environment:
</p>
<p>Create and activate a virtual environment:
</p>
<p>$ python3 -m venv venv<br/>
$ source venv/bin/activate (on Windows: $ call venv\Source\\activate)
</p>
<p>Install openSpex using pip:
</p>
<p>(venv) pip install open-spex
</p>
<p>Run openSpex by executing 
</p>
<p>venv/bin/openSpex  (Linux) <br/>
or  <br/>
venv/Scripts/openSpex (Windows) 
</p>
<h2><a name="section_1_3">Getting started</a></h2>

<ul>
  <li>Analysis on individual files:
</li></ul>
<p>        Open a sample, gas background (not mandatory), and a detector background file using File-&gt;Open-&gt;PHD in the menu. Loaded spectra can be inspected in the different tabs to the right. Different spectrum projections can be plotted together by ticking appropriate check-boxes. The sample tab contains check-boxes for projecting all loaded spectra (also from the Gasbk and Detbk tabs). The other tabs only show spectra belonging to that particular datatype.
</p>
<p>Set the BGM-analysis options in Options-&gt;BGM Analysis. Analyze by selecting Measurement-&gt;BGM Analysis. Detailed results are written to the log-window (left), and some results are also found in the upper part of the sample tab. The measurement can be saved for later use as a pkl-file in File-&gt;Save-&gt;Measurement.
</p>
<ul>
  <li>Analysis of multiple measurements in one go:
</li></ul>
<p>Copy all data files except the detector background files into one directory, and the detector background files into another. Set the selected data- and detbk paths in Options-&gt;General. 
If you want the individual measurements to be saved as pkl-files, also set 'Result path' and make sure that the "Save"-box is ticked. Select the analysis options in Options-&gt;BGM analysis, then Save and Close the Options window. Analyze by selecting Measurement Set-&gt;Calculate.
</p>
<p>The measurement set time series is displayed in the Plot tab to the very right. The Measurement set can be saved as a pkl- or csv-file (File-&gt;Save). If a data point in the time-series is left-clicked, and Option-&gt;General-&gt;Use markers was selected, the sample will be marked with a red circle, and some data printed to the log window. If, in addition, Option-&gt;General-&gt;Load marked has been ticked, and measurements were saved during the analysis ("save" was ticked in Options-&gt;General when the measurement set was created), the measurement is loaded into the other tabs. If an already marked sample is right-clicked, the sample is unmarked. The measurement set can be further analyzed and displayed using the other actions in the 'Measurement set' menu (see below).  
</p>
<h2><a name="section_1_4">Menu</a></h2>

<hr/>
File
<hr/>

<ul>
  <li>Open
  <ul>
    <li>Measurement (.pkl)
<p>                Load and displays a measurement pkl-file. Depending on what was stored, a measurement can contain all data for a sample, gas background, detector background and QC, as well as analysis results. 
</p>
    </li><li>Measurement set (.pkl)
<p>                Load and display a measurement set pkl-file.
        A measurement set contains data (analysis results and other sample information) for several measurements.
</p>
    </li><li>PHD
    <ul>
      <li>Sample, Gasbk, Detbk, QC, or Calib PHD
<p>                        Load a PHD file on IMS-format. If the data type is not according to the selected type, the file will not be loaded (can be ignored by selecting Options-&gt;General-&gt;Ignore PHD file type).
</p>
    </li></ul>
  </li></ul>
  </li><li>Save
  <ul>
    <li>Measurement (.pkl)
<p>                Save the currently loaded measurement to a pkl-file. 
</p>
    </li><li>Measurement set (.pkl)
<p>                Save the currently loaded measurement set to a pkl-file. 
</p>
    </li><li>Measurement report
<p>                Save the analysis report for the currently loaded measurement to a text file.
</p>
    </li><li>Measurement set report
<p>                Save the analysis report for the currently loaded measurement set to a text file.
  </p></ul>
  </li><li>Export
  <ul>
    <li>Measurement set (.csv)
<p>                Save selected data of the the currently loaded measurement set to a csv-file that can be opened as a spreadsheet.
</p>
    </li><li>PHD
    <ul>
      <li>Sample, Gasbk, Detbk, QC, or Calib
<p>                        Save a loaded sample as PHD-file on IMS-format.
    </p></ul>
  </li></ul>
  </li><li>Clear log
<p>        Clear the log window. 
</p>
  </li><li>Quit
<p>        Close the application.
</p>
</li></ul>
<hr/>
Measurement
<hr/>

<ul>
  <li>BGM analysis
<p>        Do a BGM analysis on the loaded measurement using the options selected in Options-&gt;BGM Analysis. An analysis report will be printed in the Log-tab. Activity concentrations will also be displayed in the upper part of the Sample tab.
</p>
  </li><li>Print PHD
  <ul>
    <li>Sample, Gasbk, Detbk, QC, or Calib
<p>                Print data on IMS-format in the log-window.
</p>
  </li></ul>
  </li><li>Clear 
<p>        Clear loaded measurement data.
</p>
</li></ul>
<hr/>
Measurement set
<hr/>

<ul>
  <li>Calculate
<p>        Calculate a measurement set by performing a BGM-analysis (according top the options set in Options-&gt;BGM Analysis) on all data stored in the data and detbk paths, as specified in Options-&gt;General. The measurement set is displayed in the Plot tab. If the separate measurements are to be saved (by ticking the "save" box in Options-&gt;General), measurements are saved individually to pkl-files. In addition, the phd-files included in the analysis can be automatically moved from the data directory to the result directory, by ticking the "move"-box in Options-&gt;General prior to the analysis. Only data files which resulted in a successful analysis will be moved. Analysis results and analyzed data are automatically stored according station code in the following directory structure, where "result" is the result path given in Options-&gt;General:
</p>
                
</li></ul>
<pre>
                /data           /station1
                                /station2
                                ...
        result/
                /results
                                /station1
                                /station2
                                ... 
</pre>
<ul>
  <li>Report
<p>        Print an analysis report on the currently loaded measurement set in the Log tab. The analysis report contains basic information on the data set, as well as some statistical analysis.
</p>
  </li><li>Time series
<p>        Plot a time series of the loaded measurement set. Plot options are set in Options-&gt;Measurement set plot.
</p>
  </li><li>Append 
<p>        Append a second measurement set to an already loaded set. The updated set is displayed as a time series in the Plot tab.
</p>
  </li><li>Frequency
<p>        Frequency distribution histograms of a selected quantity (one of activity concentration, activity concentration LC, MDC, activity, activity LC, or MDA selected in Options-&gt;Measurement set plot) are plotted in the Plot tab.
</p>
  </li><li>MIRC3 
<p>        Plot the loaded measurement set as a multi-3-isotope plot in the Plot tab. In addition, a discrimination line is displayed as a red line. The discriminating line is calculated according to: "Kalinowski, M.B., Axelsson, A., Bean, M. et al. Discrimination of Nuclear Explosions against Civilian Sources Based on Atmospheric Xenon Isotopic Activity Ratios. Pure Appl. Geophys. 167, 517-539 (2010). <a href="https://doi.org/10.1007/s00024-009-0032-1">https://doi.org/10.1007/s00024-009-0032-1</a>". Note that the ratio uncertainties in the MIRC-plots are calculated according to the "Fieller's theorem"; see "A. Ringbom and A. Axelsson, On the calculation of activity concentrations and nuclide ratios from measurements of atmospheric radioactivity, Appl. Rad. Isot., 156, Feb. 2020.", <a href="https://doi.org/10.1016/j.apradiso.2014.05.020">https://doi.org/10.1016/j.apradiso.2014.05.020</a> , and references therein. In cases where the uncertainty ellipse includes any of the ratio axes, Fieller's theorem yields infinite confidence intervals in positive, negative, or both directions. If that is the case, the uncertainties are set to zero in the plots.
</p>
  </li><li>MIRC4
<p>        Plot the loaded measurement set as a multi-4-isotope plot in the Plot tab. In addition, a discrimination line is plotted in red, as described for MIRC3. 
</p>
  </li><li>Plot parameter
  <ul>
    <li>Xe Volume, Xenon yield, Air Volume, Show errors.
<p>                A checkable menu for plotting a time series of one or more of the following quantities: Stable xenon volume, stable xenon yield, and sampled air volume.
</p>
  </li></ul>
  </li><li>Unmark all
<p>        All measurements in a measurement set that have been marked by right-clicking a data point (surrounded by red circles) are unmarked.
</p>
  </li><li>Clear
<p>        Delete the loaded measurement set.
</p>
</li></ul>
<hr/>
Options
<hr/>

<p>To save selected options, do Save followed by Close.    
</p>
<ul>
  <li>General
  <ul>
    <li>Ignore PHD datatype
<p>                If selected, ignore datatype when manually loading individual PHD-files (File-&gt;Open-&gt;PHD). If not selected, it will not be possible to load a file with data type not equal to the one selected in the menu.
</p>
    </li><li>Verbose
<p>                More information is printed to the log tab.
</p>
    </li><li>Use markers
<p>                Data points in a measurement set can be marked by right-clicking. When doing so, basic information on the measurement also will be printed to the log-window.
</p>
    </li><li>Load marked sample
<p>                A measurement selected by right-clicking will be loaded into the other tabs. Note that this only works if a measurement pkl-file belonging to the selected measurement is found in the directory where it was first created during a measurement set analysis.
</p>
    </li><li>Hide marked samples.
<p>                Marked samples are not shown in the time series or MIRC-plots.
</p>
    </li><li>1D Histogram scale
<p>                Select unit for the 1D-histograms shown in the measurement tabs.
</p>
    </li><li>Data path
<p>                Path for SAMPLEPHD and GASBKPHD -files used to create a measurement set. If "Move" is selected, files resulting in a successful analysis will be moved to the result directory. Only sample and gas background files are moved. Any detector background files are left untouched. 
</p>
    </li><li>Detbk path
<p>                Path for DETBK files used to create a measurement set. Can be the same as the data path above. 
</p>
    </li><li>Result path
<p>                Path used to store analysis results and moved data files. This only works if "Save" is selected. 
</p>
  </li></ul>
  </li><li>BGM Analysis
  <ul>
    <li>Use gas background 
<p>                The analysis is performed using gas background if it is found. If not, the analysis is done using detector background only. 
</p>
    </li><li>Method
    <ul>
      <li>Use ROI 7-10/ Original
<p>                        There are two main ways to run BGM. Either is it run using the original method as described in [1], where six ROIs are used. The Xe-133 activity is obtained by calculating ROI 3 and 4 separately, and then combine the results. As an alternative (the option 'Use ROI 7-10'), different parts of ROI4 (i.e. the four ROIs 7-10) are combined according to the detection pattern. If for example Xe-131m is detected, ROI 7 and 9, which excludes ROI5, are combined and used as "ROI 4". This modification is introduced in order to take care of samples which lack interference factors from ROI 5 and 6 into other ROIs. For samples with strong metastable activities, this can otherwise cause a slight overestimation of the Xe-133 activity. If these interference factors are included in the calibration, the original method should be used. 
</p>
    </li></ul>
    </li><li>Correct for Xe-133m ingrowth
<p>                Corrects for Xe-133m-&gt;Xe133 ingrowth if Xe-133m detected. 
</p>
    </li><li>Beta offset, Beta tweak, Gamma offset, Gamma tweak
<p>                Adjust the ROI limits using tweaking factors. The energy scales are adjusted according to new channel = &lt;offset&gt; + &lt;tweak&gt;*&lt;old channel&gt;. The calibration method is set to "Tweaked".
</p>
  </li></ul>
  </li><li>Measurement set plot
<p>        Settings that will affect the following Measurement set plots: 'timeseries', 'compare', and 'frequency'. For the 'timeseries', one or several of [AC,LC,MDC,A,LCA,MDA] can be selected; for the 'frequency' and 'compare' plots, one of [AC,LC,MDC,A,LCA,MDA] has to be selected. </p>
</li></ul>
</li></ul></li></ul>
</body>
</html>
"""
