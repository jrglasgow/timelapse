#!/usr/bin/env python

from capture_image import *
import gphoto2 as gp
import sys
import time
import Image, ImageStat, math

#MIN_INTER_SHOT_DELAY_SECONDS = timedelta(seconds=30)
MIN_BRIGHTNESS = 20000
MAX_BRIGHTNESS = 30000
target_dir = '/media/usb'
delay_seconds=10

CONFIGS = [
  ("1/1600", 2), #"1/3200", 200 iso
  ("1/1600", 2), #"1/2500", 200 iso
  ("1/1600", 2), #"1/2000", 200 iso
  ("1/2000", 2), #"1/1600", 200 iso
  ("1/1600", 2), #"1/1250", 200 iso
  ("1/1000", 2), # 1/1000", 200 iso
  ("1/800", 2), # 1/800", 200 iso
  ("1/800", 2), # 1/640", 200 iso
  ("1/500", 2), # 1/500", 200 iso
  ("1/500", 2), # 1/400", 200 iso
  ("1/320", 2), # 1/320", 200 iso
  ("1/250", 2), # 1/250", 200 iso
  ("1/200", 2), # 1/200", 200 iso
  ("1/160", 2), # 1/160", 200 iso
  ("1/160", 2), # 1/125", 200 iso
  ("1/100", 2), # 1/100", 200 iso
  ("1/80", 2), # 1/80", 200 iso
  ("1/60", 2), # 1/60", 200 iso
  ("1/50", 2), # 1/50", 200 iso
  ("1/40", 2), # 1/40", 200 iso
  ("1/30", 2), # 1/30", 200 iso
  ("1/20", 2), # 1/20", 200 iso
  ("1/15", 2), # 1/15", 200 iso
  ("1/13", 2), # 1/13", 200 iso
  ("1/10", 2), # 1/10", 200 iso
  ("1/6", 2), # 1/6", 200 iso
  ("1/5", 2), # 1/5", 200 iso
  ("1/4", 2), # 1/4", 200 iso
  ("0.3", 2), # 0.3", 200 iso
  ("0.3", 2), # 0.3", 200 iso
  (17, 2), # 0.8", 200 iso
  (16, 2), # 1", 200 iso
  (15, 2), # 1.3", 200 iso
  (14, 2), # 1.6", 200 iso
  (13, 2), # 2", 200 iso
  (12, 2), # 2.5", 200 iso
  (11, 2), # 3.2", 200 iso
  (10, 2), # 4", 200 iso
  (9, 2), # 5", 200 iso
  (8, 2), # 6", 200 iso
  (7, 2), # 8", 200 iso
  (6, 2), # 10", 200 iso
  (5, 2), # 13", 200 iso
  (4, 2), # 15", 200 iso
  (3, 2), # 20", 200 iso
  (2, 2), # 25", 200 iso
  (1, 2), # 30", 200 iso
  (1, 3), # 30", 400 iso
  (1, 4), # 30", 800 iso
  (1, 5), # 30", 1600 iso
]

def set_config(camera, context, config):
  pass


#
# get the brightness of an image
#
def get_brightness( im_file ):
  im = Image.open(im_file)
  stat = ImageStat.Stat(im)
  r,g,b = stat.mean
  return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

#
# get a preview image from the camera and check the brightness
#
def check_preview_image(camera, context):
  preview_file = '/tmp/preview.jpg'
  cam_file = gp.check_result(gp.gp_camera_capture_preview(camera, context))
  gp.check_result(gp.gp_file_save(cam_file, preview_file))
  brightness = get_brightness(preview_file)
  return brightness

if __name__=='__main__':

  context = gp.Context()
  camera = gp.Camera()
  camera.init(context)

  sequence = 1

  while 1:
    start_time = time.time()
    # get am image
    image_path = capture_image(camera, context, target_dir, sequence)
    print "Image %05d taken" % (sequence)

    # check to see if the camera settings need to be changed
    brightness = check_preview_image(camera, context)
    print "brightness: %s " % brightness


    # change the settings if necessary
    
    # see how long it has taken
    end_time = time.time()
    total_time = end_time - start_time

    # wait for next image
    wait_time = delay_seconds - total_time
    print "wait_time: %s seconds" % (wait_time)
    if (wait_time > 0):
      # there is some time left, so wait
      time.sleep(delay_seconds - total_time)

    # increment the counter
    sequence+=1
    pass
  pass
