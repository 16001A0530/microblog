import urllib
from flask import Flask
from flask import render_template, request

from datetime import datetime

from pymongo import MongoClient
from pymongo.cursor import Cursor

# def create_app():

app = Flask(__name__)

url = 'mongodb+srv://Venkatesh:Venkatesh@projects.9l17r.mongodb.net/microblog?retryWrites=true&w=majority'

try:
    client = MongoClient(url)
except ConnectionError as e:
    print(e)
else:
    app.db = client.microblog

@app.route('/home', methods=['GET', 'POST'])
def home():

    entries = []

    if request.method == 'POST':
        entry_content = request.form.get('content')
        date = datetime.today()
        # .strftime('%Y-%m-%d')
        # f_date = datetime.strptime(date, '%Y-%m-%d').strftime('%b %d')
        app.db.entries.insert(dict(content=entry_content, date=date))

    for entry in app.db.entries.find({}):
        date = entry['date'].strftime('%Y-%m-%d')

        entries.append(dict(
            content = entry['content'],
            date = date,
            f_date = datetime.strptime(date, '%Y-%m-%d').strftime('%b %d')
        ))

    return render_template('index.html', entries=entries)

# create_app()