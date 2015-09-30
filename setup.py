from distutils.core import setup

setup(
    name='NightlyDownload',
    version='0.1.0',
    author='Bryan Waite',
    author_email='bryanwaite@gmail.com',
    scripts=['nightlydownload.py', 'ndterminate.py'],
    license='LICENSE.txt',
    description='Scripts to schedule downloads',
    long_description=open('README.md').read(),
    install_requires=[
        "pycurl >= 7.19.3",
    ],
)
