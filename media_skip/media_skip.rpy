###############################################################################
#
# Media Skip by HB38 (https://ko-fi.com/hb38_psk)
#
###############################################################################
# This file contains code for adding an easy way to skip movies (and music) in
# Ren'Py. It is designed for you to drag and drop the folder into your ~/game/
# folder.  To invoke this use the following:
#
# call screen media_skip("images/movie_name.webm")
#
# Media Skip supports the following attributes:
#
# hold_time - This is the length of time the player will have to press and hold
# the button this many seconds to skip the screen. This is a float, the default
# is 2.0.
#
# show_time - This is the length of time the "skip" screen will show over the
# media when initially shown. If the user does not interact with it, it will hide
# after this many seconds. This is a float, the default is 2.0.
#
# override_length - You can use this attribute to manually set the time the skip
# screen will display, if you don't want to automatically get it from the media.
# This is a float, the default is None.
#
# align - Lets you manually set the alignment of where the skip text and icons
# appear.  This is a tuple of floats (x,y), the default is (0.95,0.95).
#
# pos - Lets you set specific pixel positions for where the skip text and icons
# appear.  This will override the align settings.  This is a tuple integers, the
# default is None.
#
# Many thanks to Feniks for their assistance (https://feniksdev.com)
#
# Mouse Button Icons by GreatDocBrown (https://greatdocbrown.itch.io/gamepad-ui)
#
# Feel free to contact me on Discord @ HB38
###############################################################################

style skip_bar:
    ysize gui.bar_size
    left_bar Frame("media_skip/bar_left.webp", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("media_skip/bar_right.webp", gui.bar_borders, tile=gui.bar_tile)
    thumb Frame("media_skip/bar_thumb.webp", gui.bar_borders, tile=gui.bar_tile)
    left_gutter 15
    right_gutter 5
    thumb_offset (0,5) #This uses a new addition to the bar that allows for a tuple to be used for an offset (added in Ren'py version 8.4.0).  Change this to a single integer if you need to backport this to earlier versions of Ren'py, but it will cause a slight transparency artifact during dissolves.
    bar_invert True
    # This style contains the image files as well as other settings for the default bar used by the skip screen.  Adjust or replace as needed.

screen media_skip(name,hold_time=2.0,show_time=2.0,override_length=None,align=(0.95,0.95),pos=None,image=False):

  if image:
      default the_media = name
  else:
    default the_media = Movie(play="{}".format(name), channel='mskip')

  default media_length = renpy.music.get_duration(channel='mskip')
  # Keep re-checking to get the length of the movie
  if override_length:
    timer override_length action Return()
  elif not media_length:
    timer 1.0/60.0 action SetScreenVariable('media_length',
      renpy.music.get_duration(channel='mskip')) repeat True
  else:
    timer media_length action Return()
    # Once we have the movie length, hide the screen after it's done playing

  add the_media align (0.5, 0.5)
  # This centers the movie in the screen

  default show_skip = False
  default held = False
  default held_time = hold_time
  default held_passed = False
  dismiss action SetScreenVariable('show_skip', True)
  # Skip options

  showif show_skip:

    vbox:
      if pos:
        pos pos
      else:
        align align
      # Places this in the bottom right corner

## If using Fenik's circular bars (https://feniksdev.itch.io/circular-bar-for-renpy) you can use this code and the included images to get them to work together:
#      hbox:
#       spacing 20
#       fixed:
#         fit_first True align (0.5, 0.5)
#         circular_bar:
#           fore_bar "colorize:media_skip/circle_bar.webp|#ffffff"
#           aft_bar "colorize:media_skip/circle_bar.webp|#000000"
#           hover_aft_bar "colorize:media_skip/circle_bar.webp|#ffffff"
#           focus_mask True
#           xysize (97, 97)
#           thumb "colorize:media_skip/circle_thumb.webp|#ffffff"
#           hover_thumb "colorize:media_skip/circle_thumb.webp|#ffffff"
#           thumb_offset absolute(35.2)
#           start_thumb "colorize:media_skip/circle_thumb.webp|#ffffff"
#           hover_start_thumb "colorize:media_skip/circle_thumb.webp|#ffffff"
#           hide_start_thumb True
#           bar_invert True
#           value AnimatedValue(value=held_time, range=hold_time, delay=0.1, old_value=None)
#         if held:
#           image "media_skip/mouse_2.webp" align (0.5,0.5)
#           # The left mouse button being pressed graphic
#         else:
#           image "media_skip/mouse_1.webp" align (0.5,0.5)
#           # The left mouse button being released graphic
#       text _("Skip") yalign 0.5
#       # The text for the skip button, customize to fit the rest of the theme of your game

# If using Fenik's circular bars (see above), you can comment out/delete the following block:
      hbox:
       spacing 20
       if held:
         image "media_skip/mouse_2.webp"
         # The left mouse button being pressed graphic
       else:
         image "media_skip/mouse_1.webp"
         # The left mouse button being released graphic
       text _("Skip") yalign 0.5 color "#ffffff"
       # The text for the skip button, customize to fit the rest of the theme of your game
      bar xysize (150,18) style 'skip_bar' value AnimatedValue(value=held_time, range=hold_time, delay=0.1, old_value=None)

      at transform:
       # This transform gives the fade in and out effect as it appears and disappears
       on start, appear:
         alpha 0.0
       on show:
         linear 0.2 alpha 1.0
       on hide:
         linear 0.2 alpha 0.0


  if show_skip:
    if not held:
      # This is the timer that triggers when it should fade the skip option if the player decides not to skip
      timer show_time action SetScreenVariable('show_skip', False)
    key "mousedown_1" action SetScreenVariable('held', True)

  if held:
    key "keyup_mousedown_1" action SetScreenVariable('held', False)
    timer 0.01 repeat True action If(held_time < 0.0, (SetScreenVariable('show_skip',False),SetScreenVariable('held_passed',True)), SetScreenVariable('held_time', held_time-0.01))
  elif held_time <= hold_time and not held_passed:
    timer 0.01 repeat True action SetScreenVariable('held_time', held_time+0.01)

  if held_passed:
    # This gives the end user just under half a second to release the button before we continue so as to prevent them from [possibly] skipping the next line of dialogue on accident
    timer 0.45 action Return()
