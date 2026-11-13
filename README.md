# TikTok Comment Crawler

Công cụ web hỗ trợ thu thập toàn bộ bình luận (bao gồm cả phản hồi/reply con) từ một video TikTok bất kỳ và xuất dữ liệu ra file CSV. 

Hệ thống kết hợp Playwright (headless browser) để tự động hóa việc xác thực phiên người dùng từ TikTok, sau đó gọi trực tiếp API nội bộ của TikTok để tải bình luận với tốc độ cao.

- **Demo trực tiếp:** [https://tiktok-comment-crawler-1.onrender.com](https://tiktok-comment-crawler-1.onrender.com)
- **Kho mã nguồn:** [https://github.com/DinhHoangPhuc3010/tiktok-comment-crawler](https://github.com/DinhHoangPhuc3010/tiktok-comment-crawler)

---

## Tính năng chính

- **Cào dữ liệu tự động:** Tự động lấy cookie phiên qua Playwright và phân trang qua API TikTok.
- **Hỗ trợ đầy đủ Reply:** Quét cả bình luận gốc lẫn các câu trả lời con bên dưới từng bình luận.
- **Xem trước trực tiếp:** Bảng hiển thị danh sách bình luận kèm phân trang và ô tìm kiếm nhanh theo nội dung hoặc tên người dùng.
- **Xuất CSV chuẩn UTF-8:** Hỗ trợ tùy chỉnh tên file khi tải về, tương thích với Microsoft Excel và Google Sheets.
- **Theo dõi tiến trình:** Hiển thị log trạng thái và số lượng dữ liệu thu thập theo thời gian thực.

---

## Cấu trúc thư mục

```text
tiktok-comment-crawler/
├── app.py              # Backend Flask (xử lý crawl đa luồng, API endpoints)
├── cmt_python.py       # Script crawl gốc dạng CLI
├── Dockerfile          # Cấu hình container chạy Playwright & Chromium
├── requirements.txt    # Danh sách thư viện Python
├── render.yaml         # Cấu hình tự động triển khai trên Render
├── Procfile            # Cấu hình WSGI Gunicorn
├── templates/
│   └── index.html      # Giao diện web chính
└── static/
    ├── css/style.css   # Giao diện
    └── js/app.js       # Xử lý tương tác, polling trạng thái và hiển thị bảng dữ liệu
```

---

## Hướng dẫn cài đặt và chạy cục bộ (Local)

### Yêu cầu hệ thống

- Python 3.10 trở lên
- pip và kết nối Internet ổn định

### Các bước thực hiện

1. **Clone repository về máy:**
   ```bash
   git clone https://github.com/DinhHoangPhuc3010/tiktok-comment-crawler.git
   cd tiktok-comment-crawler
   ```

2. **Khởi tạo môi trường ảo (khuyến nghị):**
   ```bash
   python -m venv venv
   # Trên Windows:
   venv\Scripts\activate
   # Trên macOS / Linux:
   source venv/bin/activate
   ```

3. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Cài đặt trình duyệt Chromium cho Playwright:**
   ```bash
   playwright install chromium
   ```

5. **Chạy ứng dụng:**
   ```bash
   python app.py
   ```
   Sau đó mở trình duyệt tại địa chỉ: `http://localhost:5000`

---

## Triển khai lên Render (Render.com)

Dự án đã cấu hình sẵn `Dockerfile` bao gồm Chromium và toàn bộ thư viện hệ thống cần thiết cho Playwright.

1. Đăng nhập vào [Render Dashboard](https://dashboard.render.com).
2. Chọn **New +** > **Web Service**.
3. Kết nối với repository `tiktok-comment-crawler`.
4. Tại mục **Runtime**, chọn **Docker** (Render sẽ tự động dùng file `Dockerfile`).
5. Chọn vùng đặt server (khuyến nghị: **Singapore** để có tốc độ kết nối tốt nhất).
6. Chọn gói dịch vụ (Free hoặc Starter tùy nhu cầu) và bấm **Deploy Web Service**.

---

## Cấu trúc dữ liệu file CSV xuất ra

Dữ liệu bình luận được lưu với mã hóa UTF-8 (có BOM) gồm các trường:

| Tên cột | Ý nghĩa |
|---|---|
| `cid` | ID định danh của bình luận |
| `text` | Nội dung văn bản của bình luận |
| `create_time` | Thời gian tạo (Unix timestamp) |
| `digg_count` | Số lượt thích bình luận |
| `reply_id` | ID bình luận gốc (nếu là reply con) |
| `reply_to_reply_id` | ID phản hồi trực tiếp (nếu là reply lồng nhau) |
| `reply_to_userid` | User ID của người nhận phản hồi |
| `reply_to_username` | Username của người nhận phản hồi |
| `user_nickname` | Tên hiển thị của người bình luận |
| `user_id` | UID của người bình luận |
| `user_sec_uid` | Chuỗi sec_uid định danh profile người dùng trên TikTok |

---

## Lưu ý kỹ thuật & Pháp lý

- TikTok áp dụng cơ chế giới hạn tần suất yêu cầu (rate limit). Ứng dụng đã thiết lập sẵn khoảng nghỉ giữa các request để đảm bảo kết nối ổn định.
- Công cụ chỉ hoạt động với các video ở chế độ công khai (public).
- Dự án phục vụ mục đích học tập, nghiên cứu và phân tích dữ liệu cá nhân. Người sử dụng chịu trách nhiệm tuân thủ Điều khoản sử dụng của nền tảng TikTok.
