# -*- coding: utf-8 -*-

from django.db.models import Count

from ccmapp.models import *
import datetime as DT


def populate():
    # clear
    BuildingCompany.objects.all().delete()
    building_company_1 = BuildingCompany(name="四建第一工程公司")
    building_company_1.save()
    building_company_2 = BuildingCompany(name="四建第二工程公司")
    building_company_2.save()

    Project.objects.all().delete()
    project1 = Project(building_company=building_company_1, instance_id='proj_1')
    project1.save()
    project_1_name_1 = ProjectName(project=project1, name="Project_1_Name_1")
    project_1_name_1.save()
    project_1_name_2 = ProjectName(project=project1, name="Project_1_Name_2")
    project_1_name_2.save()
    project2 = Project(building_company=building_company_2, instance_id='proj_2')
    project2.save()
    project_2_name_1 = ProjectName(project=project2, name="Project_2_Name_1")
    project_2_name_1.save()
    project3 = Project(building_company=building_company_2, instance_id='proj_3')
    project3.save()
    project_3_name_1 = ProjectName(project=project3, name="Project_3_Name_1")
    project_3_name_1.save()
    project4 = Project(building_company=building_company_2, instance_id='proj_4')
    project4.save()
    project_4_name_1 = ProjectName(project=project4, name="Project_4_Name_1")
    project_4_name_1.save()


    contract = Contract(project=project1, sign_number='sign_1', checked_date_time=DT.datetime.now(), checked=True)
    contract.save()

    Sample.objects.all().delete()
    SampleAlert.objects.all().delete()
    sample1 = Sample(project=project1, company=building_company_1, instance_id='1', contract=contract, name="混凝土试件", regular=False, num='10', hnt_yhtj='标准养护', exam_result=120)
    sample1.save()
    sample2 = Sample(project=project1, company=building_company_1, instance_id='2', contract=contract,
                     name="钢筋", regular=True, num='11',
                     hnt_yhtj='标准养护', exam_result=130
                     )
    sample2.save()



    sample_alert_1 = SampleAlert(company=building_company_1, project=project1, alert_type = AlertType.SAMPLE,
                                 sample=sample1, sample_name='混凝土试件', create_time=DT.datetime.now(),
                                 update_time=DT.datetime.now(),
                                 status=SampleAlert.CREATED
                                 )
    sample_alert_1.save()
    sample_alert_2 = SampleAlert(company=building_company_1, project=project1, alert_type = AlertType.SAMPLE,
                                 sample=sample2, sample_name='钢筋',
                                 create_time=DT.datetime.now(), update_time=DT.datetime.now(),
                                 status=SampleAlert.CREATED
                                 )
    print DT.datetime.now()
    sample_alert_2.save()

    sample1 = Sample(project=project2, company=building_company_2,  instance_id='3', contract=contract,
                     name="混凝土试件", regular=True, num='10',
                     hnt_yhtj='非标准养护', exam_result=120
                     )
    sample1.save()
    sample2 = Sample(project=project2, company=building_company_2, instance_id='4', contract=contract,
                     name="钢筋", regular=False, num='11',
                     hnt_yhtj='非标准养护', exam_result=10)
    sample2.save()
    sample3 = Sample(project=project2, company=building_company_2, instance_id='5', contract=contract,
                     name="混凝土试件", regular=True, num='10',
                     hnt_yhtj='非标准养护', exam_result=120
                     )
    sample3.save()

    sample4 = Sample(project=project3, company=building_company_2, instance_id='6', contract=contract,
                     name="钢筋", regular=False, num='11',
                     hnt_yhtj='标准养护', exam_result=130
                     )
    sample4.save()

    sample_alert_1 = SampleAlert(company=building_company_2, project=project2, alert_type = AlertType.SAMPLE,
                                 sample=sample1, sample_name='混凝土试件',
                                 create_time=DT.datetime.now(), update_time=DT.datetime.now(),
                                 status=SampleAlert.CREATED
                                 )
    sample_alert_1.save()

    sample_alert_4 = SampleAlert(company=building_company_2, project=project3, alert_type = AlertType.SAMPLE,
                                 sample=sample4, sample_name='混凝土试件',
                                 create_time=DT.datetime.now(), update_time=DT.datetime.now(),
                                 status=SampleAlert.CREATED
                                 )
    sample_alert_4.save()

    alerts = Alert.objects.all()
    # for a in alerts:
    #     print vars(a)
    old_time = DT.datetime.now() - DT.timedelta(days=7)
    alerts = Alert.objects.filter(create_time__lt=DT.datetime.now(), create_time__gt=old_time)
    # for a in alerts:
    #     print vars(a)
    groupby_project = Alert.objects.filter(create_time__lt=DT.datetime.now(), create_time__gt=old_time).values(
        'project_id').annotate(dcount=Count('id'))

    for g in groupby_project:
        print g
        proj = Project.objects.get(pk=g['project_id'])
        print proj.instance_id
        names = proj.names.all()
        for ent in names:
            print ent.name

    # groupby_company = Alert.objects.filter(create_time__lt=DT.datetime.now(), create_time__gt=old_time).values(
    #     'company_id').annotate(dcount=Count('id'))
    #
    # for g in groupby_company:
    #     print g
    #
    # total_open_alerts = Alert.objects.exclude(status=SampleAlert.CLOSED).count()
    # print total_open_alerts


if __name__ == '__main__':
    pass
