import setuptools

long_description = '''
Generate HTML. Usage:
	import genhtml
	html=genhtml.HTML()
	p=html.open('p')
	p.attrs['style']='color:red;'
	p.write('Hello!')
	html.commit(p)
	tags=html.get_tags()
	tags[0].write('Using genhtml')
	html.set_tags(tags)
	html.open_in_browser()
	print(genhtml.formated(html.output()))
'''

setuptools.setup(
    name="genhtml",
    version="1.3.0",
    author='Vadim Simakin',
    author_email="sima.vad@gmail.com",
    description="Html5 generator",
    long_description=long_description,
    long_description_content_type="text/plain",
    packages=['genhtml'],
    install_requires=['bs4', 'lxml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
