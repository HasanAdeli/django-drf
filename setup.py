from setuptools import setup, find_packages

setup(
    name='postman-drf',
    version='0.1.1',
    author='Hassan adeli',
    author_email='hasanadeli1374@gmail.com',
    description='A package to convert Postman collections to Django rest framework code and vice versa.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/HasanAdeli/postman-drf',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'typer'
    ]
)
