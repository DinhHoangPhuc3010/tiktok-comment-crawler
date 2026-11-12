# 🕷️ TikTok Comment Crawler

<div align="center">

![TikTok Comment Crawler](https://img.shields.io/badge/TikTok-Comment%20Crawler-fe2c55?style=for-the-badge&logo=tiktok&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.5x-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Thu thập toàn bộ bình luận & reply từ bất kỳ video TikTok nào — ngay trên trình duyệt của bạn.**

[🚀 Demo Live](https://tiktok-comment-crawler.onrender.com) · [📖 Hướng dẫn](#-hướng-dẫn-sử-dụng) · [🐛 Báo lỗi](https://github.com/DinhHoangPhuc3010/tiktok-comment-crawler/issues)

</div>

---

## 📌 Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 🔗 **Nhập link TikTok** | Hỗ trợ mọi định dạng link video TikTok |
| 🤖 **Tự động crawl** | Dùng Playwright để lấy session hợp lệ, sau đó gọi API TikTok để thu thập toàn bộ comment |
| 💬 **Crawl cả Reply** | Thu thập comment gốc lẫn toàn bộ reply con |
| 📊 **Hiển thị trực tiếp** | Xem bình luận ngay trên web — phân trang, tìm kiếm theo nội dung/tên user |
| 📄 **Xuất CSV** | Đặt tên file tùy ý rồi tải về — mã hóa UTF-8 đầy đủ tiếng Việt |
| ⚡ **Log thời gian thực** | Theo dõi tiến trình crawl từng bước |
| 🌙 **Giao diện Dark Mode** | Thiết kế tối hiện đại, responsive trên mọi thiết bị |

---

## 📂 Cấu trúc dự án

```
tiktok-comment-crawler/
├── app.py                  # Flask backend — API routes & crawl logic
├── cmt_python.py           # Script gốc (tham khảo)
├── requirements.txt        # Thư viện Python cần thiết
├── Procfile                # Cấu hình deploy Render/Railway
├── render.yaml             # Render blueprint
├── render-build.sh         # Render build script
├── .gitignore
├── templates/
│   └── index.html          # Giao diện web chính
├── static/
│   ├── css/
│   │   └── style.css       # Stylesheet toàn bộ
│   └── js/
│       └── app.js          # Frontend logic (fetch API, table, pagination)
└── output/                 # Thư mục lưu file CSV tạm (tự tạo)
```

---

## 🚀 Hướng dẫn sử dụng

### Cách 1 — Chạy local (khuyến nghị)

#### Yêu cầu
- Python **3.10+**
- pip

#### Các bước

```bash
# 1. Clone repo
git clone https://github.com/DinhHoangPhuc3010/tiktok-comment-crawler.git
cd tiktok-comment-crawler

# 2. Tạo môi trường ảo (tùy chọn nhưng nên làm)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Cài Playwright browsers (chỉ cần làm 1 lần)
playwright install chromium

# 5. Chạy server
python app.py
```

Mở trình duyệt tại: **http://localhost:5000**

---

### Cách 2 — Deploy lên Render (miễn phí)

> ⚠️ Render miễn phí có thể bị giới hạn tài nguyên. Playwright cần **ít nhất 512MB RAM**.

1. Fork repo này về tài khoản GitHub của bạn
2. Đăng ký tài khoản tại [render.com](https://render.com)
3. Tạo **New Web Service** → kết nối với repo GitHub `DinhHoangPhuc3010/tiktok-comment-crawler`
4. Cấu hình:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium`
   - **Start Command**: `gunicorn app:app --workers 2 --timeout 300`
5. Nhấn **Deploy** và chờ hoàn thành

---

### Cách 3 — Deploy lên Railway

1. Fork repo → Đăng nhập [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub repo**
3. Thêm biến môi trường:
   - `SECRET_KEY` = chuỗi bất kỳ (ví dụ: `my-super-secret-key`)
4. Railway sẽ tự đọc `Procfile` và deploy

---

## 🖥️ Hướng dẫn giao diện

### Bước 1 — Nhập link video

```
https://www.tiktok.com/@username/video/7559970565407149319
```

Dán link vào ô **"Link video TikTok"** (hoặc nhấn nút 📋 để dán từ clipboard).

### Bước 2 — Đặt tên file CSV

Nhập tên file tùy ý (không cần đuôi `.csv`), ví dụ: `review_san_pham_A`.

### Bước 3 — Bắt đầu crawl

Nhấn **🚀 Bắt đầu Crawl**. Hệ thống sẽ:
1. Mở trình duyệt ảo (headless), tải trang TikTok để lấy cookie hợp lệ
2. Click vào khu vực comment để kích hoạt API
3. Gọi API TikTok theo từng trang (cursor-based pagination)
4. Thu thập toàn bộ comment + reply

### Bước 4 — Xem kết quả

Sau khi crawl xong, bảng bình luận hiện ra ngay bên dưới:
- **Tìm kiếm** theo nội dung hoặc tên người dùng
- **Phân trang** 50 comment/trang
- Xem loại (Gốc / Reply), số lượng ❤️

### Bước 5 — Tải về

Nhấn **⬇️ Tải file CSV về máy**. File CSV được mã hóa UTF-8 với BOM (mở được trực tiếp trong Microsoft Excel mà không bị lỗi font tiếng Việt).

---

## 📊 Cấu trúc file CSV xuất ra

| Cột | Mô tả |
|-----|-------|
| `cid` | ID comment |
| `text` | Nội dung bình luận |
| `create_time` | Thời gian đăng (Unix timestamp) |
| `digg_count` | Số lượt thích |
| `reply_id` | ID comment cha (nếu là reply) |
| `reply_to_reply_id` | ID reply cha (nếu reply lồng nhau) |
| `reply_to_userid` | User ID được reply |
| `reply_to_username` | Username được reply |
| `user_nickname` | Tên hiển thị của người comment |
| `user_id` | UID của người comment |
| `user_sec_uid` | Secure UID (dùng để tìm profile) |

---

## ⚙️ Cơ chế hoạt động

```
[User nhập URL]
      ↓
[Flask API /api/crawl/start]
      ↓
[Thread riêng: do_crawl()]
      ├── Playwright (headless Chrome)
      │     ├── Mở trang TikTok → lấy cookies hợp lệ
      │     └── Click nút comment → kích hoạt session
      │
      └── requests (API TikTok)
            ├── GET /api/comment/list/ → comment gốc (cursor pagination)
            └── GET /api/comment/list/reply/ → reply của từng comment
                ↓
         [Lưu vào memory + file CSV]
                ↓
[Frontend poll /api/crawl/status/ mỗi 2s]
      ↓
[Hiển thị bảng + cho tải CSV]
```

---

## ❓ FAQ

**Q: Tại sao crawl mất thời gian?**  
A: TikTok có cơ chế rate limiting. Hệ thống tự động chờ giữa các trang để đảm bảo không bị chặn IP hoặc huỷ session.

**Q: Có thể crawl video riêng tư (private) không?**  
A: Không. Chỉ hỗ trợ video công khai (public).

**Q: File CSV mở trong Excel có bị lỗi font không?**  
A: Không, file được xuất với chuẩn UTF-8-BOM tương thích 100% với Microsoft Excel, Google Sheets và Numbers.

---

## 🛡️ Lưu ý pháp lý

Công cụ này chỉ được phát triển cho mục đích **nghiên cứu và học thuật**. Người dùng tự chịu trách nhiệm tuân thủ Điều khoản Dịch vụ của TikTok và các quy định về bảo vệ quyền riêng tư.

---

## 📄 License

Phát hành dưới giấy phép [MIT License](LICENSE).
