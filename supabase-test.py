import os
import dotenv
import supabase

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)
response = client.table('User').select('*').eq('organization', 1).execute()
print(response)

