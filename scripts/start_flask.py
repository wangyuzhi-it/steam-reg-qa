"""独立启动 Flask,只跑服务。"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from app import app  # noqa: E402

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5083
app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False, threaded=True)