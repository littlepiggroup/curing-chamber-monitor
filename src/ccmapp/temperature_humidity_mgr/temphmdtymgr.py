# -*- coding: utf-8 -*-
import threading
import time

from ccmapp.collect_subscribe.collect_subscribe import save_alert_notification
from ccmapp.models import Project, Sensor, TemperatureHumidityData, TemperatureAlert, HumidityAlert
import random
import logging

logger = logging.getLogger(__name__)



def collect_save_temperature_humidity_data():
    pass
    # Scan all registered projects' senors and collect data
    # And save data to TemperatureHumidityData
    projects = Project.objects.all()
    for project in projects:
        # logger.info("Try to collect sensor data for project: %s", project.project_name)
        company = project.company
        sensors = project.sensors.all()

        for sensor in sensors:
            logger.info("Collect data from sensor: %s", sensor.device_number)
            data = collect_sensor_data(sensor)
            temphmdty = TemperatureHumidityData(company=company, sensor=sensor, project=project,
                                                temperature=data['temperature'], humidity=data['humidity'])
            temphmdty.save()
            alert_check(project, sensor, temphmdty)
        else:
            pass
            # logger.warn("There is no sensors for project: %s", project.project_name)


def collect_sensor_data(sensor):
    '''
    :param sensor:
    :return: {'temperature': 10.0, 'humidity':10}
    '''
    temperature = random.randrange(-30, 100)
    humidity = random.randrange(0, 100)
    data = {'temperature': temperature, 'humidity': humidity}
    return data


def get_sensor(param):
    pass


def save_sensor_data(data_map):
    project = Project.objects.get(id=data_map['project'])
    sensor = Sensor.objects.get(project=project, device_number=data_map['device_number'])
    temp_float = data_map['temperature']
    humidity_int = data_map['humidity']
    company = project.company
    temp_humidity_data = TemperatureHumidityData(
        company=company,
        project=project,
        sensor=sensor,
        temperature=temp_float,
        humidity=humidity_int
    )
    temp_humidity_data.save()
    alert_check(project, sensor, temp_humidity_data)


def test_save_sensor_data():
    data_map = {'temperature':25.0,
                'humidity': 70, 'device_number': '1', 'project': 1}
    save_sensor_data(data_map)


def mock_senor_data_generator():

    class DataCollectorThread(threading.Thread):

        def run(self):
            while True:
                gen_mock_data()

    DataCollectorThread().start()


def gen_mock_data():
    logger.debug('Sleep 5 seconds...')
    time.sleep(5)
    data_map = {'device_number': '1', 'project': 1}
    temperature = random.randint(10, 40) * 1.0
    humidity = random.randint(40, 100)
    data_map['temperature'] = temperature
    data_map['humidity'] = humidity
    logger.debug('Mock data:%s', data_map)
    save_sensor_data(data_map)
    logger.debug('Data saved')


def is_temperature_alert(sensor_data, sensor):
    '''

    :param sensor_data:
    :param sensor:
    :return: (True, 'Alert Description') or (False, None)
    '''
    temp = sensor_data.temperature
    if temp > sensor.temperature_high:
        logger.debug('Temperature is too high!')
        return True, u'温度为%s,大于上限温度%s' % (temp, sensor.temperature_high)
    if temp < sensor.temperature_low:
        logger.debug('Temperature is too low!')
        return True, u'温度为%s,小于下限温度%s' % (temp, sensor.temperature_low)
    return False, None

def is_humidity_alert(sensor_data, sensor):
    temp = sensor_data.humidity
    if temp > sensor.humidity_high:
        logger.debug('humidity is too high!')
        return True, u'湿度为%s,大于上限湿度%s' % (temp, sensor.humidity_high)
    if temp < sensor.humidity_low:
        logger.debug('humidity is too low!')
        return True, u'湿度为%s,小于下限湿度%s' % (temp, sensor.humidity_low)
    return False, None


def alert_check(project, sensor, sensor_data):
    temp_alert = is_temperature_alert(sensor_data, sensor)
    if temp_alert[0]:
        logger.info('Find temperature alert for sensor: %d. Temperature is %f', sensor.id, sensor_data.temperature)
        # description = '项目%s中，发现了温度报警, 设备号:%s, 温度值：%s, 温度数据收集时间:%s。请注意处理!' % (
        #     project.project_name,
        #     sensor.device_number,
        #     sensor_data.temperature,
        #     str(sensor_data.create_time)
        # )
        description = temp_alert[1]
        alert = TemperatureAlert(
            sensor=sensor,
            project=project,
            company=project.company,
            description=description,
            comment='Empty comment',
            status=TemperatureAlert.CREATED
        )
        alert.save()
        save_alert_notification(alert)

    humidity_alert = is_humidity_alert(sensor_data, sensor)
    if humidity_alert[0]:
        logger.info('Find humidity alert for sensor: %d. Humidity is %s', sensor.id, sensor_data.humidity)
        description = humidity_alert[1]
        alert = HumidityAlert(
            sensor=sensor,
            project=project,
            company=project.company,
            description=description,
            comment='Empty comment',
            status=TemperatureAlert.CREATED
        )
        alert.save()
        save_alert_notification(alert)
