from bs4 import BeautifulSoup as soup
import requests
import operator
import spacy
import praw

NUM_ARTICLES_NEWS = 48
NUM_ARTICLES_REDDIT = 48

common_words = ['the', 'be', 'of', 'and', 'a', 'to', 'in', 'he', 'have', 'it', 'that', 'for', 'they', 'I', 'with', 'as', 'not', 'on', 'she', 'at', 'by', 'this', 'we', 'you', 'do', 'but', 'from', 'or', 'which', 'one', 'would', 'all', 'will', 'there', 'say', 'says' 'said', 'who', 'make', 'when', 'can', 'more', 'if', 'no', 'man', 'out', 'other', 'what', 'time', 'up', 'go', 'about', 'than', 'into', 'could', 'state', 'only', 'new', 'year', 'some', 'take', 'come', 'these', 'know', 'see', 'use', 'get', 'like', 'then', 'first', 'any', 'work', 'now', 'many', 'such', 'give', 'over', 'think', 'most', 'even', 'find', 'day', 'also', 'after', 'way', 'many', 'must', 'look', 'before', 'great', 'back', 'through', 'long', 'where', 'much', 'should', 'well', 'people', 'down', 'own', 'just', 'U.S.', 'new', 'old', 'best', 'google', 'apple', 'health']

freq = dict()
dataCandidate = dict()
data = []
numWords = 30
cutOff = 0


nlp = spacy.load('en_core_web_sm')

reddit = praw.Reddit(client_id='CJRbQeTdLuw50Q', client_secret='JyjuTwMj263CZKwa1D-vDQ9f5IM', user_agent='test app')

def updateFrequencyValue(word, numTime):
    if word in freq:
        freq[word] += numTime
    else:
        freq[word] = numTime

def runReadSpike():
    # extract headlines from bullet list
    url = "https://readspike.com/"
    response = requests.get(url, timeout=10)
    content = soup(response.content, "html.parser")
    for headline in (content.findAll(class_='bbc-section') + content.findAll(class_='engadget-section') + content.findAll(class_='arstechnica-section') + content.findAll(class_='newscientist-section') + content.findAll(class_='slashdot-section') + content.findAll(class_='wired-section') + content.findAll(class_='theonion-section')):
        s = headline.text

        doc = nlp(s)
        prev = None
        for w in doc:
            inCommons : bool = w.lemma_.lower() in common_words
            if((w.is_stop == False) and w.text.isalpha() and
                (w.pos_ == "PROPN" or w.pos_ == "NOUN" or w.pos_ == "ADJ")):
                if (not inCommons):
                    updateFrequencyValue(w.text, 1) # add the word itself
                if (prev != None and prev != w.text): # add a pair of words
                    updateFrequencyValue(prev + " " + w.text, 2) # intentially do it twice
                prev = w.text

def runCNN():
    # extract headlines from bullet list
    url = "https://lite.cnn.io/en"
    response = requests.get(url, timeout=10)
    content = soup(response.content, "html.parser")
    for headline in content.findAll('a'):
        s = headline.text

        doc = nlp(s)
        prev = None
        for w in doc:
            inCommons : bool = w.lemma_.lower() in common_words
            if((w.is_stop == False) and w.text.isalpha() and
                (w.pos_ == "PROPN" or w.pos_ == "NOUN" or w.pos_ == "ADJ")):
                if (not inCommons):
                    updateFrequencyValue(w.text, 1) # add the word itself
                if (prev != None and prev != w.text): # add a pair of words
                    updateFrequencyValue(prev + " " + w.text, 2) # intentially do it twice
                prev = w.text

def runNPR():
    for i in range(1001, 1001 + NUM_ARTICLES_NEWS):

        # extract headlines from bullet list
        url = "https://text.npr.org/t.php?tid=" + str(i)
        response = requests.get(url, timeout=10)
        content = soup(response.content, "html.parser")
        for headline in content.findAll('li'):

            s = headline.text
            if(s != "Contact Us" and s != "Terms of Use" and 
               s!= "Permissions" and s!= "Privacy Policy"): # manual edits to cut out 4 irrelevant points
                
                doc = nlp(s)
                prev = None
                for w in doc:

                    inCommons : bool = w.lemma_.lower() in common_words
                    if((w.is_stop == False) and w.text.isalpha() and
                       (w.pos_ == "PROPN" or w.pos_ == "NOUN" or w.pos_ == "ADJ")):
                        if (not inCommons):
                            updateFrequencyValue(w.text, 1) # add the word itself
                        if (prev != None and prev != w.text): # add a pair of words
                            updateFrequencyValue(prev + " " + w.text, 2) # intentially do it twice
                        prev = w.text

def runReddit(freq_avg_from_news):
    top_posts = reddit.subreddit('worldnews').top("day", limit=NUM_ARTICLES_REDDIT)
    for post in top_posts:
        doc = nlp(post.title)
        prev = None
        for w in doc: 
            inCommons : bool = w.lemma_.lower() in common_words

            if((w.is_stop == False) and w.text.isalpha() and
               (w.pos_ == "PROPN" or w.pos_ == "NOUN" or w.pos_ == "ADJ")):
                    freqScore = int(min(max(1, int(post.score / 100)), freq_avg_from_news))
                    if (not inCommons):
                        updateFrequencyValue(w.text, freqScore)
                    if (prev != None and prev != w.text):
                        updateFrequencyValue(prev + " " + w.text, 1.5*freqScore) 
                    prev = w.text

def runThroughArticles():
    # news articles
    runReadSpike()
    runCNN()
    runNPR()

    # reddit posts
    freq_avg = 0
    for n in freq.values():
        freq_avg += n
    freq_avg /= len(freq)
    runReddit(freq_avg)

def ORDER(x):
    return len(x)*2 + freq.get(x)

def findFreqThreshold():
    # find threshold
    total = 0.0
    maxVal = 0.0
    for n in freq.values():
        if (n > maxVal):
            maxVal = n
        total += n
    
    return min(int(maxVal*2/3), int(total / len(freq)*2))

def isARepeat(candidate) -> bool:
    c = candidate.split()
    for d in dataCandidate.keys():
        inData = d.split()
        for inDataWord in inData:
            if (inDataWord in c or inDataWord.lower() in c or inDataWord.capitalize() in c):
                return True
    return False

def scrapeArticles():

    runThroughArticles()
    freq_threshold = findFreqThreshold()

    # populate the dataCandidate with non-repeating, high enough freq words
    for word in sorted(freq.keys(), key = ORDER, reverse=True):        
        if ((freq[word] > freq_threshold) and (not isARepeat(word))):
            dataCandidate.update({word: freq[word]})
    
    # Find the cut off
    counter = 0
    cutOff = 0
    for value in sorted(dataCandidate.values(), reverse=True):
        if (counter == numWords):
            cutOff = value
        counter += 1
    
    # print(dataCandidate)
    # print(cutOff)
    
    # Put the dataCandidates that satisfies the cut off into data
    for key in dataCandidate.keys():
        if (dataCandidate[key] >= cutOff):
            data.append({"word": key,
                        "value": dataCandidate[key],
                        "url": "https://news.google.com/search?q=" + key})
    # print(freq)
    # print(data)

    return data