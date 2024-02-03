from flask import Flask, jsonify, request
from db import SessionLocal, User
from pydantic import BaseModel
import json
import bcrypt

app = Flask(__name__)


db = SessionLocal()

class CreateUser(BaseModel):
    username: str
    password: str
    
@app.route('/register/', methods=['POST'])
def register():
    user_data = request.json
    user = CreateUser(**user_data)
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Close the database session (if not using Flask's @app.after_request)
    db.close()
    # Serialize the user data (optional)
    serialized_user = {"id": db_user.id, "username": db_user.username}  # Exclude password field
    return jsonify({"message": "User created successfully", "user": serialized_user})

@app.route('/all/', methods=['GET'])
def get_all_users():
    users = db.query(User).all()
    serialized_users = [{"id": user.id, "username": user.username} for user in users]
    return jsonify({"users": serialized_users})

@app.route('/delete/<user_id>/', methods=['DELETE'])
def delete_user(user_id: int):
    user = db.query(User).filter(User.id==user_id).first()
    db.delete(user)
    db.commit()
    db.close()
    return jsonify({"message": "user is deleted....!!!"})

@app.route('/update/<user_id>/', methods=['PATCH'])
def update_user(user_id:int):   
    update_user_data = request.json
    user = db.query(User).filter(User.id==user_id).first()
    #CHECK USER EXISTING
    if user:
        #update user object with new data
        for key, value in update_user_data.items():
            setattr(user, key, value)
        db.commit()
        return jsonify({"message": f"User with ID {user_id} updated successfully"})
    else:
        return jsonify({"message": f"User with ID {user_id} not found"})
    


if __name__ == "__main__":
    app.run(debug=True)

    

