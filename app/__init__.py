from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__,'/instance')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gear.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=365)
app.secret_key = os.urandom(16)
db = SQLAlchemy(app)

class gearDb(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    brand = db.Column(db.String(40))
    current = db.Column(db.Boolean)
    sizeCode = db.Column(db.String(40))
    color = db.Column(db.String(40))
    lobes = db.Column(db.Integer)
    weightG = db.Column(db.Float)
    strengthKn = db.Column(db.Float)
    fullName = db.Column(db.String(80))
    lowFitMm = db.Column(db.Float)
    upFitMm = db.Column(db.Float)

    def __repr__(self):
        return '<Gear %r>' % self.id



def refresh(operation=None, items=[]):
    print('Entering refresh with operation: ', operation, ' and items: ', items)
    if 'aRack' not in session:
        session['aRack'] = {}
    if 'brand' not in session:
        session['brand'] = '*ALL*'
    if operation == 'add' and not items == False:
        for item in items:
            if item in session['aRack']:
                session['aRack'][item] += 1
            else:
                session['aRack'][item] = 1
        print('Completed Add')
    elif operation == 'rem' and not items == False:
        for item in items:
            try:
                session['aRack'].pop(item)
            except:
                print('Tried to remove item which does not exist.')
        print('Completed Rem')
    session.modified = True
    print('aRack now is: ', session['aRack'])
    print('brand now is: ', session['brand'])
    return


def getData():
    print('Getting Data from session aRack: ', session['aRack'])
    data = db.session.query(gearDb).filter(gearDb.id.in_(
        list(session['aRack'].keys()))).order_by(gearDb.id).all()
    session['data'] = [{key: item.__dict__[key] for key in item.__dict__.keys(
    ) if key != '_sa_instance_state'} for item in data]
    session.modified = True
    return data


@app.route('/')
def landing():
    return render_template('/landing.html')

@app.route('/graph')
def index():
    refresh()  # refreshes
    arack = getData()  # gets data from the current session
    if session['brand'] == '*ALL*':
        gear = gearDb.query.order_by(gearDb.brand).all()
    else:
        gear = gearDb.query.filter(
            gearDb.brand == session['brand']).order_by(gearDb.id).all()
    brands = [item[0] for item in db.session.query(
        gearDb.brand).distinct(gearDb.brand).all()]
    return render_template('/index.html', gear=gear, brands=brands, arack=arack)


@app.route('/query')
def query():
    session['brand'] = request.args.get('selectBrand')
    return redirect('/graph')


@app.route('/add')
def add():
    print('Adding to Rack: ', list(request.args.keys()))
    arack = refresh('add', list(request.args.keys()))
    return redirect('/graph')


@app.route('/rem')
def rem():
    print('Removing from Rack: ', list(request.args.keys()))
    arack = refresh('rem', request.args.keys())
    return redirect('/graph')


@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/anotherpath')
def anotherpath():
    print('In anotherpath route :', list(request.args.keys()))
    return render_template('/about.html')

@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


if __name__ == '__main__':
    app.run()
