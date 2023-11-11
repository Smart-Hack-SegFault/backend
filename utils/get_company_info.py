def get_user_hours(user_id, tag_id, sb_client):
    user_skill = sb_client.table('User_Skill').select('*').eq('user', user_id).eq('tag', tag_id).execute().data[0]
    days_worked = sb_client.table('DailyWork').select('*').eq('user_skill', user_skill['id']).execute().data

    days_hours_sum = 0
    for day in days_worked:
        days_hours_sum += day['hours']

    return user_skill['init_hours'] + days_hours_sum