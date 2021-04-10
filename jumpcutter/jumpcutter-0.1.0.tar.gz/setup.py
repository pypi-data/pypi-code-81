# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jumpcutter', 'jumpcutter.src']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=4.4.2,<4.5.0',
 'imageio>=2.9.0,<2.10.0',
 'matplotlib>=3.3.1,<3.4.0',
 'moviepy>=1.0.3,<1.1.0',
 'nose>=1.3.7,<1.4.0',
 'numpy>=1.19.1,<1.20.0',
 'pillow>=7.2.0,<7.3.0',
 'proglog>=0.1.9,<0.2.0',
 'scipy>=1.5.2,<1.6.0',
 'sympy>=1.6.2,<1.7.0']

entry_points = \
{'console_scripts': ['jumpcutter = jumpcutter.__main__:main']}

setup_kwargs = {
    'name': 'jumpcutter',
    'version': '0.1.0',
    'description': 'Jumpcut silent parts of your videos automagically',
    'long_description': '## What is jumpcutter?\n\nJumpcutter is a program that is written in Python to automatically jump-cut silent parts of your videos.\nThe purpose here is to ease your post recording work.\n\nCheck out [the medium post](https://medium.com/@emkademy/how-to-jump-cut-silent-parts-of-your-videos-automatically-with-python-2e4b96320dc1)\nfor more information.\n\n## Prerequisites\n\nIf you use Docker, there is a Dockerimage that is prepared to run this repository. You can simply go into ./docker folder\nand run ./build_docker.sh\n\n```bash\ncd ./docker\nchmod +x ./build_docker.sh\n./build_docker.sh\n```\n\nIf you don\'t want to use docker, you can install the Python packages that are specified in "requirements.txt" to run the program.\n\n```bash\npip3 install -r requirements.txt\n```\n\n## Demo\n\n[![Watch the video](https://img.youtube.com/vi/UDjzm_lzWOA/hqdefault.jpg)](https://youtu.be/UDjzm_lzWOA)\n\n## How to run it?\nThere are 8 command line arguments you can run the program with. \nBefore explaining them, I would like to say that most of these parameters \nhave a default value that “just works”. So, if you don’t want you don’t need to specify \n(or know) almost any of these parameters. You will be just fine with the default values.\n\n1. `--input`, `-i`: Path to the video that you want to jump-cut.\n2. `--output`, `-o`: Path to where you want to save the output video.\n3. `--magnitude-threshold-ratio`, `-m`: The percentage of the maximum value of your audio signal that you would like to \n     consider as silent a signal (default: 0.02).\n4. `--duration-threshold`, `-d`: Minimum number of required seconds in silence to cut it out. For example if this parameter \n     is 0.5, it means that the silence parts have to last minimum 0.5 seconds, otherwise they won\'t be jump-cut (default: 0.5).\n5. `--failure-tolerance-ratio`, `-f`: Most of the times, there are 44100 audio signal values in 1 second of a video. \n     Let\'s say the "--duration-threshold" was set to 0.5. This means that, we need to check minimum 22050 signal \n     values to see if there is a silent part of not. What happens if we found 22049 values that we consider as silent, \n     but there is 1 value that is above our threshold. Should we just throw this part of the video and consider it as a \n     loud signal? I think we shouldn\'t. This parameter leaves some room for failure, it tolerates high signal values until \n     some point. Let\'s say it is set to 0.1, it means that 10% of the signal that is currently being investigated can \n     have values that are higher than our threshold, but they are still going to be considered as a silent part (default: 0.1).\n6. `--spaces-on-edges`, `-s`: Leaves some space on the edges of silence cut. E.g. if it is found that there is \n     silence between 10th and 20th second of the video, then instead of cutting it out directly, we cut out \n     (10+space_on_edges)th and (20-space_on_edges)th seconds of the clip (default: 0.1).\n7. `--silence-part-speed`, `-x`: If this parameter is given, instead of cutting the silent parts out, the script will \n     speed them up "x" times.\n8. `--min-loud-part-duration`, `-l`: If this parameter is given, loud parts of the video that are shorter then this \n     parameter will also be cut.\n     \n## Examples of running the program\n\n```bash\n# The simplest way you can run the program\npython main.py -i input_video.mp4 -o output_video.mp4\n# If you want, you can also set the other parameters that was mentioned\npython main.py -i input_video.mp4 -o output_video.mp4 -m 0.05 -d 1.0 -f 0.2 -s 0.2 -x 2000 -l 1.0\n```\n',
    'author': 'Kivanc Yuksel',
    'author_email': 'emkademy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kivancyuksel/jumpcutter.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
