from flask import Flask, jsonify, request, abort
from db import SessionLocal, User, Order
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


def serialize_user(user):
    return {"id": user.id, "username": user.username}


@app.route('/all/<user_id>/', methods=['GET'])
def get_all_users(user_id):
    try:
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            return jsonify({"user": serialize_user(user)} if user else {"message": "User not found"})

        users = db.query(User).all()
        serialized_users = [serialize_user(user) for user in users]
        return jsonify({"users": serialized_users})
    finally:
        db.close()


@app.route('/delete/<user_id>/', methods=['DELETE'])
def delete_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    db.close()
    return jsonify({"message": "user is deleted....!!!"})


@app.route('/update/<user_id>/', methods=['PATCH'])
def update_user(user_id: int):
    update_user_data = request.json
    user = db.query(User).filter(User.id == user_id).first()
    # CHECK USER EXISTING
    if user:
        # update user object with new data
        for key, value in update_user_data.items():
            setattr(user, key, value)
        db.commit()
        return jsonify({"message": f"User with ID {user_id} updated successfully"})
    else:
        return jsonify({"message": f"User with ID {user_id} not found"})


###place order for users

class OrderCreate(BaseModel):
    user_id: int
    order_name: str
    order_quantity: int


@app.route('/place-order/', methods=['POST'])
def place_order():
    order_data = OrderCreate(**request.json)
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        abort(404, description="User not found")

    new_order = Order(name=order_data.order_name, quantity=order_data.order_quantity)
    user.orders.append(new_order)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.close()

    return jsonify({"message": "Order placed successfully"})


def serialize_orders(order):
    return {"id": order.id, "order name": order.name, "order quantity": order.quantity}


@app.route('/all-orders/', methods=['GET'])
def get_orders():
    orders = db.query(Order).all()
    serialized_orders = [serialize_orders(order) for order in orders]
    return jsonify({"orders": serialized_orders})


if __name__ == "__main__":
    app.run(debug=True)
