from flask import Flask, render_template
from webCrawler import scrapeArticles


app = Flask(__name__)

@app.route('/')

def index():
    data = scrapeArticles()
    return render_template("index.html", data = data)

if __name__ == "__main__": 
    app.run(debug=True)