from __future__ import annotations
import math
from collections import namedtuple
from enum import Enum
from PIL import Image as ImageModule
from PIL.Image import Image
from PIL import ImageDraw

import sizes
import colors
from colors import COLOR_BG, COLOR_FACTION
from icon_mode import IconMode


shape_data = namedtuple('shape_data', ['draw_shape', 'offset', 'size'])
type_cache: dict[tuple[Shape, IconMode], Image] = {}


def _draw_bomber(img: Image, mode: IconMode):
    w, h = img.width, img.height

    d = w // 2
    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(0, h - 3), (w - 1, h - 2)], COLOR_BG)  # remove tech level pixels

    img_draw.line([(0, h - 3), (d - 1, 0)], mode.value.outline)
    img_draw.line([(w - 1, h - 3), (d, 0)], mode.value.outline)
    img_draw.line([(1, h - 3), (d - 1, 1)], mode.value.outline)
    img_draw.line([(w - 2, h - 3), (d, 1)], mode.value.outline)

    img_draw.line([(0, h - 3), (0, h - 1)], mode.value.outline)
    img_draw.line([(w - 1, h - 3), (w - 1, h - 1)], mode.value.outline)

    img_draw.line([(0, h - 1), (w - 1, h - 1)], mode.value.outline)

    ImageDraw.floodfill(img, (w // 2, h // 2), COLOR_FACTION)


def _draw_bot(img: Image, mode: IconMode):
    w, h = img.width, img.height

    d = h // 2
    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(0, h - 3), (w - 1, h - 2)], COLOR_BG)  # remove tech level pixels

    img_draw.line([(0, d - 1), (d - 1, 0)], mode.value.outline)
    img_draw.line([(0, d), (d - 1, h - 1)], mode.value.outline)
    img_draw.line([(w - 1, d - 1), (w - d, 0)], mode.value.outline)
    img_draw.line([(w - 1, d), (w - d, h - 1)], mode.value.outline)

    img_draw.line([(1, d - 1), (d, 0)], mode.value.outline)
    img_draw.line([(1, d), (d, h - 1)], mode.value.outline)
    img_draw.line([(w - 2, d - 1), (w - d - 1, 0)], mode.value.outline)
    img_draw.line([(w - 2, d), (w - d - 1, h - 1)], mode.value.outline)

    img_draw.line([(d - 1, 0), (w - d, 0)], mode.value.outline)
    img_draw.line([(d - 1, h - 1), (w - d, h - 1)], mode.value.outline)

    ImageDraw.floodfill(img, (w // 2, h // 2), COLOR_FACTION)


def _draw_factory(img: Image, mode: IconMode):
    w, h = img.width, img.height

    img_draw = ImageDraw.Draw(img)
    img_draw.line([(0, 0), (w - 1, 0)], mode.value.outline)
    img_draw.line([(0, h - 1), (w - 1, h - 1)], mode.value.outline)
    img_draw.line([(0, 0), (0, h - 1)], mode.value.outline)
    img_draw.line([(w - 1, 0), (w - 1, h - 1)], mode.value.outline)

    img_draw.rectangle([(1, 1), (w - 2, h - 2)], COLOR_FACTION)


def _draw_factoryhq(img: Image, mode: IconMode):
    _draw_factory(img, mode)

    w, h = img.width, img.height
    th = max(1, math.ceil(img.height / 10))
    g = max(1, math.ceil(img.height / 7))

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(g, g), (g + th - 1, h - g - 1)], mode.value.type)
    img_draw.rectangle([(w - g - th, g), (w - g - 1, h - g - 1)], mode.value.type)

    return img


def _draw_fighter(img: Image, mode: IconMode):
    w, h = img.width, img.height

    d = w // 2
    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(0, h - 3), (w - 1, h - 2)], COLOR_BG)  # remove tech level pixels
    img_draw.line([(d - 1, 0), (0, w - 1)], mode.value.outline)
    img_draw.line([(d, 0), (w - 1, w - 1)], mode.value.outline)

    img_draw.line([(d - 1, 1), (0, w)], mode.value.outline)
    img_draw.line([(d, 1), (w - 1, w)], mode.value.outline)

    img_draw.line([(0, w - 1), (0, w + 1)], mode.value.outline)
    img_draw.line([(w - 1, w - 1), (w - 1, w + 1)], mode.value.outline)
    img_draw.line([(0, w + 1), (w - 1, w + 1)], mode.value.outline)

    ImageDraw.floodfill(img, (w // 2, h // 2), COLOR_FACTION)


def _draw_gunship(img: Image, mode: IconMode):
    w, h = img.width, img.height

    d = w // 5
    img_draw = ImageDraw.Draw(img)

    img_draw.rectangle([(0, h - 3), (w - 1, h - 2)], COLOR_BG)  # remove tech level pixels

    img_draw.line([(0, 2), (d, h - 1)], mode.value.outline)
    img_draw.line([(w - 1, 2), (w - d - 1, h - 1)], mode.value.outline)
    img_draw.line([(0, 1), (d, h - 2)], mode.value.outline)
    img_draw.line([(w - 1, 1), (w - d - 1, h - 2)], mode.value.outline)

    img_draw.line([(0, 0), (w - 1, 0)], mode.value.outline)
    img_draw.line([(d, h - 1), (w - d - 1, h - 1)], mode.value.outline)

    ImageDraw.floodfill(img, (w // 2, h // 2), COLOR_FACTION)


def _draw_land(img: Image, mode: IconMode):
    w, h = img.width, img.height

    d = w // 2
    img_draw = ImageDraw.Draw(img)
    img_draw.line([(0, d - 1), (d - 1, 0)], mode.value.outline)
    img_draw.line([(0, d), (d - 1, h - 1)], mode.value.outline)
    img_draw.line([(d, 0), (w - 1, d - 1)], mode.value.outline)
    img_draw.line([(d, h - 1), (w - 1, d)], mode.value.outline)

    img_draw.line([(1, d - 1), (d - 1, 1)], mode.value.outline)
    img_draw.line([(1, d), (d - 1, h - 2)], mode.value.outline)
    img_draw.line([(d, 1), (w - 2, d - 1)], mode.value.outline)
    img_draw.line([(d, h - 2), (w - 2, d)], mode.value.outline)

    for x in range(2, d):
        img_draw.line([(x, d - x + 1), (x, d + x - 2)], COLOR_FACTION)
        img_draw.line([(w - x - 1, d - x + 1), (w - x - 1, d + x - 2)], COLOR_FACTION)


def _draw_ship(img: Image, mode: IconMode):
    w, h = img.width, img.height
    d = w // 2

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(0, h - 3), (w - 1, h - 2)], COLOR_BG)  # remove tech level pixels

    img_draw.arc([(0, 0), (w - 1, w - 1)], 180, 360, mode.value.outline, width=1)

    if mode.value.outline != COLOR_FACTION:
        for y in range(d - 1, -1, -1):
            x = 0
            while img.getpixel((d - x - 1, y)) != mode.value.outline:
                if img.getpixel((d - x - 1, y - 1)) == mode.value.outline and img.getpixel((d - x - 2, y)) == mode.value.outline:
                    img.putpixel((d - x - 1, y), mode.value.outline)
                if img.getpixel((d + x, y - 1)) == mode.value.outline and img.getpixel((d + x + 1, y)) == mode.value.outline:
                    img.putpixel((d + x, y), mode.value.outline)
                x += 1

    img_draw.line([(0, d), (0, h - 1)], mode.value.outline)
    img_draw.line([(w - 1, d), (w - 1, h - 1)], mode.value.outline)
    img_draw.line([(0, h - 1), (w - 1, h - 1)], mode.value.outline)

    ImageDraw.floodfill(img, (w // 2, h // 2), COLOR_FACTION)


def _draw_structure(img: Image, mode: IconMode):
    w, h = img.width, img.height

    img_draw = ImageDraw.Draw(img)

    img_draw.line([(0, 0), (0, h - 2)], mode.value.outline)
    img_draw.line([(0, 0), (w - 1, 0)], mode.value.outline)
    img_draw.line([(w - 1, 0), (w - 1, h - 2)], mode.value.outline)
    img_draw.line([(0, h - 1), (w - 1, h - 1)], mode.value.outline)

    img_draw.rectangle([(1, 1), (w - 2, h - 2)], COLOR_FACTION)


def _draw_submarine(img: Image, mode: IconMode):
    w, h = img.width, img.height
    d = w // 2

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(0, h - 3), (w - 1, h - 2)], COLOR_BG)  # remove tech level pixels

    img_draw.arc([(0, h - 1 - w), (w - 1, h - 1)], 0, 180, mode.value.outline, width=1)

    if mode.value.outline != COLOR_FACTION:
        for y in range(h - 1 - d, h - 1):
            x = 0
            while img.getpixel((d - x - 1, y)) != mode.value.outline:
                if img.getpixel((d - x - 1, y + 1)) == mode.value.outline and img.getpixel((d - x - 2, y)) == mode.value.outline:
                    img.putpixel((d - x - 1, y), mode.value.outline)
                if img.getpixel((d + x, y + 1)) == mode.value.outline and img.getpixel((d + x + 1, y)) == mode.value.outline:
                    img.putpixel((d + x, y), mode.value.outline)
                x += 1

    img_draw.line([(0, 0), (0, h - 1 - d)], mode.value.outline)
    img_draw.line([(w - 1, 0), (w - 1, h - 1 - d)], mode.value.outline)
    img_draw.line([(0, 0), (w - 1, 0)], mode.value.outline)

    ImageDraw.floodfill(img, (w // 2, h // 2), COLOR_FACTION)


class Shape(Enum):
    Bomber = shape_data(_draw_bomber, int(round(sizes.ICON_SIZE_BOMBER[1] * 0.075)), sizes.ICON_SIZE_BOMBER)
    Bot = shape_data(_draw_bot, 0, sizes.ICON_SIZE_BOT)
    Factory = shape_data(_draw_factory, 0, sizes.ICON_SIZE_FACTORY)
    FactoryHq = shape_data(_draw_factoryhq, 0, sizes.ICON_SIZE_FACTORY)
    Fighter = shape_data(_draw_fighter, int(round(sizes.ICON_SIZE_FIGHTER[1] * 0.15)), sizes.ICON_SIZE_FIGHTER)
    Gunship = shape_data(_draw_gunship, 0, sizes.ICON_SIZE_GUNSHIP)
    Land = shape_data(_draw_land, 0, sizes.ICON_SIZE_LAND)
    Ship = shape_data(_draw_ship, int(round(sizes.ICON_SIZE_FIGHTER[1] * 0.05)), sizes.ICON_SIZE_SHIP)
    Structure = shape_data(_draw_structure, 0, sizes.ICON_SIZE_STRUCTURE)
    Sub = shape_data(_draw_submarine, int(round(-sizes.ICON_SIZE_FIGHTER[1] * 0.00)), sizes.ICON_SIZE_SUB)

    @staticmethod
    def get_shape_pic(shape: Shape, mode: IconMode) -> Image:
        if (shape, mode) not in type_cache:
            img = ImageModule.new("RGBA", shape.value.size, (0, 0, 0, 0))
            shape.value.draw_shape(img, mode)
            # img.save(f'done_shapes\{shape.name}-{mode.name}.png', 'png')
            type_cache[(shape, mode)] = img

        return type_cache[(shape, mode)]


def draw_shape(img: Image, mode: IconMode, shape: Shape):
    pic = Shape.get_shape_pic(shape, mode)
    img.alpha_composite(pic, (0, 0))


def draw_wall(img: Image, mode: IconMode):
    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(0, 0), (img.width - 1, img.height - 1)], COLOR_FACTION, mode.value.outline)


def draw_experimental(img: Image, mode: IconMode):
    img_draw = ImageDraw.Draw(img)
    w, h = img.size
    d = w // 2

    img_draw.ellipse([(0, 0), (w - 1, h - 1)], COLOR_FACTION, mode.value.outline, width=1)

    if mode.value.outline == COLOR_FACTION:
        return

    for y in range(d - 1, -1, -1):
        x = 0
        while img.getpixel((d - x - 1, y)) != mode.value.outline:
            if img.getpixel((d - x - 1, y - 1)) == mode.value.outline and img.getpixel((d - x - 2, y)) == mode.value.outline:
                img.putpixel((d - x - 1, y), mode.value.outline)
            if img.getpixel((d + x, y - 1)) == mode.value.outline and img.getpixel((d + x + 1, y)) == mode.value.outline:
                img.putpixel((d + x, y), mode.value.outline)
            x += 1

    for y in range(h - 1 - d, h - 1):
        x = 0
        while img.getpixel((d - x - 1, y)) != mode.value.outline:
            if img.getpixel((d - x - 1, y + 1)) == mode.value.outline and img.getpixel((d - x - 2, y)) == mode.value.outline:
                img.putpixel((d - x - 1, y), mode.value.outline)
            if img.getpixel((d + x, y + 1)) == mode.value.outline and img.getpixel((d + x + 1, y)) == mode.value.outline:
                img.putpixel((d + x, y), mode.value.outline)
            x += 1


def draw_nuke(img: Image):
    img_draw = ImageDraw.Draw(img)
    w, h = img.size
    d = w // 2
    c = max(1, h // 12)
    th = max(1, h // 12) + 1

    img_draw.ellipse([(0, 0), (w - 1, h - 1)], colors.COLOR_NUKE, colors.COLOR_BLACK, width=1)
    img_draw.ellipse([(d - c - 1, d - c - 1), (d + c, d + c)], colors.COLOR_BLACK)

    for yt in range(-d - 1, d + 2):
        y = yt + 0.5
        for xt in range(-d - 1, d + 2):
            x = xt + 0.5
            if y * y + x * x >= (d - th) * (d - th) or x * x + y * y <= (c + th) * (c + th):
                continue

            a = math.atan2(y / d, x / d)
            if -math.pi / 3 < a < 0 or -math.pi < a < -math.pi * 2 / 3 or math.pi / 3 < a < math.pi * 2 / 3:
                img.putpixel((int(d + x), int(d + y)), colors.COLOR_BLACK)


def draw_antinuke(img: Image):
    img_draw = ImageDraw.Draw(img)
    w, h = img.size

    img_draw.ellipse([(0, 0), (w - 1, h - 1)], colors.COLOR_ANTINUKE, colors.COLOR_BLACK, width=1)

    d = w // 2
    g = max(1, math.ceil(d * 0.25))
    th = max(1, math.ceil(d / 6))

    img_draw = ImageDraw.Draw(img)

    for t in range(th):
        img_draw.line([(g + t, g), (w - 1 - g, h - 1 - g - t)], colors.COLOR_BLACK)
        img_draw.line([(g, g + t), (w - 1 - g - t, h - 1 - g)], colors.COLOR_BLACK)

        img_draw.line([(g + t, h - 1 - g), (w - 1 - g, g + t)], colors.COLOR_BLACK)
        img_draw.line([(g, h - 1 - g - t), (w - 1 - g - t, g)], colors.COLOR_BLACK)


def draw_commander_old(img: Image, mode: IconMode):
    img_draw = ImageDraw.Draw(img)
    w, h = img.size

    d = w // 2
    g = max(1, math.ceil(d * 0.15))
    th = max(1, math.ceil(d / 6))
    th2 = th + 4
    hs = max(1, math.ceil(h / 8))
    ls = max(1, math.ceil(h * 0.55))

    img_draw = ImageDraw.Draw(img)

    img_draw.line([(d, hs), (d, ls)], mode.value.outline, width=th2)
    img_draw.line([(g, hs * 2 + g), (w - g - 1, hs * 2 + g)], mode.value.outline, width=th2 - 2)
    img_draw.line([(d - th, ls - 1), (d + th, ls - 1)], mode.value.outline, width=th2)

    img_draw.line([(d - th, ls - 1), (d - (h - ls) // 2, h)], mode.value.outline, width=th2)
    img_draw.line([(d + th, ls - 1), (d + (h - ls) // 2, h)], mode.value.outline, width=th2)

    img_draw.ellipse([(d - hs - 2, 0), (d + hs + 2, hs * 2 + 2)], mode.value.outline, mode.value.outline, width=1)

    color = colors.COLOR_FACTION if mode in (IconMode.Rest, IconMode.Selected) else colors.COLOR_WHITE
    offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if any([img.getpixel((x + o[0], y + o[1])) == COLOR_BG for o in offsets]):
                continue
            img.putpixel((x, y), color)


def draw_commander(img: Image, mode: IconMode):
    w, h = img.size

    if mode is IconMode.Rest:
        orig = ImageModule.open('templates/icon_commander_generic_rest.png')
    elif mode is IconMode.Over:
        orig = ImageModule.open('templates/icon_commander_generic_over.png')
    elif mode is IconMode.Selected:
        orig = ImageModule.open('templates/icon_commander_generic_selected.png')
    else:
        orig = ImageModule.open('templates/icon_commander_generic_selectedover.png')

    resized = orig.resize((w, h), ImageModule.NEAREST)

    img.alpha_composite(resized, (0, 0))
