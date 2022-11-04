# Image Altar

#### Video Demo:  <URL HERE>
### Description:
    > This was my final project for the CS50P course
#### Intro
    I opted to produce something for this final project that would be very different to something I would produce for work, so I settled on a bitmap image altering toy with a variety of features.
    The program uses Pillow and Pycairo (two libraries I hadn't really been exposed to previously) to read in a bitmap image file, and to re-render it as a vector image which blocks of the bitmap replaced in some form, loaning the colour of that block the new replacement symbol, with the intent to still evoke the previous image.
    I attempted to structure Image Altar in such a way that it could readily have additional transformation outputs added later, but have submitted it with 5 (maybe 5.5...) different transformations (examples of each below).
#### Use
    Image Altar uses parsearg to run through a terminal, -h output below:

    '''
    usage: project.py [-h] [-o O] [-m M] [-r R] [-s S] [-g G] [-bg BG] [-cc CC CC CC] f         
                                                                                            
    positional arguments:                                                                       
      f             Filename of image to alter                                                  
                                                                                                
    options:
      -h, --help    show this help message and exit
      -o O          Filename of output image
      -m M          Select Mode, Valid options are: pixelize, arrows, circles, dotty, squiggles,     
                    stars
      -r R          Number of pixels to pixelate image by (Integer)
      -s S          Size of Vector Image
      -g G          Enable Grayscale (True or False)
      -bg BG        Enable Background Shade, between 0 and 1, default is transparent
      -cc CC CC CC  RGB Code for circle colours (Dotty mode only)
      -sa SA        Spin angle in degrees for stars mode (default is no spin)
    '''
