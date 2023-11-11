import os
import dotenv
import supabase
import pandas as pd
from utils import get_user_info as user_query
from data_manipulation import statistics

from fastapi import FastAPI

app = FastAPI()

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/user/{user_id}/skill/{tag_id}/hours")
async def fetch_user_skill_hours(user_id, tag_id):
    data = user_query.get_user_skill_hours(user_id, tag_id, client)
    return data


@app.get("/user/{user_id}/skill/{tag_id}/stats")
async def fetch_user_skill_days_stats(user_id, tag_id):
    temp = pd.DataFrame(user_query.get_user_skill_days(user_id, tag_id, client))
    data = temp[['date', 'hours']]
    stats = statistics.compute_stats_work_days(data)
    return stats, data


# implement get_streak, get_similar_skills
@app.get("/user/{user_id}/skill/recommend")
async def get_recommended_skills():
    pass
