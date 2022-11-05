# Testing bitmap formatting and information with libraries

from PIL import Image, ImageOps
import numpy as np
import cairo
import math
import sys
import argparse
import os


def main():
    if check_filename(args.o):
        pixed = pixellate(sys.argv[1], blocksize=args.r)
        if args.m == "pixelize":
            print("Pixellating and reducing size of image")
            pix_to_image(pixed, gscale=args.g, filename=args.o + '.png')
        elif args.m == "arrows":
            print("Converting image to arrows")
            arrows(pixed, args.s, gscale=args.g, filename=args.o + '.svg', background=args.bg)
        elif args.m == "squiggles":
            print("Converting image to squiggles")
            squiggles(pixed, args.s, gscale=args.g, filename=args.o + '.svg', background=args.bg)
        elif args.m == "stars":
            print("Converting image to stars")
            draw_stars(pixed, args.s, gscale=args.g, filename=args.o + '.svg', background=args.bg, spin_angle=args.sa)
        elif args.m == "dotty":
            print("Converting image to sized dots")
            draw_dot_map(pixed, args.s, filename=args.o + '.svg', background=args.bg, colour=args.cc)
        elif args.m == "circles":
            print("Converting image to circles")
            draw_circle(pixed, args.s, gscale=args.g, filename=args.o + '.svg', background=args.bg)


def check_filename(filename):
    # Check to see if the output file already exists to avoid accidental file replacement
    if os.path.exists(filename + '.svg') or os.path.exists(filename + '.png'):
        while True:
            yn = input(f"File {filename} already exists, do you want to overwrite? (Y/N): ")
            if yn.lower().strip() in ("y", "yes"):
                return True
            elif yn.lower().strip() in ("n", "no"):
                print("Operation aborted")
                return False
            else:
                print("Resonse not recognized")
                pass
    else:
        return True


def pixellate(image: str, blocksize=15):
    raw_image = Image.open(image)
    # noinspection PyTypeChecker
    pix = np.array(ImageOps.exif_transpose(raw_image))
    if raw_image.size[0] < blocksize:
        raise ValueError("Pixel block size is greater than the number of pixels in the width of the image")
    elif raw_image.size[0] < blocksize:
        raise ValueError("Pixel block size is greater than the number of pixels in the height of the image")
    crop_w = raw_image.size[1] % blocksize
    crop_l = raw_image.size[0] % blocksize
    pix = np.delete(pix, distribute_both_ends(crop_l), 1)
    pix = np.delete(pix, distribute_both_ends(crop_w), 0)
    new = []
    for x in range(int(pix.shape[0] / blocksize)):
        new_row = []
        for y in range(int(pix.shape[1] / blocksize)):
            r = np.average(pix[x * blocksize:x * blocksize + blocksize, y * blocksize:y * blocksize + blocksize, 0])
            g = np.average(pix[x * blocksize:x * blocksize + blocksize, y * blocksize:y * blocksize + blocksize, 1])
            b = np.average(pix[x * blocksize:x * blocksize + blocksize, y * blocksize:y * blocksize + blocksize, 2])
            new_row.append((r, g, b))
        new.append(new_row)
    return np.array(new, dtype=np.uint8)


def distribute_both_ends(crop: int):
    cropr = np.arange(int(crop))
    spread = [i - crop if i > crop/2-1 else i for i in cropr]
    return spread


# Saves pixellated image, can be used for other bitmap outputs in future
def pix_to_image(pix_array: np.array, gscale=False, filename='output.png'):
    if gscale:
        pix_array = grayscale(pix_array)
    new_image = Image.fromarray(pix_array)
    new_image.save(filename)


# Sets up a cairo vector surface and context for use by generated vector modes
def setup_vector_draw(cmap: np.array, res: int, filename="output.svg"):
    sfc = cairo.SVGSurface(filename, cmap.shape[1] * res, cmap.shape[0] * res)
    ctx = cairo.Context(sfc)
    ctx.scale(res, res)
    cmap = cmap/256
    return sfc, ctx, cmap


# Modified cmap to grayscale
def grayscale(cmap: np.array):
    for i in cmap:
        for j in i:
            av = np.average(j)
            j[:] = av
    return cmap


# Drawing background rectangle for generated vector images
def draw_bg(colour: float, width: int, height: int, ctx):
    if 1 >= colour >= 0:
        ctx.set_source_rgb(colour, colour, colour)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()
        ctx.move_to(0, 0)


# Replaces image pixels with circles, background is transparent by default
def draw_circle(cmap: np.array, res: int, gscale=False, filename="output.svg", background=5):
    if gscale:
        cmap = grayscale(cmap)
    sfc, ctx, cmap = setup_vector_draw(cmap, res, filename)
    draw_bg(background, cmap.shape[1], cmap.shape[0], ctx)
    for x, i in enumerate(cmap):
        for y, j in enumerate(i):
            ctx.set_source_rgb(*j)
            ctx.arc(y, x, 0.5, 0, 2 * math.pi)
            ctx.close_path()
            ctx.fill()
    sfc.finish()
    sfc.flush()


# Replaces image pixels with stars, background is transparent by default
def draw_stars(cmap: np.array, res: int, gscale=False, filename="output.svg", background=5, spin_angle=10):
    if gscale:
        cmap = grayscale(cmap)
    sfc, ctx, cmap = setup_vector_draw(cmap, res, filename)
    draw_bg(background, cmap.shape[1], cmap.shape[0], ctx)
    h = 0.4
    for x, i in enumerate(cmap):
        for y, j in enumerate(i):
            spin = x * spin_angle * np.pi / 180 + y * spin_angle * np.pi / 180
            ctx.set_source_rgb(*j)
            ctx.move_to(y + 0.5 + 0.5 * np.sin(spin), x + 0.5 * np.cos(spin) - 0.5)
            ctx.rel_line_to(h * np.sin(18 * np.pi / 180 - spin), h * np.cos(18 * np.pi / 180 - spin))
            ctx.rel_line_to(h * np.cos(spin), h * np.sin(spin))
            ctx.rel_line_to(-h * np.cos(36 * np.pi / 180 - spin), h * np.sin(36 * np.pi / 180 - spin))
            ctx.rel_line_to(h * np.cos(72 * np.pi / 180 + spin), h * np.sin(72 * np.pi / 180 + spin))
            ctx.rel_line_to(-h * np.cos(36 * np.pi / 180 + spin), -h * np.sin(36 * np.pi / 180 + spin))
            ctx.rel_line_to(-h * np.cos(36 * np.pi / 180 - spin), h * np.sin(36 * np.pi / 180 - spin))
            ctx.rel_line_to(h * np.cos(72 * np.pi / 180 - spin), -h * np.sin(72 * np.pi / 180 - spin))
            ctx.rel_line_to(-h * np.cos(36 * np.pi / 180 + spin), -h * np.sin(36 * np.pi / 180 + spin))
            ctx.rel_line_to(h * np.cos(spin), h * np.sin(spin))
            ctx.fill()
    sfc.finish()
    sfc.flush()


# Replaces image pixels with circles of varying radius according to shade
# Single tone only, specified tone in args.cc, default is grayscale
def draw_dot_map(cmap: np.array, res: int, filename="output.svg", background=5, colour=(0, 0, 0)):
    cmap = grayscale(cmap)
    sfc, ctx, cmap = setup_vector_draw(cmap, res, filename)
    draw_bg(background, cmap.shape[1], cmap.shape[0], ctx)
    ctx.set_source_rgb(*colour)
    for x, i in enumerate(cmap):
        for y, j in enumerate(i):
            ctx.arc(y + 0.5, x + 0.5, (1 - j[0])/1.5, 0, 2 * math.pi)
            ctx.close_path()
            ctx.fill()
    sfc.finish()
    sfc.flush()


# Replaces image pixels with .svg of arrows oriented at 90° to eachother
def arrows(cmap: np.array, res: int, line_width=0.2, arrow_length=0.7,
           end_length=0.3, gscale=False, filename="output.svg", background=5):
    if gscale:
        cmap = grayscale(cmap)
    sfc, ctx, cmap = setup_vector_draw(cmap, res, filename)
    draw_bg(background, cmap.shape[1], cmap.shape[0], ctx)
    ctx.set_line_width(line_width)
    new_row = False
    for y, i in enumerate(cmap):
        if new_row:
            direction = "RIGHT"
            new_row = False
        else:
            direction = "UP"
            new_row = True
        for x, j in enumerate(i):
            ctx.set_source_rgb(*j)
            if direction == "RIGHT":
                ctx.move_to(x-line_width/4, y+arrow_length/2)
                ctx.rel_line_to(arrow_length, 0)
                ctx.rel_move_to(-end_length, end_length)
                ctx.rel_line_to(end_length, -end_length)
                ctx.rel_line_to(-end_length, -end_length)
                direction = "UP"
            elif direction == "UP":
                ctx.move_to(x+arrow_length/2, y+line_width/4)
                ctx.rel_line_to(0, arrow_length)
                ctx.rel_move_to(end_length, end_length - arrow_length)
                ctx.rel_line_to(-end_length, -end_length)
                ctx.rel_line_to(-end_length, end_length)
                direction = "RIGHT"
            ctx.stroke()
    sfc.finish()
    sfc.flush()


# Replace image picels with .svg of squiggly lines running North-West to South-East
def squiggles(cmap: np.array, res: int, line_width=0.5, gscale=False, filename="output.svg", background=5):
    if gscale:
        cmap = grayscale(cmap)
    sfc, ctx, cmap = setup_vector_draw(cmap, res, filename)
    draw_bg(background, cmap.shape[1], cmap.shape[0], ctx)
    ctx.set_line_width(line_width)
    for x, i in enumerate(cmap):
        for y, j in enumerate(i):
            ctx.set_source_rgb(*j)
            ctx.move_to(y, x)
            ctx.rel_curve_to(0.25, 0, 0.25, 0, 0.251, 0.251)
            ctx.rel_curve_to(0, 0.25, 0, 0.25, 0.251, 0.251)
            ctx.rel_curve_to(0.25, 0, 0.25, 0, 0.251, 0.251)
            ctx.rel_curve_to(0, 0.25, 0, 0.25, 0.251, 0.251)
            ctx.stroke()
    sfc.finish()
    sfc.flush()


if __name__ == '__main__':
    # Instituting parsearg operations before running main
    parser = argparse.ArgumentParser()
    parser.add_argument("f", help='Filename of image to alter')
    parser.add_argument("-o", default='output', help='Filename of output image (extension not required)')
    parser.add_argument("-m", default='pixelize', choices=("arrows", "pixelize", "circles", "dotty",
                                                           "squiggles", "stars"),
                        help='Select Mode')
    parser.add_argument("-r", default=20, help='Number of pixels to pixelate image by (Integer)', type=int)
    parser.add_argument("-s", default=10, help='Size of Vector Image', type=int)
    parser.add_argument("-g", default=False, help='Enable Grayscale (True or False)', type=bool)
    parser.add_argument("-bg", default=2, help='Enable Background Shade, between 0 and 1, '
                        'default is transparent', type=float)
    parser.add_argument("-cc", default=(0, 0, 0), help='RGB Code for circle colours (Dotty mode only)',
                        type=float, nargs=3)
    parser.add_argument("-sa", default=0, help='Spin angle in degrees for stars mode (default is no spin)', type=float)
    args = parser.parse_args()
    main()
