from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
# db.init_app(app)

class Data(db.Model):
  __tablename__ = "data"

  id        = db.Column(db.Integer, primary_key=True)
  rna_id    = db.Column(db.String(20), nullable=True)
  rna_id_ex = db.Column(db.String(20), nullable=True)
  gestion   = db.Column(db.String(20), nullable=True)

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/assos')
def assos():
  datas = Data.query.limit(10).all()
  #for data in datas:
  #  print(f"{data.rna_id}")
  
  #stmt = select(Data)
  #result = db.session.execute(stmt)
  #for data in result.scalars():
  #  print(f"{data.rna_id}")

  return render_template('assos.html', datas=datas)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)

if __name__ == '__main__':
  app.run()

@app.route('/edit/<int:id>' ,methods=['GET','POST'])
def edit(id):

  data = Data.query.get(id)

  if request.method == 'POST':
    data.rna_id = request.form['rna_id']
    data.rna_id_ex = request.form['rna_id_ex']
    data.gestion = request.form['gestion']
    db.session.commit()
    return redirect(url_for('assos'))

  return render_template('edit.html', data=data)

@app.route('/add' ,methods=['GET','POST'])
def add():

  if request.method == 'POST':
    rna_id = request.form['rna_id']
    rna_id_ex_id = request.form['rna_id_ex']
    gestion = request.form['gestion']
    new_data = Data(rna_id=rna_id, rna_id_ex=rna_id_ex, gestion=gestion)
    db.session.add(new_data)
    db.session.commit()
    return redirect(url_for('assos'))

  return render_template('add.html')
@app.route('/delete/<id>',methods=['GET','POST'])
def delete(id):

  data = Data.query.get(id)
  db.session.delete(data)
  db.session.commit()
  return redirect(url_for('assos'))

@app.route('/tableau')
def tableau():
    return render_template('tableau.html')

@app.route('/gestion')
def gestion():
  return render_template('gestion.html')

@app.route('/visualisation2')
def visualisation2():

    datas = Data.query.all()
    gestion_count = {}

    for d in datas:
        if d.gestion in gestion_count:
            gestion_count[d.gestion] += 1
        else:
            gestion_count[d.gestion] = 1

    gestion_values = list(gestion_count.values())
    gestion_labels = list(gestion_count.keys())

    data = {
        'values': gestion_values,
        'labels': gestion_labels

    }

    return render_template('visualisation2.html', graph_data=json.dumps(data))

@app.route('/radar')
def radar():
    data = {
        'labels': ['011S', '012P', '013S', '014S'],
        'datasets': [{
            'label': 'gestion',
            'data': [1542, 3994, 1346, 1840],
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': 1
        }]
    }

    config = {
        'type': 'radar',
        'data': data,
        'options': {
            'scales': {
                'r': {'beginAtZero': True}
            }
        }
    }

    return render_template('radar.html', config=config)


if __name__ == '_main_':

    app.run()