# đŸ•·ï¸ TikTok Comment Crawler

<div align="center">

![TikTok Comment Crawler](https://img.shields.io/badge/TikTok-Comment%20Crawler-fe2c55?style=for-the-badge&logo=tiktok&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.5x-45ba4b?style=for-the-badge&logo=playwright&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Thu tháº­p toĂ n bá»™ bĂ¬nh luáº­n & reply tá»« báº¥t ká»³ video TikTok nĂ o â€” ngay trĂªn trĂ¬nh duyá»‡t cá»§a báº¡n.**

[đŸ€ Demo Live](https://tiktok-comment-crawler.onrender.com) Â· [đŸ“– HÆ°á»›ng dáº«n](#-hÆ°á»›ng-dáº«n-sá»­-dá»¥ng) Â· [đŸ› BĂ¡o lá»—i](https://github.com/DinhHoangPhuc3010/tiktok-comment-crawler/issues)

</div>

---

## đŸ“Œ TĂ­nh nÄƒng

| TĂ­nh nÄƒng | MĂ´ táº£ |
|-----------|-------|
| đŸ”— **Nháº­p link TikTok** | Há»— trá»£ má»i Ä‘á»‹nh dáº¡ng link video TikTok |
| đŸ¤– **Tá»± Ä‘á»™ng crawl** | DĂ¹ng Playwright Ä‘á»ƒ láº¥y session há»£p lá»‡, sau Ä‘Ă³ gá»i API TikTok Ä‘á»ƒ thu tháº­p toĂ n bá»™ comment |
| đŸ’¬ **Crawl cáº£ Reply** | Thu tháº­p comment gá»‘c láº«n toĂ n bá»™ reply con |
| đŸ“ **Hiá»ƒn thá»‹ trá»±c tiáº¿p** | Xem bĂ¬nh luáº­n ngay trĂªn web â€” phĂ¢n trang, tĂ¬m kiáº¿m theo ná»™i dung/tĂªn user |
| đŸ“„ **Xuáº¥t CSV** | Äáº·t tĂªn file tĂ¹y Ă½ rá»“i táº£i vá» â€” mĂ£ hĂ³a UTF-8 Ä‘áº§y Ä‘á»§ tiáº¿ng Viá»‡t |
| â¡ **Log thá»i gian thá»±c** | Theo dĂµi tiáº¿n trĂ¬nh crawl tá»«ng bÆ°á»›c |
| đŸŒ™ **Giao diá»‡n Dark Mode** | Thiáº¿t káº¿ tá»‘i hiá»‡n Ä‘áº¡i, responsive trĂªn má»i thiáº¿t bá»‹ |

---

## đŸ“‚ Cáº¥u trĂºc dá»± Ă¡n

```
tiktok-comment-crawler/
â”œâ”€â”€ app.py                  # Flask backend â€” API routes & crawl logic
â”œâ”€â”€ cmt_python.py           # Script gá»‘c (tham kháº£o)
â”œâ”€â”€ requirements.txt        # ThÆ° viá»‡n Python cáº§n thiáº¿t
â”œâ”€â”€ Procfile                # Cáº¥u hĂ¬nh deploy Render/Railway
â”œâ”€â”€ .gitignore
â”œâ”€â”€ templates/
â”‚   â””â”€â”€ index.html          # Giao diá»‡n web chĂ­nh
â”œâ”€â”€ static/
â”‚   â”œâ”€â”€ css/
â”‚   â”‚   â””â”€â”€ style.css       # Stylesheet toĂ n bá»™
â”‚   â””â”€â”€ js/
â”‚       â””â”€â”€ app.js          # Frontend logic (fetch API, table, pagination)
â””â”€â”€ output/                 # ThÆ° má»¥c lÆ°u file CSV táº¡m (tá»± táº¡o)
```

---

## đŸ€ HÆ°á»›ng dáº«n sá»­ dá»¥ng

### CĂ¡ch 1 â€” Cháº¡y local (khuyáº¿n nghá»‹)

#### YĂªu cáº§u
- Python **3.10+**
- pip

#### CĂ¡c bÆ°á»›c

```bash
# 1. Clone repo
git clone https://github.com/DinhHoangPhuc3010/tiktok-comment-crawler.git
cd tiktok-comment-crawler

# 2. Táº¡o mĂ´i trÆ°á»ng áº£o (tĂ¹y chá»n nhÆ°ng nĂªn lĂ m)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. CĂ i thÆ° viá»‡n
pip install -r requirements.txt

# 4. CĂ i Playwright browsers (chá»‰ cáº§n lĂ m 1 láº§n)
playwright install chromium

# 5. Cháº¡y server
python app.py
```

Má»Ÿ trĂ¬nh duyá»‡t táº¡i: **http://localhost:5000**

---

### CĂ¡ch 2 â€” Deploy lĂªn Render (miá»…n phĂ­)

> â ï¸ Render miá»…n phĂ­ cĂ³ thá»ƒ bá»‹ giá»›i háº¡n tĂ i nguyĂªn. Playwright cáº§n **Ă­t nháº¥t 512MB RAM**.

1. Fork repo nĂ y vá» tĂ i khoáº£n GitHub cá»§a báº¡n
2. ÄÄƒng kĂ½ tĂ i khoáº£n táº¡i [render.com](https://render.com)
3. Táº¡o **New Web Service** â†’ káº¿t ná»‘i vá»›i repo GitHub
4. Cáº¥u hĂ¬nh:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium`
   - **Start Command**: `gunicorn app:app --workers 2 --timeout 300`
5. Nháº¥n **Deploy** vĂ  chá» hoĂ n thĂ nh

---

### CĂ¡ch 3 â€” Deploy lĂªn Railway

1. Fork repo â†’ ÄÄƒng nháº­p [railway.app](https://railway.app)
2. **New Project** â†’ **Deploy from GitHub repo**
3. ThĂªm biáº¿n mĂ´i trÆ°á»ng:
   - `SECRET_KEY` = chuá»—i báº¥t ká»³ (vĂ­ dá»¥: `my-super-secret-key`)
4. Railway sáº½ tá»± Ä‘á»c `Procfile` vĂ  deploy

---

## đŸ–¥ï¸ HÆ°á»›ng dáº«n giao diá»‡n

### BÆ°á»›c 1 â€” Nháº­p link video

```
https://www.tiktok.com/@username/video/7559970565407149319
```

DĂ¡n link vĂ o Ă´ **"Link video TikTok"** (hoáº·c nháº¥n nĂºt đŸ“‹ Ä‘á»ƒ dĂ¡n tá»« clipboard).

### BÆ°á»›c 2 â€” Äáº·t tĂªn file CSV

Nháº­p tĂªn file tĂ¹y Ă½ (khĂ´ng cáº§n Ä‘uĂ´i `.csv`), vĂ­ dá»¥: `review_san_pham_A`.

### BÆ°á»›c 3 â€” Báº¯t Ä‘áº§u crawl

Nháº¥n **đŸ€ Báº¯t Ä‘áº§u Crawl**. Há»‡ thá»‘ng sáº½:
1. Má»Ÿ trĂ¬nh duyá»‡t áº£o (headless), táº£i trang TikTok Ä‘á»ƒ láº¥y cookie há»£p lá»‡
2. Click vĂ o khu vá»±c comment Ä‘á»ƒ kĂ­ch hoáº¡t API
3. Gá»i API TikTok theo tá»«ng trang (cursor-based pagination)
4. Thu tháº­p toĂ n bá»™ comment + reply

### BÆ°á»›c 4 â€” Xem káº¿t quáº£

Sau khi crawl xong, báº£ng bĂ¬nh luáº­n hiá»‡n ra ngay bĂªn dÆ°á»›i:
- **TĂ¬m kiáº¿m** theo ná»™i dung hoáº·c tĂªn ngÆ°á»i dĂ¹ng
- **PhĂ¢n trang** 50 comment/trang
- Xem loáº¡i (Gá»‘c / Reply), sá»‘ lÆ°á»£ng â¤ï¸

### BÆ°á»›c 5 â€” Táº£i vá»

Nháº¥n **â¬‡ï¸ Táº£i file CSV vá» mĂ¡y**. File CSV Ä‘Æ°á»£c mĂ£ hĂ³a UTF-8 vá»›i BOM (má»Ÿ Ä‘Æ°á»£c trong Excel tiáº¿ng Viá»‡t).

---

## đŸ“ Cáº¥u trĂºc file CSV xuáº¥t ra

| Cá»™t | MĂ´ táº£ |
|-----|-------|
| `cid` | ID comment |
| `text` | Ná»™i dung bĂ¬nh luáº­n |
| `create_time` | Thá»i gian Ä‘Äƒng (Unix timestamp) |
| `digg_count` | Sá»‘ lÆ°á»£t thĂ­ch |
| `reply_id` | ID comment cha (náº¿u lĂ  reply) |
| `reply_to_reply_id` | ID reply cha (náº¿u reply lá»“ng nhau) |
| `reply_to_userid` | User ID Ä‘Æ°á»£c reply |
| `reply_to_username` | Username Ä‘Æ°á»£c reply |
| `user_nickname` | TĂªn hiá»ƒn thá»‹ cá»§a ngÆ°á»i comment |
| `user_id` | UID cá»§a ngÆ°á»i comment |
| `user_sec_uid` | Secure UID (dĂ¹ng Ä‘á»ƒ tĂ¬m profile) |

---

## â™ï¸ CÆ¡ cháº¿ hoáº¡t Ä‘á»™ng

```
[User nháº­p URL]
      â†“
[Flask API /api/crawl/start]
      â†“
[Thread riĂªng: do_crawl()]
      â”œâ”€â”€ Playwright (headless Chrome)
      â”‚     â”œâ”€â”€ Má»Ÿ trang TikTok â†’ láº¥y cookies há»£p lá»‡
      â”‚     â””â”€â”€ Click nĂºt comment â†’ kĂ­ch hoáº¡t session
      â”‚
      â””â”€â”€ requests (API TikTok)
            â”œâ”€â”€ GET /api/comment/list/ â†’ comment gá»‘c (cursor pagination)
            â””â”€â”€ GET /api/comment/list/reply/ â†’ reply cá»§a tá»«ng comment
                â†“
         [LÆ°u vĂ o memory + file CSV]
                â†“
[Frontend poll /api/crawl/status/ má»—i 2s]
      â†“
[Hiá»ƒn thá»‹ báº£ng + cho táº£i CSV]
```

---

## â“ FAQ

**Q: Táº¡i sao crawl máº¥t thá»i gian lĂ¢u?**  
A: TikTok cĂ³ rate limiting. Script tá»± Ä‘á»™ng chá» giá»¯a cĂ¡c request Ä‘á»ƒ trĂ¡nh bá»‹ block.

**Q: CĂ³ thá»ƒ crawl video private khĂ´ng?**  
A: KhĂ´ng. Chá»‰ crawl Ä‘Æ°á»£c comment cá»§a video cĂ´ng khai.

**Q: File CSV má»Ÿ bá»‹ lá»—i font tiáº¿ng Viá»‡t?**  
A: File Ä‘Æ°á»£c lÆ°u vá»›i encoding UTF-8-BOM. Náº¿u má»Ÿ báº±ng Excel, chá»n **Data > From Text/CSV** vĂ  chá»n encoding UTF-8.

**Q: CĂ³ thá»ƒ dĂ¹ng cho má»¥c Ä‘Ă­ch thÆ°Æ¡ng máº¡i khĂ´ng?**  
A: Chá»‰ dĂ¹ng cho nghiĂªn cá»©u, há»c thuáº­t. Vui lĂ²ng tuĂ¢n thá»§ [Terms of Service cá»§a TikTok](https://www.tiktok.com/legal/terms-of-service).

---

## đŸ›¡ï¸ LÆ°u Ă½ phĂ¡p lĂ½

CĂ´ng cá»¥ nĂ y chá»‰ Ä‘Æ°á»£c phĂ¡t triá»ƒn cho má»¥c Ä‘Ă­ch **nghiĂªn cá»©u vĂ  há»c thuáº­t**. NgÆ°á»i dĂ¹ng chá»‹u trĂ¡ch nhiá»‡m tuĂ¢n thá»§:
- [TikTok Terms of Service](https://www.tiktok.com/legal/terms-of-service)
- CĂ¡c quy Ä‘á»‹nh vá» quyá»n riĂªng tÆ° dá»¯ liá»‡u táº¡i Ä‘á»‹a phÆ°Æ¡ng

---

## đŸ¤ ÄĂ³ng gĂ³p

Pull requests vĂ  issues luĂ´n Ä‘Æ°á»£c chĂ o Ä‘Ă³n! Vui lĂ²ng:
1. Fork repo
2. Táº¡o branch má»›i: `git checkout -b feature/ten-tinh-nang`
3. Commit thay Ä‘á»•i: `git commit -m "feat: thĂªm tĂ­nh nÄƒng X"`
4. Push vĂ  táº¡o Pull Request

---

## đŸ“„ License

MIT License â€” xem file [LICENSE](LICENSE) Ä‘á»ƒ biáº¿t thĂªm chi tiáº¿t.

---

<div align="center">

Made with â¤ï¸ in Vietnam đŸ‡»đŸ‡³

</div>

