import csv
import time
from playwright.sync_api import sync_playwright
import requests

post_url = 'https://www.tiktok.com/@aifuture1230/video/7559970565407149319?q=AI%20video%20vietnam&t=1793238863257'
post_id = post_url.split('/')[-1].split('?')[0] # Lọc sạch id video tránh dính tham số thừa

all_comments = []
captured_cookies = {}
captured_headers = {}

print("Đang khởi động trình duyệt để mở video và kích hoạt khung comment...")

# --- BƯỚC 1: DÙNG PLAYWRIGHT ĐỂ GIẢ LẬP HÀNH VI CLICK MỞ COMMENT ---
with sync_playwright() as p:
    # Mở trình duyệt (để headless=False để bạn thấy nó thao tác trực quan)
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    # Bắt sự kiện mạng để hứng request API comment thực tế từ TikTok
    def handle_request(route, request):
        # Cho phép request đi qua bình thường nhưng ta có thể lấy thông tin headers nếu cần
        route.continue_()

    page.goto(post_url, timeout=60000)
    time.sleep(3) # Chờ trang load xong cơ bản

    try:
        print("Đang tìm và click vào mục/nút comment theo XPath của bạn...")
        xpath_comment_button = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div/button/div/div/span'
        
        # Đợi nút xuất hiện và click vào nó
        page.wait_for_selector(f"xpath={xpath_comment_button}", timeout=10000)
        page.locator(f"xpath={xpath_comment_button}").click()
        
        print("Đã click thành công! Đang chờ TikTok tải API comment...")
        time.sleep(5) # Chờ API comment được gọi và trả về dữ liệu trên trình duyệt
        
    except Exception as e:
        print(f"Không tìm thấy hoặc không click được vào nút comment qua XPath: {e}")
        print("Tiếp tục thử chạy cào API dự phòng...")

    # Lấy cookies và một số thông tin phiên bản từ trình duyệt tự động để requests dùng chung
    cookies = context.cookies("https://www.tiktok.com")
    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    
    captured_headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': post_url,
        'cookie': cookie_str,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    
    browser.close()

print("Đã lấy được phiên làm việc hợp lệ từ trình duyệt. Bắt đầu cào hàng loạt bằng requests...")

# --- BƯỚC 2: HÀM CÀO DỮ LIỆU SỬ DỤNG HEADERS ĐÃ ĐƯỢC CẬP NHẬT COOKIE CHUẨN ---

def fetch_comments(post_id, cursor=0):
    url = f'https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={post_id}&count=20&cursor={cursor}'
    try:
        resp = requests.get(url, headers=captured_headers, timeout=10)
        return resp.json()
    except Exception as e:
        print("Lỗi khi tải comment cha:", e)
        return None

def fetch_replies(post_id, comment_id, cursor=0):
    url = f'https://www.tiktok.com/api/comment/list/reply/?aid=1988&aweme_id={post_id}&comment_id={comment_id}&count=20&cursor={cursor}'
    try:
        resp = requests.get(url, headers=captured_headers, timeout=10)
        return resp.json()
    except Exception as e:
        print("Lỗi khi tải reply:", e)
        return None

def parse_comments(data, video_id):
    rows = []
    comments = data.get('comments', [])
    for cm in comments:
        row = {
            'cid': cm.get('cid'),
            'text': cm.get('share_info', {}).get('desc') or cm.get('text'),
            'create_time': cm.get('create_time'),
            'digg_count': cm.get('digg_count'),
            'reply_id': cm.get('reply_id'),
            'reply_to_reply_id': cm.get('reply_to_reply_id'),
            'reply_to_userid': cm.get('reply_to_userid', ''),
            'reply_to_username': cm.get('reply_to_username', ''),
            'user_nickname': cm.get('user', {}).get('nickname'),
            'user_id': cm.get('user', {}).get('uid'),
            'user_sec_uid': cm.get('user', {}).get('sec_uid'),
        }
        rows.append(row)

        reply_total = cm.get('reply_comment_total', 0)
        if reply_total > 0:
            print(f" -> Đang tải {reply_total} reply cho comment ID: {cm.get('cid')}")
            reply_cursor = 0
            while True:
                reply_data = fetch_replies(video_id, cm.get('cid'), reply_cursor)
                if not reply_data or 'comments' not in reply_data:
                    break
                for rp in reply_data['comments']:
                    rp_row = {
                        'cid': rp.get('cid'),
                        'text': rp.get('share_info', {}).get('desc') or rp.get('text'),
                        'create_time': rp.get('create_time'),
                        'digg_count': rp.get('digg_count'),
                        'reply_id': rp.get('reply_id'),
                        'reply_to_reply_id': rp.get('reply_to_reply_id'),
                        'reply_to_userid': rp.get('reply_to_userid', ''),
                        'reply_to_username': rp.get('reply_to_username', ''),
                        'user_nickname': rp.get('user', {}).get('nickname'),
                        'user_id': rp.get('user', {}).get('uid'),
                        'user_sec_uid': rp.get('user', {}).get('sec_uid'),
                    }
                    rows.append(rp_row)
                
                if reply_data.get('has_more') == 1:
                    reply_cursor = reply_data.get('cursor', reply_cursor + 20)
                    time.sleep(0.5)
                else:
                    break
    return rows

# --- BƯỚC 3: VÒNG LẶP CHÍNH ĐỂ CÀO TOÀN BỘ ---
cursor = 0
page = 1
print("Bắt đầu cào dữ liệu bình luận TikTok...")

while True:
    print(f"Đang tải trang comment số {page} (cursor={cursor})...")
    data = fetch_comments(post_id, cursor)
    if not data:
        print("Không nhận được dữ liệu hoặc hết kết nối.")
        break
        
    rows = parse_comments(data, post_id)
    if rows:
        all_comments.extend(rows)
        print(f" -> Đã lấy tổng cộng {len(rows)} mục (cha + con) từ trang này.")
    
    if data.get('has_more') == 1:
        cursor = data.get('cursor', cursor + 20)
        page += 1
        time.sleep(1)
    else:
        print("Đã quét hết toàn bộ bình luận.")
        break

# Lưu ra CSV
keys = ['cid','text','create_time','digg_count','reply_id','reply_to_reply_id','reply_to_userid','reply_to_username','user_nickname','user_id','user_sec_uid']
output_filename = 'tiktok_comments_test_2.csv'
with open(output_filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(all_comments)

print(f"Thành công! Đã lưu {len(all_comments)} comments/replies vào file {output_filename}")