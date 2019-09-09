# News Cloud

<img src="/square.png" width="300"> <img src="/sample.JPG" height="270">


## What it does
News Cloud is a chrome extension that aggregates text from a variety of news sites (NPR, CNN, BBC, Ars Technica, Reddit, and etc.) and overrides the new tab page to display shared trending phrases based on word frequency. We take these trending phrases and display them in a word cloud comprised of hyperlinks sized according to their occurrence. The hyperlinks redirect to a Google News search of the keyword or phrases.

## How to use
While we are able to make it into a local extension, this chrome extension is still under construction as we aim to deploy it after improving algorithms and load times. However, if you would like to experience it locally, please follow these instructions.

Assuming Python 3.6 and above,
1. pip install packages: 
```
pip install request bs4 spacy praw flask
```

2. Download this repository
3. In the wordCloudExtension directory, run python 
```
python ./app.py
```

4. Open http://localhost:5000/ in your browser and wait for the news word cloud to load. 

## What's next for News Cloud
1. The web scraping and frequency calculation algorithm creates a significant loading time whenever the site is opened which limits its effectiveness as a new-tab extension. This was the main reason why we were unable to effectively deploy the Flask project onto a PaaS like AWS, GCP, and Heroku because the HTML request would always time out.

2. Another feature that we would like to include is a customization menu that allows the user to add more news sources, change background image, and settings regarding word cloud generation.

We are excited to continue developing News Cloud into the useful and convenient news source that we conceived of.

## Contributors
- Jiachen (Amy) Liu
- Allen Liu

## Credits
- News Cloud logo is original
- Background image in the new tab belongs to Firewatch

## Notes
This began as a Hackathon submission to PennApps XX. View submission here: https://devpost.com/software/news-cloud
