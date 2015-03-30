#! /usr/bin/env python

import gphoto2 as gp
import os
import time

def capture_image(camera, context, target_dir='/tmp', sequence=0):
  file_path = camera.capture(gp.GP_CAPTURE_IMAGE, context)
  extention = file_path.name.split('.')[-1]
  if (sequence != 0):
    file_name = 'image-%05d.%s' % (sequence, extention)
  else :
    file_name = 'image-%s.%s' % (time.strftime('%Y%m%d-%H%M%S'), extention)

  target = os.path.join(target_dir, file_name)

  camera_file = gp.check_result(camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, context))
  gp.check_result(gp.gp_file_save(camera_file, target))


if __name__=='__main__':
  context = gp.Context()
  camera = gp.Camera()
  camera.init(context)
  capture_image(camera, context, '/media/usb')
  #capture_image(camera, context)
  camera.exit(context)

