import logging
import os
import time
import telepot
import config
from gpiozero import MotionSensor
from logging.config import fileConfig
from picamera2 import Picamera2


def create_camera():
    cam = Picamera2()
    cam.start()
    time.sleep(2)
    capture_config = cam.create_still_configuration()
    cam.switch_mode(capture_config)
    return cam


def create_folder_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def send_picture(file):
    try:
        log.debug("Sending picture")
        bot.sendPhoto(config.telepot_chat_id, open(file, 'rb'))
    except Exception as e:
        log.error("Error sending picture: {}".format(e))


def send_message(message):
    try:
        log.debug("Sending message: {}".format(message))
        bot.sendMessage(config.telepot_chat_id, message)
    except Exception as e:
        log.error("Error sending message: {}".format(e))


def generate_date_time_filename(prefix):
    return '{}_{}_{}_{}_{}.jpg'.format(prefix, time.strftime('%Y'), time.strftime('%m'), time.strftime('%d'),
                                       time.strftime('%H'))


def take_picture():
    try:
        log.info("Taking picture")
        file = generate_date_time_filename("./{}/motion".format(config.data_folder))
        camera.capture_file(file)
        return file
    except Exception as e:
        log.error("Error taking picture: {}".format(e))
        return None


def delete_files_older_than(seconds, directory):
    try:
        for file in os.listdir(directory):
            if os.stat(os.path.join(directory, file)).st_mtime < time.time() - seconds:
                os.remove(os.path.join(directory, file))
    except Exception as e:
        log.error("Error deleting files: {}".format(e))


def get_file_size_in_kb(file):
    return os.path.getsize(file) / 1024


fileConfig('logging.ini')
log = logging.getLogger('Main')

camera = create_camera()
pir = MotionSensor(config.motion_sensor_pin)
bot = telepot.Bot(config.telepot_token)
log.info("Motion sensor started")
send_message("Motion sensor started")

create_folder_if_not_exists(config.data_folder)
no_motion_file_size = 0
while True:
    pir.wait_for_motion()
    log.info("Motion detected")
    send_message("Motion detected")
    while pir.motion_detected:
        filename = take_picture()
        if filename and abs(get_file_size_in_kb(filename) - no_motion_file_size) > config.image_size_diff_threshold_kb:
            send_picture(filename)
        if config.take_picture_delay_seconds > 0:
            time.sleep(config.take_picture_delay_seconds)
    log.info("No motion")
    filename = take_picture()
    if filename:
        no_motion_file_size = get_file_size_in_kb(filename)
    send_message("No motion")
    delete_files_older_than(config.delete_pictures_older_than_seconds, config.data_folder)
