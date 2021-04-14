def test_get_pixels():
    import pydicom
    import numpy as np
    from barbell2light.dicom import get_pixels
    p = pydicom.read_file('/Users/Ralph/Desktop/image.dcm')
    pixels = get_pixels(p, normalize=[0, 200])
    print('[{}, {}]'.format(np.min(pixels), np.max(pixels)))
