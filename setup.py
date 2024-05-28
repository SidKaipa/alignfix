from setuptools import setup, find_packages

setup(
    name='alignfix',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'alignfix=alignfix.main:main'
        ]
    },
    install_requires=[
        'numpy',
        'pyfaidx'
    ],
    author='Jason Chiu, Author 2, Author 3',
    author_email='jmchiu@ucsd.edu, author2@example.com, author3@example.com',
    description='A tool for aligning short Illumina reads to a genome based on a seed and extend method.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/alignfix',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)