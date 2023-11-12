from openai import OpenAI
import dotenv
import os
import json


dotenv.load_dotenv()
system_prompt = os.environ.get("SYSTEM_PROMPT")
api_key = os.environ.get("OPENAI_KEY2")

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key
)


skill_levels = ['beginner', 'intermediate', 'advanced', 'professional', 'expert']


def skill_improv_task_suggestion(tags, level):  # tags va fi un string si level un numar intre 0 si 4
    query_body = f"\"{tags}\", {skill_levels[level]}"
    for i in range(5):
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": query_body
                    }
                ],
                model="gpt-4",
                max_tokens=512,
                temperature=1.01,
                stop=["\n{"]
            )
            json_ans = json.loads(response.choices[0].message.content)
            if not (isinstance(json_ans["project"], str) and isinstance(json_ans["description"], str) and isinstance(json_ans['hours'], int)):
                raise ValueError
            return json_ans
        except:
            continue
