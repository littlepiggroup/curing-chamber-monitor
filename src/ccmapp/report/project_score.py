# -*- coding: utf-8 -*-
from collections import namedtuple

from django.db import connection

from ccmapp import models
from ccmapp.collect_subscribe.collect_subscribe import get_proj_ids_collected_by_user


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def projects_sample_score(proj_ids, days=30):
    SCORE_POLICY = 3
    sample_data = {
        1: {"id": 1, "sample_deduction": -3.5},
        2: {"id": 2, "sample_deduction": -3.5}

    }
    sample_data = {proj_id:{"id": proj_id, "sample_deduction": 0.0} for proj_id in proj_ids}

    sql = '''
        SELECT
            project_id,
            count(id)*-0.5 as deduction
        FROM ccmapp_samplealert
        WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) >= %s AND status = 'CREATED'
                AND TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s AND project_id IN (%s)
        GROUP BY project_id;
    ''' % (SCORE_POLICY, days, ','.join([str(x) for x in proj_ids]))

    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            sample_data[named_row.project_id]['sample_deduction']=float(named_row.deduction)

    return sample_data


def projects_video_score(proj_ids, days=30):
    video_data = {
        1: {"id": 1, "video_deduction": -5.5},
        2: {"id": 2, "video_deduction": -4.5},
    }
    video_data = {proj_id:{"id": proj_id, "video_deduction": 0.0} for proj_id in proj_ids}
    sql = '''
    SELECT
        project_id,
        count(id) * -2.0 as deduction
    FROM ccmapp_videoalert
    WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s AND project_id IN (%s)
    GROUP BY project_id;
    ''' % (days, ','.join([str(x) for x in proj_ids]))
    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            video_data[named_row.project_id]['video_deduction']=float(named_row.deduction)

    return video_data


def get_project_ids(comp_id):
    if comp_id is not None:
        company = models.BuildingCompany.objects.get(pk=int(comp_id))
        proj_ids = [y.id for y in company.projectlist.all()]
    else:
        proj_ids = [y.id for y in models.Project.objects.all()]
    return proj_ids


def projects_temperature_score(proj_ids, days=30):
    pass
    data = {
        1: {"id": 1, "temperature_deduction": -5.0},
        2: {"id": 2, "temperature_deduction": -4.0},
    }
    data = {proj_id:{"id": proj_id, "temperature_deduction": 0.0} for proj_id in proj_ids}

    sql = '''
    SELECT
        project_id,
        count(id)*-1.0 as deduction
    FROM ccmapp_temperaturealert
    WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s AND project_id IN (%s)
    GROUP BY project_id;

    ''' % (days, ','.join([str(x) for x in proj_ids]))
    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            data[named_row.project_id]['temperature_deduction'] = float(named_row.deduction)

    return data


def projects_humidity_score(proj_ids, days):
    pass
    data = {
        1: {"id": 1, "humidity_deduction": -5.0},
        2: {"id": 2, "humidity_deduction": -5.0},

    }
    data = {proj_id:{"id": proj_id, "humidity_deduction": 0.0} for proj_id in proj_ids}

    sql = '''
    SELECT
        project_id,
        count(id)*-1.0 as deduction
    FROM ccmapp_humidityalert
    WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s AND project_id IN (%s)
    GROUP BY project_id;

    ''' % (days, ','.join([str(x) for x in proj_ids]))
    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            data[named_row.project_id]['humidity_deduction'] = float(named_row.deduction)

    return data

def merge_two_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z

def merge_scores(x, y):
    for k, v in y.items():
        x[k] = merge_two_dicts(x[k], y[k])
    return x


def company_projects_total_score(user_id, comp_id, orderby_score_asc=True, days=30):
    collect_proj_ids = get_proj_ids_collected_by_user(user_id)
    proj_ids = get_project_ids(comp_id)
    projects = models.Project.objects.filter(pk__in=proj_ids)
    project_id_to_name = dict([(proj.id, proj.project_name) for proj in projects])
    project_id_to_company_name = dict([(proj.id, proj.company_name) for proj in projects])

    sample_scores = projects_sample_score(proj_ids, days)
    video_scores = projects_video_score(proj_ids, days)
    temperature_scores = projects_temperature_score(proj_ids, days)
    humidity_scores = projects_humidity_score(proj_ids, days)
    score_list = [sample_scores, video_scores,
                  temperature_scores, humidity_scores]
    all_scores = reduce(lambda s, t: merge_scores(s, t), score_list)

    def get_total_score(e):
        def inner_merge_score(u, w):
            if w[0].endswith('deduction'):
                return u + w[1]
            else:
                return u

        total_score = reduce(inner_merge_score, e.items(), 0.0)
        return total_score

    def add_score_and_name(k,v):
        v['project_name'] = project_id_to_name[k]
        v['company_name'] = project_id_to_company_name[k]
        v['is_collect'] = k in collect_proj_ids
        score_temp = 100.0 + get_total_score(v)
        if score_temp < 0:
            v['score'] = 0.0
        else:
            v['score'] = score_temp
        return v

    all_scores = {k: add_score_and_name(k, v) for k, v in all_scores.items()}
    print all_scores
    sorted_result = sorted(all_scores.values(), key=lambda e: e['score'], reverse=not orderby_score_asc)
    for x in sorted_result:
        print x
    return sorted_result

if __name__ == '__main__':
    company_projects_total_score(1, False)
