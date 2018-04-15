# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple

from django.db import connection

# Two dimensions: 1. global group/sub-company/project; 2. Current/LastDay/LastWeek/LastMonth
from ccm.ccmapp.models import BuildingCompany


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ccmapp_alert")
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM ccmapp_alert")
        named_rows = namedtuplefetchall(cursor)

        for row in rows:
            print row
        for row in named_rows:
            print row


def monthly_report_bad_sample():
    '''

    :return:
    '''
    report_duration_days = 30

    sql = '''SELECT company_id, sample_name, count(id) as bad_sample_count FROM ccmapp_samplealert
WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s
GROUP BY company_id, sample_name;''' % (report_duration_days)
    all_column_names = ['company_id', '混凝土试件', '砂浆', '钢筋','水泥', '砖', '水泥土',
                        '试件报警总数']

    all_company_ids = [comp.id for comp in BuildingCompany.objects.all()]
    id_to_row = dict([(comp_id, [comp_id, 0, 0, 0, 0, 0, 0, 0]) for comp_id in all_company_ids])
    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            company_id = named_row.company_id
            target_row = id_to_row[company_id]
            target_row[all_column_names.index(named_row.sample_name)] = named_row.bad_sample_count
    # Compute bad_sample_total
    for id,row in id_to_row.items():
        row[-1] = sum(row[1:len(row)-1])
    return (all_column_names, id_to_row)

def monthly_report_sample_alert():
    SCORE_POLICY = 1 # TODO: change to 3 days.
    report_duration_days = 30
    sql_deduction = '''
        SELECT company_id, count(id)*0.5 as deduction FROM ccmapp_samplealert   
        WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) >= %s AND status = 'CREATED' AND TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s
        GROUP BY company_id;
            ''' % (SCORE_POLICY, report_duration_days)

    all_company_ids = [comp.id for comp in BuildingCompany.objects.all()]
    id_to_row = dict([(comp_id, [comp_id, 0.0]) for comp_id in all_company_ids])
    all_column_names = ['company_id', '试件不合格报警减分']

    with connection.cursor() as cursor:
        cursor.execute(sql_deduction)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            company_id = named_row.company_id
            target_row = id_to_row[company_id]
            target_row[2] = named_row.deduction
    return (all_column_names, id_to_row)

def monthly_report_temperature_humidity():
    report_duration_days = 30

    temperatur_humidity_sql = '''SELECT company_id, count(id) as temperature_humidity_total, count(id) as temperature_humidity_alert_deduction FROM ccmapp_temphumdtyalert
WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s
GROUP BY company_id;
    ''' % (report_duration_days)
    all_company_ids = [comp.id for comp in BuildingCompany.objects.all()]
    id_to_row = dict([(comp_id, [comp_id, 0, 0.0]) for comp_id in all_company_ids])
    all_column_names = ['company_id', '温湿度报警总数', '温湿度报警减分']

    with connection.cursor() as cursor:
        cursor.execute(temperatur_humidity_sql)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            company_id = named_row.company_id
            target_row = id_to_row[company_id]
            target_row[1] = named_row.temperature_humidity_total
            target_row[2] = named_row.temperature_humidity_alert_deduction
    return (all_column_names, id_to_row)


def monthly_report_video():
    report_duration_days = 30

    video_alert_sql = '''SELECT company_id, count(id) as video_alert_total, count(id)*2 as video_alert_deduction FROM ccmapp_videoalert
            WHERE TIMESTAMPDIFF(DAY, create_time, NOW()) <= %s
            GROUP BY company_id;
    ''' % (report_duration_days)
    all_company_ids = [comp.id for comp in BuildingCompany.objects.all()]
    id_to_row = dict([(comp_id, [comp_id, 0, 0.0]) for comp_id in all_company_ids])
    all_column_names = ['company_id', '监控报警总数', '监控报警减分']

    with connection.cursor() as cursor:
        cursor.execute(video_alert_sql)
        named_rows = namedtuplefetchall(cursor)
        for named_row in named_rows:
            company_id = named_row.company_id
            target_row = id_to_row[company_id]
            target_row[1] = named_row.video_alert_total
            target_row[2] = named_row.video_alert_deduction
    return (all_column_names, id_to_row)


def join_report():
    sample_report = monthly_report_bad_sample()
    sample_alert_report = monthly_report_sample_alert()
    temperature_humidity_report = monthly_report_temperature_humidity()
    video_report = monthly_report_video()
    all_company_id_name = dict([(comp.id,comp.name) for comp in BuildingCompany.objects.all()])
    headers = ['工程公司'] + sample_report[0][1:] + sample_alert_report[0][1:] \
              + temperature_humidity_report[0][1:] + video_report[0][1:] + ['总得分']
    print len(headers)
    for h in headers:
        print h,
    print '\n-----------------------------------------------------------------'
    rows = []
    for company_id in all_company_id_name.keys():
        new_row = [all_company_id_name[company_id]]
        report_list = [sample_report, sample_alert_report, temperature_humidity_report, video_report]
        for report in report_list:
            new_row += report[1][company_id][1:]
        # total_score
        total_score = 100 - new_row[-1] - new_row[-3] - new_row[-5]
        new_row.append(total_score)
        rows.append(new_row)
    for row in rows:
        print len(row)
        for cell in row:
            print cell,
        print '\n'