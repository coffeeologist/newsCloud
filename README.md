# wordCloudExtension

## What it does
News Cloud is a chrome extension that aggregates text from a variety of news sites (NPR, CNN, BBC, Ars Technica, Reddit, and etc.) and overrides the new tab page to display shared trending phrases based on word frequency. We take these trending phrases and display them in a word cloud comprised of hyperlinks sized according to their occurrence. The hyperlinks redirect to a Google News search of the keyword or phrases.

## How to use
This chrome extension is still under construction as we aim to deploy it after improving algorithms and load times. However, if you would like to experience it locally, please follow these instructions.

Assuming Python 3.6 and above,
1. pip install packages: request, bs4, spacy, praw, flask
2. clone or fork this repository
3. In the wordCloudExtension directory, run python ./app.py
