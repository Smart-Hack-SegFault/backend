import pandas as pd
import matplotlib.pyplot as plt

import os
import dotenv
import supabase

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

client = supabase.create_client(url, key)
response = client.table('User').select('id', 1).execute()

def compute_stats(people):  # people
    stats_ore_munca_total = people["ore_tasks"].describe()
    stats_ore_invatare_curs_total = people["ore_curs"].describe()
    stats_ore_invatare_personale_total = people["ore_inv"].describe()



