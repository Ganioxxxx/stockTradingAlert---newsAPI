from email import header
from email.quoprimime import body_check
from multiprocessing import Condition
from urllib import response
import requests
import os
from urllib import response
from urllib.request import HTTPPasswordMgrWithDefaultRealm
from twilio.rest import Client
from dotenv import load_dotenv
from yaml import load

load_dotenv()



# API 
STOCK = "MSFT",
COMPANY_NAME = "Microsoft"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY= os.environ.get("STOCK_API_KEY")
NEWS_API_KEY= os.environ.get("NEWS_API_KEY")
TWILIO_SID= os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN=os.environ.get("TWILIO_AUTH_TOKEN")


#PARAMS
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,    "datatype": "json",
    "outputsize": "compact",
    "apikey": STOCK_API_KEY
}

news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
}


response = requests.get(STOCK_ENDPOINT, params=stock_params)

data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_stock = data_list[0]
yesterday_closing_price = yesterday_stock["4. close"]
print(yesterday_closing_price)

one_day_before_yesterday_stock = data_list[1]
one_day_before_yesterday_closing_price = one_day_before_yesterday_stock["4. close"]
print(one_day_before_yesterday_closing_price)

diffrence = (float(yesterday_closing_price) -   float(one_day_before_yesterday_closing_price))
upper_down = None
if diffrence > 5:
    upper_down = "⬆️"
else :
    upper_down = "⬇️"


diffrence_percent = round((diffrence / float(yesterday_closing_price)) * 100)
print(diffrence_percent)

if diffrence_percent > 5:
    
    print("Wzroslo")


news_response = requests.get(NEWS_ENDPOINT, params=news_params)

articles = news_response.json()["articles"]

first_three_articles = articles[:3]

#MESSAGE FORMAT
formatted_article_list = [f"{STOCK}: {upper_down}{diffrence_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in first_three_articles]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN,)



# MESSAGE SENDER
for article in formatted_article_list: 
    message = client.messages.create(
          body = article,
          from_ = "your twilio acc number",
           to = "your number"
    )
