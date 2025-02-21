import requests
import os
import logging
import uuid
from flask import Config, Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import DB_CONFIG
from huggingface_api import huggingface_image_api, huggingface_video


# Cấu hình logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Khởi tạo Flask app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG["SQLALCHEMY_DATABASE_URI"]    # type: ignore
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = DB_CONFIG["SQLALCHEMY_TRACK_MODIFICATION"]
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = DB_CONFIG["SQLALCHEMY_ENGINE_OPTIONS"]

app.config['UPLOAD_FOLDER'] = os.path.expanduser("~/Picture")  # Sử dụng thư mục mặc định của hệ thống
#API URL Hugging Face
app.config['HUGGINGFACE_API_KEY'] = DB_CONFIG["HUGGINGFACE_API_KEY"]
app.config['IMAGE_API_URL'] = DB_CONFIG["IMAGE_API_URL"]

# URL của mô hình
app.config['VIDEO_API_URL'] = "https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w"



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
    return handle_404_error(e)


# Route Update: chỉnh sửa người dùng
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.name = data['name']
        user.age = data['age']
        db.session.commit()
        return jsonify({"message": "User updated successfully", "user": user.to_json()}), 200
    return handle_404_error("User not found")

# Route DELETE: Xóa người dùng theo ID
@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)  # Lấy người dùng theo ID
    if user:
        db.session.delete(user)  # Xóa người dùng
        db.session.commit()  # Lưu thay đổi
        return jsonify({"message": f"User with ID {user_id} deleted successfully"}), 200
    else:
        return handle_404_error("not found")
# Route Search: tìm kiếm   
@app.route('/users/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    users = User.query.filter(User.name.ilike(f"%{name}%")).all()
    return jsonify([user.to_json() for user in users])

    # Hook: Đảm bảo đóng kết nối sau khi xử lý xong
    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #       logger.error(f"Error during teardown: {exeption}")
    #     db.session.remove()
# Route POST: Thêm người dùng mới
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name= data['name'], age= data['age'])
    db.session.add(new_user)    # Thêm vào database
    db.session.commit()         # Lưu thay đổi
    return jsonify({"message": "User added successfully", 
                    "user": new_user.to_json()}), 201

# input >>>>>>>
# json= {
#     "id": 1,
#     "content": "nội dung",
#     "type": "image/video",
#     "description": "Tạo ảnh | dựng video 3-5s"
# }


# Đảm bảo thư mục lưu trữ tồn tại 
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route('/upload', methods=["POST"])
def create_video():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    id = data.get("id")
    content = data.get("content")
    file_type = data.get("type")
    description = data.get("description")
   
    # Kiểm tra các trường bắt buộc
    if not all([id, content, file_type, description]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        api_result = {}
        
        # Xử lý ảnh nếu file_type là "image"
        if file_type == "image":
            #Gọi API Hugging Face để tạo ảnh từ mô tả
            payload = {"inputs":description}
            image_data = huggingface_image_api(app.config['IMAGE_API_URL'] ,app.config['HUGGINGFACE_API_KEY'] , payload)
            # Kiểm tra phản hồi từ API
            if image_data and image_data.status_code == 200:
                # Lưu ảnh vào file (hoặc xử lý tùy ý)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], f"generated_image_{id}.png")
                with open(image_path, "wb") as f:
                    f.write(image_data.content)
                
                api_result = {"message": "Image generated successfully", "image_path": image_path}
            else:
                api_result = {"error": f"Failed to process image with Hugging Face API: {image_data.text}"}
        elif file_type == "video":
            payload = {"inputs": description}
            video_data = huggingface_video(app.config['VIDEO_API_URL'], app.config['HUGGINGFACE_API_KEY'], payload)

            if isinstance(video_data, bytes):  # Kiểm tra nếu phản hồi là dữ liệu nhị phân (video)
                video_path = os.path.join(app.config["UPLOAD_FOLDER"], f"generated_video_{id}.mp4")
                with open(video_path, "wb") as f:
                    f.write(video_data)
                
                api_result = {"message": "Video generated successfully", "video_path": video_path}
            else:
                api_result = {"error": f"Failed to process video with Hugging Face API: {video_data}"}

        else:
            api_result = {"message": "File is not an image or video, skipping Hugging Face API processing"}
     
        return jsonify({
            "data": {
                "id": id,
                "content": content,
                "type": file_type,
                "description": description,
                "api_result": api_result
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Trình xử lý lỗi tùy chỉnh
@app.errorhandler(404)
def handle_404_error(e):
    logger.error(f"404 Error: {e}")
    return jsonify({"error": "The requested resource was not found"}), 404

@app.errorhandler(500)
def handle_500_error(e):
    logger.error(f"500 Error: {e}")
    return jsonify({"error": "An internal server error occurred"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled Exception: {e}")
    return jsonify({"error": "An unexpected error occurred"}), 500


# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)