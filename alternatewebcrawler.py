from bs4 import BeautifulSoup as soup
import requests
import operator
import spacy
import praw

import sys

orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f


freq_threshold = 0
NUM_ARTICLES_NEWS = 48
NUM_ARTICLES_REDDIT = 48

common_words = ['the', 'be', 'of', 'and', 'a', 'to', 'in', 'he', 'have', 'it', 'that', 'for', 'they', 'I', 'with', 'as', 'not', 'on', 'she', 'at', 'by', 'this', 'we', 'you', 'do', 'but', 'from', 'or', 'which', 'one', 'would', 'all', 'will', 'there', 'say', 'says' 'said', 'who', 'make', 'when', 'can', 'more', 'if', 'no', 'man', 'out', 'other', 'what', 'time', 'up', 'go', 'about', 'than', 'into', 'could', 'state', 'only', 'new', 'year', 'some', 'take', 'come', 'these', 'know', 'see', 'use', 'get', 'like', 'then', 'first', 'any', 'work', 'now', 'many', 'such', 'give', 'over', 'think', 'most', 'even', 'find', 'day', 'also', 'after', 'way', 'many', 'must', 'look', 'before', 'great', 'back', 'through', 'long', 'where', 'much', 'should', 'well', 'people', 'down', 'own', 'just', 'U.S.', 'new']

freq = dict()
dataCandidate = dict()
data = []

nlp = spacy.load('en_core_web_sm')

reddit = praw.Reddit(client_id='CJRbQeTdLuw50Q', client_secret='JyjuTwMj263CZKwa1D-vDQ9f5IM', user_agent='test app')

def addToFreq(word, numTime):
    if word in freq:
        freq[word] += numTime
    else:
        freq[word] = numTime

def runThroughArticles():
    # news articles
    for i in range(1001, 1001 + NUM_ARTICLES_NEWS):
        url = "https://text.npr.org/t.php?tid=" + str(i)
        response = requests.get(url, timeout=10)
        content = soup(response.content, "html.parser")

        for headline in content.findAll('li'):
            s = headline.text
            if(s != "Contact Us" and s != "Terms of Use" and s!= "Permissions" and s!= "Privacy Policy"):
                doc = nlp(s)
                prev = None
                for w in doc:
                    inCommons = w.lemma_ in common_words
                    # print(inCommons)
                    if((w.is_stop == False) and (w.text.isalpha()) and
                       (w.pos_ == "PROPN" or w.pos_ == "NOUN" or w.pos_ == "ADJ") and (not inCommons) ):
                        # print(addToFreq(w.text))
                        if (prev != None and prev != w.text):
                            addToFreq(prev + " " + w.text, 1) # intentially do it twice
                        prev = w.text

    # reddit posts
    
    freq_avg = 0
    for n in freq.values():
        freq_avg += n
    freq_avg /= len(freq)

    # print("****" + str(freq_avg))


    top_posts = reddit.subreddit('worldnews').top("day", limit=NUM_ARTICLES_REDDIT)
    for post in top_posts:
        doc = nlp(post.title)
        prev = None
        for w in doc: 
            inCommons = w.lemma_ in common_words

            if((w.is_stop == False) and (w.text.isalpha()) and 
               (w.pos_ == "PROPN" or w.pos_ == "NOUN" or w.pos_ == "ADJ") and not inCommons):
                    freqScore = int(min(max(1, int(post.score / 100)), freq_avg))
                    addToFreq(w.text, freqScore)
                    if (prev != None and prev != w.text):
                        # print(prev + " " + w.text + " | score: " + str(freqScore * 2))
                        addToFreq(prev + " " + w.text, 1*freqScore) # TWICE!
                    prev = w.text
                    

def isARepeat(w) -> bool:
    word = w.split()
    for c in dataCandidate.keys():
        inData = c.split()

        for i in range (len(inData)):
            if (inData[i] in word):
                # print("FOUND A REPEAT! " + w + " |and| " + c)
                return True
        
    return False

def func(x):
    return len(x) + freq.get(x)

def scrapeArticles():
    runThroughArticles()

    # find threshold
    sum = 0
    maxVal = 0
    for n in freq.values():
        if (n > maxVal):
            maxVal = n
        sum += n
    
    # print("SUM: " + str(sum))
    freq_threshold = min(maxVal/2, sum / len(freq)*2)

    # print("THRESH: " + str(freq_threshold))
    # find threshold - end
    for key in sorted(freq.keys(), key = func, reverse=True):
        # print("word: " + key + " value: " + str(freq[key]))

        if (freq[key] > freq_threshold and
            isARepeat(key) == False):
            dataCandidate[key] = freq[key]
    
    print("SHOULD BE AN EMPTY DATA: " )
    print(data)

    counter = 0
    thirtyth = 0
    for values in sorted(dataCandidate.values(), reverse=True):
        if (counter == 30):
            thirtyth = values
        counter += 1

    print("DATACANDIDATES: ")
    print(dataCandidate)
    print("THIRTY: " + str(thirtyth))
    
    for key in dataCandidate.keys():
        if (dataCandidate[key] >= thirtyth):
            data.append({"word": key,
                        "value": dataCandidate[key],
                        "url": "https://news.google.com/search?q=" + key})
    # print(freq)
    print("DATA:")
    print(data)

    return data

scrapeArticles()