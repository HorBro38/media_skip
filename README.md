# Media Skip for Ren'py
by HB38

This Project is a drop in library for adding an easy way to skip movies (and music) in Ren'Py.  Here is an example of the default settings, which can be fully customized to match the style of your game:

![skip_movie](https://github.com/HorBro38/media_skip/blob/main/skip_video.gif?raw=true)

## How to Use
It is designed for you to drag and drop the folder into your ~/game/ folder.  To invoke this use the following:

`call screen media_skip("images/movie_name.webm")`

## Attributes
Media Skip supports the following attributes:

`hold_time` - This is the length of time the player will have to press and hold the button this many seconds to skip the screen.  This is a float, the default is `2.0`.

`show_time` - This is the length of time the "skip" screen will show over the media when initially shown.  If the user does not interact with it, it will hide after this many seconds.  This is a float, the default is `2.0`.

`override_length` - You can use this attribute to manually set the time the skip screen will display, if you don't want to automatically get it from the media.  This is a float, the default is `None`.

`align` - Lets you manually set the alignment of where the skip text and icons appear.  This is a tuple of floats (x,y), the default is `(0.95,0.95)`.

`pos` - Lets you set specific pixel positions for where the skip text and icons appear.  This will override the align settings (if used).  This is a tuple of integers, the default is `None`.

## Terms of Use
Feel free to use this as you desire, credit is not necessary but always appreciated (feel free to simply credit HB38).

## Optional Extras
If you've got a copy of [Feniks' circular bars](https://feniksdev.itch.io/circular-bar-for-renpy), you can use the included commented code to swap to that style with ease:

![skip_ring](https://github.com/HorBro38/media_skip/blob/main/skip_ring.gif?raw=true)

## Acknowledgements
Many thanks to Feniks for their assistance (https://feniksdev.com).

Mouse Button Icons by GreatDocBrown (https://greatdocbrown.itch.io/gamepad-ui)

## Want to leave a tip?
[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/hb38_psk)
