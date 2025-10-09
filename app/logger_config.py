import logging
import uuid
import time
from logging.handlers import RotatingFileHandler
from contextvars import ContextVar
import os

# Context variable for request tracking
request_id_var = ContextVar("request_id", default=None)

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure main logger
logger = logging.getLogger("devmate")
logger.setLevel(logging.INFO)

# Handlers
file_handler = RotatingFileHandler("logs/devmate.log", maxBytes=1_000_000, backupCount=3)
console_handler = logging.StreamHandler()

# Professional log format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | [%(request_id)s] | %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# Inject request ID into each record
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get() or "-"
        return True


logger.addFilter(RequestIDFilter())


def set_request_id():
    """Generate and set a unique request ID."""
    request_id_var.set(str(uuid.uuid4())[:8])


def log_request_start(endpoint: str):
    """Log the start of a request."""
    set_request_id()
    logger.info(f"START {endpoint}")
    return time.time()  # start time


def log_request_end(endpoint: str, start_time: float):
    """Log the end of a request and its duration."""
    duration = time.time() - start_time
    logger.info(f"END {endpoint} | Duration: {duration:.2f}s")
