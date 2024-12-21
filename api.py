# from flask import Flask, jsonify, request
# from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Khởi tạo ứng dụng Flask
# app = Flask(__name__)

# # Dữ liệu giả định (mock data)
# data = [
#     {"id": 1, "name": "Alice", "age": 25},
#     {"id": 2, "name": "Bob", "age": 30},
#     {"id": 3, "name": "Charlie", "age": 35}
# ]
# #--------------------------------------------------------------------------
# # Route GET: Lấy danh sách người dùng
# @app.route('/users', methods=['GET'])
# def get_users():
#     return jsonify(data), 200

# # Route GET: Lấy thông tin một người dùng theo ID
# @app.route('/users/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     user = next((user for user in data if user['id'] == user_id), None)
#     if user:
#         return jsonify(user), 200
#     return jsonify({"error": "User not found"}), 404

# # Route POST: Tạo người dùng mới
# @app.route('/users', methods=['POST'])
# def create_user():
#     new_user = request.get_json()
#     if not new_user or not 'name' in new_user or not 'age' in new_user:
#         return jsonify({"error": "Invalid input"}), 400
#     new_user['id'] = len(data) + 1
#     data.append(new_user)
#     return jsonify(new_user), 201

# # Route PUT: Cập nhật thông tin người dùng
# @app.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     user = next((user for user in data if user['id'] == user_id), None)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     update_data = request.get_json()
#     user.update(update_data)  # Cập nhật thông tin người dùng
#     return jsonify(user), 200

# # Route DELETE: Xóa người dùng
# @app.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     print(data)
#     # global data
#     data = [user for user in data if user['id'] != user_id]
#     return jsonify({"message": "User deleted successfully"}), 200

# # Chạy ứng dụng Flask
# if __name__ == '__main__':
#     app.run(debug=True)
