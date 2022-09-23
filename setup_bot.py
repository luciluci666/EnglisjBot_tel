import os

from modules.create_db import create_db
from config import DEBUG, ROOT_DIR, DATABASE_NAME
from modules.parse_data import Parse

if __name__ == "__main__":
    if not os.path.isfile(f'{ROOT_DIR}/{DATABASE_NAME}'):      
        create_db()
    Parse().main()
    
