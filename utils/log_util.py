import logging
import os
from datetime import datetime
#日志配置
def get_logger():
    logs='./logs'
    if not os.path.exists(logs):os.mkdir(logs)
    log_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"./logs/api_log_{log_time}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file,encoding="utf-8"),
                  logging.StreamHandler()
                  ]
        )
    return logging.getLogger(__name__)
logger = get_logger()
