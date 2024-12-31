
# Cấu hình kết nối DB mysql

DB_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://root:123456Tt@localhost/ten_csd",
    "SQLALCHEMY_TRACK_MODIFICATION": "FALSE",
    "SQLALCHEMY_ENGINE_OPTIONS":
    {
        "pool_size": 10,        # Số lượng kết nối tối đa
        "pool_recycle": 280,    # Tái sử dụng kết nối sau 280s
        "pool_timeout": 30      # Thời gian chờ trước khi timeout
    },

}