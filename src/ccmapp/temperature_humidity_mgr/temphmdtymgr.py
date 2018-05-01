from ccmapp.models import Project,BuildingCompany,TemperatureHumidityData


def collect_save_data():
    pass
    # Scan all registered projects' senors and collect data
    # And save data to TemperatureHumidityData
    projects = Project.objects.all()
    for project in projects:
        company = project.company
        sensors = project.sensors
        for sensor in sensors:
            data = collect_data(sensor)
            temphmdty = TemperatureHumidityData(company=company, sensor=sensor, project=project,
                                                temperature=data['temperature'], humidity=data['humidity'])
            temphmdty.save()


def collect_data(sensor):
    '''

    :param sensor:
    :return: {'temperature': 10.0, 'humidity':10}
    '''

    pass
    data = {}
    return data

def add_sensor():
    pass