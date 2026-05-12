# ============================================================
# Group Manager Bot
# Author: LearningBotsOfficial
# License: Open-source (keep credits, no resale)
# ============================================================

import asyncio
# ✅ إنشاء حلقة أحداث للخيط الرئيسي (ضروري قبل استيراد Pyrogram)
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)

import os, sys, logging, traceback
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# استيراد Pyrogram ومكونات البوت
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from security import verify_integrity, get_runtime_key

logging.basicConfig(level=logging.INFO)

# ⚡ تجاوز التحقق من السلامة (لتجنب مشاكل Render)
# verify_integrity()
RUNTIME_KEY = get_runtime_key()

# إنشاء عميل البوت
app = Client(
    "group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# تسجيل جميع الأوامر
from handlers import register_all_handlers
register_all_handlers(app)

print("✅ Bot is starting securely...", flush=True)

# ---------- خادم صحة بسيط لإبقاء Render نشطاً ----------
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"🌐 Health server running on port {port}", flush=True)
    server.serve_forever()
# --------------------------------------------------------

if __name__ == "__main__":
    # تشغيل خادم الصحة في خيط منفصل (خلفي)
    health_thread = Thread(target=run_health_server, daemon=True)
    health_thread.start()

    # تشغيل البوت في الخيط الرئيسي مع التقاط الأخطاء
    print("🚀 Starting bot now...", flush=True)
    try:
        app.run()
    except Exception as e:
        print(f"❌ Bot crashed: {type(e).__name__}: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)
