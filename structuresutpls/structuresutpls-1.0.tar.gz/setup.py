from setuptools import setup
setup(
    name="structuresutpls",
    install_requires=["openseespy","numpy","matplotlib"],
    version="1.0",
    Platform="Windows, Linux, MacOS",
    Description="Proyecto de Tesis UTPL: El comportamiento y conceptualización de una columna de hormigón armado resultado resulta compleja y pocas veces entendido en toda su magnitud.  Debido principalmente a que la solución teórica propuesta por la mecánica de estructuras está compuesta de conceptos abstractos o desarrollos matemáticos complejos.  la cual ha obligado a que el sistema de educación cambie de forma radical, pasando de una educación mayoritariamente presencial a una virtual.",
    author="Ronal Valencia",
    author_email="adelitacalle_rivera@hotmail.es",
    license="GPL",
    url="https://www.utpl.edu.ec/",
    packages=['estructuras-utpl','estructuras-utpl.estructuras'],
    scripts=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)