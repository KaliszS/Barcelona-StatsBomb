from neo4j import GraphDatabase
import os
from dotenv import load_dotenv, find_dotenv


env_loc = find_dotenv(".env")
load_dotenv(env_loc)

uri = os.environ.get("NEO4J_URI")
username = os.environ.get("NEO4J_USERNAME")
password = os.environ.get("NEO4J_PASSWORD")

db = GraphDatabase.driver(uri, auth=(username, password))