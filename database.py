try:
    import uuid
    from flask import Config, Flask, jsonify, request
    from flask_sqlalchemy import SQLAlchemy

    # Khởi tạo Flask app
    app = Flask(__name__)
    app.config.from_object(Config)


    # Cấu hình kết nối DB mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456Tt@localhost/ten_csd'  
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_size": 10,        # Số lượng kết nối tối đa
        "pool_recycle": 280,    # Tái sử dụng kết nối sau 280s
        "pool_timeout": 30      # Thời gian chờ trước khi timeout
    }
    # Khởi tạo SQLAlchemy
    db = SQLAlchemy(app)
    
    # Định nghĩa mô hình cơ sở dữ liệu
    class User(db.Model):
        id = db.Column(db.String(36), primary_key=True)
                      # default=lambda: str(uuid.uuid4())) # UUID random
        name = db.Column(db.String(100), nullable=False)
        age = db.Column(db.Integer, nullable=False)
        def __init__(self, **kwargs):
            self.id = str(uuid.uuid4())     # UUID random
            super(User, self).__init__(**kwargs)
        def to_json(self):
            rv = {
                "id": self.id,
                "name": self.name,
                "age": self.age                             
            }
            return rv
        
    # Khởi tạo cơ sở dữ liệu
    @app.before_request
    def create_tables():
        db.create_all()

    # Route GET: lấy danh sách người dùng
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all() # Lất tất cả người dùng
        # users = db.session.query(User).all()
        return jsonify([user.to_json() for user in users])

    # Lấy thông tin người dùng theo ID
    @app.route('/users/<string:user_id>', methods=['GET'])
    def get_user(user_id):
        print("in ",user_id)
        # user = User.query.get(user_id) # Lấy người dùng theo ID
        user = db.session.query(User).filter_by(id=user_id).first() # sử dụng session
       
        # db = next(get_db())
        # user = db.query(User).filter(User.id == user.id).first()
        if user:
            return jsonify(user.to_json())
        return jsonify({"error": "User not found"}), 404

    # Route POST: Thêm người dùng mới
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        new_user = User(name= data['name'], age= data['age'])
        
        db.session.add(new_user)    # Thêm vào database
        db.session.commit()         # Lưu thay đổi
        return jsonify({"message": "User added successfully", 
                        "user": new_user.to_json()}), 201

    # Route DELETE: Xóa người dùng theo ID
    @app.route('/users/<string:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get(user_id)  # Lấy người dùng theo ID
        if user:
            db.session.delete(user)  # Xóa người dùng
            db.session.commit()  # Lưu thay đổi
            return jsonify({"message": f"User with ID {user_id} deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
        
    # Hook: Đảm bảo đóng kết nối sau khi xử lý xong
    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db.session.remove()

    # Chạy ứng dụng Flask
    if __name__ == '__main__':
        app.run(debug=True)

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Đã xảy ra lỗi không mong muốn: {e}")