from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import jsonify,request

# initialize flask app

app = Flask(__name__)
CORS(app)

# config database url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:your_password@localhost/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize the database
db = SQLAlchemy(app)


#setup model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def to_json(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
        
with app.app_context():
        db.create_all()        



@app.route("/api/user/<int:user_id>", methods = ["PATCH"])
def update_contact(user_id):
    user = Users.query.get(user_id)
    
    if not user:
        return jsonify({"message": "user not found"}), 404
    
    data = request.json
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    
    db.session.commit()
    
    return jsonify({"message": "user updated"}), 200

@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get(user_id)
    
    if not user:
        return jsonify({"message": "user not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message":"user deleted"}), 200

@app.route("/api/user", methods=["GET"])
def getUser():
    users = Users.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@app.route("/api/user", methods = ["POST"])
def createUser():
    name = request.json.get("name")
    email = request.json.get("email")
    
    if not name or not email:
        return{
            jsonify({"message": "you must include a name and an email"}),
            400,
        }
        
    new_user = Users(name = name, email = email)
    try:
        db.session.add(new_user)
        db.session.commit()  
    except Exception as e:
        return jsonify({"message": str(e)}),400
    
    return jsonify({"message": "user added successfully"}), 201      

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
