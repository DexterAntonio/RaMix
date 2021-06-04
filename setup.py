import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='ramix',
    version='1.0.0',
    description='RaMix: A Python package for generating Raman Mixture Spectra',
    long_description="RaMix generates synthetic Raman mixture spectra."
                     "These mixture spectra can be used to compare the predictive "
                     "performance of different chemoinformatics algorithms, such as "
                     "partial least squares (PLS) and 1D Convolution Neural Networks (1D-CNN).",

    long_description_content_type='text',
    url='https://github.com/DexterAntonio/ramix',
    author='Dexter Antonio',
    author_email='dexter.d.antonio@gmail.com',
    license="MIT",
    packages=['ramix'],
    include_package_data=True,
    install_requires=['numpy'],

    classifiers=[
        'Development Status :: 3 - beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='raman spectra synthetic',
    project_urls={
        'Documentation': 'https://kul-group.github.io/MAZE-sim/build/html/index.html',
        'Source': 'https://github.com/DexterAntonio/RaMix/',
        'Tracker': 'https://github.com/RaMix/issues',
    },
    python_requires='>=3'
)
