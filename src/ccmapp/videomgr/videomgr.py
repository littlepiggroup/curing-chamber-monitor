# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
import random
import sched
import threading
from threading import current_thread

import requests
import json
import logging

import time

from django.conf import settings

from ccmapp.mediamgr import mediamgr

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


# Video transfomer
def transfer_video_to_mp4(origin_file_path, target_folder):
    # Get extention
    # Call ffmpeg
    # Go.
    pass

# ----------- Start: logic to save video -----------

def prepare_video_store_info(project_id):
    target_relative_path = 'projects/' + str(project_id) + '/videos'
    datetime_now = datetime.now()
    date_str = str(datetime_now.date())
    epoch_secs = int((datetime_now - datetime(1970, 1, 1)).total_seconds())
    file_name = 'video_' + date_str + "_" + str(epoch_secs) + '.mp4'
    mediamgr.create_sub_dirs(settings.MEDIA_ROOT, target_relative_path)
    target_file_path = re.sub(r'\$', '', settings.MEDIA_ROOT) + '/' + target_relative_path + '/' + file_name
    data_map = {
        'abs_file_path': target_file_path,
        'url_path': 'media/'+target_relative_path + '/' + file_name
    }
    return data_map

def save_to_mp4(rtmp_address, save_path):
    from subprocess import call
    # rtmp_address = 'rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a'
    # save_path = '/home/jichao/somewhere/curing-chamber-monitor/temp/xxxx.mp4'
    duration_seconds = 10
    #cmds = ['ffmpeg', '-t', str(duration_seconds), '-i', rtmp_address, '-acodec', 'copy', '-vcodec', 'copy', save_path]
    cmds= ['touch', save_path]
    cmd_str = ' '.join(cmds)
    logger.info('Command to save mp4: %s', cmd_str)
    rc = call(cmds)
    if rc != 0:
        # TODO Log detailed error
        logger.error('Saving video failed.')
    else:
        logger.info('Save video successfully.')


def add_video_object(camera, save_path, url_path):
    from ccmapp.models import Video
    project = camera.project
    video = Video(camera=camera, project=project, save_abs_path=save_path, url_path=url_path, video_type=Video.AUTO)
    video.save()


def collect():
    from ccmapp.models import Camera
    cameras = Camera.objects.all()
    cameras_amount = len(cameras)
    if cameras_amount > 0:
        print 'Found %s cameras. Start to save live streams' % len(cameras)
    else:
        print "Didn't find any camera. Have nothing to do."

    for camera in cameras:
        rtmp_address = camera.rtmp_address
        path_info = prepare_video_store_info(camera.project_id)
        save_path = path_info['abs_file_path']
        save_to_mp4(rtmp_address, save_path)
        add_video_object(camera, save_path, path_info['url_path'])

# ----------- End: logic to save video -----------


# ---------- Start: Ezviz interact code ----------


class EzvizClient(object):
    def __init__(self, ezviz_account_model):
        self.ezviz_url = "https://open.ys7.com"
        # https://open.ys7.com/doc/zh/book/index/user.html
        # 获取到的accessToken有效期是7天

        current_time = (datetime.now() - datetime.utcfromtimestamp(0)).total_seconds()*1000
        if ezviz_account_model.access_token is None or current_time > ezviz_account_model.access_token_expire_time:
            # Update access token
            access_token_and_expire_time = self.fetch_access_token(ezviz_account_model.app_key,
                                                                   ezviz_account_model.secret)
            ezviz_account_model.access_token = access_token_and_expire_time[0]
            ezviz_account_model.access_token_expire_time = long(access_token_and_expire_time[1])
            ezviz_account_model.save()
        self.access_token = ezviz_account_model.access_token

    def fetch_access_token(self, app_key, secret):

        form_params = {'appKey': app_key,
                   'appSecret': secret}
        url = "%s%s" % (self.ezviz_url, '/api/lapp/token/get')
        resp = requests.post(url, data=form_params)
        parsed_body = json.loads(resp.text)
        rc = parsed_body['code']
        msg = parsed_body['msg']
        expire_time = parsed_body['data']['expireTime']
        access_token = parsed_body['data']['accessToken']
        if rc != '200':
            err_msg = "Error when fetch access key. code: %s, message: %s " % (rc,msg)
            logger.error(err_msg)
            raise Exception(err_msg)
        return (access_token, expire_time)

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


def ezviz_get_rtmp_address():
    client = EzvizClient('at.1mizlvc9c533bg3rblm1vd9c32819jpw-8kxg6vg1ii-08xyaou-zjsy00jpp')
    rtmp_address = client.get_rtmp_adr_smooth('762881292')
    print rtmp_address

# ---------- End: Ezviz interact code ----------


# TODO: ----------- Start: Scheduler related code-----------


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
    tomorrow_day = datetime.today() + timedelta(days=1)
    candidates = [7, 8, 9]
    point_idx = random.randrange(0, len(candidates))
    point = candidates[point_idx]
    point_time = datetime.fromordinal(tomorrow_day.toordinal()) + datetime.timedelta(hours=point)
    return time.mktime(point_time.timetuple()) + point_time.microsecond / 1E6

# ----------- End: Scheduler related codee-----------


if __name__ == '__main__':
    app_key = 'f0278514f31b41dab85b96a7f2510fcf'
    app_secret = 'ff7f1cfe82b907c24a06dca343eb04ed'
    client = EzvizClient(None)
    client.fetch_access_token(app_key, app_secret)

