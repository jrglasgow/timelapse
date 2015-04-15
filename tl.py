#!/usr/bin/env python
from __future__ import print_function
from capture_image import *
import gphoto2 as gp
import sys
import time, logging
import Image, ImageStat, math

#MIN_INTER_SHOT_DELAY_SECONDS = timedelta(seconds=30)
MIN_BRIGHTNESS = 20000
MAX_BRIGHTNESS = 30000
target_dir = '/media/usb'
logfile = '/home/pi/bin/timelapse.log'
# delay between shots
delay_seconds = 10
# the number of images to average to determine if brightness nees to be adjusted
b_avg = 10
brightness = {}
# the brightness tolerance before it is adjusted
b_tolerence = 10


#
# log something to the file
#
def log(text):
  f = open(logfile, 'w+')
  print ("%s| %s" % (time.strftime('%Y-%m-%d--%H-%M-%S'), text), file=f)
  f.close()

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

def trace(frame, event, arg):
  log("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
  return trace

#
# adjust the brightness
#
def adjust_brightness(camera, context, sequence):
  brightness[sequence % b_avg] = check_preview_image(camera, context)
  #print "brightness: %s " % brightness
  avg = average_brightness()
  log ("avg = %s" % avg)

  if ((100 - avg) > b_tolerence):
    log("needs to be brighter")
    make_brighter(camera, context)
    pass
  elif ((avg - 100) > b_tolerence):
    log("needs to be darker")
    make_darker(camera, context)
    pass
  else:
    pass
  # get the current shutter speed

#
# change the shutterspeed to make the photos darker
#
def make_darker(camera, context):
  # get the current brightness
  config, speed = get_speed(camera, context)
  log("shutter speed: %s" % speed.get_value())
  setting_number = get_current_setting_number(speed)
  if (setting_number > 0 and setting_number < (speed.count_choices() - 1)):
    # the setting less than the maximum, so we can make it darker
    log("set the shutter speed: %s" % (speed.get_choice(setting_number + 1)))
    speed.set_value(speed.get_choice(setting_number + 1))
    camera.set_config(config, context)
    pass
  else:
    log("dark as can get, nothing to do")
    return

#
# change the shutterspeed to make the photos brighter
#
def make_brighter(camera, context):
  # get the current brightness
  #
  #config = camera.get_config(context)
  config, speed = get_speed(camera, context)
  log("shutter speed: %s" % speed.get_value())
  #config.get_child_by_name('main').get_child_by_name('capturesettings').get_child_by_name('shutterspeed')
  setting_number = get_current_setting_number(speed)
  if (setting_number > 1 and setting_number < (speed.count_choices() - 1)):
    # the setting greater than the minimum, so we can make it lighter
    log("set the shutter speed: %s" % (speed.get_choice(setting_number - 1)))
    speed.set_value(speed.get_choice(setting_number - 1))
    camera.set_config(config, context)
    pass
  else:
    log("bright as can get, nothing to do")
    return

def get_speed(camera, context):

  config, speed = get_config(['main','capturesettings', 'shutterspeed'], camera, context);
  #print "speed_config: %s" % speed_config
  #shutter_speed = speed_config.get_value()
  log("shutter speed: %s" % speed_config.get_value())
  #print "speed_config.count_choices(): %s" % speed_config.count_choices()
  #print "setting_number: %s" % setting_number
  return [config, speed]

#
# get a camera confgiuration
#
def get_config(path, camera, context):
  path.reverse()
  config = camera.get_config(context)
  setting = traverse_config(path, config)
  return [config, setting]

#
# get the setting number for the current choice
#
def get_current_setting_number(config):
  for i in range(0, config.count_choices() - 1):
    #print "%s : %s" % (i, config.get_choice(i))
    if (config.get_choice(i) == config.get_value()):
      return i
    pass
  pass

#
# recursively traverse the config to get the setting and change it
#
def traverse_config(path, config):
  this_config = config.get_child_by_name(path.pop())
  if (len(path)):
    return traverse_config(path, this_config)
  else:
    return this_config
  pass

#
# take the last b_avg brightness readings and calculate the average
#
def average_brightness():
  b = 0.0
  count = 0
  for i in brightness.values():
    b += i
    count += 1
    pass
  return b/count

#
# run the timelapse
#
def timeLapse():

  camera_initialized = False
  while (camera_initialized == False):
    try:
      context = gp.Context()
      camera = gp.Camera()
      camera.init(context)
      camera_initialized = True
    except gp.GPhoto2Error as e:
      #print('e: %s' % e)
      message = 'No Camera detected, is it asleep? Please wake it up or check batteries.'
      print(message);
      log(message)
      time.sleep(10)


  
  try:


    sequence = 1
    log("target_dir: %s" % target_dir)
    
    while 1:
      log('')
      log('')
      log('')
      log('')
      log('')
      start_time = time.time()
      #print "sequence: %05d" % sequence
      # get an image
      image_path = capture_image(camera, context, target_dir, sequence)
      log("Image %05d taken" % (sequence))

      # check to see if the camera settings need to be changed
      avg = adjust_brightness(camera, context, sequence)


      # change the settings if necessary

      # see how long it has taken
      end_time = time.time()
      total_time = end_time - start_time

      # wait for next image
      wait_time = delay_seconds - total_time
      log("wait_time: %s seconds" % (wait_time))
      if (wait_time > 0):
        # there is some time left, so wait
        time.sleep(delay_seconds - total_time)

      # increment the counter
      sequence += 1
      pass
    pass
  except KeyboardInterrupt:
    camera.exit(context)
    sys.exit()
  except (RuntimeError, TypeError, NameError):
    print('RuntimeError: %s' % RuntimeError)
    print('TypeError: %s' % TypeError)
    print('NameError: %s' % NameError)

#
# create a name for the new directory
#
def get_directory():
  count = 0
  while True:
    temp = '%s/%s--%05d' % (target_dir, time.strftime('%Y-%m-%d'), count)
    if os.path.exists(temp):
      count += 1
    else:
      log("Files will be saved in this directory: %s " % (temp))
      # make sure the directory is created
      os.makedirs(temp)

      return temp

if __name__=='__main__':
  logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)

  # create a new directory for this timelapse which is based on the current time
  target_dir = get_directory()
  
  #sys.settrace(trace)
  timeLapse()

