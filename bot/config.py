from dotenv import load_dotenv

from os import getenv


load_dotenv()

ADMIN_ID = [131588321, 1677276933, 631403016]

TOKEN = getenv('TOKEN')

# Database

HOST = getenv('HOST')
DB_USER = getenv('DB_USER')
PASSWORD = getenv('PASSWORD')
DB_NAME = getenv('DB_NAME')
PORT = getenv('PORT')
