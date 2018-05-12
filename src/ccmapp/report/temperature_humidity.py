from django.db import connection

from ccmapp.report.utils import namedtuplefetchall


def project_sensor_data_series(project_id, sensor_id, days):
    '''
    :param project_id:
    :param days:
    :return: order by timestamp asc. [
                    {"temperature":25.3, "humidity":75.0, "timestamp":"?", "has_temperature":true, "has_humidity":true}
                    , ... ]
             "temperature":-100.0, "temperature": -100.0. Responds for no data.
    '''
    sql = ''
    if project_id is not None:
        sql = '''
        SELECT
            ccmapp_temperaturehumiditydata.temperature AS temperature,
            ccmapp_temperaturehumiditydata.humidity AS humidity,
            ccmapp_temperaturehumiditydata.temperature > -100.0 AS has_temperature,
            ccmapp_temperaturehumiditydata.humidity > -1 AS has_humidity,
            ccmapp_temperaturehumiditydata.collect_time AS collect_time
        FROM ccmapp_temperaturehumiditydata
        WHERE project_id = %s AND sensor_id = %s AND TIMESTAMPDIFF(DAY, ccmapp_temperaturehumiditydata.collect_time, NOW()) <= %s
        ORDER BY collect_time ASC;
        ''' % (project_id, sensor_id, days)
    else:
        sql = '''
        SELECT
            ccmapp_temperaturehumiditydata.temperature AS temperature,
            ccmapp_temperaturehumiditydata.humidity AS humidity,
            ccmapp_temperaturehumiditydata.temperature > -100.0 AS has_temperature,
            ccmapp_temperaturehumiditydata.humidity > -1 AS has_humidity,
            ccmapp_temperaturehumiditydata.collect_time AS collect_time
        FROM ccmapp_temperaturehumiditydata
        WHERE sensor_id = %s AND TIMESTAMPDIFF(DAY, ccmapp_temperaturehumiditydata.collect_time, NOW()) <= %s
        ORDER BY collect_time ASC;
        ''' % (sensor_id, days)

    project__sensor_temperature_humidity = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        named_rows = namedtuplefetchall(cursor)
        for row in named_rows:
            temperature_humidity_data = {}
            temperature_humidity_data['temperature'] = row.temperature
            temperature_humidity_data['humidity'] = row.humidity
            temperature_humidity_data['has_humidity'] = True if row.has_humidity == 1 else False
            temperature_humidity_data['has_temperature'] = True if row.has_temperature == 1 else False
            temperature_humidity_data['collect_time'] = row.collect_time
            project__sensor_temperature_humidity.append(temperature_humidity_data)
    return project__sensor_temperature_humidity
