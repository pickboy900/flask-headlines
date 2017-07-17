import feedparser
from flask import Flask, render_template
application = Flask(__name__)

RSS_FEED = { 'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
			 'cnn': "http://rss.cnn.com/rss/edition.rss",
			 'fox': "http://feeds.foxnews.com/foxnews/latest",
			 'iol': "http://www.iol.co.za/cmlink/1.640"
			}
@application.route("/")
@application.route('/<publication>')
def get_news(publication='bbc'):
	feed = feedparser.parse(RSS_FEED[publication])
	first_article = feed['entries']
	return render_template('home.html', articles=first_article)

if __name__=="__main__":
	application.run(port=5000, debug=True)