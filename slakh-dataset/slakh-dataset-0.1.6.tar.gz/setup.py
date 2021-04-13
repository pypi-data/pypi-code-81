# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slakh_dataset']

package_data = \
{'': ['*'], 'slakh_dataset': ['splits/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'pretty_midi>=0.2.9,<0.3.0',
 'torch>=1.8.1,<2.0.0',
 'torchaudio>=0.8.1,<0.9.0',
 'tqdm>=4.60.0,<5.0.0']

setup_kwargs = {
    'name': 'slakh-dataset',
    'version': '0.1.6',
    'description': 'Unofficial PyTorch dataset for Slakh',
    'long_description': "# Slakh PyTorch Dataset\n\nUnofficial PyTorch dataset for [Slakh](http://www.slakh.com/).\n\nThis project is a work in progress, expect breaking changes!\n\n## Roadmap\n\n### Automatic music transcription (AMT) usecase with audio and labels\n\n- [x] Specify dataset split (`original`, `splits_v2`, `redux`)\n- [x] Add new splits (`redux_no_pitch_bend`, ...) (Should also be filed upstream) (implemented by `skip_pitch_bend_tracks`)\n- [x] Load audio `mix.flac` (all the instruments comined)\n- [x] Load individual audio mixes (need to combine audio in a streaming fashion)\n- [x] Specify `train`, `validation` or `test` group\n- [x] Choose sequence length\n- [x] Reproducable load sequences (usefull for validation group to get consistent results)\n- [ ] Add more instruments (`eletric-bass`, `piano`, `guitar`, ...)\n- [x] Choose between having audio in memory or stream from disk (solved by `max_files_in_memory`)\n- [x] Add to pip\n\n### Audio source separation usecase with different audio mixes\n- [ ] List to come\n\n\n## Usage\n\n1. Download the Slakh dataset (see the official [website](http://www.slakh.com/)). It's about 100GB compressed so expect using some time on this point.\n\n2. Install the Python package with pip:\n```bash\npip install slakh-dataset\n```\n\n3. Convert the audio to 16 kHz (see https://github.com/ethman/slakh-utils)\n\n4. You can use the dataset (AMT usecase):\n\n```python\nfrom torch.utils.data import DataLoader\nfrom slakh_dataset import SlakhAmtDataset\n\n\ndataset = SlakhAmtDataset(\n    path='path/to/slakh-16khz-folder'\n    split='redux', # 'splits_v2','redux-no-pitch-bend'\n    audio='mix', # 'mix'\n    instrument='electric-bass', # or `midi_programs`\n    # midi_programs=[33, 34, 35, 36, 37],\n    groups=['train'],\n    skip_pitch_bend_tracks=True,\n    sequence_length=327680,\n    max_files_in_memory=200,\n)\n\nbatch_size = 8\nloader = DataLoader(dataset, batch_size, shuffle=True, drop_last=True)\n\n# train model on dataset...\n```\n\n## Acknowledgement\n\n- This code is based on the dataset in [Onset and Frames](https://github.com/jongwook/onsets-and-frames) by Jong Wook Kim which is MIT Lisenced.\n\n- Slakh http://www.slakh.com/\n\n\n",
    'author': 'Henrik Grønbech',
    'author_email': 'henrikgronbech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
