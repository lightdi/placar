from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Placar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time1_nome = db.Column(db.String(50), nullable=False)
    time1_pontuacao = db.Column(db.Integer, nullable=False)
    time2_nome = db.Column(db.String(50), nullable=False)
    time2_pontuacao = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Placar {self.id}>'

# Cria o banco de dados e as tabelas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    placar = Placar.query.first()
    if not placar:
        placar = Placar(time1_nome='Time A', time1_pontuacao=0, time2_nome='Time B', time2_pontuacao=0)
        db.session.add(placar)
        db.session.commit()
    return render_template('index.html', placar=placar)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    placar = Placar.query.first()
    if not placar:
        placar = Placar(time1_nome='Time A', time1_pontuacao=0, time2_nome='Time B', time2_pontuacao=0)
        db.session.add(placar)
        db.session.commit()

    if request.method == 'POST':
        placar.time1_nome = request.form['time1_nome']
        placar.time1_pontuacao = int(request.form['time1_pontuacao'])
        placar.time2_nome = request.form['time2_nome']
        placar.time2_pontuacao = int(request.form['time2_pontuacao'])
        db.session.commit()
        #return redirect(url_for('index'))

    return render_template('admin.html', placar=placar)

if __name__ == '__main__':
    app.run(host="192.168.0.101", port=80, debug=True)