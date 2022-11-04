# Image Altar

#### Video Demo:  <URL HERE>
### Description:
> This was my final project for the CS50P course
#### Intro
I opted to produce something for this final project that would be very different to something I would produce for work, 
so I settled on a bitmap image altering toy with a variety of features.  
The program uses Pillow and Pycairo (two libraries I hadn't really been exposed to previously) to read in a bitmap image 
file, and to re-render it as a vector image which replaces blocks of the bitmap in some form, lending the colour of the 
block to the new replacement symbol, with the intent to still evoke the previous image.  
I attempted to structure Image Altar in such a way that it could readily have additional transformation outputs added 
later, but have submitted it with 5 (maybe 5.5...) different transformations (examples of each below).
#### Use
Image Altar uses parsearg to run through a terminal, -h output below:
    '''
    usage: project.py [-h] [-o O] [-m M] [-r R] [-s S] [-g G] [-bg BG] [-cc CC CC CC] f         
                                                                                            
    positional arguments:                                                                       
      f             Filename of image to alter                                                  
                                                                                                
    options:
      -h, --help    show this help message and exit
      -o O          Filename of output image
      -m M          Select Mode, Valid options are: pixelize, arrows, circles, dotty, squiggles, stars
      -r R          Number of pixels to pixelate image by (Integer)
      -s S          Size of Vector Image
      -g G          Enable Grayscale (True or False)
      -bg BG        Enable Background Shade, between 0 and 1, default is transparent
      -cc CC CC CC  RGB Code for circle colours (Dotty mode only)
      -sa SA        Spin angle in degrees for stars mode (default is no spin)
    '''
# Pixelize
If no mode is specified, the "pixelize" mode is selected by dafault. Fundamentally, the pixellize mode is a side effect 
of the program itself, rather than an intended useful output. It simply reads in a bitmap image, and then creates a new 
pixellated bitmap from it with pixels of the specified size, of the average colour of the block. Remaining pixels of the
original image that would not fit evenly into the new array are discarded evenly from each edge of the original image.  
There are existing interpolative functions that exist within pillow for this purpose that could have been used instead, 
but I actively chose to rewrite this algorith for both the challenge (this is an exercise in education after all) and to 
have full control of the output array.  
The key option for pixelize is -r (default is 20), which controls the number of pixels in the square block (sized r x r) 
that is used to pixelize the original image.

Example of pixelize outputs below:
> python project.py Dog_Photos/Olive.jpg -r 20
|Original picture of Olive|python project.py Dog_Photos/Olive.jpg -r 20|python project.py Dog_Photos/Olive.jpg -r 30|
|![Olive]<img src="Dog_Photos/Olive.jpg">|![Olive -r 20]<img src="Olive -r 20.jpg">|![Olive -r 30]<img src="Olive -r 30.jpg">|
