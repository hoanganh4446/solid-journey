import gspread
from google.oauth2.service_account import Credentials
import datetime

# Đọc thông tin xác thực từ tệp JSON
creds = Credentials.from_service_account_file(
    'sound-jigsaw-394510-c7746fdc8d26.json', 
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# Kết nối với Google Sheets
client = gspread.authorize(creds)

# Mở Google Sheets bằng ID (thay 'your_spreadsheet_id' bằng ID thật)
sheet = client.open_by_key('1NGvIr_m8Oay0dHoRDeD9mL5v-QqD1UPNFYbrZ93AWcY')  # Lấy ID từ URL của Google Sheets
worksheet = sheet.get_worksheet(1)  # Lấy sheet thứ 2 (chỉ số bắt đầu từ 0)

# Hàm chuyển đổi từ ISO 8601 sang định dạng "GIỜ NGÀY THÁNG NĂM"
def format_date_with_time(date_str):
    if date_str:
        # Loại bỏ phần 'T' và 'Z' khỏi chuỗi
        date_str = date_str.replace('T', ' ').replace('Z', '')
        try:
            # Chuyển chuỗi thành đối tượng datetime
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')  # Định dạng ngày giờ
            # Định dạng lại ngày giờ theo kiểu "06:42 NGÀY 22 THÁNG 6 NĂM 2025"
            return dt.strftime("%H:%M Ngày %d Tháng %m Năm %Y")  
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None
    return None

# Hàm cập nhật tất cả dữ liệu từ Airtable lên Google Sheets
def update_all(records):
    print(f"Đang xử lý {len(records)} bản ghi từ Airtable.")
    for record in records:
        fields = record.get('fields', {})
        device_id = fields.get('Device ID')
        model = fields.get('Model')
        serial_number = fields.get('Serial Number')
        start_date = format_date_with_time(fields.get('Start Date'))
        expected_end = format_date_with_time(fields.get('Expected End'))
        status = fields.get('Status')
        location = fields.get('Location')
        notes = fields.get('Notes')
        paused_time = fields.get('Paused Time (hrs)', 0)
        last_resume_time = fields.get('Last Resume Time')
        target_time = fields.get('Target Time (hours)', 0)
        running_time = fields.get('Running Time (hours)', 0)
        total_pause_time = fields.get('Total Pause Time (hours)', 0)
        last_tested_at = fields.get('Last Tested At (hours)', 0)
        test_interval = fields.get('Test Interval (hours)', 0)
        next_test = fields.get('Next Test (hours)')
        qr_link = fields.get('QR Link')

        # Lấy thời gian hiện tại để lưu vào TimeLog
        time_log = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Dữ liệu để thêm vào Google Sheets
        row = [
            time_log, device_id, model, serial_number, start_date, expected_end, status, location, notes, paused_time, last_resume_time, 
            target_time, running_time, total_pause_time, last_tested_at, test_interval, next_test, qr_link,  
            # Thêm TimeLog vào cuối
        ]

        # Thêm dữ liệu vào Google Sheets
        worksheet.append_row(row)  # append_row sẽ thêm dữ liệu vào cuối bảng
        print(f"✅ Đã thêm dữ liệu cho thiết bị {device_id} vào Google Sheets.")
