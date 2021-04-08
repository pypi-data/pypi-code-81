

bands_c3_ls_common = {
    "nbart_blue": ["nbart_blue"],
    "nbart_green": ["nbart_green"],
    "nbart_red": ["nbart_red"],
    "nbart_nir": ["nbart_nir", "nbart_near_infrared"],
    "nbart_swir_1": ["nbart_swir_1", "nbart_shortwave_infrared_1"],
    "nbart_swir_2": ["nbart_swir_2", "nbart_shortwave_infrared_2"],
    "oa_nbart_contiguity": ["oa_nbart_contiguity", "nbart_contiguity"],
    "oa_fmask": ["oa_fmask", "fmask"],
}

bands_c3_ls_7 = bands_c3_ls_common.copy()
bands_c3_ls_7.update({
    "nbart_panchromatic": [],
})


bands_c3_ls_8 = bands_c3_ls_7.copy()
bands_c3_ls_8.update({
    "nbart_coastal_aerosol": ["coastal_aerosol",  "nbart_coastal_aerosol"],
})


