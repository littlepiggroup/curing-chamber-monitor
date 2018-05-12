# -*- coding: utf-8 -*-
import logging
import socket , sys, time, binascii,struct

import socket
print socket.getdefaulttimeout()
socket.setdefaulttimeout(3600)

reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger(__name__)


def parse_raw_data_to_record(raw_data):
    '''

    :param raw_data:
    :return:  {'temperature':'xx', 'humidity':'xx', 'device_number':'xxxx'}
    '''
    logger.info("Try to parse %s", raw_data)
    project_hex = raw_data[0:2]
    device_hex = raw_data[2:4]
    humidity_hex = raw_data[6:10]
    temp_hex = raw_data[10:14]
    project_int = int(project_hex, 16)
    sensor_str = str(int(device_hex, 16))
    temp_float = int(temp_hex, 16)/10.0
    humidity_int = int(humidity_hex, 16)/10
    data_map = {'project': project_int, 'device_number': sensor_str,
                'temperature': temp_float, 'humidity': humidity_int}
    return data_map


def save_collected_data(raw_data):
    from ccmapp.temperature_humidity_mgr.temphmdtymgr import save_sensor_data
    if raw_data is None or len(raw_data) < 14:
        logger.warn("Raw data is not valid. Ignore it: %s", raw_data)
        return
    data_map = parse_raw_data_to_record(raw_data)
    logger.debug("Data parsed map: %s", data_map)
    save_sensor_data(data_map)


def test_parse_raw_data_to_record():
    hex_a = '01010C0106016D'
    r = parse_raw_data_to_record(hex_a)
    print r


def start_server():
    socket.setdefaulttimeout(None)
    logger.info('Socket accept timeout None')
    web = None
    try:
        command = '\x01\x03\x00\x00\x00\x06\xC5\xC8'
        # ip = socket.gethostbyname(socket.gethostname() )
        ip = '0.0.0.0'
        #开启ip和端口
        ip_port = (ip,8899)
        #生成句柄
        web = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #绑定端口
        web.bind(ip_port)
        #最多连接数
        web.listen(5)
        #等待信息
        print type(command)
        print command.encode('hex')

        # Test method: echo -ne '\x01\x01\x0C\x01\x06\x01\x6D\x36\x37\x38\x00'|nc 127.0.0.1 8899

        #开启死循环
        while True:
            logger.info('Wait for new client connecting')
            conn, addr = web.accept()
            logger.info('Got new connection %s.', addr)
            size = 1024
            try:
                while True:
                    logger.info('Send command.')
                    conn.send(command)
                    time.sleep(1)
                    logger.debug('Try to receive data.')
                    data = conn.recv(size)
                    if data:
                        # Set the response to echo back the recieved data
                        logger.debug('Got data. Size: %d', len(data))
                        data_hex = data.encode('hex')
                        logger.debug("Data hex format: %s", data_hex)
                        parsed_map = None
                        try:
                            save_collected_data(data_hex)
                        except Exception, parse_e:
                            logger.warn('Got parse error. Ignore it')
                            logger.exception(parse_e)
                        except:
                            logger.error('Unknown error')
                    else:
                        sleep_duration = 2
                        logger.debug('Got nothing. Sleep %d second', sleep_duration)
                        time.sleep(sleep_duration)
                        # raise Exception('Client disconnected')
            except Exception, e:
                logger.error('Error and close connection')
                logger.exception(e)
                conn.close()
    except Exception, e:
        logger.error('Error and close socket.')
        logger.exception(e)
        if web is not None:
            web.close()

# Twisted
from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone


class SensorDataHandler(protocol.Protocol):
    def __init__(self):
        logger.debug('Init one SensorDataHandler.')
        self.cur_peer = None

    def connectionMade(self):
        self.cur_peer = self.transport.getPeer()
        logger.info('Got client: %s' % self.cur_peer)

    def dataReceived(self, data):
        logger.info('Current client: %s' % self.cur_peer)

        logger.debug('Got data. Size: %d', len(data))
        data_hex = data.encode('hex')
        logger.debug("Data hex format: %s", data_hex)
        save_collected_data(data_hex)

    def connectionLost(self, reason=connectionDone):
        logger.info('Close connection with client: %s' % self.cur_peer)
        logger.warn('Connection close reason: %s' % reason)


class SensorDataHandlerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SensorDataHandler()


def start_twisted_server():
    reactor.listenTCP(8899, SensorDataHandlerFactory())
    reactor.run(installSignalHandlers=0)

if __name__ == '__main__':
    start_server()
