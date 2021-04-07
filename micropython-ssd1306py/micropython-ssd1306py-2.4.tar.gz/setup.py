from setuptools import setup, find_packages
filepath = 'README.md'
setup(
        name="micropython-ssd1306py",
        version="2.4",
        description="ssd1306 driver",
        long_description=open(filepath, encoding='utf-8').read(),
        long_description_content_type="text/markdown",
        author="jdh99",
        author_email="jdh821@163.com",
        url="https://github.com/jdhxyy/ssd1306py-micropython",
        packages=find_packages(),
        include_package_data=True,
        data_files=[filepath, 'ssd1306py/*.txt']
    )
