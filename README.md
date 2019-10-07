![build_status](https://api.travis-ci.org/khufkens/daymetpy.svg)
![status](https://img.shields.io/pypi/status/daymetpy.svg)
![version number](https://img.shields.io/pypi/v/daymetpy.svg)
![python](https://img.shields.io/pypi/pyversions/daymetpy.svg)
<a href="https://www.buymeacoffee.com/H2wlgqCLO" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" height="21px" ></a>
<a href="https://liberapay.com/khufkens/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg" height="21px"></a>

## daymetpy: A python library for accessing Daymet surface weather data
 
daymetpy attempts to fill the need for easy, integrated access to gridded daily Daymet weather data. The data are hosted by the Oak Ridge National Laboratories DAAC and accessed from [their web service](https://daymet.ornl.gov/web_services.html).

## Installation

Install the package using [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) and the following command:

```python
pip install daymetpy
```

## Use

Example code to calculate the temperature difference between Denver and Miami is given below. This gives an idea of code functionality and use. A worked example in an ipython notebook format can be found in the 'example' subdirectory.

```python
import sys
import daymetpy
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

denver_loc = (-104.9903, 39.7392)
miami_loc = (-80.2089, 25.7753)

denver = daymetpy.daymet_timeseries(lon=denver_loc[0], lat=denver_loc[1], start_year=2012, end_year=2014)
miami = daymetpy.daymet_timeseries(lon=miami_loc[0], lat=miami_loc[1], start_year=2012, end_year=2014)

fig, ax1 = plt.subplots(1, figsize=(18, 10))
rolling3day = denver.rolling(15).mean()
ax1.fill_between(rolling3day.index, rolling3day.tmin, rolling3day.tmax, 
                 alpha=0.4, lw=0, label='Denver', color=sns.xkcd_palette(['faded green'])[0])
ax1.set_title('Denver vs Miami temps (15 day mean)', fontsize=20)
rolling3day = miami.rolling(15).mean()
ax1.fill_between(rolling3day.index, rolling3day.tmin, rolling3day.tmax, 
                 alpha=0.4, lw=0, label='Miami', color=sns.xkcd_palette(['dusty purple'])[0])
ax1.set_ylabel(u'Temp. (°C)', fontsize=20)
fig.tight_layout()
plt.legend(fontsize=20)
```

## Requirements
Pandas / seaborn are required.

## Contributors
* Koen Hufkens: koen.hufkens@gmail.com
* Colin Talbert
