from ccm.ccmapp.models import *
import datetime as DT

def populate():
    # clear
    BuildingCompany.objects.all().delete()
    building_company = BuildingCompany(name="test_company")
    building_company.save()

    Project.objects.all().delete()
    new_project = Project(building_company=building_company)
    new_project.save()


    contract = Contract(project=new_project, sign_number='sign_1', checked_date_time=DT.datetime.now(), checked=True)
    contract.save()

    sample1 = Sample(project=new_project, instance_id='1', contract=contract, name="Sample1", regular=True, num='10')
    sample1.save()
    sample2 = Sample(project=new_project, instance_id='2', contract=contract, name="Sample2", regular=True, num='11')
    sample2.save()

    sample_alert_1 = SampleAlert(company=building_company, project = new_project,
                                 sample=sample1, create_time = DT.datetime.now(), update_time = DT.datetime.now(),
                                 status = SampleAlert.CREATED
                                 )
    sample_alert_1.save()
    sample_alert_2 = SampleAlert(company=building_company, project=new_project,
                                 sample=sample2, create_time=DT.datetime.now(), update_time=DT.datetime.now(),
                                 status = SampleAlert.CREATED
                                 )
    sample_alert_2.save()
    alerts = Alert.objects.all()
    for a in alerts:
        print vars(a)
    old_time = DT.datetime.now() - DT.timedelta(days=7)
    alerts = Alert.objects.filter(create_time__lt=DT.datetime.now(), create_time__gt=old_time)
    for a in alerts:
        print vars(a)


if __name__ == '__main__':
    pass
