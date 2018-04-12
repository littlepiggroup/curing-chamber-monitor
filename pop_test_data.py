from django.db.models import Count

from ccm.ccmapp.models import *
import datetime as DT


def populate():
    # clear
    BuildingCompany.objects.all().delete()
    building_company = BuildingCompany(name="test_company")
    building_company.save()

    Project.objects.all().delete()
    project1 = Project(building_company=building_company, instance_id='proj_1')
    project1.save()
    project_1_name_1 = ProjectName(project=project1, name="Project_1_Name_1")
    project_1_name_1.save()
    project_1_name_2 = ProjectName(project=project1, name="Project_1_Name_2")
    project_1_name_2.save()
    project2 = Project(building_company=building_company, instance_id='proj_2')
    project2.save()
    project_2_name_1 = ProjectName(project=project2, name="Project_2_Name_1")
    project_2_name_1.save()

    contract = Contract(project=project1, sign_number='sign_1', checked_date_time=DT.datetime.now(), checked=True)
    contract.save()

    Sample.objects.all().delete()
    SampleAlert.objects.all().delete()
    sample1 = Sample(project=project1, instance_id='1', contract=contract, name="Sample1", regular=True, num='10')
    sample1.save()
    sample2 = Sample(project=project1, instance_id='2', contract=contract, name="Sample2", regular=True, num='11')
    sample2.save()

    sample_alert_1 = SampleAlert(company=building_company, project=project1,
                                 sample=sample1, create_time=DT.datetime.now(), update_time=DT.datetime.now(),
                                 status=SampleAlert.CREATED
                                 )
    sample_alert_1.save()
    sample_alert_2 = SampleAlert(company=building_company, project=project1,
                                 sample=sample2, create_time=DT.datetime.now(), update_time=DT.datetime.now(),
                                 status=SampleAlert.CREATED
                                 )
    sample_alert_2.save()

    sample1 = Sample(project=project2, instance_id='3', contract=contract, name="Sample1", regular=True, num='10')
    sample1.save()
    sample2 = Sample(project=project2, instance_id='4', contract=contract, name="Sample2", regular=True, num='11')
    sample2.save()

    sample_alert_1 = SampleAlert(company=building_company, project=project2,
                                 sample=sample1, create_time=DT.datetime.now(), update_time=DT.datetime.now(),
                                 status=SampleAlert.CREATED
                                 )
    sample_alert_1.save()


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
