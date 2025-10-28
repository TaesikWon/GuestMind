# app/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 로그 폴더 없으면 생성
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 포맷
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 파일 핸들러 (5MB까지, 3개 백업)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

# 루트 로거 설정
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

# 가져다 쓸 전역 로거
logger = logging.getLogger("soulstay")
