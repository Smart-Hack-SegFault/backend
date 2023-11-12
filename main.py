import os
import dotenv
import supabase
import pandas as pd
from utils import get_user_info as user_query
from utils import get_company_info as org_query
from data_manipulation import statistics
from ai_integration import gpt_integration as ai

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
    stats, data = statistics.compute_stats_work_days(data)
    return stats, data


@app.get("/user/{user_id}/skill/recommend")
async def get_recommended_skills(user_id):
    return user_query.get_recommended_skills(user_id, client)


@app.get("/user/{user_id}/skill/{skill_id}/streak")
async def get_skill_streak(user_id, skill_id):
    return user_query.get_user_skill_streak(user_id, skill_id, client)


@app.get("/user/{user_id}/daily-activity")
async def get_daily_activity(user_id):
    return user_query.get_user_dailies(user_id, client)


@app.get("/user/recommendation/{tags}/{level}")
async def get_ai_recommendation(tags: str, level: int):
    return ai.skill_improv_task_suggestion(tags, level)


@app.get("/user/{user_id}/top-categories")
async def get_user_top_categories(user_id):
    return user_query.get_user_top_categories(user_id, client)

@app.get('/org/{org_id}/employees')
async def get_org_employees(org_id):
    return org_query.get_employees(org_id, client)
