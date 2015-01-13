======
pmdive
======


About
=====

Script for generating pattern for paper model of OpenDive (http://www.durovis.com/opendive.html) compatible 3D glasses.

Requirements
============

"Durovis OpenDive Lens Kit" - you can order it by Amazon

Usage
=====

python script usage example:

    ::

        python pmdive.py --page_width=210 --pupillary_distance=70 --noscript output.svg

If SVG file was created without --noscript parameter, it can be opened in web browser with additional parameters:

    ::

        file:///C:/temp/pmdive.svg?dimensions=132.6x65.5x6.18;pd=20;page=1

Attributes
==========

- page_width -- target page width in mm (default:297mm)
- page_height -- target page height in mm (default:420mm)
- device_width -- the width of the smartphone in mm
- device_height -- the height of the smartphone in mm
- device_depth -- the depth of the smartphone in mm
- dimensions -- dimensions in form HxWxD
- device_screen_middle -- the middle of the smartphones screen (default: None if
  the middle of screen is the middle of the smartphone)
- lens_focal_length -- the focal length of the lens in mm (default: 40mm)
- lens_diameter -- the diameter of the lens in mm (default:26mm)
- strap_width -- the width of mask strap in mm
- pupillary_distance -- the pupillary distance in mm
- pd -- alias for pupillary_distance
- page -- page number (1 or 2) for multipage output (default: None)
- noscript -- do not add JavaScript to target SVG file
- logo -- logo file (in png, jpg or svg format)

