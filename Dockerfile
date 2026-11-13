FROM python:3.11-slim

# Ngăn Python tạo .pyc và bật log trực tiếp
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Cài đặt libatomic1 và ca-certificates để Playwright Node.js driver chạy được trên Debian Slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatomic1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt Chromium và toàn bộ thư viện hệ thống cần thiết cho browser
RUN playwright install --with-deps chromium

# Copy toàn bộ source code
COPY . .

# Render dùng biến môi trường PORT (mặc định 10000)
ENV PORT=10000
EXPOSE 10000

# Chạy ứng dụng qua Gunicorn
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 300"]
