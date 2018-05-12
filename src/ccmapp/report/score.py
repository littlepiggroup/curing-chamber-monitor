# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple

from django.db import connection

# Two dimensions: 1. global group/sub-company/project; 2. Current/LastDay/LastWeek/LastMonth
from ccmapp.models import BuildingCompany
import xlsxwriter
import sys

import logging

logger = logging.getLogger(__name__)


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


# def my_custom_sql():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM ccmapp_alert")
#         rows = cursor.fetchall()
#         cursor.execute("SELECT * FROM ccmapp_alert")
#         named_rows = namedtuplefetchall(cursor)
#
#         for row in rows:
#             print row
#         for row in named_rows:
#             print row


def monthly_report_bad_sample(report_duration_days):
    '''

    :return:
    '''
    sql = '''SELECT company_id, sample_name, count(id) as bad_sample_count 
            FROM ccmapp_samplealert
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
            if named_row.sample_name in all_column_names:
                target_row[all_column_names.index(named_row.sample_name)] = named_row.bad_sample_count
            else:
                logger.warn("Not include such sample: %s", named_row.sample_name)

    # Compute bad_sample_total
    for id, row in id_to_row.items():
        row[-1] = sum(row[1:len(row)-1])
    return (all_column_names, id_to_row)


def monthly_report_sample_alert(report_duration_days):
    SCORE_POLICY = 3 # TODO: change to 3 days.
    sql_deduction = '''
        SELECT 
            company_id, 
            count(id)*0.5 as deduction 
        FROM ccmapp_samplealert   
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
            target_row[1] = float(named_row.deduction)
            if len(target_row) != 2:
                raise Exception('In monthly_report_sample_alert, data width is not correct. Expect:%s, Actual: %s.' %
                                (2, len(target_row)))
    return (all_column_names, id_to_row)


def monthly_report_temperature_humidity(report_duration_days):

    temperatur_humidity_sql = '''
    SELECT 
        company_id, 
        count(id) as temperature_humidity_total, 
        count(id) as temperature_humidity_alert_deduction 
    FROM ccmapp_temphumdtyalert
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


def monthly_report_video(report_duration_days):

    video_alert_sql = '''
    SELECT 
        company_id, 
        count(id) as video_alert_total, 
        count(id)*2 as video_alert_deduction FROM ccmapp_videoalert
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
    return all_column_names, id_to_row

def gen_report_as_json(report_duration_days, orderby_score_asc=True):
    '''

    :return:  [{"company_id":"<id>", "company_name", "score"},...]
    '''
    all_companies = BuildingCompany.objects.all()
    all_company_id_name = dict([(comp.id,comp.name) for comp in all_companies])
    all_company_name_id = dict([(comp.name,comp.id) for comp in all_companies])
    ret_data = []
    detail_rows = join_report(all_company_id_name,report_duration_days, orderby_score_asc)
    for row in detail_rows:
        json_company_report = {
            'company_id': all_company_name_id[row[0]],
            'company_name': row[0],
            'unqualified_sample_count': row[-7],
            'temperature_humidity_alert_count': row[-5],
            'video_alert_count': row[-3],
            'score': row[-1]
        }
        ret_data.append(json_company_report)
    return ret_data


def join_report(all_company_id_name, report_duration_days, orderby_score_asc=True):
    sample_report = monthly_report_bad_sample(report_duration_days)
    sample_alert_report = monthly_report_sample_alert(report_duration_days)
    temperature_humidity_report = monthly_report_temperature_humidity(report_duration_days)
    video_report = monthly_report_video(report_duration_days)
    headers = ['工程公司'] + sample_report[0][1:] + sample_alert_report[0][1:] \
              + temperature_humidity_report[0][1:] + video_report[0][1:] + ['总得分']
    # print len(headers)
    # for index, w in enumerate(headers):
    #     print "%s: %s" % (index, w)
    # print '\n-----------------------------------------------------------------'
    rows = []
    for company_id in all_company_id_name.keys():
        new_row = [all_company_id_name[company_id]]
        report_list = [sample_report, sample_alert_report, temperature_humidity_report, video_report]
        for report in report_list:
            new_row += report[1][company_id][1:]

        total_score_temp = 100 - new_row[-1] - new_row[-3] - new_row[-5]
        total_score = 0.0
        if total_score_temp > 0:
            total_score = total_score_temp
        new_row.append(total_score)
        rows.append(new_row)

    return sorted(rows, key=lambda x : x[-1], reverse=not orderby_score_asc)


#
# reload(sys)
# sys.setdefaultencoding('utf8')

def gen_excel_report(gen_path, data):
    # create worksheet
    workbook = xlsxwriter.Workbook(gen_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:P', 12)

    # set format
    title_format = workbook.add_format()
    title_format.set_align('center')
    title_format.set_bold()
    title_format.set_font_size(18)

    title1_format = workbook.add_format()
    title1_format.set_border(1)
    title1_format.set_left(2)
    title1_format.set_top(2)
    title1_format.set_align('center')
    title1_format.set_align('vcenter')
    title1_format.set_text_wrap()
    title1_format.set_bold()

    title2_format = workbook.add_format()
    title2_format.set_border(1)
    title2_format.set_top(2)
    title2_format.set_align('center')
    title2_format.set_align('vcenter')
    title2_format.set_text_wrap()
    title2_format.set_bold()

    title3_format = workbook.add_format()
    title3_format.set_border(1)
    title3_format.set_right(2)
    title3_format.set_top(2)
    title3_format.set_align('center')
    title3_format.set_align('vcenter')
    title3_format.set_text_wrap()
    title3_format.set_bold()

    title4_format = workbook.add_format()
    title4_format.set_align('center')
    title4_format.set_bold()
    title4_format.set_border(1)

    # first cell format
    first_cell_format = workbook.add_format()
    first_cell_format.set_align('center')
    first_cell_format.set_bottom(1)
    first_cell_format.set_left(2)

    first2_cell_format = workbook.add_format()
    first2_cell_format.set_align('center')
    first2_cell_format.set_left(2)
    first2_cell_format.set_bottom(2)

    # last cell format
    last_cell_format = workbook.add_format()
    last_cell_format.set_align('center')
    last_cell_format.set_bottom(1)
    last_cell_format.set_right(2)

    last2_cell_format = workbook.add_format()
    last2_cell_format.set_align('center')
    last2_cell_format.set_bottom(2)
    last2_cell_format.set_right(2)

    # middle cell format
    mid_cell_format = workbook.add_format()
    mid_cell_format.set_align('center')
    mid_cell_format.set_border(1)

    mid2_cell_format = workbook.add_format()
    mid2_cell_format.set_align('center')
    mid2_cell_format.set_border(1)
    mid2_cell_format.set_bottom(2)

    # header
    worksheet.merge_range('A1:N1', '试验管理月报表', title_format)
    worksheet.merge_range('A2:A3', '工程公司', title1_format)
    worksheet.merge_range('B2:G2', '送检不合格数', title2_format)

    worksheet.write('B3', '混凝土试件', title4_format)
    worksheet.write('C3', '砂浆', title4_format)
    worksheet.write('D3', '钢筋', title4_format)
    worksheet.write('E3', '水泥', title4_format)
    worksheet.write('F3', '砖', title4_format)
    worksheet.write('G3', '水泥土', title4_format)

    worksheet.merge_range('H2:H3', '不合格数总计', title2_format)
    worksheet.merge_range('I2:I3', '试验不合格报警处理', title2_format)
    worksheet.merge_range('J2:K3', '养护室温湿度报警\n（次数）', title2_format)
    worksheet.merge_range('L2:M3', '养护室现场监控报警\n（次数）', title2_format)
    worksheet.merge_range('N2:N3', '总得分', title3_format)

    for i in range(len(data)):
        for j in range(len(data[i])):
            if j == 0:
                if i == len(data) - 1:
                    worksheet.write(i + 3, j, data[i][j], first2_cell_format)
                else:
                    worksheet.write(i + 3, j, data[i][j], first_cell_format)
            elif j == len(data[i]) - 1:
                if i == len(data) - 1:
                    worksheet.write(i + 3, j, data[i][j], last2_cell_format)
                else:
                    worksheet.write(i + 3, j, data[i][j], last_cell_format)
            else:
                if i == len(data) - 1:
                    worksheet.write(i + 3, j, data[i][j], mid2_cell_format)
                else:
                    worksheet.write(i + 3, j, data[i][j], mid_cell_format)

    workbook.close()


def gen_final_report(file_path):
    all_company_id_name = dict([(comp.id,comp.name) for comp in BuildingCompany.objects.all()])
    rows = join_report(all_company_id_name, 30)
    gen_excel_report(file_path, rows)

# data = [["EMC",2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],["DELL",1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
#
# gen_excel_report("teset.xlsx",data)


