import setuptools

setuptools.setup(
    name="streamlit-query-builder",
    version="0.0.6",
    author="Mohammad Falakmasir",
    author_email="falakmasir@gmail.com",
    description="react-query-builder interface for streamlit",
    long_description="compile SQL queries in UI",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
