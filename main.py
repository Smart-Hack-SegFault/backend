import os
import dotenv
import supabase
import pandas as pd
from utils import get_user_info as user_query

from fastapi import FastAPI


app = FastAPI()


dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{user_id}/{tag_id}")
async def fetch_user_task_hours(user_id, tag_id):
    data = user_query.get_user_task_hours(user_id, tag_id, client)
    return data

@app.get("/hello/{user_id}/{tag_id}")
async def fetch_user_task_days(user_id, tag_id):
    data = user_query.get_user_task_days(user_id, tag_id, client)
    return data