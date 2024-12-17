import mysql.connector
from mysql.connector import Error

try:
    # Kết nối đến MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456Tt",
        database="ten_csd"
    )

    if connection.is_connected():
        print("Kết nối thành công!")

     # Tạo con trỏ để thao tác với CSDL
    cursor = connection.cursor()

    # Thực hiện lệnh SQL
    sql_code = '''
        SELECT *
        FROM shop;
    '''
    cursor.execute(sql_code)

    # Lấy kết quả truy vấn
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Error as e:
    print(f"Lỗi khi kết nối đến MySQL: {e}")
    
finally:
    # Đảm bảo đóng kết nối
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Kết nối đã được đóng.")