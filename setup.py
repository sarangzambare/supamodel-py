from setuptools import setup, find_packages

setup(
    name='supamodel-py',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'supamodel=supamodel.supamodel:main',
        ],
    },
    author='Sarang Zambare',
    author_email='sarang.zambare@gmail.com',
    description='A tool for MLEs to monitor and control experiments from mobile phones',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
