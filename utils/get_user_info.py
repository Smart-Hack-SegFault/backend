from datetime import datetime, timedelta


def get_recommended_skills(user_id, sb_client):
    user_skills = sb_client.table('User_Skill').select('Tags(*)').eq('user', user_id).execute().data
    categories = [category['Tags']['category'] for category in user_skills]

    skills = sb_client.table('Tags').select('*').in_('category', categories).execute()
    return skills


def get_user_skill_hours(user_id, tag_id, sb_client):
    user_skill = sb_client.table('User_Skill').select('*').eq('user', user_id).eq('tag', tag_id).execute().data[0]
    days_worked = sb_client.table('DailyWork').select('*').eq('user_skill', user_skill['id']).execute().data

    days_hours_sum = 0
    for day in days_worked:
        days_hours_sum += day['hours']

    return user_skill['init_hours'] + days_hours_sum


def get_user_skill_days(user_id, tag_id, sb_client):
    user_skill = sb_client.table('User_Skill').select('*').eq('user', user_id).eq('tag', tag_id).execute().data[0]
    days_worked = sb_client.table('DailyWork').select('*').eq('user_skill', user_skill['id']).execute().data

    return days_worked


def get_user_skill_streak(user_id, skill_id, sb_client):
    user_skill = sb_client.table('User_Skill').select('id').eq('user', user_id).eq('tag', skill_id).execute().data[0]
    skill_dailies = sb_client.table('DailyWork').select('date').eq('user_skill', user_skill['id']).order('date',
                                                                                                         desc=True).execute().data

    dates = [datetime.strptime(date['date'], "%Y-%m-%d") for date in skill_dailies]

    if dates:
        streak = 1

        for i in range(1, len(skill_dailies)):
            if dates[i - 1] - timedelta(days=1) == dates[i]:
                streak += 1

        return streak

    return 0
