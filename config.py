from dotenv import load_dotenv
import os
load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))