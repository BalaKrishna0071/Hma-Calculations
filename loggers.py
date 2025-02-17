import logging
import os.path
from config import log_dir

log_file = os.path.join(log_dir, "app.log")
logger = logging.getLogger(__name__)

# log format
log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
logging.basicConfig(format=log_format, filename=log_file, level=logging.DEBUG)

