import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')
client = Client(account_sid, auth_token)

OWM_API_KEY = os.environ.get('OWM_API_KEY')
OWM_Endpoint = 'https://api.openweathermap.org/data/2.5/onecall'
seoul_lat = 37.590000
seoul_lon = 127.016500
london_lat = 51.507351
london_lon = -0.127758
parameters = {
    'appid': OWM_API_KEY,
    'lat': seoul_lat,
    'lon': seoul_lon,
    'exclude': 'current,minutely,alerts,daily'
}

response = requests.get(url=OWM_Endpoint, params=parameters)
response.raise_for_status()
data = response.json()
hourly = data['hourly']

need_umbrella: bool = False
for hour in hourly[:12]:
    condition = hour['weather'][0]['id']
    if condition < 700:
        need_umbrella = True
        break

if need_umbrella:  # only set up the client if you actually need to send an email to it, otherwise you are wasting!
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="Hey Hamza, It will rain today, carry an umbrella!",
        from_='+14423336371',
        to='+821098999793'
    )

    print(message.sid)
    print(message.status)
