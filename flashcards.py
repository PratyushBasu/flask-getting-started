from datetime import datetime
from flask import (Flask, render_template, abort, jsonify, request, redirect, url_for)
from model import db, save_db


app = Flask(__name__)

# Flashcards home page
@app.route('/')
def welcome():
    # return 'Welcome to my Flash Cards application.'
    return render_template(
        "welcome.html",
        message = "Here's a message from view.",
        cards=db)

# Individual flash card page
@app.route('/card/<int:idx>')
def card_view(idx):
    try:
        if idx < 1 or idx > len(db):
            raise
        card=db[idx-1]
        return render_template('card.html',
                               card=card,
                               card_no=idx,
                               max_card_no=len(db))
    except:
        abort(404)

# Add flash card
@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        card = {'question': request.form['question'],
                'answer': request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('card_view', idx=len(db)))
    else:
        return render_template("add_card.html")

# Delete flash card
@app.route('/del_card/<int:idx>', methods=['GET', 'POST'])
def del_card(idx):
    try:
        if request.method == 'POST':
            if idx < 1 or idx > len(db):
                raise
            db.pop(idx-1)
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("del_card.html", card=db[idx-1])
    except:
        abort(404)

# flash cards list (api)
@app.route('/api/cards/')
def api_card_list():
    return jsonify(db)

# flash cards individual (api)
@app.route('/api/card/<int:idx>')
def api_card_detail(idx):
    try:
        if idx < 1 or idx > len(db):
            raise
        return db[idx - 1]
    except:
        abort(404)

# Add a page to show the page hit count
countr = 0
@app.route('/view_count')
def view_count():
    global countr
    countr += 1
    return 'This page has been visited {} time(s)'.format(countr)

# Date function to print time when the page was requested
@app.route('/date')
def date():
    return 'This page was served at: ' + str(datetime.now().strftime("%d-%b-%Y  %I:%M:%S %p"))


if __name__ == '__main__':
    app.run(debug=True)

    request.json