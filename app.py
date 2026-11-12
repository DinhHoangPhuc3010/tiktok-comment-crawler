"""
TikTok Comment Crawler - Flask Web Application
Dựa trên logic từ cmt_python.py
"""

import csv
import io
import json
import os
import threading
import time
import uuid
from datetime import datetime

from flask import Flask, Response, jsonify, render_template, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "tiktok-crawler-secret-2024")

# Thư mục lưu file CSV tạm thời
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lưu trạng thái các job crawl theo session_id
crawl_jobs = {}


# ─────────────────────────────────────────────────────────────
# CORE CRAWL LOGIC (từ cmt_python.py)
# ─────────────────────────────────────────────────────────────

def do_crawl(job_id: str, post_url: str, filename: str):
    """Hàm chạy trong thread riêng để crawl comment TikTok."""
    job = crawl_jobs[job_id]
    job["status"] = "running"
    job["logs"] = []
    job["comments"] = []
    job["total"] = 0

    def log(msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {msg}"
        job["logs"].append(entry)
        print(entry)

    try:
        # Import playwright ở đây để tránh lỗi khi chạy thread
        from playwright.sync_api import sync_playwright
        import requests as req_lib

        post_id = post_url.split("/")[-1].split("?")[0]
        job["post_id"] = post_id

        log("Đang khởi động trình duyệt để lấy session cookie từ TikTok...")

        captured_headers = {}

        # BƯỚC 1: Dùng Playwright lấy cookies hợp lệ
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            log(f"Đang mở trang TikTok: {post_url[:60]}...")
            page.goto(post_url, timeout=60000)
            time.sleep(3)

            try:
                log("Đang tìm và click vào nút comment...")
                xpath_comment_button = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div/button/div/div/span'
                page.wait_for_selector(f"xpath={xpath_comment_button}", timeout=10000)
                page.locator(f"xpath={xpath_comment_button}").click()
                log("Đã click nút comment! Chờ TikTok tải API...")
                time.sleep(5)
            except Exception as e:
                log(f"Không click được nút comment ({e}), tiếp tục với cookies hiện có...")

            cookies = context.cookies("https://www.tiktok.com")
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])

            captured_headers = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "referer": post_url,
                "cookie": cookie_str,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            }

            browser.close()

        log("Đã lấy session hợp lệ. Bắt đầu cào comment bằng API...")

        # BƯỚC 2: Hàm gọi API
        def fetch_comments(pid, cursor=0):
            url = f"https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={pid}&count=20&cursor={cursor}"
            try:
                resp = req_lib.get(url, headers=captured_headers, timeout=10)
                return resp.json()
            except Exception as e:
                log(f"Lỗi tải comment cha: {e}")
                return None

        def fetch_replies(pid, comment_id, cursor=0):
            url = f"https://www.tiktok.com/api/comment/list/reply/?aid=1988&aweme_id={pid}&comment_id={comment_id}&count=20&cursor={cursor}"
            try:
                resp = req_lib.get(url, headers=captured_headers, timeout=10)
                return resp.json()
            except Exception as e:
                log(f"Lỗi tải reply: {e}")
                return None

        def parse_comments(data, video_id):
            rows = []
            comments = data.get("comments", [])
            for cm in comments:
                row = {
                    "cid": cm.get("cid"),
                    "text": cm.get("share_info", {}).get("desc") or cm.get("text"),
                    "create_time": cm.get("create_time"),
                    "digg_count": cm.get("digg_count"),
                    "reply_id": cm.get("reply_id"),
                    "reply_to_reply_id": cm.get("reply_to_reply_id"),
                    "reply_to_userid": cm.get("reply_to_userid", ""),
                    "reply_to_username": cm.get("reply_to_username", ""),
                    "user_nickname": cm.get("user", {}).get("nickname"),
                    "user_id": cm.get("user", {}).get("uid"),
                    "user_sec_uid": cm.get("user", {}).get("sec_uid"),
                }
                rows.append(row)

                reply_total = cm.get("reply_comment_total", 0)
                if reply_total > 0:
                    log(f"  → Đang tải {reply_total} reply cho comment {cm.get('cid')}...")
                    reply_cursor = 0
                    while True:
                        reply_data = fetch_replies(video_id, cm.get("cid"), reply_cursor)
                        if not reply_data or "comments" not in reply_data:
                            break
                        for rp in reply_data["comments"]:
                            rp_row = {
                                "cid": rp.get("cid"),
                                "text": rp.get("share_info", {}).get("desc") or rp.get("text"),
                                "create_time": rp.get("create_time"),
                                "digg_count": rp.get("digg_count"),
                                "reply_id": rp.get("reply_id"),
                                "reply_to_reply_id": rp.get("reply_to_reply_id"),
                                "reply_to_userid": rp.get("reply_to_userid", ""),
                                "reply_to_username": rp.get("reply_to_username", ""),
                                "user_nickname": rp.get("user", {}).get("nickname"),
                                "user_id": rp.get("user", {}).get("uid"),
                                "user_sec_uid": rp.get("user", {}).get("sec_uid"),
                            }
                            rows.append(rp_row)
                        if reply_data.get("has_more") == 1:
                            reply_cursor = reply_data.get("cursor", reply_cursor + 20)
                            time.sleep(0.5)
                        else:
                            break
            return rows

        # BƯỚC 3: Vòng lặp cào toàn bộ
        all_comments = []
        cursor = 0
        page_num = 1

        while True:
            if job.get("cancelled"):
                log("Người dùng đã huỷ crawl.")
                break

            log(f"Đang tải trang comment #{page_num} (cursor={cursor})...")
            data = fetch_comments(post_id, cursor)

            if not data:
                log("Không nhận được dữ liệu hoặc hết kết nối.")
                break

            rows = parse_comments(data, post_id)
            if rows:
                all_comments.extend(rows)
                job["comments"] = all_comments
                job["total"] = len(all_comments)
                log(f"  → Lấy được {len(rows)} mục trang này. Tổng: {len(all_comments)}")

            if data.get("has_more") == 1:
                cursor = data.get("cursor", cursor + 20)
                page_num += 1
                time.sleep(1)
            else:
                log("✅ Đã quét hết toàn bộ bình luận!")
                break

        # Lưu ra CSV
        if all_comments:
            keys = [
                "cid", "text", "create_time", "digg_count",
                "reply_id", "reply_to_reply_id", "reply_to_userid",
                "reply_to_username", "user_nickname", "user_id", "user_sec_uid",
            ]
            safe_filename = filename if filename.endswith(".csv") else filename + ".csv"
            filepath = os.path.join(UPLOAD_FOLDER, f"{job_id}_{safe_filename}")
            with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(all_comments)

            job["csv_path"] = filepath
            job["csv_name"] = safe_filename
            log(f"✅ Đã lưu {len(all_comments)} comments vào {safe_filename}")

        job["status"] = "done"

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
        job["logs"].append(f"[ERROR] {str(e)}")
        print(f"Crawl error: {e}")


# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/crawl/start", methods=["POST"])
def start_crawl():
    data = request.get_json()
    post_url = (data or {}).get("url", "").strip()
    filename = (data or {}).get("filename", "tiktok_comments").strip() or "tiktok_comments"

    if not post_url or "tiktok.com" not in post_url:
        return jsonify({"error": "URL TikTok không hợp lệ!"}), 400

    job_id = str(uuid.uuid4())
    crawl_jobs[job_id] = {
        "status": "pending",
        "logs": [],
        "comments": [],
        "total": 0,
        "csv_path": None,
        "csv_name": None,
        "cancelled": False,
        "post_url": post_url,
        "filename": filename,
        "created_at": datetime.now().isoformat(),
    }

    thread = threading.Thread(target=do_crawl, args=(job_id, post_url, filename), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/api/crawl/status/<job_id>")
def crawl_status(job_id):
    job = crawl_jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job không tồn tại"}), 404

    return jsonify({
        "status": job["status"],
        "total": job["total"],
        "logs": job["logs"][-30:],  # Chỉ trả 30 log gần nhất
        "has_csv": job["csv_path"] is not None,
        "csv_name": job["csv_name"],
        "error": job.get("error"),
    })


@app.route("/api/crawl/comments/<job_id>")
def get_comments(job_id):
    job = crawl_jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job không tồn tại"}), 404

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    search = request.args.get("search", "").strip().lower()

    comments = job.get("comments", [])

    if search:
        comments = [
            c for c in comments
            if search in (c.get("text") or "").lower()
            or search in (c.get("user_nickname") or "").lower()
        ]

    total = len(comments)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = comments[start:end]

    return jsonify({
        "comments": paginated,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total > 0 else 1,
    })


@app.route("/api/crawl/cancel/<job_id>", methods=["POST"])
def cancel_crawl(job_id):
    job = crawl_jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job không tồn tại"}), 404
    job["cancelled"] = True
    return jsonify({"message": "Đã gửi lệnh huỷ"})


@app.route("/api/crawl/download/<job_id>")
def download_csv(job_id):
    job = crawl_jobs.get(job_id)
    if not job or not job.get("csv_path"):
        return jsonify({"error": "File CSV chưa sẵn sàng"}), 404

    csv_path = job["csv_path"]
    if not os.path.exists(csv_path):
        return jsonify({"error": "File không tồn tại trên server"}), 404

    return send_file(
        csv_path,
        mimetype="text/csv; charset=utf-8",
        as_attachment=True,
        download_name=job["csv_name"],
    )


@app.route("/api/jobs")
def list_jobs():
    result = []
    for jid, job in crawl_jobs.items():
        result.append({
            "job_id": jid,
            "status": job["status"],
            "total": job["total"],
            "post_url": job.get("post_url", ""),
            "csv_name": job.get("csv_name", ""),
            "created_at": job.get("created_at", ""),
        })
    return jsonify(sorted(result, key=lambda x: x["created_at"], reverse=True))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)

