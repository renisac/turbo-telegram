import os
from setuptools import setup, find_packages
import versioneer

# vagrant doesn't appreciate hard-linking
if os.environ.get('USER') == 'vagrant' or os.path.isdir('/vagrant'):
    del os.link

setup(
    name="ri_registry",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Registry SDK",
    long_description="Software Development Kit for the REN-ISAC Registry",
    url="https://github.com/renisac/turbo-telegram",
    license='MPLv2',
    classifiers=[
               "Topic :: System :: Networking",
               "Environment :: Other Environment",
               "Intended Audience :: Developers",
               "Programming Language :: Python",
               ],
    keywords=['security'],
    author="Wes Young",
    author_email="wes@ren-isac.net",
    packages=find_packages(),
    install_requires=[
        'prettytable',
        'pyaml',
        'requests',
        'arrow',
        'pytest'
    ],
    scripts=[],
    entry_points={
        'console_scripts': [
            'ren=ri_registry.client:main',
        ]
    },
)
