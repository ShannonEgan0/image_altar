# Testing bitmap formatting and information with libraries

from PIL import Image
import numpy as np
import cairo
import math
import sys
import argparse


def main():
    pixed = pixellate(sys.argv[1], size=9)
    if args.m == "pixelize":
        print("Pixellating and reducing size of image")
        pix_to_image(pixed, filename=args.o + '.png')
    elif args.m == "arrows":
        print("Converting image to arrows")
        arrows(pixed, args.r, gscale=args.g, filename=args.o + '.svg', background=args.bg)
    elif args.m == "dotty":
        print("Converting image to sized dots")
        draw_dot_map(pixed, args.r, filename=args.o + '.svg')
    elif args.m == "circles":
        print("Converting image to circles")
        draw_circle(pixed, args.r, gscale=args.g, filename=args.o + '.svg')


def pixellate(image: str, size=15):
    raw_image = Image.open(image)
    # noinspection PyTypeChecker
    pix = np.array(raw_image)
    crop_w = raw_image.size[1] % size
    crop_l = raw_image.size[0] % size
    pix = np.delete(pix, distribute_both_ends(crop_l), 1)
    pix = np.delete(pix, distribute_both_ends(crop_w), 0)
    new = []
    for x in range(int(pix.shape[0] / size)):
        new_row = []
        for y in range(int(pix.shape[1] / size)):
            r = np.average(pix[x * size:x * size + size, y * size:y * size + size, 0])
            g = np.average(pix[x * size:x * size + size, y * size:y * size + size, 1])
            b = np.average(pix[x * size:x * size + size, y * size:y * size + size, 2])
            new_row.append((r, g, b))
        new.append(new_row)
    return np.array(new, dtype=np.uint8)


def distribute_both_ends(crop: int):
    cropr = np.arange(int(crop))
    spread = [i - crop if i > crop/2-1 else i for i in cropr]
    return spread


def pix_to_image(pix_array: np.array, filename='output.png'):
    new_image = Image.fromarray(pix_array)
    new_image.save(filename)


def setup_vector_draw(cmap: np.array, res: int, filename="output.svg"):
    sfc = cairo.SVGSurface(filename, cmap.shape[1] * res, cmap.shape[0] * res)
    ctx = cairo.Context(sfc)
    ctx.scale(res, res)
    cmap = cmap/256
    return sfc, ctx, cmap


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


def draw_dot_map(cmap: np.array, res: int, filename="output.svg", background=5):
    cmap = grayscale(cmap)
    sfc, ctx, cmap = setup_vector_draw(cmap, res, filename)
    draw_bg(background, cmap.shape[1], cmap.shape[0], ctx)
    ctx.set_source_rgb(0, 0, 0)
    for x, i in enumerate(cmap):
        for y, j in enumerate(i):
            ctx.arc(y, x, (1 - j[0])/1.5, 0, 2 * math.pi)
            ctx.close_path()
            ctx.fill()
    sfc.finish()
    sfc.flush()


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


def grayscale(cmap: np.array):
    for i in cmap:
        for j in i:
            av = np.average(j)
            j[:] = av
    return cmap


def draw_bg(colour: float, width: int, height: int, ctx):
    if 1 >= colour >= 0:
        ctx.set_source_rgb(colour, colour, colour)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()
        ctx.move_to(0, 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("f", help='Filename of image to alter')
    parser.add_argument("-o", default='output', help='Filename of output image')
    parser.add_argument("-m", default='pixelize', help='Select Mode, options are: arrows, pixelize, circles, dotty')
    parser.add_argument("-r", default=20, help='Resolution of image', type=int)
    parser.add_argument("-g", default=False, help='Enable Grayscale', type=bool)
    parser.add_argument("-bg", default=2, help='Enable Background Shade, between 0 and 1, '
                                               'default is transparent', type=float)
    args = parser.parse_args()
    main()
