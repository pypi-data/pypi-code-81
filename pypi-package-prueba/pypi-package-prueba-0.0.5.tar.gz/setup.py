from setuptools import setup, find_packages

setup(
    name="pypi-package-prueba",
    version="0.0.5",
    license="MIT",
    description="Paquete de prueba, clase Python",
    # En caso de que mi paquete incluya librerias de terceros agrego la siguiente linea...
    # install_requires=["math", "numpy"],
    packages=find_packages(),
    author="Benjamin Schell",
    url="https://github.com/Benjaprogramado/pypi-package-Prueba"
)
