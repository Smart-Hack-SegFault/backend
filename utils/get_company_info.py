def get_user_hours(user_id, tag_id, sb_client):
    user_skill = sb_client.table('User_Skill').select('*').eq('user', user_id).eq('tag', tag_id).execute().data[0]
    days_worked = sb_client.table('DailyWork').select('*').eq('user_skill', user_skill['id']).execute().data

    days_hours_sum = 0
    for day in days_worked:
        days_hours_sum += day['hours']

    return user_skill['init_hours'] + days_hours_sum


def get_employees(org_id, sb_client):
    employees = sb_client.table('User').select('*, Roles(*)').eq('organization', org_id).order('org_hours',
                                                                                               desc=True).execute().data
    return employees


def get_role(org_id, role_id, sb_client):
    role = sb_client.table('User').select('*').eq('organization', org_id).order('org_hours', desc=True).eq('org_role',
                                                                                                           role_id).execute().data
    return role


def get_role_employees_points(role_id, sb_client):
    skills_for_role = sb_client.table('Role_Skill').select('*, Tags(*)').eq('role', role_id).execute().data
    employees_for_role = sb_client.table('User').select('*, User_Skill(*)').eq('org_role', role_id).execute().data

    skills_dict = {}
    for skill in skills_for_role:
        skills_dict[skill['Tags']['id']] = True

    employees_points = {}
    for employee in employees_for_role:
        for skill in employee['User_Skill']:
            if skill['tag'] in skills_dict:
                if employee['name'] not in employees_points:
                    employees_points[employee['name']] = skill['points']
                else:
                    employees_points[employee['name']] += skill['points']

    result = sorted(employees_points.items(), key=lambda val: val[1], reverse=True)
    return [{"name": val[0], "points": val[1]} for val in result]
