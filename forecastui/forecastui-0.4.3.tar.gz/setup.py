from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

def glob_fix(package_name, glob):
    # This assumes setup.py lives in the folder that contains the package
    package_path = pathlib.Path(f'./{package_name}').resolve()
    return [str(path.relative_to(package_path))
            for path in package_path.glob(glob)]

setup(
    name='forecastui',
    version='0.4.3',
    description='User interface designed for data logging over serial',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/altairLab/elasticteam/forecast/forecast-atlas',
    author='Matteo Meneghetti',
    author_email='matteo@meneghetti.dev',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        "flask",
        "flask-restful",
        "flask-socketio >= 5.0",
        "requests",
        "pyyaml >= 5.0",
        "easyserial >= 0.2"
    ],
    extras_require = {
        "qt":  ["pycuteweb"]
    },
    include_package_data=True,
    package_data={
        'forecastui': [*glob_fix('forecastui', 'dist_client/**/*'),
            *glob_fix('forecastui', 'assets/**/*')]
    },
    entry_points={
        'console_scripts': [
            'forecastui=forecastui.app:main',
        ],
    },
    project_urls={
        'Source': 'https://gitlab.com/altairLab/elasticteam/forecast/forecast-atlas',
    },
)
