# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import connection

from ccmapp.models import Project, SampleAlert, VideoAlert, TemperatureAlert, HumidityAlert
from ccmapp.report.utils import namedtuplefetchall


def get_concrete_alert_count(company_id, alert_table, days = 30):
    sql = ''
    if company_id is None:
        sql = '''
        SELECT COUNT(id) AS alert_count FROM TABLE_NAME
        WHERE (TABLE_NAME.create_time IS NULL OR TIMESTAMPDIFF(DAY, TABLE_NAME.create_time, NOW()) <= %s);
        ''' % (days)
    else:
        sql = '''
        SELECT COUNT(id) AS alert_count FROM TABLE_NAME
        WHERE TABLE_NAME.company_id = %s
                AND (TABLE_NAME.create_time IS NULL OR TIMESTAMPDIFF(DAY, TABLE_NAME.create_time, NOW()) <= %s);
        ''' % (company_id, days)
    sql = sql.replace('TABLE_NAME', alert_table)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        alert_count = named_rows[0].alert_count
    return alert_count


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
        ccmapp_project.company_id AS company_id,
        ccmapp_project.id AS project_id,
        count(ccmapp_alert.id) AS alert_count,
        count(ccmapp_alert.id) > 0 AS has_alert
    FROM ccmapp_project LEFT OUTER JOIN ccmapp_alert ON ccmapp_project.id = ccmapp_alert.project_id
    WHERE ccmapp_project.company_id = %s
        AND (ccmapp_alert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_alert.create_time, NOW()) <= %s)
    GROUP BY ccmapp_project.id
    ;
        ''' % (company_id, days)
    else:
        # All companies data.
        report_sql = '''

        SELECT
            ccmapp_project.company_id AS company_id,
            ccmapp_project.id AS project_id,
            count(ccmapp_alert.id) AS alert_count,
            count(ccmapp_alert.id) > 0 AS has_alert
        FROM ccmapp_project LEFT OUTER JOIN ccmapp_alert ON ccmapp_project.id = ccmapp_alert.project_id
        WHERE (ccmapp_alert.create_time IS NULL OR TIMESTAMPDIFF(DAY, ccmapp_alert.create_time, NOW()) <= %s)
        GROUP BY ccmapp_project.id
        ;
            ''' % (days)
    report_map = {}
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
        report_map['normal_project_count'] = good_project_counter
        report_map['alert_project_count'] = bad_project_counter
    for alert in [SampleAlert, VideoAlert, TemperatureAlert, HumidityAlert]:
        key = alert.__name__.replace('Alert', '').lower() + '_alert_count'
        report_map[key] = get_concrete_alert_count(company_id, alert._meta.db_table, days)

    return [report_map]


def get_project_filter_sql(company_id, project_id):
    sql = '1=1'
    if project_id is not None:
        sql = 'ccmapp_project.id = %s' % project_id
    elif company_id is not None:
        sql = 'ccmapp_project.company_id = %s' % company_id
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
    temperature_alert_count_map = get_alert_count(project_filter_sql, days, 'ccmapp_temperaturealert')
    humidity_alert_count_map = get_alert_count(project_filter_sql, days, 'ccmapp_humidityalert')

    proj_ids = sample_alert_count_map.keys()
    proj_id_to_project = get_id_to_project(proj_ids)
    proj_id_to_company_name = get_project_id_to_company_name(proj_ids)
    proj_reports = []
    for proj_id in proj_ids:
        sample_alert_count = sample_alert_count_map[proj_id]
        video_alert_count = video_alert_count_map[proj_id]
        temperature_alert_count = temperature_alert_count_map[proj_id]
        humidity_alert_count = humidity_alert_count_map[proj_id]

        score = 100.0 - (sample_alert_count * 0.5 + video_alert_count * 2.0 + temperature_alert_count * 1.0 + humidity_alert_count * 1.0)
        proj_reports.append({
            'id': proj_id,
            'project_name': get_project_name(proj_id),
            'image_url': proj_id_to_project[proj_id].image_url,
            'company_name': proj_id_to_company_name[proj_id],
            'score': score,
            'sample_alert_count': sample_alert_count,
            'video_alert_count': video_alert_count,
            'temperature_alert_count': temperature_alert_count,
            'humidity_alert_count': humidity_alert_count
        })
    return sorted(proj_reports, key=lambda x: x['score'])


def get_id_to_project(proj_ids):
    projects = Project.objects.filter(pk__in=proj_ids)
    return dict([(proj.id,proj) for proj in projects])

def get_project_name(proj_id):
    proj = Project.objects.get(pk=proj_id)
    return proj.project_name

def get_project_id_to_company_name(proj_ids):
    sql = '''
    SELECT 
    ccmapp_project.id AS proj_id,
    ccmapp_buildingcompany.name AS company_name 
    from ccmapp_project LEFT JOIN ccmapp_buildingcompany 
    ON ccmapp_project.company_id  = ccmapp_buildingcompany.id 
    WHERE ccmapp_project.id in (%s);
    ''' % ','.join([str(id) for id in proj_ids])
    id_to_name  = {}
    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        for row in named_rows:
            id_to_name[row.proj_id] = row.company_name

    return id_to_name

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
        ccmapp_project.company_id AS company_id,
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
