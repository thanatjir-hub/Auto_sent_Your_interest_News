import os
import re
import smtplib
import feedparser
import requests
import time
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

# ==========================================
# 1. ดึงค่าตัวแปรตั้งค่าจาก GitHub Secrets
# ==========================================
rss_url = os.environ.get("RSS_URL")
API_KEY = os.environ.get("GEMINI_API_KEY")
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
app_password = os.environ.get("APP_PASSWORD")

if not all([API_KEY, sender_email, receiver_email, app_password]):
    raise ValueError("❌ ตั้งค่าตัวแปรใน GitHub Secrets ไม่ครบ กรุณาตรวจสอบ!")

# ==========================================
# 2. ดึงข้อมูลข่าวสาร (RSS) ฉบับทะลวงบล็อก
# ==========================================
print(f"กำลังดึงข้อมูลจาก {rss_url} ...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

try:
    response = requests.get(rss_url, headers=headers, timeout=15)
    print(f"สถานะการเชื่อมต่อเว็บ: HTTP {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ เว็บไซต์ปลายทางบล็อกการเข้าถึง (Error {response.status_code}) จบการทำงาน")
        exit()

    feed = feedparser.parse(response.content)
    news_data = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        raw_content = entry.get('summary', '')
        clean_snippet = BeautifulSoup(raw_content, "html.parser").get_text()
        short_snippet = clean_snippet[:200].strip() + "..."
        
        news_data.append({
            "title": title,
            "link": link,
            "contentSnippet": short_snippet
        })

    print(f"✅ ดึงข้อมูลสำเร็จ! ได้ข่าวมาทั้งหมด {len(news_data)} หัวข้อ")

    if len(news_data) == 0:
        print("❌ ไม่พบเนื้อหาข่าว (อาจโดนระบบป้องกันซ่อนเนื้อหาไว้) ขอจบการทำงาน")
        exit()
        
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการดึงข้อมูล: {e}")
    exit()

# ==========================================
# 3. จัดกลุ่มข้อมูล (Aggregate)
# ==========================================
aggregated_news_text = ""
for news in news_data:
    aggregated_news_text += f"Title: {news['title']}\nLink: {news['link']}\nSnippet: {news['contentSnippet']}\n--- \n\n"
    time.sleep(15)
# ==========================================
# 4. ส่งให้ AI (Gemini) สรุปผล
# ==========================================
print("🤖 กำลังส่งข้อมูลให้ Gemini สรุปข่าว...")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

system_prompt = """==คุณคือบรรณาธิการบริหารและนักสรุปข่าวขั้นเทพ
หน้าที่ของคุณคือสรุปข้อมูลข่าว "ทั้งหมด" ที่ได้รับมาด้านล่างนี้ โดยไม่ต้องคัดทิ้ง (ยกเว้นข่าวที่มีชื่อซ้ำกันเป๊ะๆ ให้ตัดออกเหลือแค่อันเดียว)

กฎเหล็ก (สำคัญมาก!!!):
- ห้ามพิมพ์ข้อความทักทาย ห้ามตอบรับคำสั่ง (เช่น "รับทราบ", "พร้อมแล้ว")
- ห้ามเกริ่นนำ หรือมีบทสนทนาใดๆ นอกเหนือจากการสรุปข่าว
- ให้เริ่มแสดงผลเป็นรูปแบบ ### [ชื่อข่าว] ทันที

คำสั่งของคุณมีดังนี้:
1. สรุปข่าวทั้งหมดทุกหัวข้อแบบสั้น กระชับ ตรงประเด็น
2. ต้องใช้รูปแบบด้านล่างนี้เป๊ะๆ เรียงต่อกันไปเรื่อยๆ จนครบทุกข่าว:

### [ชื่อข่าว]
**สรุป:** [สรุปเนื้อหาหลักและประโยชน์ที่ได้รับ รวมกันไม่เกิน 2-3 บรรทัด]
**อ่านต่อ:** [ใส่ Link ของข่าว]
---"""

final_prompt = f"{system_prompt}\n\nข้อมูลข่าวทั้งหมด:\n{aggregated_news_text}"
response = model.generate_content(final_prompt)
ai_summary_result = response.text
print("✅ Gemini สรุปข่าวเสร็จเรียบร้อย!")

# ==========================================
# 5. จัดหน้าตา HTML
# ==========================================
ai_text = ai_summary_result
ai_text = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank" class="btn">คลิกเพื่ออ่านบทความเต็ม</a>', ai_text)
ai_text = re.sub(r'^### (.*)', r'<h2 class="news-title">\1</h2>', ai_text, flags=re.MULTILINE)
ai_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', ai_text)
ai_text = re.sub(r'^---$', r'<hr class="divider">', ai_text, flags=re.MULTILINE)
ai_text = ai_text.replace('\n', '<br>')
ai_text = re.sub(r'(<br>\s*){3,}', '<br><br>', ai_text)

html_template = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: 'Sarabun', 'Segoe UI', Tahoma, Geneva, sans-serif; background-color: #f4f7f6; color: #333333; line-height: 1.6; padding: 20px; }}
    .container {{ max-width: 650px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    h1 {{ text-align: center; color: #2c3e50; border-bottom: 3px solid #1a73e8; padding-bottom: 15px; margin-bottom: 30px; }}
    .news-title {{ color: #1a73e8; font-size: 20px; margin-top: 30px; margin-bottom: 10px; }}
    strong {{ color: #d93025; }}
    .divider {{ border: 0; border-top: 1px dashed #e0e0e0; margin: 30px 0; }}
    .btn {{ display: inline-block; margin: 10px 0; padding: 10px 20px; background-color: #1a73e8; color: #ffffff !important; text-decoration: none; border-radius: 6px; font-weight: bold; }}
    .btn:hover {{ background-color: #1557b0; }}
    .footer {{ text-align: center; margin-top: 40px; font-size: 12px; color: #999999; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>📰 สรุปข่าวเด่นประจำวัน</h1>
    {ai_text}
    <div class="footer">
      สรุปและส่งอัตโนมัติด้วย Python & GitHub Actions 🚀
    </div>
  </div>
</body>
</html>
"""

# ==========================================
# 6. ส่งอีเมล
# ==========================================
message = MIMEMultipart("alternative")
message["Subject"] = "📰 สรุปข่าวเด่นประจำวัน (เสิร์ฟด่วนโดย AI)"
message["From"] = sender_email
message["To"] = receiver_email
message.attach(MIMEText(html_template, "html"))

try:
    print("📧 กำลังส่งอีเมล...")
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("✅ ส่งอีเมลสำเร็จแล้ว! จบการทำงาน")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการส่งอีเมล: {e}")
finally:
    server.quit()
