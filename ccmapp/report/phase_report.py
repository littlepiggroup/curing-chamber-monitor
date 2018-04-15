# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple

from django.db import connection

from ccmapp.models import Project


def time_para_to_days(time_range):
    if time_range == 'last_month':
        days = 30
    elif time_range == 'last_week':
        days = 7
    elif time_range == 'last_day':
        days = 1
    else:
        raise Exception('Unknown time_range: %s' % time_range)
    return days

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def company_phase_report(company_id, days=30):
    '''

    :param company_id:
    :param days:
    :return: {'normal_project_count':3, 'alert_project_count': 6}
    '''
    if company_id is not None:
        company_id = int(company_id) # protect against SQL injection.

        report_sql = '''
        SELECT
        ccmapp_project.building_company_id AS building_company_id,
        ccmapp_project.id AS project_id,
        count(ccmapp_alert.id) AS alert_count,
        count(ccmapp_alert.id) > 0 AS has_alert
    FROM ccmapp_project LEFT OUTER JOIN ccmapp_alert ON ccmapp_project.id = ccmapp_alert.project_id
    WHERE ccmapp_project.building_company_id = %s
        AND (ccmapp_alert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_alert.create_time, NOW()) <= %s)
    GROUP BY ccmapp_project.id
    ;
        ''' % (company_id, days)
    else:
        # All companies data.
        report_sql = '''
        SELECT
            ccmapp_project.building_company_id AS building_company_id,
            ccmapp_project.id AS project_id,
            count(ccmapp_alert.id) AS alert_count,
            count(ccmapp_alert.id) > 0 AS has_alert
        FROM ccmapp_project LEFT OUTER JOIN ccmapp_alert ON ccmapp_project.id = ccmapp_alert.project_id
        WHERE (ccmapp_alert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_alert.create_time, NOW()) <= %s)
        GROUP BY ccmapp_project.id
        ;
            ''' % (days)

    with connection.cursor() as cursor:
        cursor.execute(report_sql)
        named_rows = namedtuplefetchall(cursor)
        good_project_counter = 0
        bad_project_counter = 0
        for row in named_rows:
            if row.has_alert:
                bad_project_counter += 1
            else:
                good_project_counter += 1
        return [{'normal_project_count': good_project_counter, 'alert_project_count': bad_project_counter}]


def get_project_filter_sql(company_id, project_id):
    sql = '1=1'
    if project_id is not None:
        sql = 'ccmapp_project.id = %s' % project_id
    elif company_id is not None:
        sql = 'ccmapp_project.building_company_id = %s' % company_id
    return sql


def company_projects_phase_report(company_id, project_id, days=30):
    '''

    :param company_id: if -1, all companies.
    :param project_id:
    :param days:
    :return: Give company's project list {'project_id': 1, 'score': 60, 'sample_alert_count':1, 'video_alert_count':3,...}
                order by score ASC
    '''
    project_filter_sql = get_project_filter_sql(company_id, project_id)
    sample_alert_count_map = get_alert_count(project_filter_sql, days, 'ccmapp_samplealert')
    video_alert_count_map = get_alert_count(project_filter_sql, days, 'ccmapp_videoalert')
    temp_humidity_alert_count_map = get_alert_count(project_filter_sql, days, 'ccmapp_temphumdtyalert')
    proj_ids = sample_alert_count_map.keys()
    proj_reports = []
    for proj_id in proj_ids:
        sample_alert_count = sample_alert_count_map[proj_id]
        video_alert_count = video_alert_count_map[proj_id]
        temp_humidity_alert_count = temp_humidity_alert_count_map[proj_id]
        score = 100.0 - (sample_alert_count * 0.5 + video_alert_count * 2.0 + temp_humidity_alert_count * 1.0)
        proj_reports.append({
            'project_id': proj_id,
            'project_names': get_project_names(proj_id),
            'score': score,
            'sample_alert_count': sample_alert_count,
            'video_alert_count': video_alert_count,
            'temperature_humidity_alert_count': temp_humidity_alert_count
        })
    return sorted(proj_reports, key=lambda x: x['score'])


def get_project_names(proj_id):
    return [project_name.name for project_name in Project.objects.get(pk=proj_id).names.all()]


def get_alert_count(project_filter_sql, days, alert_table_name):
    '''

    :param company_id:
    :param days:
    :param alert_table_name:
    :return:  map: {project_id, alert_count}
    '''
    alert_sql = '''
        SELECT
        ccmapp_project.building_company_id AS building_company_id,
        ccmapp_project.id AS project_id,
        count(ALERT_TABLE_NAME.id) AS alert_count
    FROM ccmapp_project LEFT OUTER JOIN ALERT_TABLE_NAME ON ccmapp_project.id = ALERT_TABLE_NAME.project_id
    WHERE %s
        AND (ALERT_TABLE_NAME.create_time IS NULL OR TIMESTAMPDIFF(DAY, ALERT_TABLE_NAME.create_time, NOW()) <= %s)
    GROUP BY ccmapp_project.id
    ;
        ''' % (project_filter_sql, days)

    actual_sql = alert_sql.replace('ALERT_TABLE_NAME', alert_table_name)

    project_to_alert_count = {}
    with connection.cursor() as cursor:
        cursor.execute(actual_sql)
        named_rows = namedtuplefetchall(cursor)
        for row in named_rows:
            project_to_alert_count[row.project_id] = row.alert_count
        return project_to_alert_count