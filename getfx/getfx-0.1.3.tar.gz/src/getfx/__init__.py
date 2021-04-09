"""

GetFX package
=============

Provides handling of FX rates using extrnal FX API.

It submits request to external FX API, parse the response and prints it in
predefined manner. Each specific FX API provider requires new module based on
:py:mod:`getfx` (e.g. :py:mod:`getfx.getfxnbp` iplements `NBP FX API
<http://api.nbp.pl/en.html>`_).

Modules:

- :py:mod:`getfx.getfx` - base functionality to be extended by specific API
- :py:mod:`getfx.getfxnbp` - specific NBP API implementation
- :py:mod:`getfx.cmdparser` - parsing commandline interface

"""

__version__ = "0.1.3"
