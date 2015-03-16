#! /usr/bin/env python

import gphoto2 as gp
context = gp.Context()
camera = gp.Camera()
camera.init(context)
text = camera.get_summary(context)
#print('Summary')
#print('=======')
#print(str(text))
#camera.exit(context)

config = camera.get_config(context)

def tl_gphoto2_type(this_type):

  if this_type == gp.GP_WIDGET_WINDOW:
    return "gp.GP_WIDGET_WINDOW %s" % this_type
  elif this_type == gp.GP_WIDGET_SECTION:
    return "gp.GP_WIDGET_SECTION %s" % this_type
  elif this_type == gp.GP_WIDGET_TEXT:
    return "gp.GP_WIDGET_TEXT %s" % this_type
  elif this_type == gp.GP_WIDGET_RANGE:
    return "gp.GP_WIDGET_RANGE %s" % this_type
  elif this_type == gp.GP_WIDGET_TOGGLE:
    return "gp.GP_WIDGET_TOGGLE %s" % this_type
  elif this_type == gp.GP_WIDGET_RADIO:
    return "gp.GP_WIDGET_RADIO %s" % this_type
  elif this_type == gp.GP_WIDGET_MENU:
    return "gp.GP_WIDGET_MENU %s" % this_type
  elif this_type == gp.GP_WIDGET_BUTTON:
    return "gp.GP_WIDGET_BUTTON %s" % this_type
  elif this_type == gp.GP_WIDGET_DATE:
    return "gp.GP_WIDGET_DATE %s" % this_type
  else:
    return "unknown %s" % (this_type)
  pass

def tl_show_config_options(config, spacing):
  this_type = config.get_type()
  if this_type == gp.GP_WIDGET_WINDOW:
    print "%sgp.GP_WIDGET_WINDOW %s" % (spacing, this_type)
  elif this_type == gp.GP_WIDGET_SECTION:
    print "%sgp.GP_WIDGET_SECTION %s" % (spacing, this_type)
  elif this_type == gp.GP_WIDGET_TEXT:
    #print "%sgp.GP_WIDGET_TEXT %s" % (spacing, this_type)
    pass
  elif this_type == gp.GP_WIDGET_RANGE:
    print "%sgp.GP_WIDGET_RANGE %s" % (spacing, this_type)
  elif this_type == gp.GP_WIDGET_TOGGLE:
    #print "%sgp.GP_WIDGET_TOGGLE %s" % (spacing, this_type)
    pass
  elif this_type == gp.GP_WIDGET_RADIO:
    #print "%sgp.GP_WIDGET_RADIO %s" % (spacing, this_type)
    for i in range(0, config.count_choices() - 1):
      print "%s%s: %s" % (spacing, i, config.get_choice(i))
      pass
  elif this_type == gp.GP_WIDGET_MENU:
    print "%sgp.GP_WIDGET_MENU %s" % (spacing, this_type)
  elif this_type == gp.GP_WIDGET_BUTTON:
    print "%sgp.GP_WIDGET_BUTTON %s" % (spacing, this_type)
  elif this_type == gp.GP_WIDGET_DATE:
    #print "%sgp.GP_WIDGET_DATE %s" % (spacing, this_type)
    pass
  else:
    print "unknown %s" % (this_type)
  pass


def tl_show_config(config, config_path='', spacing=''):
  config_path = "%s.%s" % (config_path, config.get_name())
  #print "%sLabel: %s (%s) Type: %s" % (spacing, str(config.get_label()), config_path, str(config.get_type()))

  #print "config.count_children(): %s" % config.count_children()
  new_spacing = "%s    " % (spacing)
  if config.count_children() > 0:
    print "%s%s" % (spacing, config.get_name())
    for i in range(0, config.count_children() - 1):
      tl_show_config(config.get_child(i), config_path, new_spacing)
  else:
    print "%s%s (%s): %s" % (spacing, config.get_name(), tl_gphoto2_type(config.get_type()), config.get_value())
    tl_show_config_options(config, new_spacing)
    #new_spacing = "%s    " % (spacing)
    #print "config.get_child(i).get_type(): %s" % config.get_child(i).get_type()
    #print "config.get_child(i).count_choices(): %s" % config.get_child(i).count_choices()
    #if config.count_choices() > 0:
    #  print "config.count_choices() > 0"
      #print "config.count_choices(): %s" % config.count_choices()
      #for i in range(0, config.count_choices() - 1):
      #  print "%s%s: %s" % (new_spacing, i, config.get_choice(i))
    pass


if __name__ == '__main__':
  tl_show_config(config)

#config.get_child_by_name('capturesettings').get_child_by_name('shutterspeed').get_value()
#config.get_child_by_name('capturesettings').get_child_by_name('shutterspeed').get_choice(52)


#config.get_child_by_name('capturesettings').get_child_by_name('shutterspeed').set_value(config.get_child_by_name('capturesettings').get_child_by_name('shutterspeed').get_choice(52))


#camera.set_config(config, context)

#file = camera.capture(gp.GP_CAPTURE_IMAGE, context)


