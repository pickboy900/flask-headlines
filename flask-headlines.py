import json, urllib.request
import feedparser, datetime
from flask import Flask, render_template, request, make_response

application = Flask(__name__)

RSS_FEED = { 'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
			 'cnn': "http://rss.cnn.com/rss/edition.rss",
			 'fox': "http://feeds.foxnews.com/foxnews/latest",
			 'iol': "http://www.iol.co.za/cmlink/1.640"
			}

DEFAULTS = {
			'publication': 'bbc',
			'city': "London,UK",
			'currency_from': "GBP",
			'currency_to': "USD"
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}\
	&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed"


EXCHANGE_URL = "https://openexchangerates.org//api/latest.json?app_id=d4b4fdf389bc45c097b33007d67fc1cf"

ARGS = ["publication", "city", "currency_from", "currency_to"]



@application.route("/", methods=["GET", "POST"])
def home():
	for var in ARGS:
		globals()[var] = set_value(var)
	articles = get_news(publication)
	(weather, cities) = get_weather(city)
	(rate, rates)=get_rate(currency_from, currency_to)
	template=render_template('home.html',
							currency_from=currency_from,
							currency_to=currency_to,
							publication=publication,
							articles=articles,
							weather=weather,
							rate=rate,
							rates=rates,
							feeds=RSS_FEED)
	response = make_response(template)
	expires= datetime.datetime.now() + datetime.timedelta(days=365)
	for var in ARGS:
		response.set_cookie(var, globals()[var], expires=expires)
	return response

def set_value(argument):
	return request.args.get(argument) or request.cookies.get(argument) or DEFAULTS[argument]


def get_news(query):
	publication = query.lower()
	feed = feedparser.parse(RSS_FEED[publication])
	return feed['entries']


def get_weather(query):
	query = urllib.parse.quote(query)
	url = WEATHER_URL.format(query)
	data = urllib.request.urlopen(url).read().decode('utf8')
	parsed = json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather = {
		"description": parsed["weather"][0]["description"],
		"temperature": parsed["main"]["temp"],
		"city": parsed["name"],
		"country": parsed["sys"]["country"]
		}
	return (weather, parsed)

def get_rate(frm, to):
	all_currency = urllib.request.urlopen(EXCHANGE_URL).read().decode()
	parsed = json.loads(all_currency).get('rates')
	frm_rate = parsed.get(frm.upper())
	to_rate = parsed.get(to.upper())
	return to_rate/frm_rate, parsed

if __name__ == "__main__":
	application.run(port=5000, debug=True)