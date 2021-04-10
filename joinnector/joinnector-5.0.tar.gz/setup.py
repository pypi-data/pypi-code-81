from setuptools import setup, find_packages

setup(
    name='joinnector',         # How you named your package folder (MyLib)
    packages=find_packages(),
    version='5.0',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Nector python SDK (nector.io is a loyalty and reward APIs platform, that allows businesses to reward deals, offers, wallet points to their customers for various actions.)',
    author='Tech, Nector',                   # Type in your name
    author_email='tech@nector.io',      # Type in your E-Mail
    url='https://github.com/joinnector/joinnector-python-sdk',
    # I explain this later on
    download_url='https://github.com/joinnector/joinnector-python-sdk/archive/5.0.tar.gz',
    # Keywords that define your package best
    keywords=['nector', 'reward', 'loyalty', 'coins', 'wallets', 'deals'],
    install_requires=[            # I get to this in a second
        'requests',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
