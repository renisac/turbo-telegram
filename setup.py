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
    license='LGPL3',
    classifiers=[
               "Topic :: System :: Networking",
               "Environment :: Other Environment",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
               "Programming Language :: Python",
               ],
    keywords=['security'],
    author="Wes Young",
    author_email="wes@ren-isac.net",
    packages=find_packages(),
    install_requires=[
        'prettytable>=0.7.2',
        'pyaml>=15.03.1',
        'requests>=2.6.0',
        'arrow>=0.6.0',
        'pytest>=2.9.2'
    ],
    scripts=[],
    entry_points={
        'console_scripts': [
            'ri=ri_registry.client:main',
        ]
    },
)
