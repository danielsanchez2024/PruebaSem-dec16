from .app import app
from flask import jsonify, request
from app.app import mongo, ObjectId

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    return jsonify([{'id': str(user['_id']), 'nombre': user['nombre'], 'correo': user['correo'], 'edad': user['edad']} for user in users])

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'id': str(user['_id']), 'nombre': user['nombre'], 'correo': user['correo'], 'edad': user['edad']})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not all(k in data for k in ('nombre', 'correo', 'edad')):
        return jsonify({'error': 'Faltan campos'}), 400
    user_id = mongo.db.users.insert_one(data).inserted_id
    return jsonify({'id': str(user_id)}), 201

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    updated = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data})
    if updated.matched_count == 0:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'message': 'Usuario actualizado'})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    deleted = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if deleted.deleted_count == 0:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'message': 'Usuario eliminado'})
