# Project Ideas
## Classification of Slums

### Data
1. We currently have about 500 images that have been manually labeled as slums vs not-slums.
2. The images are from Google Earth and were screen captured manually. Is it possible to automate capturing images to build a training data set?

### Challenges
1. Fitting a binary classifier may not be appropriate. There are many areas that are "in between" a slum vs. non-slum.
2. We might not have enough data right now to build a great classifier.

## Classification of Socioeconomic Characteristics of Villages

### Data
1. We have some data from 2002 and 2012 on poverty level of every village in India in 2002 and 2012, and clean polygons that roughly approximate those villages.
2. We know a few major assets, education levels, and income category by household.

### Challenges
1. Fitting a binary classifier here may also not be appropriate
2. How can we generate training data?

### Outcomes
1. Rich vs Poor Village?
2. Perhaps instead of classification problem it's a prediction problem where we're trying to predict average household income?
3. Crop Yield?

# Literature Review

## Using Satellite Imagery to Find Villages In Need
[Targeting Direct Cash Transfers to the Extremely Poor](http://ssg.mit.edu/~krv/pubs/AbelsonVS_kdd2014.pdf)
1. This paper (Section 3. AVAILABLE DATA AND CROWDSOURCING DEPLOYMENT) has really good detail on what the project of getting training data entails. Read this!

Extract images from Google Satelites API?
This stackoverflow [link](http://stackoverflow.com/questions/9087166/how-can-i-extract-a-satellite-image-from-google-maps-given-a-lat-long-rectangle) will likely be helpful.
