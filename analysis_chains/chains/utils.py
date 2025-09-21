from datetime import datetime
import pandas as pd
import socket
import os

def write_csv(df, network):
    # Lấy ngày hiện tại
    current_date = datetime.now().strftime('%d%m%Y')
    
    # Lấy thư mục chứa script này
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Lên một cấp để vào thư mục chính
    destake_dir = os.path.dirname(script_dir)
    # Tạo đường dẫn thư mục data
    data_test_dir = os.path.join(destake_dir, 'data')
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(data_test_dir, exist_ok=True)
    
    # Thêm ngày vào tên file
    csv_file = os.path.join(data_test_dir, f'{current_date}_{network}.csv')
    
    # Ghi DataFrame vào file CSV
    df.to_csv(csv_file, index=False)
    print(f'Dữ liệu đã được ghi vào {csv_file}')

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except Exception as e:
        return str(e)