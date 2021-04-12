"""Loading and plotting

This example illustrates the simple usage of the
:class:`flimage.FLImage <flimage.core.FLImage>` class for reading and
managing quantitative phase data. The attribute ``FLImage.fluorescence``
yields the image data.

The image shows a young retina cell. The original dataset, available on
`figshare <https://doi.org/10.6084/m9.figshare.8055407.v1>`_
(*retina-young_sinogram_fli.h5*) :cite:`Schuermann2017`, can be opened in
the same manner using the
:class:`flimage.FLSeries <flimage.series.FLSeries>` class.
"""
import matplotlib.pylab as plt
import flimage

# load the experimental data
fli = flimage.FLImage(h5file="./data/retina_p10.h5", h5mode="r")

# plot
plt.figure(figsize=(4, 3))

plt.subplot(title="fluorescence image of a mouse retina cell")
plt.imshow(fli.fl, cmap="YlGnBu_r")

plt.tight_layout()
plt.show()
