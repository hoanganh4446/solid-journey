import time
from threading import Thread
from modules import google_sheets  # Mã cập nhật Google Sheets
from modules import airtable  # Mã lấy dữ liệu từ Airtable

# Hàm cập nhật mỗi 4 giờ vào Google Sheets
def update_google_sheets():
    while True:
        try:
            # Lấy tất cả các bản ghi từ Airtable
            response = airtable.fetch_records()
            if response.status_code != 200:
                print("❌ Lỗi khi lấy dữ liệu từ Airtable.")
                continue

            records = response.json().get('records', [])

            # Cập nhật dữ liệu lên Google Sheets
            google_sheets.update_all(records)
            print("✅ Đã cập nhật dữ liệu lên Google Sheets.")
        except Exception as e:
            print(f"⚠️ Lỗi: {e}")
        time.sleep(14400)  # Đợi 4 giờ = 14400 giây

# Hàm cập nhật thay đổi nhỏ mỗi 30 giây vào Google Sheets
def update_changes_google_sheets():
    last_state = {}  # Lưu trữ trạng thái trước để so sánh
    while True:
        try:
            # Lấy tất cả các bản ghi từ Airtable
            response = airtable.fetch_records()
            if response.status_code != 200:
                print("❌ Lỗi khi lấy dữ liệu từ Airtable.")
                continue

            records = response.json().get('records', [])

            # Kiểm tra và cập nhật các thay đổi
            for record in records:
                device_id = record.get('fields', {}).get('Device ID')
                if device_id:
                    if device_id in last_state and last_state[device_id] != record:
                        print(f"✅ Cập nhật thay đổi cho thiết bị {device_id}")
                        google_sheets.update_record(record)  # Cập nhật bản ghi vào Google Sheets
                    last_state[device_id] = record
        except Exception as e:
            print(f"⚠️ Lỗi: {e}")
        time.sleep(30)  # Đợi 30 giây trước khi kiểm tra lại

# Chạy cả hai hàm trong hai thread riêng biệt
if __name__ == "__main__":
    thread_google_sheets = Thread(target=update_google_sheets)
    thread_changes_google_sheets = Thread(target=update_changes_google_sheets)

    # Bắt đầu các thread
    thread_google_sheets.start()
    thread_changes_google_sheets.start()

    # Đảm bảo các thread chạy liên tục
    thread_google_sheets.join()
    thread_changes_google_sheets.join()

    print("✅ Hoàn thành cập nhật dữ liệu lên Google Sheets.")
