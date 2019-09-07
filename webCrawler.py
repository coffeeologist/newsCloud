from bs4 import BeautifulSoup as soup
import requests
import operator
import spacy

FREQ_THRESHOLD = 15
NUM_ARTICLES = 30

freq = dict()
data = []

nlp = spacy.load('en_core_web_sm')

def addToFreq(word):
    if word in freq:
        freq[word] += 1
    else:
        freq[word] = 1

def runThroughArticles():
    for i in range(1001, 1001 + NUM_ARTICLES):
        url = "https://text.npr.org/t.php?tid=" + str(i)
        response = requests.get(url, timeout=10)
        content = soup(response.content, "html.parser")

        for headline in content.findAll('li'):
            s = headline.text
            if(s != "Contact Us" and s != "Terms of Use" and s!= "Permissions" and s!= "Privacy Policy"):
                doc = nlp(s)
                prev = None
                for w in doc:
                    if(w.is_stop == False and 
                       (w.pos_ == "PROPN" or w.pos_ == "VERB" or w.pos_ == "NOUN" or w.pos_ == "ADJ")):
                        addToFreq(w.text)
                        if (prev != None):
                            addToFreq(prev + " " + w.text)
                            addToFreq(prev + " " + w.text) # intentially do it twice
                        prev = w.text

def findThreshold():
    sum = 0
    for n in freq.values():
        sum += n
    
    FREQ_THRESHOLD = sum / 175

def isARepeat(w) -> bool:
    for d in data:
        inData = d.get("word").split()
        candidate = w.split()

        for i in range (len(inData)):
            if (inData[i] in candidate):
                return True
        
    return False

def scrapeArticles():
    runThroughArticles()
    findThreshold()
    for key in sorted(freq.keys(), key = len, reverse=True):
        if (freq[key] > FREQ_THRESHOLD and
            isARepeat(key) == False):
            data.append({"word": key,
                         "value": freq[key],
                         "url": "https://www.google.com/search?q=" + key})
    return data

scrapeArticles()
'''
for key in freq.keys():
    if (freq[key] > 2):
        print("\"" + str(key) + "\" : " + str(freq[key]))
'''


# Narrowing down the space to the article in the page
#(since there are many other irrelevant elements in the page)

#headlines = soup.find(class_="ul")


'''
# Getting the keywords section 
keyword_section = soup.find(class_="keywords-section")
# Same as: soup.select("div.article-wrapper grid row div.keywords-section")

# Getting a list of all keywords which are inserted into a keywords list in line 7.
keywords_raw = keyword_section.find_all(class_="keyword")
keyword_list = [word.get_text() for word in keywords_raw]
'''