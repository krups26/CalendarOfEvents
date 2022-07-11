from io import BytesIO
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy 
import urllib.request as urllib2
import ssl, json
import subprocess
import datetime
import time
import calendar
from datetime import date
import pdfkit

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home ():
    return render_template('home.html')

@app.route('/print_template', methods=['GET', 'POST'])
def index():
   # if request.get_method == 'POST':
        #file = request.files['file']
        #return f'Uploaded: {file.filename}'
    #return render_template('home.html')


    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    oneweek = datetime.timedelta(days=6)
    week = today + oneweek
    day = datetime.date.today().weekday()
    firstday = today
    lastday = week        

    f_search = firstday.strftime("%Y-%m-%d")
    t_search = lastday.strftime("%Y-%m-%d")

    url = "https://indico.cern.ch/export/categ/0.json?f=2022-07-01&t=2022-07-01&order=start" + f_search + "&t=" + t_search + "&order=start"
    print(url)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request, context=ssl._create_unverified_context())
    data = json.loads(response.read())
    n=data['count']
    # print(n)
    # print(data)


    body = """
    <!-- daa.html -->

    <body>
        <html>

        <head>
            <title>TIFR</title>
            <style>
                body {
                    height: 1000px;
                    width: 850px;
                    margin-left: auto;
                    margin-right: auto;
                }
            </style>

        </head>


        <body topmargin="50px" bottommargin="50px" leftmargin="50px" rightmargin="50px">
            <center>
                <h2>TATA INSTITUTE OF FUNDAMENTAL RESEARCH</h2>
                <h1><b>
                        <font color="blue"><i>Department of Astronomy & Astrophysics</i></font>
                    </b></h1>
                    

            </center>
            <center>
                <h1> Seminar</h1>
            </center>
            <hr>
            <P style="margin-left: 20px;">
            <table>
                <tr>
                    <td style="width: 200px;">
                        <h3> Title </h3>
                    </td>
                    <td style="width: 40px; text-align: center;">
                        <h3> : </h3>
                    </td>
                    <td>
                        <h3> MAIN_TITLE </h3>
                    </td>
                </tr>
                <tr>
                    <td style="width: 200px;">
                        <h3> url </h3>
                    </td>
                    <td style="width: 40px; text-align: center;">
                        <h3> : </h3>
                    </td>
                    <td>
                        <h3> MAIN_URL </h3>
                    </td>
                </tr>
                <tr>
                    <td style="width: 200px;">
                        <h3> Start Date & Time </h3>
                    </td>
                    <td style="width: 40px; text-align: center;">
                        <h3> : </h3>
                    </td>
                    <td>
                        <h3> MAIN_START_DATE_DATE at MAIN_START_DATE_TIME </h3>
                    </td>
                </tr>
                <tr>
                    <td style="width: 200px;">
                        <h3> End Date & Time </h3>
                    </td>
                    <td style="width: 40px; text-align: center;">
                        <h3> : </h3>
                    </td>
                    <td>
                        <h3> MAIN_END_DATE_DATE at MAIN_END_DATE_TIME </h3>
                    </td>
                </tr>
                <tr>
                    <td style="width: 200px;">
                        <h3> Location </h3>
                    </td>
                    <td style="width: 40px; text-align: center;">
                        <h3> : </h3>
                    </td>
                    <td>
                        <h3> MAIN_LOCATION </h3>
                    </td>
                </tr>
            </table>
            </p>

            <h3>
                <center> <u> Abstract: </u> </center>
            </h3>
            <h3 style="text-align: justify"> MAIN_DESCRIPTION </h3>

            <h3 style="text-align: right; margin-top: 100px"> MAIN_ORGANIZER <br> (Organizer, ASET Forum) </h3>
        </body>

        </html>
    """

    body=body.replace('MAIN_TITLE',data['results'][0]['title'])
    body=body.replace('MAIN_DESCRIPTION',data['results'][4]['description'])
    body=body.replace('MAIN_START_DATE',data['results'][0]['startDate']['date'])
    body=body.replace('MAIN_END_DATE',data['results'][0]['endDate']['date'])
    body=body.replace('MAIN_LOCATION',data['results'][0]['location'])
    body=body.replace('MAIN_ADDRESS',data['results'][0]['address'])
    body=body.replace('MAIN_ORGANIZER',data['results'][0]['organizer'])
    body=body.replace('MAIN_URL',data['results'][0]['url'])

    pdfkit.from_string(body, 'SK.pdf') #with --page-size=Legal and --orientation=Landscape


@app.route('/search')
def search():
    return render_template('search_date.html')

@app.route('/daydate')
def daydate():
    return render_template('calendar.html')    

@app.route('/template')
def choose_template():
    return render_template('choose_template.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') ,404


if __name__ == '__main__':
    app.debug = True
    app.run()