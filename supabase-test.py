import os
import dotenv
import supabase

from utils import get_user_info as gui
from utils import get_company_info as gci

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)
# response = client.table('Organizations').select('*, User()').eq('id', 1).order('date').execute()
# print(response)

resp = gci.get_role_employees_points(4, client)
print(resp)
