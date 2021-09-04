from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
app.config["SECRET_KEY"] = "541sdfge87swdkvxwfsfsmkoes49sef"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)

    # def create
    # def udpate
    # def delete
    # def get_one_admin


@app.route('/admin/login', methods=["POST"])
def login():
    data = request.get_json(force=True)

    if session['connected']:
        return {"message" : "USER_ALREADY_CONNECTED"}

    admin = Admin.query.filter_by(username=data['username']).first()
    if not admin:
        return jsonify({'message': 'BAD_USER'})

    if not check_password_hash(admin.password, data['password']):
        return jsonify({'message': 'BAD_CREDENTIAL'})

    session['connected'] = True
    session['user_connected'] = admin.public_id
    return {"message": "SUCCESS"}


@app.route('/admin/create', methods=['POST'])
def signup():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'message': 'NO_DATA'})

    pwd_generated = generate_password_hash(data['password'].strip())
    uuid = str(uuid4())
    admin = Admin(username=data['username'], public_id=uuid, password=pwd_generated)

    try:
        db.session.add(admin)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message' : 'USER_EXIST'})

    return jsonify({'message': 'SUCCESS'})

@app.route("/admin/logout", methods=['GET'])
def logout():
    session['connected'] = None
    session['user_connected'] = None
    return jsonify({"message": "SUCCESS"})

@app.route("/test_connection", methods=['GET'])
def test():
    if session['connected'] and session['user_connected']:
        return jsonify({"message" : "USER_IS_CONNECTED"})
    return jsonify({'message' : "NO_CONNECTED"})


"""

class Classe(db.Model):
    id_classe = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True)
    label = db.Column(db.String(45))

    def add_classe(self):
        db.session.add(self)
        db.session.commit()
        return True

    @classmethod
    def get_all(cls):
      
        data = cls.query.all()
        if data:
            output_data = []
            for classe in data:
                output_data.append({"code":classe.code, "label": classe.label})
            return output_data
        return False

    @classmethod
    def update_classe(cls,data):
        cls.code = data["code"]
        cls.label = data["label"]
        db.session.update()
        db.session.commit()
        return True

    #def update()
    #def delete()
    #det get_one_classe()


@app.route("/q")
def home():
    #data = Classe.get_all()
    
    if data:
        print(data)
        return "<h1>cest bien </h1> "
    return "<h1>echec</h1>"






class Etudiant(db.Model):
    id_etudiant = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100) , nullable=False)
    prenom = db.Column(db.String(100) , nullable=True)
    date_naissance = db.Column(db.DateTime)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id_classe', ondelete="SET NULL"))
    matieres = db.relationship('Note', backref=db.backref('etudiant', lazy=True) )


class Examen(db.Model):
    id_examen = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(45))


class Matiere(db.Model):
    id_matiere = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(45), nullable=False)


class Note(db.Model):
    id_note = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Float)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiant.id_etudiant', ondelete="CASCADE"))
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id_matiere', ondelete="CASCADE"))
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id_examen', ondelete="CASCADE"))

"""

if __name__ == "__main__":
    app.run(debug=True)
