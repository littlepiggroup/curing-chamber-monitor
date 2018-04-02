import datetime
import random
import sched
import threading
from threading import current_thread

import requests
import json
import logging

import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class RecordScheduler(object):
    def __init__(self):
        pass

    def start_job(self):
        pass


class VideoSchedulerThread(threading.Thread):
    def run(self):
        start_scheduler()


def routine_task(my_sched):
    print current_thread().name
    print 'Do something'
    collect()
    print 'Done'
    a = time.time() + 20
    my_sched.enterabs(a, 1, routine_task, (my_sched,))


def start_scheduler():
    print current_thread().name
    s = sched.scheduler(time.time, time.sleep)
    next_time = time.time() + 5
    s.enterabs(next_time, 1, routine_task, (s,))
    s.run()


def get_tomorrow_point():
    tomorrow_day = datetime.date.today() + datetime.timedelta(days=1)
    candidates = [7, 8, 9]
    point_idx = random.randrange(0, len(candidates))
    point = candidates[point_idx]
    point_time = datetime.datetime.fromordinal(tomorrow_day.toordinal()) + datetime.timedelta(hours=point)
    return time.mktime(point_time.timetuple()) + point_time.microsecond / 1E6


class EzvizClient(object):
    def __init__(self, access_token, ezviz_url="https://open.ys7.com"):
        self.ezviz_url = ezviz_url
        self.access_token = access_token

    def get_rtmp_adr_smooth(self, device_serial_number):
        url = "%s%s" % (self.ezviz_url, '/api/lapp/live/address/get')
        logger.info("Send request to %s" % url)
        # accessToken=at.1mizlvc9c533bg3rblm1vd9c32819jpw-8kxg6vg1ii-08xyaou-zjsy00jpp&source=762881292%3A1

        channel = 1
        form_params = {'accessToken': self.access_token,
                       'source': '%s:%s' % (device_serial_number, channel)}
        resp = requests.post(url, data=form_params)
        parsed_body = json.loads(resp.text)
        code = parsed_body['code']
        logger.info("Response code: %s" % code)
        logger.info("Got response: %s" % resp.text)
        target_data_item = None
        for data_item in parsed_body['data']:
            device_no = data_item['deviceSerial']
            channel_no = data_item['channelNo']
            if device_no == device_serial_number and channel_no == channel:
                logger.info("Found correct target device and channel: %s,%s" % (device_no, channel_no))
                target_data_item = data_item
                break
        return target_data_item['rtmp']


class VideoCollector(object):
    def __init__(self, camera):
        self.camera = camera

    def capture_video(self):
        # ffmpeg -t 30 -i rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a -acodec copy -vcodec copy abc.mp4
        pass


def add_video_object(camera, save_path, url_path):
    from ccm.ccmapp.models import Video
    video = Video(camera=camera, save_abs_path=save_path, url_path=url_path)
    video.save()


def collect():
    from ccm.ccmapp.models import Camera
    cameras = Camera.objects.all()
    for camera in cameras:
        rtmp_address = camera.rtmp_address
        import os
        dir_path = os.getcwd() + '/ccm/ccmapp/static'
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        dir_path = dir_path + '/videos'
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        save_name = '%s-%s-%s.mp4' % (camera.project.id, camera.device_serial_number, int(time.time()))
        save_path = dir_path + "/" + save_name
        save_to_mp4(rtmp_address, save_path)
        url_path = 'static/videos/'+save_name
        add_video_object(camera, save_path, url_path)


def save_to_mp4(rtmp_address, save_path):
    from subprocess import call
    # rtmp_address = 'rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a'
    # save_path = '/home/jichao/somewhere/curing-chamber-monitor/temp/xxxx.mp4'
    duration = 5 # seconds
    cmds = ['ffmpeg', '-t', str(duration), '-i', rtmp_address, '-acodec', 'copy', '-vcodec', 'copy', save_path]
    print ' '.join(cmds)
    rc = call(cmds)
    if rc != 0:
        print 'CMD failed!'


def ezviz():
    client = EzvizClient('at.1mizlvc9c533bg3rblm1vd9c32819jpw-8kxg6vg1ii-08xyaou-zjsy00jpp')
    rtmp_address = client.get_rtmp_adr_smooth('762881292')
    print rtmp_address


if __name__ == '__main__':
    save_to_mp4()