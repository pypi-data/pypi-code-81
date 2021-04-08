import numpy as np
import root_numpy as rnp
import ROOT

def main():
	'''
	Generate ROOT file as input for tests.
	'''
	# root_histogram_1d = ROOT.TH1F('root_histogram_1d_name', 'root_histogram_1d_title', 4, -1.0, 1.0)
	f = ROOT.TFile('example.root', 'recreate');
	hist2d = ROOT.TH2F('root_histogram_2d_name', 'root_histogram_2d_title', 4, -1.0, 1.0, 2, -1.0, 1.0)
	# The zero padding is for the under-/overflows
	areas = np.transpose(np.array([
		[0., 0., 0., 0., 0., 0.],
		[0., 1., 2., 3., 4., 0.],
		[0., 5., 6., 7., 8., 0.],
		[0., 0., 0., 0., 0., 0.],
		]))
	area_errors = np.transpose(np.array([
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.0, 0.4, 0.3, 0.2, 0.1, 0.0],
		[0.0, 0.8, 0.7, 0.6, 0.5, 0.0],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		]))
	rnp.array2hist(areas, hist2d, errors=area_errors)
	hist2d.Write('root_histogram_2d_name');
	f.Close()



if __name__ == '__main__':
	main()
