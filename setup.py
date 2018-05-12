from distutils.core import setup
setup(
  name = 'daymetpy',
  packages = ['daymetpy'],
  version = '1.0.0',
  license = 'AGPL-3',
  description = 'A library for accessing Daymet surface weather data',
  author = 'Koen Hufkens',
  author_email = 'koen.hufkens@gmail.com',
  url = 'https://github.com/khufkens/daymetpy',
  download_url = 'https://github.com/khufkens/daymetpy/archive/1.0.0.tar.gz',
  keywords = ['daymet', 'climatology', 'ORNL','weather'],
  classifiers = [
    # Status
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Information Analysis',

    # License
    'License :: OSI Approved :: GNU Affero General Public License v3',

    # Python versions supported
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5'
  ],
)
