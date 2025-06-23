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

# Chạy hàm cập nhật dữ liệu lên Google Sheets
if __name__ == "__main__":
    thread_google_sheets = Thread(target=update_google_sheets)
    thread_google_sheets.start()
    thread_google_sheets.join()  # Đảm bảo thread này chạy liên tục
    print("✅ Hoàn thành cập nhật dữ liệu lên Google Sheets.")
