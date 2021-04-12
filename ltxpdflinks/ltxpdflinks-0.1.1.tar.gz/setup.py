# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ltxpdflinks']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'colorlog>=4.8.0,<5.0.0']

entry_points = \
{'console_scripts': ['ltxpdflinks = ltxpdflinks.__main__:main']}

setup_kwargs = {
    'name': 'ltxpdflinks',
    'version': '0.1.1',
    'description': 'Extract links in PDF graphics for inclusion in LaTeX documents',
    'long_description': 'ltxpdflinks — include PDF graphics with links in LaTeX documents  \n================================================================\n\nTo include fancy graphics (say a diagram) in your LaTeX document, a common\nprocess is to design the diagram using your favorite graphics designer program,\nto export the figure as a PDF graphic, and to use::\n\n  \\includegraphics[width=10cm]{my_figure}\n\nAnd it works great.  Until you\'d like to have figures with clickable links.  You\nmight even want to have links in your diagram to within the document—maybe a\nclickable link to a document section, equation, or an item in your bibliography.\n\nThe ``ltxpdflinks`` tool provides a simple solution to include a PDF with its\nlinks.  It includes ways to encode links to within the document, like you\'d\nobtain with ``\\ref`` and ``\\cite`` in LaTeX.\n\n\nQuick Start\n~~~~~~~~~~~\n\nTo get started:\n\n1. Install ``ltxpdflinks``::\n\n     pip3 install ltxpdflinks\n\n2. Download the ``phflplx.sty`` file here::\n\n     https://github.com/phfaist/ltxpdflinks/releases\n\n[Self-note TODO: I still need to publish releases on github.com & on PyPI! For\nnow, you need to run ``poetry build``, ``pip3 install\ndist/ltxpdflinks-0.1.0.tar.gz`` and ``(cd phflplx && latex phflplx.ins)``. ]\n\nTo compile your document:\n\n1. Drop the file ``phflplx.sty`` in the same folder as your latex source file,\n   and add to your document preamble::\n\n     \\usepackage{phflplx}\n     \\DeclareGraphicsExtensions{.lplx,.pdf}\n\n   [I\'m assuming you\'re loading the ``graphicx`` (or alternatively\n   ``graphics``) and the ``hyperref`` packages, too.]\n\n   Note: If you\'d like to include also other file types in your document\n   (e.g., ``.png``, ``.jpeg``, etc.), you need to add them to the\n   ``\\DeclareGraphicsExtensions`` argument, too.  See doc for the\n   `graphicx package <https://mirror.clientvps.com/CTAN/macros/latex/required/graphics/grfguide.pdf>`_.\n\n2. Run the ``ltxpdflinks`` command-line program for all your PDF files that\n   contain links::\n\n     > ltxpdflinks myfigure1.pdf\n\n3. Compile your LaTeX document as usual.\n\n\nHow to include links to other parts of the LaTeX document:\n\n1. When creating your figure in your favorite drawing software, create a "web\n   hyperlink" with an URL of the following form::\n\n     latexref://<type-of-reference>/<reference-target>\n\n   For a link to a section, equation, etc. (when you\'d use ``\\ref`` /\n   ``\\autoref`` / ``\\cref`` in LaTeX), use ``latexref://ref/<label-target>``\n   where you replace ``<label-target>`` by the LaTeX label of the object you\'re\n   referencing (the argument of the ``\\label{...}`` command in LaTeX).\n\n   For a link to a bibliographic reference entry (as in ``\\cite{...}``), use\n   ``latexref://cite/<bibtex-key>``, where you replace ``<bibtex-key>`` by the\n   bibliographic reference key you\'d like to refer to (the argument you\'d use to\n   the ``\\cite{...}`` command).\n\n2. These special URL links are automatically converted to LaTeX references by\n   the ``ltxpdflinks`` utility and the ``phflplx`` package.\n\n\nFeatures\n~~~~~~~~\n\n- Special link conversions::\n\n    latexref://ref/XXXXXX   →   link to XXXXXX label as via \\ref{XXXXXX}\n    \n    latexref://cite/XXXXXX   →   link to XXXXXX citation as via \\cite{XXXXXX}\n\n  (In the future I\'ll probably add ways to plug in custom link conversions.  The\n  code is extendible & you can add them yourself already if you invoke\n  ``ltxpdflinks`` via your own python script.)\n\n- Full support for rotation, scaling and clipping via options to\n  ``\\includegraphics[...]{...}``\n\n- Links use the format defined in the LaTeX document (colors & border relevant\n  for link type URL/internal reference/citation as specified via the\n  ``hyperref`` package.)\n\n- Simple Python implementation which you can use via your own custom script if\n  you\'d like to add link conversions or customize the process in any way.\n\n  To get started::\n\n    import ltxpdflinks\n\n    extractor = ltxpdflinks.PdfGraphicLinksExtractor(fname)\n    extracted = extractor.extractGraphicLinks()\n\n    converter = ltxpdflinks.LatexRefsLinkConverter()\n    converter.convertLinks(extracted)\n\n    lplxexporter = ltxpdflinks.LplxPictureEnvExporter()\n    lplx_content = lplxexporter.export(extracted)\n\n    with open(\'my_ouput_file_will_be_overwritten.lplx\', \'w\') as foutput:\n        foutput.write(lplx_content)\n\n\n\nPlanned improvements\n~~~~~~~~~~~~~~~~~~~~\n\n- Support the possibility (as an opt-in option) to preserve link styling\n  (border, color, etc.)  instead if using the document links style\n\n- Support for internal annotations within the PDF graphic (from one part of\n  the graphic to another)\n\n- Support for other types of annotations ?\n\n- Support for generation of ``.pax`` files for use with the `pax LaTeX package\n  <https://www.ctan.org/pkg/pax>`_ instead\n\n\nExisting alternatives\n~~~~~~~~~~~~~~~~~~~~~\n\n- You can also directly create your diagrams natively in LaTeX using `TiKZ\n  <https://www.overleaf.com/learn/latex/TikZ_package>`_.  I prefer to prepare\n  diagrams with drawing software, but that\'s a personal preference.\n    \n- The `pax LaTeX package and associated utility <https://www.ctan.org/pkg/pax>`_\n  also includes PDF links and annotations using a similar philosophy; it also\n  provides a separate command-line tool to process PDF files before inclusion.\n\n  As far as I could tell, `pax` supports more PDF annotations and preserves link\n  styles.  It doesn\'t seem to provide link conversion to LaTeX references and\n  citations for internal links.  It also doesn\'t seem to fully support rotation\n  and clipping via options to ``\\includegraphics``.  The command-line utility is\n  written in Java.\n\n  This option has been around for a while, so it might definitely be more\n  stable!\n',
    'author': 'Philippe Faist',
    'author_email': 'philippe.faist@bluewin.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phfaist/ltxpdflinks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
