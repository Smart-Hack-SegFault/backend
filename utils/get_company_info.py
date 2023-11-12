def get_user_hours(user_id, tag_id, sb_client):
    user_skill = sb_client.table('User_Skill').select('*').eq('user', user_id).eq('tag', tag_id).execute().data[0]
    days_worked = sb_client.table('DailyWork').select('*').eq('user_skill', user_skill['id']).execute().data

    days_hours_sum = 0
    for day in days_worked:
        days_hours_sum += day['hours']

    return user_skill['init_hours'] + days_hours_sum


def get_employees(org_id, sb_client):
    employees = sb_client.table('User').select('*').eq('organization', org_id).order('org_hours', desc=True).execute().data
    return employees


def get_role(org_id, role_id, sb_client):
    role = sb_client.table('User').select('*').eq('organization', org_id).order('org_hours', desc=True).eq('org_role', role_id).execute().data
    return role