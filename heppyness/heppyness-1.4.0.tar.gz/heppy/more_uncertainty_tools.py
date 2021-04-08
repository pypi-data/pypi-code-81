def copy_relative_uncertainties(this, reference):
	pass



def add_flat_relative_uncertainty(this):
	'''
	(Useful for luminosity uncertainty, or roughly estimated theoretical uncertainties of MC backgrounds)
	'''
	pass



def take_difference_as_uncertainty(this, reference, name='', symmetrise=False):
	'''
	Add the nominal difference between two histograms as an uncertainty

	* if name not given, will be automatically set based on histogram names
	'''
	pass