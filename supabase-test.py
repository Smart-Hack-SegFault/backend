import os
import dotenv
import supabase

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)

client.table("Test-Table").insert({'name': 'Lucian'}).execute()
