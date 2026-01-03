from setuptools import setup, find_packages

setup(
    name='proxy6-client',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'aiohttp>=3.8.0',
    ],
    license='MIT',
    author='Aleksey Novikov',
    author_email='...',
    description='Клиент для API Proxy6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/V1vaak/PROXY6_TOOLS',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

)
