import motor.motor_asyncio
import os
from dotenv import load_dotenv, find_dotenv


env_loc = find_dotenv(".env")
load_dotenv(env_loc)

port = int(os.environ.get("MONGO_PORT"))
username = os.environ.get("MONGO_USERNAME")
password = os.environ.get("MONGO_PASSWORD")

mongo_driver = motor.motor_asyncio.AsyncIOMotorClient("db", port)

db = mongo_driver.barcelona
