import os
import dotenv
import supabase

from utils import get_user_info as gui

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)
# response = client.table('Organizations').select('*, User()').eq('id', 1).order('date').execute()
# print(response)

resp = gui.get_user_skill_streak(2, 7, client)
print(resp)
