from datetime import datetime, timedelta


def get_recommended_skills(user_id, sb_client):
    
    user_skills = sb_client.table('User_Skill').select('Tags(*, Categories(*))').eq('user', user_id).execute().data
    categories = [category['Tags']['category'] for category in user_skills]

    skills = sb_client.table('Tags').select('*, Categories(*)').in_('category', categories).execute().data

    user_skills_id = [val['Tags']['id'] for val in user_skills]
    return [skill for skill in skills if skill['id'] not in user_skills_id]


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
        sub = timedelta(days=1)
        streak = 1

        if (dates[0].date() != datetime.today().date() - sub) and (dates[0].date() != datetime.today().date()):
            return 0

        for i in range(1, len(skill_dailies)):
            if dates[i - 1].date() == dates[i].date():
                continue
            if dates[i - 1].date() - sub == dates[i].date():
                streak += 1

        return streak

    return 0


def get_user_dailies(user_id, sb_client):
    user_skills_dailies = sb_client.table('User_Skill').select('DailyWork(date)').eq('user', user_id).execute().data

    result = []
    for skill in user_skills_dailies:
        for date in skill['DailyWork']:
            date['count'] = 1
            result.append(date)

    return result


def get_user_top_categories(user_id, sb_client):
    data = sb_client.table("User_Skill").select("*, Tags(*, Categories(*))").execute()


def get_user_top_categories(user_id, sb_client):
    user_skills = sb_client.table('User_Skill').select("*, Tags(*, Categories(*)), DailyWork(hours)").eq('user',
                                                                                                         user_id).execute().data
    hours_per_category = {}

    def get_hours(skill):
        total = 0
        if skill['DailyWork']:
            for day_worked in skill['DailyWork']:
                total += day_worked['hours']

        total += skill['init_hours']
        return total

    for skill in user_skills:
        skill_hours = get_hours(skill)
        skill_category = skill['Tags']['Categories']['category']

        if skill_category not in hours_per_category:
            hours_per_category[skill_category] = [skill_hours, [(skill['Tags']['name'], skill_hours)]]
        else:
            hours_per_category[skill_category][0] += skill_hours
            hours_per_category[skill_category][1].append((skill['Tags']['name'], skill_hours))

    sorted_categories = sorted(hours_per_category.items(), key=lambda val: val[1][0], reverse=True)[:3]

    result = []
    for elem in sorted_categories:
        result.append({"name": elem[0], "total_hours": elem[1][0], "skills": elem[1][1]})

    return result
