import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("devmate")
logger.setLevel(logging.INFO)

# File handler (rotates after 1MB, keeps last 3 logs)
file_handler = RotatingFileHandler("logs/devmate.log", maxBytes=1_000_000, backupCount=3)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers if not already added
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
