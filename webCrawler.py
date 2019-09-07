from bs4 import BeautifulSoup as soup
import requests
import operator

freq = dict()

# most common english words: https://www.rypeapp.com/most-common-english-words/

def addToFreq(txt):
    for word in txt.split():
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1

def scrapeArticles():
    for i in range(1001, 1049):
        url = "https://text.npr.org/t.php?tid=" + str(i)
        response = requests.get(url, timeout=10)
        content = soup(response.content, "html.parser")

        for headline in content.findAll('li'):
            s = headline.text
            if(s != "Contact Us" and s != "Terms of Use" and s!= "Permissions" and s!= "Privacy Policy"):
                addToFreq(headline.text)
    
scrapeArticles()

for key in freq.keys():
    if (freq[key] > 2):
        print("\"" + str(key) + "\" : " + str(freq[key]))



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