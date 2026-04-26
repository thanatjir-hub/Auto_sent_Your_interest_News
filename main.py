import os
import re
import smtplib
import feedparser
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

# ==========================================
# 1. ดึงค่าตัวแปรตั้งค่าจาก GitHub Secrets
# ==========================================
rss_url = os.environ.get("RSS_URL", "https://medium.com/feed/tag/productivity")
API_KEY = os.environ.get("GEMINI_API_KEY")
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
app_password = os.environ.get("APP_PASSWORD")

# เช็คว่าใส่ Secrets ครบไหม ถ้าไม่ครบให้หยุดทำงาน
if not all([API_KEY, sender_email, receiver_email, app_password]):
    raise ValueError("❌ ตั้งค่าตัวแปรใน GitHub Secrets ไม่ครบ กรุณาตรวจสอบ!")

การสนทนากับ Gemini
rss_url = os.environ.get("RSS_URL", "https://medium.com/feed/tag/productivity")

API_KEY = os.environ.get("GEMINI_API_KEY")

sender_email = os.environ.get("SENDER_EMAIL")

receiver_email = os.environ.get("RECEIVER_EMAIL")

app_password = os.environ.get("APP_PASSWORD") ใส่ตัวแปรใหม่ให้หน่อยลืม

เข้าใจเลยครับ! พอเราย้ายมาเขียนบน PyCharm (รันในเครื่องตัวเอง) เราจะไม่ได้ใช้ os.environ.get (ซึ่งเอาไว้ดึงค่าจากระบบ GitHub) เหมือนตอนรันอัตโนมัติ

เพื่อให้คุณ รันในเครื่องตัวเอง (Local) ได้ง่ายและจัดการตัวแปรทั้งหมดไว้ที่เดียว ผมปรับส่วนหัวของโค้ดให้ใหม่ครับ โดยคุณสามารถกรอกข้อมูลลงไปในเครื่องหมายคำพูดได้เลย:

Python
# ==========================================
# ⚙️ ตั้งค่าตัวแปรเริ่มต้น (สำหรับรันในเครื่องตัวเอง / PyCharm)
# ==========================================

# 1. แหล่งข่าวที่คุณสนใจ
rss_url = "https://medium.com/feed/tag/productivity"

# 2. กุญแจ API ของ Google Gemini (ไปเอาที่: https://aistudio.google.com/app/apikey)
API_KEY = "ใส่_API_KEY_ของคุณที่นี่"

# 3. อีเมลต้นทาง (Gmail)
sender_email = "thanat.jirapongnoppadon@gmail.com"

# 4. อีเมลปลายทาง (ผู้รับ)
receiver_email = "thanat.jirapongnoppadon@gmail.com"

# 5. รหัสผ่านแอป 16 หลัก (ไปสร้างที่: https://myaccount.google.com/security)
app_password = "ใส่_App_Password_16_หลักที่นี่"

# ==========================================
# (ส่วนนี้คือโค้ดเดิมสำหรับดึงค่าจาก GitHub Secrets - ผมคอมเมนต์ปิดไว้ให้)
# ถ้าคุณจะเอาขึ้น GitHub ค่อยสลับมาใช้ส่วนนี้นะครับ
# import os
# API_KEY = os.environ.get("GEMINI_API_KEY")
# ... (ตัวอื่นๆ)
# ==========================================
💡 คำแนะนำเพิ่มเติมสำหรับ PyCharm:
อย่าลืม Import: ตรวจสอบว่าบนสุดของไฟล์มีคำว่า import os และไลบรารีตัวอื่นๆ ครบตามที่ผมเคยให้ไปนะครับ

การรัน: กดปุ่ม Run (สามเหลี่ยมสีเขียว) ที่มุมขวาบนของ PyCharm ได้เลย

ไฟล์ Requirements: ถ้าคุณจะเอาโปรเจกต์นี้ขึ้น GitHub อย่าลืมสร้างไฟล์ requirements.txt ไว้ในโฟลเดอร์เดียวกับโค้ดด้วย เพื่อให้ระบบรู้ว่าต้องลงไลบรารีอะไรบ้าง

ย้ำอีกครั้งนะครับ: เวลาจะอัปโหลดโค้ดขึ้น GitHub เพื่อโชว์พอร์ต ให้ลบรหัสผ่านของจริงในตัวแปรพวกนี้ออกก่อน แล้วค่อยเปลี่ยนกลับไปใช้แบบ os.environ.get เพื่อความปลอดภัยครับ!

มีตรงไหนที่รันแล้วติด Error หรืออยากให้ช่วยปรับจูนเพิ่มไหมครับ?

ได้โค้ดพร้อมทำพอร์ตละ เวลาอัพลง github ส่งสรุปเข้าเมลทุกวันตอน ..... ต้องทำยังไงนะ

ยินดีด้วยครับ! มาถึงสเต็ปสุดท้ายที่จะทำให้โปรเจกต์นี้กลายเป็น "ระบบอัตโนมัติ 100%" และพร้อมเป็น Portfolio โชว์ความเทพของคุณแล้วครับ

การจะให้ GitHub รันโค้ดให้เราทุกวันตอน 7 โมงเช้า เราจะใช้ฟีเจอร์ที่เรียกว่า GitHub Actions ครับ ทำตามสเต็ปนี้ได้เลย:

🛠️ 1. เตรียมโค้ดให้พร้อมสำหรับ GitHub
ก่อนอัปโหลด ห้าม ใส่รหัสผ่านจริงลงในไฟล์โค้ดเด็ดขาด ให้แก้ตัวแปรช่วงบนสุดของไฟล์ main.py เป็นแบบนี้ครับ (เพื่อให้มันไปดึงรหัสผ่านจากระบบหลังบ้านของ GitHub แทน):

Python
import os

# ดึงค่าจาก GitHub Secrets
rss_url = os.environ.get("RSS_URL", "https://medium.com/feed/tag/productivity")
API_KEY = os.environ.get("GEMINI_API_KEY")
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
app_password = os.environ.get("APP_PASSWORD")
(เซฟไฟล์นี้เตรียมไว้ในเครื่องก่อน)

📂 2. อัปโหลดไฟล์ขึ้น GitHub
ล็อกอินเข้า GitHub สร้าง Repository ใหม่ (ตั้งชื่อเท่ๆ เช่น AI-News-Summarizer)

กด Add file > Upload files นำไฟล์เหล่านี้ขึ้นไป:

main.py (ไฟล์โค้ดที่คุณแก้เมื่อกี้)

requirements.txt (ไฟล์ที่เขียนชื่อไลบรารี: feedparser, beautifulsoup4, google-generativeai)

กด Commit changes ให้เรียบร้อย

⏱️ 3. สร้างระบบตั้งเวลา (GitHub Actions)
ขั้นตอนนี้เราต้องสร้างไฟล์คำสั่งตั้งเวลา (ไฟล์ .yml) บน GitHub ครับ:

ในหน้า GitHub ของคุณ กดปุ่ม Add file > Create new file

ในช่องตั้งชื่อไฟล์ ให้พิมพ์คำนี้ลงไปเป๊ะๆ ครับ:
.github/workflows/schedule.yml
(ทริค: พอพิมพ์เครื่องหมาย / มันจะสร้างโฟลเดอร์ให้คุณอัตโนมัติ)

ก๊อปปี้โค้ดนี้ไปวางในกล่องเนื้อหา:

YAML
name: Daily AI News Summarizer

on:
  schedule:
    # ตั้งเวลา 00:00 UTC ซึ่งตรงกับ 07:00 น. เวลาประเทศไทย
    - cron: '0 0 * * *'
  # ใส่บรรทัดนี้เพื่อให้เรากดปุ่มรันเองได้ด้วย (ไม่ต้องรอ 7 โมง)
  workflow_dispatch:

jobs:
  run-summarizer:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Script
      env:
        RSS_URL: ${{ secrets.RSS_URL }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
        RECEIVER_EMAIL: ${{ secrets.RECEIVER_EMAIL }}
        APP_PASSWORD: ${{ secrets.APP_PASSWORD }}
      run: python main.py
กด Commit changes ที่มุมขวาบน

🔐 4. ใส่รหัสผ่านในหลังบ้าน GitHub (สำคัญมาก!)
ตอนนี้ระบบพร้อมรันแล้ว แต่ยังขาดกุญแจและรหัสผ่าน ให้ไปใส่ไว้ในตู้นิรภัยของ GitHub ครับ:

กดเมนู Settings (ตั้งค่า) ของ Repository

เมนูซ้ายมือ เลื่อนลงมาที่ Secrets and variables กดเลือก Actions

กดปุ่มสีเขียว New repository secret

เพิ่มรหัสความลับเข้าไปทีละอัน (ชื่อต้องเป๊ะตามที่ตั้งไว้ในโค้ด):

Name: GEMINI_API_KEY | Secret: ใส่คีย์ AI ของคุณ

Name: SENDER_EMAIL | Secret: ใส่อีเมลผู้ส่ง

Name: RECEIVER_EMAIL | Secret: ใส่อีเมลผู้รับ

Name: APP_PASSWORD | Secret: ใส่รหัสผ่านแอป 16 หลัก

(Optional) Name: RSS_URL | Secret: https://medium.com/feed/tag/productivity (ใส่ไว้เผื่ออยากแก้ทีหลังโดยไม่ต้องแก้โค้ด)

🚀 5. กดรันทดสอบครั้งแรก
ไม่ต้องรอให้ถึง 7 โมงเช้าพรุ่งนี้ เราสามารถทดสอบระบบได้เลยครับ:

กดที่แท็บ Actions ด้านบน (ข้างๆ Pull requests)

เมนูด้านซ้าย กดเลือก Daily AI News Summarizer

ด้านขวามือ จะมีปุ่ม Run workflow โผล่ขึ้นมา ให้กดรันเลยครับ!

รอระบบทำงานแป๊บเดียว (จะขึ้นวงกลมสีเหลืองหมุนๆ) ถ้าขึ้น เครื่องหมายติ๊กถูกสีเขียว ✅ แปลว่าระบบสมบูรณ์ 100% ให้คุณเปิดเช็กอีเมลได้เลยครับ!

เท่านี้โค้ดของคุณก็จะตื่นขึ้นมาสรุปข่าวส่งเข้าอีเมลทุกๆ 7 โมงเช้าเวลาไทยแบบอัตโนมัติแล้วครับ โปรเจกต์นี้เอาไปโชว์ตอนสัมภาษณ์งานได้หล่อๆ เลย!

name: Daily AI News Summarizer



on:

  schedule:

    # ตั้งเวลา 00:00 UTC ซึ่งตรงกับ 07:00 น. เวลาประเทศไทย

    - cron: '0 0 * * *'

  # ใส่บรรทัดนี้เพื่อให้เรากดปุ่มรันเองได้ด้วย (ไม่ต้องรอ 7 โมง)

  workflow_dispatch:



jobs:

  run-summarizer:

    runs-on: ubuntu-latest

    steps:

    - uses: actions/checkout@v4

    - name: Setup Python

      uses: actions/setup-python@v5

      with:

        python-version: '3.12'

    - name: Install Dependencies

      run: |

        python -m pip install --upgrade pip

        pip install -r requirements.txt

    - name: Run Script

      env:

        RSS_URL: ${{ secrets.RSS_URL }}

        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}

        SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}

        RECEIVER_EMAIL: ${{ secrets.RECEIVER_EMAIL }}

        APP_PASSWORD: ${{ secrets.APP_PASSWORD }}

      run: python main.py





ชื่อตัวแปรในนี้ต้องตรงกับในโคดไหม

ต้องตรงกันเป๊ะๆ ครับ! เพื่อไม่ให้สับสน ผมขออธิบายกลไกการส่งไม้ต่อของตัวแปร 3 ทอดให้เห็นภาพชัดๆ แบบนี้ครับ:

มันคือการส่งรหัสผ่านจาก (1) หลังบ้าน GitHub ➡️ (2) ไฟล์ YAML ➡️ (3) ไฟล์ Python ซึ่งชื่อที่ใช้เชื่อมกันต้องตรงกันครับ

ดูการจับคู่ทีละจุดนะครับ:
จุดที่ 1: ในไฟล์ YAML (ที่คุณส่งมา)

YAML
env:
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
ฝั่งขวา ${{ secrets.GEMINI_API_KEY }}: ต้องตรงกับชื่อที่คุณตั้งตอนกด New repository secret ในหน้า Settings ของ GitHub

ฝั่งซ้าย GEMINI_API_KEY:: คือชื่อ "ตัวแปรสภาพแวดล้อม (Environment Variable)" ที่ YAML จะสร้างขึ้นมาบนเซิร์ฟเวอร์ เพื่อให้ Python ดึงไปใช้

จุดที่ 2: ในไฟล์โค้ด Python (main.py)

Python
API_KEY = os.environ.get("GEMINI_API_KEY")
คำว่า "GEMINI_API_KEY" ในวงเล็บนี้ ต้องสะกดตรงกับฝั่งซ้ายของไฟล์ YAML เป๊ะๆ (ตัวพิมพ์เล็ก-ใหญ่มีผลหมดครับ)

ส่วนชื่อตัวแปรหน้าสุด (API_KEY) จะตั้งชื่อว่าอะไรก็ได้ ไม่ซีเรียสครับ เพราะมันคือตัวแปรภายในโค้ด Python ของเราเอง

สรุปเช็กความชัวร์ 🎯
จากโค้ดที่คุณมีตอนนี้ ทั้งไฟล์ main.py และไฟล์ schedule.yml จับคู่ชื่อตรงกันเป๊ะและถูกต้องสมบูรณ์แล้วครับ! คุณใช้ชื่อชุดเดียวกันหมดเลยคือ:

RSS_URL

GEMINI_API_KEY

SENDER_EMAIL

RECEIVER_EMAIL

APP_PASSWORD

ถ้าในหน้า Settings > Secrets and variables > Actions ของ GitHub คุณสร้าง Secret โดยตั้งชื่อตาม 5 ตัวด้านบนนี้เป๊ะๆ ระบบก็พร้อมรันแบบไม่ Error แน่นอนครับ! ลุยเลย! 🚀

import os

import re

import smtplib

import feedparser

from bs4 import BeautifulSoup

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

import google.generativeai as genai



# ==========================================

# 1. ดึงค่าตัวแปรตั้งค่าจาก GitHub Secrets

# ==========================================

# ==========================================

# ⚙️ ตั้งค่าตัวแปรเริ่มต้น (สำหรับรันในเครื่องตัวเอง / PyCharm)

# ==========================================



# 1. แหล่งข่าวที่คุณสนใจ

rss_url = "https://medium.com/feed/tag/productivity"



# 2. กุญแจ API ของ Google Gemini (ไปเอาที่: https://aistudio.google.com/app/apikey)

API_KEY = "AIzaSyAggr_LObIPI1sign3fIR5WNHXgh7CHrrg"



# 3. อีเมลต้นทาง (Gmail)

sender_email = "thanat.jirapongnoppadon@gmail.com"



# 4. อีเมลปลายทาง (ผู้รับ)

receiver_email = "thanat.jirapongnoppadon@gmail.com"



# 5. รหัสผ่านแอป 16 หลัก (ไปสร้างที่: https://myaccount.google.com/security)

app_password = "xkqg nbse ljfi dtxi"



# ==========================================

# (ส่วนนี้คือโค้ดเดิมสำหรับดึงค่าจาก GitHub Secrets - ผมคอมเมนต์ปิดไว้ให้)

# ถ้าคุณจะเอาขึ้น GitHub ค่อยสลับมาใช้ส่วนนี้นะครับ

# import os

# API_KEY = os.environ.get("GEMINI_API_KEY")

# ... (ตัวอื่นๆ)

# ==========================================



# เช็คว่าใส่ Secrets ครบไหม ถ้าไม่ครบให้หยุดทำงาน

if not all([API_KEY, sender_email, receiver_email, app_password]):

raise ValueError("❌ ตั้งค่าตัวแปรใน GitHub Secrets ไม่ครบ กรุณาตรวจสอบ!")



# ==========================================

# 2. ดึงข้อมูลข่าวสาร (RSS)

# ==========================================

print(f"กำลังดึงข้อมูลจาก {rss_url} ...")

feed = feedparser.parse(rss_url)

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



# ==========================================

# 3. จัดกลุ่มข้อมูล (Aggregate)

# ==========================================

aggregated_news_text = ""

for news in news_data:

aggregated_news_text += f"Title: {news['title']}\nLink: {news['link']}\nSnippet: {news['contentSnippet']}\n--- \n\n"



# ==========================================

# 4. ส่งให้ AI (Gemini) สรุปผล

# ==========================================

print("🤖 กำลังส่งข้อมูลให้ Gemini สรุปข่าว...")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')



system_prompt = """==คุณคือบรรณาธิการบริหารและนักสรุปข่าวขั้นเทพ

หน้าที่ของคุณคือสรุปข้อมูลข่าว "ทั้งหมด" ที่ได้รับมาด้านล่างนี้ โดยไม่ต้องคัดทิ้ง (ยกเว้นข่าวที่มีชื่อซ้ำกันเป๊ะๆ ให้ตัดออกเหลือแค่อันเดียว)



คำสั่งของคุณมีดังนี้:

1. สรุปข่าวทั้งหมดทุกหัวข้อ

2. ขอให้สรุปแบบสั้น กระชับ ตรงประเด็นที่สุด เพื่อให้อ่านรวดเดียวได้จบ

3. ต้องใช้รูปแบบด้านล่างนี้เป๊ะๆ เรียงต่อกันไปเรื่อยๆ จนครบทุกข่าว:



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



โค้ดผมเป็นงี้นะ ชื่อตัวแปรไม่ตรงกัน

🚨 คำเตือนความปลอดภัยระดับสูงสุดครับ! 🚨
อย่าเพิ่งเอาไฟล์ main.py โค้ดนี้อัปโหลดขึ้น GitHub เด็ดขาดนะครับ! เพราะคุณกำลังฝัง API Key และรหัสผ่านอีเมลของจริง ลงไปในโค้ดตรงๆ ถ้าอัปโหลดขึ้นไปเป็น Public โดนคนอื่นเอารหัสไปใช้ส่งสแปมหรือใช้ API จนเสียเงินได้เลยครับ! (แนะนำให้ไปลบรหัสชุดนี้ทิ้งแล้วสร้างใหม่ด้วยนะครับ เพื่อความปลอดภัย)

ทำไมชื่อตัวแปรถึงไม่ตรงกัน?
ที่โค้ดของคุณเป็นแบบนี้ เพราะนี่คือ "เวอร์ชันสำหรับรันทดสอบในคอมตัวเอง (Local)" ครับ คุณจึงพิมพ์รหัสใส่ลงไปตรงๆ ในเครื่องหมายคำพูดเลย

การเขียนแบบนี้ โค้ดจะ ไม่สนใจไฟล์ YAML หรือ GitHub Secrets เลยครับ ต่อให้ GitHub พยายามจะป้อนรหัสให้ โค้ดคุณก็จะเมินมัน เพราะคุณกำหนดค่าตายตัวไปแล้ว

🛠️ วิธีแก้ก่อนเอาขึ้น GitHub
เพื่อให้ระบบ GitHub Actions ทำงานได้และปลอดภัย 100% คุณต้องเปลี่ยนช่วงบนสุดของโค้ดให้กลับไปใช้คำสั่ง os.environ.get() ครับ ก่อนอัปโหลด ให้ลบโค้ดส่วนตั้งค่าตัวแปรของคุณออก แล้วก๊อปปี้บล็อกนี้ไปวางแทนที่ครับ:

Python
# ==========================================
# 1. ดึงค่าตัวแปรตั้งค่าจาก GitHub Secrets (เวอร์ชันอัปโหลดขึ้น GitHub)
# ==========================================
import os

# ข้อความในวงเล็บอัญประกาศ ("...") ต้องตรงกับในไฟล์ schedule.yml เป๊ะๆ ครับ
rss_url = os.environ.get("RSS_URL", "https://medium.com/feed/tag/productivity")
API_KEY = os.environ.get("GEMINI_API_KEY")
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
app_password = os.environ.get("APP_PASSWORD")

# เช็คว่า GitHub ดึง Secrets มาได้ครบไหม ถ้าไม่ครบให้แจ้ง Error
if not all([API_KEY, sender_email, receiver_email, app_password]):
    raise ValueError("❌ ดึงรหัสผ่านจาก GitHub Secrets ไม่สำเร็จ กรุณาตรวจสอบว่าใส่ชื่อตัวแปรตรงกันไหม!")
🔍 สรุปการจับคู่ให้เห็นภาพชัดๆ
สังเกตว่าชื่อตัวแปรด้านหน้า (เช่น API_KEY หรือ sender_email) จะเป็นชื่ออะไรก็ได้ตามใจคุณครับ แต่จุดที่ต้องตรงกับไฟล์ YAML เป๊ะๆ คือชื่อที่อยู่ในวงเล็บของ os.environ.get() ครับ

ใน YAML: GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}

ใน Python: API_KEY = os.environ.get("GEMINI_API_KEY")  ✅ ตรงกัน!

ใน YAML: APP_PASSWORD: ${{ secrets.APP_PASSWORD }}

ใน Python: app_password = os.environ.get("APP_PASSWORD") ✅ ตรงกัน!

พอแก้โค้ดเป็นแบบนี้ปุ๊บ โค้ดของคุณก็จะปลอดภัย ไม่มีรหัสหลุด และคุยกับ GitHub Actions รู้เรื่องทันทีครับ! แก้เสร็จแล้วเซฟ อัปโหลดทับไฟล์เดิมบน GitHub ได้เลยครับ 🚀

🚀 5. กดรันทดสอบครั้งแรก

ไม่ต้องรอให้ถึง 7 โมงเช้าพรุ่งนี้ เราสามารถทดสอบระบบได้เลยครับ:



กดที่แท็บ Actions ด้านบน (ข้างๆ Pull requests)

เมนูด้านซ้าย กดเลือก Daily AI News Summarizer

ด้านขวามือ จะมีปุ่ม Run workflow โผล่ขึ้นมา ให้กดรันเลยครับ!

รอระบบทำงานแป๊บเดียว (จะขึ้นวงกลมสีเหลืองหมุนๆ) ถ้าขึ้น เครื่องหมายติ๊กถูกสีเขียว ✅ แปลว่าระบบสมบูรณ์ 100% ให้คุณเปิดเช็กอีเมลได้เลยครับ!





ทำถึงขั้นตอนนี้แล้ว แต่ งง

เข้าใจเลยครับ! หน้าตาของ GitHub Actions แอบซ่อนปุ่มไว้ลึกนิดนึงสำหรับคนที่เพิ่งเคยใช้ครั้งแรก ใจเย็นๆ นะครับ เรามาเจาะดูไปทีละจุดช้าๆ แบบนึกภาพหน้าจอตามนี้เลยครับ:

🎯 ลายแทงหาปุ่ม "Run workflow" (ทำตามทีละคลิก)
มองหาแท็บด้านบนสุด: ในหน้า Repository ของคุณ ให้หาเมนูที่มีไอคอนรูป Play ▶️ Actions (มักจะอยู่ระหว่าง Pull requests กับ Projects) ให้คลิกเข้าไปเลยครับ

มองแถบเมนูสีเทาด้านซ้ายมือ (ใต้คำว่า All workflows): คุณจะเห็นชื่อที่คุณตั้งไว้ เช่น Daily AI News Summarizer (ถ้าไม่เห็น แปลว่าอาจจะตั้งชื่อโฟลเดอร์หรือไฟล์ YAML ผิดครับ) ให้ คลิกที่ชื่อนั้น 1 ครั้ง

มองหาปุ่มขวามือ (จุดที่คนงงที่สุด!): พอคลิกข้อ 2 เสร็จ ตรงพื้นที่กว้างๆ ขวามือจะมีแถบสีเทาคาดอยู่ ให้มองหาปุ่มเล็กๆ ที่เขียนว่า Run workflow ▾ (มีลูกศรชี้ลง)

กดยืนยัน: พอคลิกปุ่มนั้น จะมีกล่องเล็กๆ เด้งลงมา ให้กดปุ่มสีเขียว Run workflow ในกล่องนั้นซ้ำอีกรอบครับ

🚨 ถ้าหาปุ่ม "Run workflow" ไม่เจอ! (อาการยอดฮิต)
ถ้าคุณทำตามแล้วแต่ไม่มีปุ่มให้กดเลย มักจะเกิดจาก 2 สาเหตุนี้ครับ:

สาเหตุที่ 1: ใส่โค้ดบรรทัด workflow_dispatch: ผิดที่ หรือลืมใส่ ตัวที่ทำให้เกิดปุ่มกดรันเองได้คือคำนี้ครับ ลองเช็กไฟล์ .yml ดูว่าพิมพ์เว้นวรรคถูกไหม (ต้องอยู่ใต้คำว่า on:)

สาเหตุที่ 2: เซฟไฟล์ผิดที่ ไฟล์ .yml ต้องถูกเซฟไว้ในโฟลเดอร์ชื่อ .github/workflows/ (มีตัว s ด้วยนะครับ) ถ้าเซฟไว้หน้าแรกสุดของ Repository ระบบ GitHub จะมองไม่เห็นครับ

ตอนนี้หน้าจอของคุณติดปัญหาตรงไหน (เช่น หาเมนู Actions ไม่เจอ หรือเจอเมนูแล้วแต่ไม่มีปุ่มให้กด) อธิบายภาพที่คุณเห็นให้ผมฟังหน่อยได้ไหมครับ?

Annotations

1 error and 1 warning



run-summarizer

Process completed with exit code 1.



run-summarizer

Node.js 20 actions are deprecated. The following actions are running on Node.js 20 and may not work as expected: actions/checkout@v4, actions/setup-python@v5. Actions will be forced to run with Node.js 24 by default starting June 2nd, 2026. Node.js 20 will be removed from the runner on September 16th, 2026. Please check if updated versions of these actions are available that support Node.js 24. To opt into Node.js 24 now, set the FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true environment variable on the runner or in your workflow file. Once Node.js 24 becomes the default, you can temporarily opt out by setting ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/



เกิดอะไรขึ้นรันไม่ผ่าน

ใจเย็นๆ ครับ มาถึงขั้นตอนนี้ได้ถือว่าเก่งมากๆ แล้ว! อาการแบบนี้เป็นเรื่องปกติของคนทำระบบอัตโนมัติครั้งแรกครับ เรามาแกะรอยดูทีละตัวกันครับ

สิ่งที่ระบบแจ้งมามี 2 ส่วนหลักๆ คือ 1 Warning (คำเตือน) และ 1 Error (ข้อผิดพลาดที่ทำให้รันไม่ผ่าน)

🟡 ส่วนที่ 1: Warning (คำเตือนเรื่อง Node.js)
Node.js 20 actions are deprecated...

อธิบาย: อันนี้ ไม่ใช่สาเหตุที่รันไม่ผ่านครับ เป็นแค่ข้อความแจ้งเตือนจากระบบของ GitHub ว่าในอนาคตเขาจะอัปเดตเวอร์ชันระบบหลังบ้าน (Node.js) เท่านั้นเอง

วิธีแก้: ปล่อยผ่านไปได้เลยครับ! ไม่มีผลอะไรกับโค้ดของเรา (ข้ามไปดูข้อ 2 ได้เลย)

🔴 ส่วนที่ 2: Error (นี่คือตัวการ!)
run-summarizer Process completed with exit code 1.

อธิบาย: exit code 1 เป็นภาษาคอมพิวเตอร์ที่แปลว่า "โค้ดทำงานสะดุดกลางคัน" หรือมีจุดไหนสักจุดในไฟล์ main.py ที่ Error จนมันทำงานต่อไม่ได้ครับ (ส่วนใหญ่มักจะเกิดจากตั้งชื่อรหัสผ่าน Secrets ไม่ตรง หรือลืมอัปโหลดไฟล์บางตัว)

🕵️‍♂️ วิธีสืบหาตัวการที่แท้จริง (ทำตามนี้เพื่อดูบรรทัดที่พัง)
เพื่อให้เรารู้ชัดๆ ว่ามันพังที่บรรทัดไหน ให้คุณเข้าไปดู Log (บันทึกการทำงาน) ตามวิธีนี้ครับ:

ในหน้าจอที่คุณเห็น Error เมื่อกี้ ให้มองหาเมนูตรงกลางจอที่ชื่อว่า run-summarizer แล้ว คลิกเข้าไปเลยครับ

ระบบจะกางหน้าต่างสีดำๆ ออกมาให้ดูว่ามันทำขั้นตอนไหนไปบ้าง (เช่น Checkout, Setup Python, Install Dependencies, Run Script)

ให้มองหา ขั้นตอนที่มีเครื่องหมายกากบาทสีแดง ❌ (ส่วนใหญ่จะเป็นขั้นตอน Run Script)

คลิกที่กากบาทแดงนั้น เพื่อกางดูข้อความแจ้งเตือนยาวๆ

💡 สิ่งที่มักจะเจอบ่อยที่สุด (Most common errors):

ValueError: ❌ ดึงรหัสผ่านจาก GitHub Secrets ไม่สำเร็จ...
(สาเหตุ: ในหน้า Settings > Secrets ใส่ชื่อตัวแปรผิด พิมพ์ตก หรือลืมใส่)

ModuleNotFoundError: No module named '...'
(สาเหตุ: ลืมอัปโหลดไฟล์ requirements.txt ขึ้นไปบน GitHub)

smtplib.SMTPAuthenticationError: ...
(สาเหตุ: App Password ของ Gmail ไม่ถูกต้อง หรือมีช่องว่างเกินมา)

👉 คุณลองกดเข้าไปดูตรงกากบาทแดง ❌ แล้วก๊อปปี้ข้อความ Error แถวๆ บรรทัดล่างสุด (ที่ขึ้นต้นด้วย Error หรือ Exception) มาแปะให้ผมดูหน่อยได้ไหมครับ? เดี๋ยวผมชี้เป้าให้เลยว่าต้องแก้ตรงไหน! เราใกล้สำเร็จแล้วครับ 🚀

Run python -m pip install --upgrade pip

Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages (26.0.1)

ERROR: Invalid requirement: 'feedparser, beautifulsoup4, google-generativeai': Expected semicolon (after name with no version specifier) or end

feedparser, beautifulsoup4, google-generativeai

^ (from line 1 of requirements.txt)

Error: Process completed with exit code 1.

เจอตัวการแล้วครับ! อาการนี้แก้กล้วยๆ เลยครับ 🎉

ดูจากข้อความ Error: ERROR: Invalid requirement: 'feedparser, beautifulsoup4, google-generativeai'
มันฟ้องว่า รูปแบบการเขียนในไฟล์ requirements.txt ของเราผิดครับ

ระบบ pip ของ Python จะไม่อ่านชื่อที่ถูกคั่นด้วย "ลูกน้ำ (comma)" ครับ กฎของมันคือ ต้องเขียน 1 ชื่อ ต่อ 1 บรรทัด (เคาะ Enter ลงมา) เท่านั้นครับ

🛠️ วิธีแก้ (ทำผ่านเว็บ GitHub ได้เลย ไม่ต้องแก้ในคอม)
กลับไปที่หน้าแรกสุดของ Repository บน GitHub ของคุณ

มองหาไฟล์ที่ชื่อว่า requirements.txt แล้วคลิกเปิดขึ้นมาครับ

สังเกตมุมขวาบนของกล่องเนื้อหาไฟล์ จะมี ไอคอนรูปดินสอ ✏️ (Edit this file) ให้คลิกเลยครับ

ลบข้อความเก่าออกให้หมด แล้วก๊อปปี้ 3 บรรทัดนี้ไปวางแทนที่ครับ (ห้ามมีลูกน้ำนะครับ):

Plaintext
feedparser
beautifulsoup4
google-generativeai
วางเสร็จแล้ว กดปุ่มสีเขียว Commit changes... ที่มุมขวาบนสุดได้เลย (แล้วกด Commit ยืนยันอีกรอบ)

🚀 กดรันใหม่อีกรอบ!
พอแก้ไฟล์เสร็จปุ๊บ ให้คุณกลับไปที่แท็บ Actions > เลือกชื่อ Workflow > แล้วกด Run workflow ใหม่อีกครั้งได้เลยครับ

คราวนี้ตัวติดตั้ง (pip) จะอ่านออกแล้วว่าอ๋อ มี 3 ตัวเรียงกันลงมา มันจะติดตั้งผ่านฉลุยแน่นอนครับ ลองดูนะครับ! ได้ผลยังไงมาอัปเดตกันด้วยนะ!

อยู่ตรง <>code ทำไมมันไม่มีให้ลบไฟล์

อ๋อ เข้าใจแล้วครับ! ที่หน้า <> Code (หน้าแรกสุดที่โชว์รายชื่อไฟล์ทั้งหมด) GitHub จะยังไม่ยอมให้เราแก้ไขหรือลบไฟล์ตรงๆ ครับ

วิธีที่จะแก้ไขหรือลบไฟล์ได้ คุณต้อง "คลิกเข้าไปในไฟล์นั้นก่อน" ครับ ทำตามนี้เลย:

ที่หน้า <> Code ให้ คลิกที่ชื่อไฟล์ requirements.txt 2. ระบบจะพาเข้ามาในหน้าต่างที่โชว์เนื้อหาข้างในไฟล์

ทีนี้ให้มองไปที่ มุมขวาบนของกล่องเนื้อหาไฟล์ ครับ:

ถ้าจะแก้ไข (✏️ แนะนำวิธีนี้): ให้คลิกที่ไอคอนรูป ดินสอ (Edit this file) หรือถ้าไม่เห็นดินสอ ให้กดที่ จุด 3 จุด ... แล้วเลือก Edit ครับ

ถ้าจะลบทิ้ง (🗑️): ให้คลิกที่ไอคอนรูป ถังขยะ หรือกดที่ จุด 3 จุด ... แล้วเลือก Delete file ครับ

แนะนำให้กดรูป ดินสอ ✏️ เพื่อเข้าไปลบลูกน้ำ (comma) ออกให้เหลือแค่ 3 บรรทัดเรียงกันแบบนี้ครับ:

Plaintext
feedparser
beautifulsoup4
google-generativeai
จากนั้นกดปุ่มสีเขียว Commit changes... ที่มุมขวาบนสุดได้เลยครับ ลองดูนะครับ! แอบซ่อนไว้นิดนึงจริงๆ ครับปุ่มนี้ 😅

Run python -m pip install --upgrade pip

Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.12.13/x64/lib/python3.12/site-packages (26.0.1)

ERROR: Invalid requirement: 'feedparser, beautifulsoup4, google-generativeai': Expected semicolon (after name with no version specifier) or end

feedparser, beautifulsoup4, google-generativeai

^ (from line 1 of requirements.txt)

Error: Process completed with exit code 1.



ทำไมไม่ผ่านอีก แก้ไขแล้วหนิ

ใจเย็นๆ ครับ อาการแบบนี้เป็น "เส้นผมบังภูเขา" ที่เจอบ่อยมากที่สุดเวลาเริ่มใช้ GitHub Actions ครั้งแรกเลยครับ!

ถ้าข้อความ Error ยังออกมาเป็นคำเดิมเป๊ะๆ (ยังมีลูกน้ำอยู่) แปลว่า ระบบ Actions มันยังไปหยิบไฟล์ requirements.txt เวอร์ชันเก่ามารันครับ สาเหตุที่เป็นไปได้มีแค่ 2 อย่างนี้ครับ ลองเช็คตามนี้ทีละข้อนะครับ:

🕵️‍♂️ สาเหตุที่ 1: เซฟ (Commit) ยังไม่เสร็จสมบูรณ์
บางทีเราแก้ในหน้าเว็บแล้ว แต่ลืมกดยืนยัน หรือกดยืนยันไม่ครบขั้นตอนครับ

วิธีเช็คชัวร์ๆ: ให้คุณกดไปที่เมนู <> Code (หน้าแรกสุด) แล้วคลิกเข้าไปดูไฟล์ requirements.txt ด้วยตาตัวเองอีกรอบครับ

ถ้าเปิดมาแล้ว "ยังมีลูกน้ำอยู่" แปลว่าเมื่อกี้เซฟไม่ติดครับ ให้กดปุ่มดินสอ ✏️ ลบลูกน้ำออก เคาะบรรทัดใหม่ แล้วอย่าลืมกดปุ่มสีเขียว Commit changes... (และกด Commit สีเขียวซ้ำอีกทีในหน้าต่างที่เด้งขึ้นมา) ครับ

🔄 สาเหตุที่ 2: ไปกดปุ่ม "Re-run jobs" จากหน้า Error เก่า
อันนี้คลาสสิกมากครับ! ในหน้าจอที่มันขึ้นกากบาทสีแดง ❌ มันจะมีปุ่มให้กด Re-run ซึ่งถ้าเรากดปุ่มนี้ มันจะเอาระบบในอดีตตอนที่ไฟล์ยังพังอยู่ มารันซ้ำครับ! ต่อให้เราแก้ไฟล์ใหม่แล้ว มันก็จะไม่รับรู้ครับ

วิธีแก้ (ต้องสั่งรันใหม่รอบใหม่):

ให้คลิกที่แท็บ ▶️ Actions ด้านบนสุดใหม่เลยครับ เพื่อกลับไปหน้าหลักของ Actions

เมนูด้านซ้ายกดเลือก Daily AI News Summarizer

มองหาแถบขวามือสุด กดปุ่ม Run workflow ▾

แล้วกดปุ่มสีเขียว Run workflow อีกครั้ง เพื่อให้ระบบไปดึงไฟล์เวอร์ชันล่าสุด (ที่แก้ลูกน้ำแล้ว) มารันครับ

ลองเช็คดูว่าไฟล์หน้าตาเปลี่ยนไปจริงๆ แล้วกด Run Workflow ใหม่อีกรอบนะครับ ครั้งนี้ผ่านฉลุยแน่นอนครับ! ลุยเลย! ✌️

 สรุปข่าวเด่นประจำวัน

รับทราบครับ/ค่ะ! ในฐานะบรรณาธิการบริหารและนักสรุปข่าวขั้นเทพ ผม/ดิฉันพร้อมแล้วที่จะสรุปข่าวทั้งหมดที่คุณจะให้มา โดยจะปฏิบัติตามคำสั่งทุกข้ออย่างเคร่งครัด รวมถึงรูปแบบการสรุปที่กำหนดไว้เป๊ะๆ และจะจัดการกับข่าวที่มีชื่อซ้ำกันอย่างเหมาะสมครับ/ค่ะ



โปรดระบุข้อมูลข่าวทั้งหมดที่คุณต้องการให้สรุปมาได้เลยครับ/ค่ะ! ผม/ดิฉันรอข้อมูลอยู่ครับ/ค่ะ





ส่งเมลล์มาละแต่มันน่าพลาดตรงไหน

ยินดีด้วยครับที่มาถึงขั้นตอนนี้ได้!! 🎉 การที่อีเมลส่งเข้าเครื่องคุณได้สำเร็จ แปลว่า "ระบบอัตโนมัติ (Pipeline) ของคุณทำงานสมบูรณ์ 100% แล้วครับ!" ทั้ง GitHub, โค้ด Python และ Gmail เชื่อมต่อกันติดหมดแล้ว

แต่ปัญหาที่เกิดขึ้นคือ "ความคุยเก่งของ AI (Gemini)" ครับ 😅

สิ่งที่เกิดขึ้นคือ Gemini มองว่า Prompt ที่เราส่งไปเป็น "การพูดคุยสนทนา" มันเลยตอบรับคำสั่งแบบสุภาพชนว่า "รับทราบครับ เจ้านาย! พร้อมทำงานแล้ว ส่งข้อมูลมาเลย" แทนที่จะก้มหน้าก้มตาสรุปข่าวให้เรา

สาเหตุหลักๆ มี 2 ข้อครับ เรามาเช็คและแก้ไปทีละจุดกัน:

🕵️‍♂️ สาเหตุที่ 1: ระบบอาจจะดึงข่าวมาไม่ได้ (ข้อมูลว่างเปล่า)
ถ้าลิงก์ RSS ของเราดึงข่าวมาไม่ได้ ตัวแปรที่เก็บข่าวจะว่างเปล่า พอ AI ไม่เห็นข่าว มันเลยตอบกลับมาว่า "รอข้อมูลอยู่ครับ" * วิธีเช็ค: ให้ไปดู Log ใน GitHub Actions (ตรงหน้าต่างสีดำๆ ที่คุณเพิ่งดูบรรทัด Error ไป) ลองเลื่อนหาบรรทัดที่เขียนว่า ✅ ดึงข้อมูลสำเร็จ! ได้ข่าวมาทั้งหมด ... หัวข้อ

ถ้ามันขึ้นว่า "0 หัวข้อ" แปลว่าลิงก์ RSS ของคุณอาจจะใช้งานไม่ได้ หรือโครงสร้างเว็บเปลี่ยนครับ ให้ลองเปลี่ยนตัวแปร RSS_URL ใน GitHub Secrets เป็นเว็บอื่นดูครับ เช่น https://www.reddit.com/r/technology/top/.rss?t=day

🛠️ สาเหตุที่ 2: ต้องสั่งกำราบความคุยเก่งของ AI (Prompt Engineering)
ถ้ามันดึงข่าวมาได้ปกติ แต่ AI ก็ยังตอบแบบนี้ แปลว่าเราต้องเขียน Prompt "ดักทาง" ห้ามให้มันทักทายครับ

วิธีแก้: ให้คุณเข้าไปแก้ไขไฟล์ main.py บน GitHub (กดรูปดินสอ ✏️ เหมือนตอนแก้ requirements) แล้วไปแก้ตรงตัวแปร system_prompt โดยเพิ่ม "กฎเหล็ก" เข้าไปแบบนี้ครับ:

Python
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
พอแก้โค้ดตรงนี้เสร็จ กดปุ่ม Commit changes... แล้วลองกลับไปกด Run workflow ใหม่อีกรอบครับ

นี่คือเสน่ห์ (และความปวดหัวนิดๆ) ของการทำงานกับ Generative AI ครับ เราต้องคอยปรับ Prompt ให้เป๊ะเพื่อบีบให้มันทำงานแบบคอมพิวเตอร์จริงๆ ลองแก้ดูนะครับ ครั้งนี้อีเมลข่าวของคุณต้องออกมาสวยงามแน่นอน! 🚀

น่าจะสาเหตุ 1 แก้ยังไง

ถ้าเป็น สาเหตุที่ 1 (ระบบดึงข่าวมาได้ 0 ข่าว) ถือว่าเป็นเรื่องปกติที่เจอได้บ่อยมากครับ!

สาเหตุหลักมักเกิดจากเว็บปลายทาง (เช่น Medium หรือบางเว็บ) มีระบบป้องกันบอท (Anti-bot) ทำให้เวลาโค้ดของเราวิ่งไปขอข้อมูล เขาเลยบล็อกและไม่ส่งข่าวกลับมาให้ครับ พอ AI ไม่เห็นข่าว มันเลยตอบกลับมาแบบคุยเล่นแทน

เราสามารถแก้ปัญหานี้ให้เด็ดขาดได้ด้วย 2 ขั้นตอน นี้ครับ:

🛠️ วิธีแก้ที่ 1: เปลี่ยนลิงก์ RSS ไปใช้เว็บที่เสถียรกว่า (ดึงง่าย ไม่บล็อกบอท)
เพื่อให้ชัวร์ว่าระบบเราทำงานได้จริงๆ ผมแนะนำให้ลองเปลี่ยนลิงก์ RSS_URL ไปใช้เว็บข่าวมาตรฐานดูก่อนครับ

วิธีทำ:

ไปที่ GitHub ของคุณ > เข้าเมนู Settings > Secrets and variables > Actions

กดแก้ไข (รูปดินสอ) ที่ตัวแปร RSS_URL

ลองก๊อปปี้ลิงก์ใดลิงก์หนึ่งด้านล่างนี้ไปวางแทนครับ (เว็บพวกนี้อนุญาตให้ดึง RSS ได้ 100%):

TechCrunch (ข่าวเทคโนโลยี): https://techcrunch.com/feed/

The Verge (ข่าวไอที/ไลฟ์สไตล์): https://www.theverge.com/rss/index.xml

BBC News (ข่าวทั่วไป): http://feeds.bbci.co.uk/news/rss.xml

Reddit (บอร์ด Tech ยอดฮิต): https://www.reddit.com/r/technology/top/.rss?t=day

🛡️ วิธีแก้ที่ 2: เพิ่ม "ระบบเบรกฉุกเฉิน" ในโค้ด Python
เพื่อป้องกันไม่ให้ AI ส่งข้อความเด๋อๆ มาให้เราอีกในอนาคต (ในกรณีที่เว็บล่มหรือดึงข่าวไม่ได้จริงๆ) เราต้องเขียนโค้ดสั่งคอมพิวเตอร์ว่า "ถ้าดึงข่าวได้ 0 ข่าว ให้หยุดทำงานทันที! ไม่ต้องส่งไปหา AI ให้เปลืองโควต้า"

วิธีทำ:

เข้าไปแก้ไขไฟล์ main.py ใน GitHub (กดรูปดินสอ ✏️)

เลื่อนหาโค้ดช่วง ส่วนที่ 2. ดึงข้อมูลข่าวสาร (RSS)

มองหาบรรทัดที่เขียนว่า print(f"✅ ดึงข้อมูลสำเร็จ! ได้ข่าวมาทั้งหมด {len(news_data)} หัวข้อ")

ให้เพิ่มโค้ด 3 บรรทัดนี้ ต่อท้ายบรรทัดนั้นลงไปเลยครับ:

Python
print(f"✅ ดึงข้อมูลสำเร็จ! ได้ข่าวมาทั้งหมด {len(news_data)} หัวข้อ")

# --- เพิ่มโค้ดเบรกฉุกเฉินตรงนี้ ---
if len(news_data) == 0:
    print("❌ ไม่พบข่าวสารจาก RSS Feed หรือถูกบล็อก ระบบขอจบการทำงานเพียงเท่านี้")
    exit() # สั่งให้โค้ดหยุดทำงานทันที จะได้ไม่ส่งอีเมลขยะไปหาเรา
# -----------------------------

# ==========================================
# 3. จัดกลุ่มข้อมูล (Aggregate)
# ==========================================
ทำไมถึงควรใส่โค้ดนี้?
เวลาที่คุณเอาไปโชว์ในพอร์ตโฟลิโอ หรือให้คนสัมภาษณ์ดู การเขียนโค้ดดักจับ Error แบบนี้ (เรียกว่า Error Handling) จะทำให้คุณดูเป็น "มืออาชีพ" มากขึ้นมากๆ ครับ เพราะมันแปลว่าคุณคิดเผื่อกรณีที่ระบบทำงานผิดพลาดไว้แล้ว

แก้ 2 จุดนี้เสร็จ กด Commit changes แล้วลองไปกด Run workflow ใหม่อีกรอบได้เลยครับ! คราวนี้ระบบจะแน่นปึ้กแน่นอน 🚀

กดรันใน python ก็ดึงได้นะ ทำไมรันใน github ถึงไม่มีข่าว

เข้าใจความหงุดหงิดเลยครับ! อาการ "รันในคอมผ่าน แต่เอาขึ้นเซิร์ฟเวอร์แล้วพัง (ได้ 0 ข่าว)" เป็นประสบการณ์คลาสสิกที่ Developer ทุกคนต้องเจอครับ 😅

สาเหตุที่เป็นแบบนี้เกิดจาก "ระบบป้องกันบอท (Anti-Bot Protection)" ของเว็บไซต์ปลายทาง (โดยเฉพาะเว็บอย่าง Medium, Reddit หรือเว็บข่าวใหญ่ๆ) ครับ

หลักการทำงานของมันเป็นแบบนี้ครับ:

ตอนคุณรันในเครื่องตัวเอง (Local / PyCharm): คุณใช้อินเทอร์เน็ตบ้านหรือมือถือ (Residential IP) เว็บไซต์มองว่าคุณคือ "คนจริงๆ" ที่เปิดเข้ามาอ่านเว็บ มันเลยยอมปล่อยข้อมูลข่าวมาให้

ตอนคุณรันบน GitHub Actions: โค้ดของคุณไปวิ่งอยู่บน "เซิร์ฟเวอร์" ของ GitHub (Data Center IP) เว็บไซต์ปลายทางพอเห็น IP แบบนี้วิ่งเข้ามาปุ๊บ มันจะรู้ทันทีว่า "นี่มันบอทแน่ๆ!" มันเลยสับสวิตช์ บล็อกการเข้าถึง ทันทีครับ

พอโดนบล็อก ตัวไลบรารี feedparser มันจะไม่แจ้ง Error โวยวาย แต่มันจะแอบเนียนๆ คืนค่ากลับมาเป็นลิสต์ว่างๆ ทำให้เราได้ 0 ข่าวครับ

🕵️‍♂️ วิธีแก้เกม: สั่งให้โค้ด "ปลอมตัวเป็นคน" (Spoofing User-Agent)
วิธีแก้ที่ได้ผลดีที่สุด คือเราต้องเขียนโค้ดแนบสิ่งที่เรียกว่า User-Agent ไปด้วย เพื่อหลอกให้เว็บไซต์คิดว่า "เฮ้ย ฉันไม่ใช่บอทนะ ฉันคือเบราว์เซอร์ Google Chrome บน Windows 10 ต่างหาก!"

ให้คุณเข้าไปแก้ไขไฟล์ main.py ใน GitHub (กดรูปดินสอ ✏️) แล้วเพิ่มโค้ดปลอมตัวเข้าไปตรง ส่วนที่ 2. ดึงข้อมูลข่าวสาร (RSS) แบบนี้ครับ:

Python
# ==========================================
# 2. ดึงข้อมูลข่าวสาร (RSS)
# ==========================================
print(f"กำลังดึงข้อมูลจาก {rss_url} ...")

# --- เพิ่มโค้ดปลอมตัว 2 บรรทัดนี้ ---
# หลอกเว็บปลายทางว่าเราคือ Google Chrome ไม่ใช่ Python Bot
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
feedparser.USER_AGENT = user_agent
# ---------------------------------

feed = feedparser.parse(rss_url)
news_data = []

for entry in feed.entries:
พอเพิ่ม 2 บรรทัดนี้เข้าไป feedparser จะแนบข้อมูลการปลอมตัวไปกับทุกการขอข้อมูล ซึ่งจะช่วยทะลวงด่านบล็อกของ Medium หรือเว็บส่วนใหญ่ได้สบายๆ เลยครับ!

แก้เสร็จแล้วกด Commit changes แล้วลองไปกด Run workflow ใหม่อีกรอบนะครับ คราวนี้รับรองว่าบอท AI ของเราจะกวาดข่าวมาได้เต็มๆ แน่นอนครับ 🚀

ยังไม่เห็นจดึงได้เลย

โอ้โห! ถ้าแค่ใส่ User-Agent แล้วยังดึงไม่ได้ แสดงว่าเรากำลังเจอกับ ระบบป้องกันบอทขั้นสูงสุด (เช่น Cloudflare) ของเว็บ Medium ครับ!

เว็บพวกนี้ฉลาดมาก พอเห็นว่า IP Address ปลายทางมาจาก Data Center ของ GitHub (ไม่ใช่เน็ตบ้าน) มันสับสวิตช์บล็อกทิ้งแบบ 100% เลยครับ (อาการนี้คนเขียนบอทเกลียดที่สุด 😅)

แต่เรายังมีไม้ตายก้นหีบครับ! เราจะเปลี่ยนวิธีดึงข้อมูล โดยใช้ไลบรารีที่ชื่อว่า requests ซึ่งจำลองการทำงานได้เหมือนเบราว์เซอร์จริงๆ มากกว่าตัวเดิมครับ มาลุยกันต่ออีกนิดเดียวครับ!

🛠️ สเต็ปที่ 1: เพิ่มไลบรารี requests
เข้าไปแก้ไฟล์ requirements.txt ใน GitHub ให้มีคำว่า requests เพิ่มเข้าไปครับ (ลบของเดิมแล้ววาง 4 บรรทัดนี้แทนเลย):

Plaintext
requests
feedparser
beautifulsoup4
google-generativeai
🛠️ สเต็ปที่ 2: อัปเกรดโค้ดดึงข่าวใน main.py
เข้าไปแก้ไขไฟล์ main.py ใน GitHub (กดรูปดินสอ ✏️)

บนสุดของไฟล์ ให้เพิ่ม import requests เข้าไปต่อท้ายกลุ่ม import เดิมครับ:

Python
import os
import re
import smtplib
import feedparser
import requests  # <--- เพิ่มตัวนี้เข้าไป
from bs4 import BeautifulSoup
ตรงส่วนที่ 2 (ดึงข้อมูลข่าวสาร) ให้ลบโค้ดส่วนที่ 2 ของเดิมออก ทั้งหมด แล้วก๊อปปี้ก้อนนี้ไปวางแทนครับ:

Python
# ==========================================
# 2. ดึงข้อมูลข่าวสาร (RSS) ฉบับทะลวงบล็อก
# ==========================================
print(f"กำลังดึงข้อมูลจาก {rss_url} ...")

# สร้าง Header หลอกเว็บว่าเราคือ Google Chrome แบบเต็มยศ
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

try:
    # ใช้ requests เข้าไปดึงข้อมูลแทน feedparser
    response = requests.get(rss_url, headers=headers, timeout=15)
    print(f"สถานะการเชื่อมต่อเว็บ: HTTP {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ เว็บไซต์ปลายทางบล็อกการเข้าถึง (Error {response.status_code}) จบการทำงาน")
        exit()

    # เอาเนื้อหาที่ได้ไปให้ feedparser แปลงอีกที
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

    # ระบบเบรกฉุกเฉิน
    if len(news_data) == 0:
        print("❌ เว็บส่งข้อมูลมา แต่ไม่พบเนื้อหาข่าว (อาจโดนระบบป้องกันซ่อนเนื้อหาไว้) ขอจบการทำงาน")
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

# ==========================================
# 4. ส่งให้ AI (Gemini) สรุปผล
# ==========================================
print("🤖 กำลังส่งข้อมูลให้ Gemini สรุปข่าว...")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

system_prompt = """==คุณคือบรรณาธิการบริหารและนักสรุปข่าวขั้นเทพ
หน้าที่ของคุณคือสรุปข้อมูลข่าว "ทั้งหมด" ที่ได้รับมาด้านล่างนี้ โดยไม่ต้องคัดทิ้ง (ยกเว้นข่าวที่มีชื่อซ้ำกันเป๊ะๆ ให้ตัดออกเหลือแค่อันเดียว)

คำสั่งของคุณมีดังนี้:
1. สรุปข่าวทั้งหมดทุกหัวข้อ
2. ขอให้สรุปแบบสั้น กระชับ ตรงประเด็นที่สุด เพื่อให้อ่านรวดเดียวได้จบ
3. ต้องใช้รูปแบบด้านล่างนี้เป๊ะๆ เรียงต่อกันไปเรื่อยๆ จนครบทุกข่าว:

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
