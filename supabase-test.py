import os
import dotenv
import supabase

from utils import get_user_info as gui

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)

resp = client.table('User').select('*').eq('organization', 1).execute().data
print(resp)
