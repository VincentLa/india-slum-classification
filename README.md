# Machine Learing Projects for Economic Research in India
This repository contains work for a few projects involving using machine learning / computer vision to predict socioeconomic characteristics of places from satellite images. The work will primarily focus on India. There are a few possible ideas:

1. Classifying locations as slums or not slums from google earth images
2. Predicting crops planted and yields (at roughly the county level of aggregation)
3. Predicting rural income (of all villages) from detailed time series data on ~500 villages over many years. This would allow us to predict incomes in another 500,000 villages, which would be really really cool.

The `delhi` folder contains some work on classifying locations as slums or not slums from google earth images of Delhi, India.

## Dev Environment Setup
### Installing Homebrew
Homebrew is a package manager for OS X. A package is a collection of code files that work together. Installing them usually means running a script (a bit of code) that puts certain files in the various directories. A lot of the packages you will want are going to have dependencies. That means they require you to have other packages already installed on your computer. Homebrew will find and install dependencies for you AND it will keep them organized in one location AND it can tell you when updates are available for them.

Installation instructions: https://brew.sh/

### Installing Python
`brew install python3`

### Installing pip
There are a few package managers that are specific to Python, and pip is the preferred one. The name pip stands for "pip installs packages". Installation instructions, in your terminal:
```
$ curl -O http://python-distribute.org/distribute_setup.py
$ python distribute_setup.py
$ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
$ python get-pip.py
```

### Installing python package dependencies
Once you have pip, you can easily install all python package dependencies this repo requires to run by simply running:
`pip3 install -r requirements.txt` on the root folder of the repo in your terminal

## Relevant Links
1. Good introduction/background on Neural Nets: http://neuralnetworksanddeeplearning.com/chap1.html
