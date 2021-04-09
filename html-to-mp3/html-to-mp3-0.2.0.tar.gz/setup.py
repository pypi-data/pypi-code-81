# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['html_to_mp3']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['html2mp3 = html_to_mp3.html_to_mp3:html2mp3']}

setup_kwargs = {
    'name': 'html-to-mp3',
    'version': '0.2.0',
    'description': 'Convert HTML and text to mp3s',
    'long_description': '# `html2mp3`\n\n> Generate `mp3`s from html text.\n\nA tiny cli I made on a fling.\n\n## CLI\n\nBasic use:\n\n```bash\n# CLI docs\nhtml2mp3\n\n# Generate from a file\nhtml2mp3 file examples/test1.html test1.mp3\n\n# Download from URL\nhtml2mp3 url https://text.npr.org/985359064\n\n# Download from URL, only generate voice from the text in the selector .paragraphs-container\nhtml2mp3 url https://text.npr.org/985359064 --select ".paragraphs-container"\n```\n\nMultiple files at once can be done (though the CLI could be improved to make this less verbose):\n\n\n```bash\nhtml2mp3 url https://text.npr.org/985359064 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985347984 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985524494 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985032748 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985498425 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985336036 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/976385244 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985470204 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985365621 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985296354 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985594759 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985125653 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985290016 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985400141 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/984387402 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/984614649 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985143101 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/982223967 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/985421813 --select ".paragraphs-container" & html2mp3 url https://text.npr.org/984870694 --select ".paragraphs-container"\n```\n\nRunning the above example (20 examples in total) took about 48s on my personal computer (`47.72s user 0.74s system 480% cpu 10.094 total`)\n\nYou can do your own tests via:\n\n```bash\ntime sh -c \'html2mp3 url https://text.npr.org/985359064 & html2mp3 url https://text.npr.org/985347984\'\n```\n\n## TODO\n\n- [ ] Testing\n- [ ] Multiple files/urls at once\n- [ ] Voice generation settings\n',
    'author': 'Michael Wooley',
    'author_email': 'wm.wooley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/michaelwooley/html-to-mp3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
