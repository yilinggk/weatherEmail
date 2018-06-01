import datetime
import smtplib
import requests
import json
from email.mime.text import MIMEText
from settings import mail_settings, send_to_addresses, send_to_names, api_key, city_name, country_code, numPeople


def fetch_forecast(api_key, request_type, city_name, country_code):
    weather_url = 'http://api.openweathermap.org/data/2.5/' +\
                  request_type + '?q=' + city_name + ',' + country_code +\
                  '&units=metric&APPID=' + api_key
    r = requests.get(weather_url)
    j = json.loads(r.text)
    return j


def build_email_html(forecast_json, nameNum):
    # build HTML to open and close email
    html_open = """\
    <html>
        <head></head>
        <body>
    """
    html_close = """\
        </body>
    </html>
    """

    # HTML body contents
    month = datetime.date.today().strftime("%B")
    day_of_week = datetime.date.today().strftime("%A")
    day_of_month = datetime.date.today().strftime("%d")

    mail_text = '<h3>Hello, ' + send_to_names[nameNum] +\
        '!</h3><p>Here is the ' + city_name + ' weather forecast ' +\
        'as of this ' + day_of_week + ', ' + month + ' ' + day_of_month + ' morning!</p>'

    weather_text = '<p><b>' + forecast_json['weather'][0]['description'] + '</b></p><p>' +\
        'Temperature: ' + str(forecast_json['main']['temp']) + ' degrees C</p><p>' +\
        'Low of: ' + str(forecast_json['main']['temp_min']) + ' degrees C</p><p>' +\
        'High of: ' + str(forecast_json['main']['temp_max']) + ' degrees C</p><p>' +\
        'Wind Speed: ' + str(forecast_json['wind']['speed']) + ' m/s</p><p>' +\
        'Cloudiness: ' + str(forecast_json['clouds']['all']) + '%</p><p>' +\
        'Humidity: ' + str(forecast_json['main']['humidity']) + '%</p>'

    # adding HTML elements together
    html_body = html_open + mail_text + weather_text + html_close

    return html_body


def send_email(mail_text, nameNum):
    # find the current time and add that to the email subject
    cur_date = datetime.date.today().strftime("%B") +\
        ' ' + datetime.date.today().strftime("%d") +\
        ', ' + datetime.date.today().strftime("%Y")

    subject = 'Daily Forecast for ' + cur_date

    COMMASPACE = ', '

    msg = MIMEText(mail_text, 'html')
    msg['Subject'] = subject
    msg['From'] = mail_settings['from']
    msg['To'] = send_to_addresses[nameNum]

    server = smtplib.SMTP_SSL(mail_settings['smtp'], 465)
    server.login(mail_settings['address'], mail_settings['pw'])
    server.set_debuglevel(1)
    server.sendmail(mail_settings['address'], send_to_addresses[nameNum], msg.as_string())
    server.quit()


if __name__ == "__main__":
    for i in range(0, numPeople):
        forecast_json = fetch_forecast(api_key, 'weather', city_name, country_code)
        mail_text = build_email_html(forecast_json, i)
        send_email(mail_text, i)







