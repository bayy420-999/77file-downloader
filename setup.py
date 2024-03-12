from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='77file-downloader',
        version='1.0.0',
        description='Simple downloader for 77file.com website',
        author='Bayu Ganteng',
        email='getkilla5@gmail.com',
        package_dir = {'': 'src'},
        packages=find_packages(where='src'),
        install_requires=['aiohttp', 'cloudscraper', 'bs4'],
        entry_points={
            'console_scripts': ['ssf_downloader=ssf_downloader.scripts.ssf_downloader:main']
        }
    )