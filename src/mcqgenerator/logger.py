import logging
import os
from datetime import datetime


LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path=os.path.join(os.getcwd(),"logs")

os.makedirs(log_path,exist_ok=True)


LOG_FILEPATH=os.path.join(log_path,LOG_FILE)

#If the logging level is set to INFO, messages from INFO and higher (INFO, WARNING, ERROR, CRITICAL) will be displayed.
#DEBUG messages won’t show because the level is higher than DEBUG.
#asctime-> current time, "lineno" error is in which line, "levelname" what error "message" which messege which we have written
logging.basicConfig(level=logging.INFO, 
        filename=LOG_FILEPATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"

)
