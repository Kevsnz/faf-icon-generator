from __future__ import annotations
import math
from enum import Enum
from functools import partial

from PIL.Image import Image, new
from PIL import ImageDraw

from icon_mode import IconMode
from sizes import TECH_LEVEL_HEIGHT, TYPE_SIZE


type_cache: dict[tuple[UnitType, IconMode], Image] = {}


def _add_hq(img: Image, mode: IconMode) -> Image:
    th = max(1, math.ceil(img.height / 10))
    g = max(1, math.ceil(img.height / 7))
    g2 = max(1, math.ceil(img.height / 10))

    img2 = new("RGBA", (img.width + th * 2 + g2 * 2, img.height), (0, 0, 0, 0))
    w, h = img2.size

    img2.alpha_composite(img, (th + g2, 0))

    img_draw = ImageDraw.Draw(img2)
    img_draw.rectangle([(0, g), (th - 1, h - g - 1)], mode.value.type)
    img_draw.rectangle([(w - th, g), (w - 1, h - g - 1)], mode.value.type)

    return img2


def _draw_type_generic(mode: IconMode) -> Image:
    return new("RGBA", (1, 1), (0, 0, 0, 0))


def _draw_type_air(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)

    for i in range(th):
        img_draw.line([(d - 1, d // 2 + i), (0 + i, d + d // 2 - 1)], mode.value.type)
        img_draw.line([(d, d // 2 + i), (w - 1 - i, d + d // 2 - 1)], mode.value.type)

    return img


def _draw_type_air_hq(mode: IconMode) -> Image:
    return _add_hq(_draw_type_air(mode), mode)


def _draw_type_antiair(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2

    v_offset = h * 8 // 8 - 1
    y_max = -999999999999

    x: float = -d + 1
    while x <= d - 1:
        y = round(math.sin(math.acos(x / d)) * h * 0.6)
        img.putpixel((d + int(round(x)), v_offset - y), mode.value.type)
        if y_max is None or v_offset - y > y_max:
            y_max = v_offset - y
        x += 0.01

    x = -d + 1
    while x <= d - 1:
        y = v_offset - round(math.sin(math.acos(x / d)) * h * 0.6) + 1
        if y <= y_max:
            img.putpixel((d + int(round(x)), y), mode.value.type)
        x += 0.01

    return img


def _draw_type_armored(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))

    g = max(1, math.ceil(h / 6))
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)

    for t in range(th):
        img_draw.line([(g + t, g), (w - 1 - g, h - 1 - g - t)], mode.value.type)
        img_draw.line([(g, g + t), (w - 1 - g - t, h - 1 - g)], mode.value.type)

        img_draw.line([(g + t, h - 1 - g), (w - 1 - g, g + t)], mode.value.type)
        img_draw.line([(g, h - 1 - g - t), (w - 1 - g - t, g)], mode.value.type)

    return img


def _draw_type_artillery(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))

    d = w // 2
    s = min(h // 2 - 1, max(3, math.ceil(h * (3 / 7) / 2)))

    img_draw = ImageDraw.Draw(img)

    img_draw.rectangle([(d - 1, h // 2 - 1 - s), (d, h // 2 + s)], mode.value.type)
    img_draw.rectangle([(d - 1 - s, h // 2 - 1), (d + s, h // 2)], mode.value.type)

    return img


def _draw_type_antiartillery(mode: IconMode) -> Image:
    img = _draw_type_artillery(mode)
    h = img.height

    img_draw = ImageDraw.Draw(img)
    d = h // 2
    s = min(4, max(1, math.ceil(h / 12)))

    img_draw.rectangle([(d - s, d - s), (d + s - 1, d + s - 1)], (0, 0, 0, 0))

    return img


def _draw_type_bomb(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))

    d = w // 2
    g = max(1, math.ceil(h / 6))
    s = max(1, math.ceil(h / 10))
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)

    for t in range(th):
        img_draw.line([(g + t, g), (d - s, d - s - t)], mode.value.type)
        img_draw.line([(g, g + t), (d - s - t, d - s)], mode.value.type)

        img_draw.line([(g + t, h - 1 - g), (d - s, d + s - 1 + t)], mode.value.type)
        img_draw.line([(g, h - 1 - g - t), (d - s - t, d + s - 1)], mode.value.type)

        img_draw.line([(w - 1 - g - t, g), (d + s - 1, d - s - t)], mode.value.type)
        img_draw.line([(w - 1 - g, g + t), (d + s - 1 + t, d - s)], mode.value.type)

        img_draw.line([(w - 1 - g - t, h - 1 - g), (d + s - 1, d + s - 1 + t)], mode.value.type)
        img_draw.line([(w - 1 - g, h - 1 - g - t), (d + s - 1 + t, d + s - 1)], mode.value.type)

    return img


def _draw_type_missile(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(d - 1, 0), (d, TYPE_SIZE - 1)], mode.value.type)

    return img


def _draw_type_antimissile(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = max(1, math.ceil(h / 8))
    st = (h - g * 2) / 3

    img_draw = ImageDraw.Draw(img)

    img_draw.rectangle([(d - 1, 0), (d, int(st))], mode.value.type)
    img_draw.rectangle([(d - 1, int(st) + g), (d, int(st * 2) + g)], mode.value.type)
    img_draw.rectangle([(d - 1, int(st * 2) + g * 2), (d, TYPE_SIZE - 1)], mode.value.type)

    return img


def _draw_type_naval(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = max(1, math.ceil(h / 7))
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)
    img_draw.arc([(0, -d // 2), (w - 1, h - d // 2 - 1)], 0, 180, mode.value.type, th)
    img_draw.rectangle([(0, g), (th - 1, d // 2 - 1)], mode.value.type)
    img_draw.rectangle([(w - th, g), (w - 1, d // 2 - 1)], mode.value.type)

    return img


def _draw_type_naval_hq(mode: IconMode) -> Image:
    return _add_hq(_draw_type_naval(mode), mode)


def _draw_type_antinavy(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = max(1, math.ceil(h / 7))
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)

    img_draw.rectangle([(g, g), (w - g - 1, g + th - 1)], mode.value.type)

    img_draw.rectangle([(d - math.ceil(th / 2), g + th + g), (d + math.ceil(th / 2) - 1, h - g - 1)], mode.value.type)

    return img


def _draw_type_intel(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = max(1, math.ceil(h / 7))
    th = max(1, math.ceil(h / 10))
    l1 = max(1, math.ceil((d - g) / 8))
    l3 = max(3, math.ceil((d - g) / 1.2))
    l2 = (l1 + l3) // 2

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(d - l3, g), (d + l3 - 1, g + th - 1)], mode.value.type)
    img_draw.rectangle([(d - l2, h // 2 - math.floor(th / 2)), (d + l2 - 1, h // 2 + math.ceil(th / 2) - 1)], mode.value.type)
    img_draw.rectangle([(d - l1, h - g - th), (d + l1 - 1, h - g - 1)], mode.value.type)

    return img


def _draw_type_counterintel(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = max(1, math.ceil(h / 7))
    th = max(1, math.ceil(h / 10))
    l1 = max(1, math.ceil((d - g) / 8))
    l3 = max(3, math.ceil((d - g) / 1.2))
    l2 = (l1 + l3) // 2

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(d - l1, h - g - th), (d + l1 - 1, h - g - 1)], mode.value.type)

    img_draw.rectangle([(d - l2, h // 2 - math.floor(th / 2)), (d - l2 + l1 * 2 - 1, h // 2 + math.ceil(th / 2) - 1)], mode.value.type)
    img_draw.rectangle([(d + l2 - l1 * 2, h // 2 - math.floor(th / 2)), (d + l2 - 1, h // 2 + math.ceil(th / 2) - 1)], mode.value.type)

    img_draw.rectangle([(d - l3, g), (d - l3 + l1 * 2 - 1, g + th - 1)], mode.value.type)
    img_draw.rectangle([(d - l1, g), (d + l1 - 1, g + th - 1)], mode.value.type)
    img_draw.rectangle([(d + l3 - l1 * 2, g), (d + l3 - 1, g + th - 1)], mode.value.type)

    return img


def _draw_type_land(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = max(1, math.ceil(h / 7))
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)

    for i in range(th):
        img_draw.line([(d - 1, g + i), (g + i, d - 1)], mode.value.type)
        img_draw.line([(d, g + i), (w - g - 1 - i, d - 1)], mode.value.type)
        img_draw.line([(g + i, d), (d - 1, h - g - i - 1)], mode.value.type)
        img_draw.line([(w - g - 1 - i, d), (d, h - g - i - 1)], mode.value.type)

    return img


def _draw_type_land_hq(mode: IconMode) -> Image:
    return _add_hq(_draw_type_land(mode), mode)


def _draw_type_directfire(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = math.ceil(h / 5 / 2)

    img_draw = ImageDraw.Draw(img)

    img_draw.rectangle([(d - 1, 1), (d, h // 2 - g - 1)], mode.value.type)
    img_draw.rectangle([(d - 1, h // 2 + g), (d, h - 2)], mode.value.type)

    img_draw.rectangle([(1, h // 2 - 1), (d - g - 1, h // 2)], mode.value.type)
    img_draw.rectangle([(d + g, h // 2 - 1), (w - 2, h // 2)], mode.value.type)

    return img


def _draw_type_mass(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = math.ceil(h / 12)
    th = max(1, math.ceil(h / 10))
    r = h // 3

    img_draw = ImageDraw.Draw(img)

    img_draw.arc([(g, g), (g + r * 2, g + r * 2)], 180, 270, mode.value.type, th)
    img_draw.arc([(w - g - 1 - r * 2, g), (w - g - 1, g + r * 2)], 270, 360, mode.value.type, th)

    img_draw.rectangle([(g + r, g), (w - g - 1 - r, g + th - 1)], mode.value.type)
    img_draw.rectangle([(g, g + r), (d - g - 1, g + r + th - 1)], mode.value.type)
    img_draw.rectangle([(d + g, g + r), (w - g - 1, g + r + th - 1)], mode.value.type)

    for y in range(h // 4):
        w = h // 4 - y - 1
        img_draw.line([(d - 1 - w, h - g - y - 1), (d + w, h - g - y - 1)], mode.value.type)

    return img


def _draw_type_energy(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = math.ceil(h / 12)
    th = max(1, math.ceil(h / 10))
    w2 = h // 4

    img_draw = ImageDraw.Draw(img)

    img_draw.rectangle([(d - w2 - 1, d - th // 2), (d + w2, d + th // 2 - 1)], mode.value.type)

    for of in range(th * 2):
        img_draw.line([(d + w2 - of, d - th // 2 - 1), (d - th + g - 1, 0)], mode.value.type)
        img_draw.line([(d - w2 + of - 1, d + th // 2), (d + th - g, h - 1)], mode.value.type)

    return img


def _draw_type_engineer(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    s = max(4, math.ceil(min(w, h) / 3))

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(1, h // 2 - 1 - s // 2), (w - 2, h // 2 - s // 2)], mode.value.type)

    img_draw.rectangle([(1, h // 2 - 1 - s // 2), (2, h // 2 + s // 2)], mode.value.type)
    img_draw.rectangle([(d - 1, h // 2 - 1 - s // 2), (d, h // 2 + s // 2)], mode.value.type)
    img_draw.rectangle([(w - 3, h // 2 - 1 - s // 2), (w - 2, h // 2 + s // 2)], mode.value.type)

    return img


def _draw_type_energy_storage(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = math.ceil(h / 12)
    th = max(1, math.ceil(h / 10))
    w2 = h // 4

    img_draw = ImageDraw.Draw(img)

    img_draw.rectangle([(d - th // 2, d - w2 - 1), (d + th // 2 - 1, d + w2)], mode.value.type)

    for of in range(th * 2):
        img_draw.line([(d - th // 2 - 1, d + w2 - of), (0, d - th + g - 1)], mode.value.type)
        img_draw.line([(d + th // 2, d - w2 + of - 1), (h - 1, d + th - g)], mode.value.type)

    return img


def _draw_type_shield(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = math.ceil(h / 12)
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)

    img_draw.arc([(g, g), (w - g - 1, h - g - 1)], 180, 360, mode.value.type, th)
    img_draw.rectangle([(d - th, h - 2 * g - th * 2), (d + th - 1, h - 2 * g - 1)], mode.value.type)

    return img


def _draw_type_antishield(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    g = math.ceil(h / 12)
    th = max(1, math.ceil(h / 10))

    img_draw = ImageDraw.Draw(img)

    img_draw.arc([(g, g), (w - g - 1, h - g - 1)], 180, 216, mode.value.type, th)
    img_draw.arc([(g, g), (w - g - 1, h - g - 1)], 258, 288, mode.value.type, th)
    img_draw.arc([(g, g), (w - g - 1, h - g - 1)], 324, 360, mode.value.type, th)
    img_draw.rectangle([(d - th, h - 2 * g - th * 2), (d + th - 1, h - 2 * g - 1)], mode.value.type)

    return img


def _draw_type_sniper(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(0, d - 1), (TYPE_SIZE - 1, d)], mode.value.type)

    return img


def _draw_type_transport(mode: IconMode) -> Image:
    w, h = TYPE_SIZE, TYPE_SIZE

    img = new("RGBA", (w, h), (0, 0, 0, 0))
    d = w // 2
    th = max(1, math.ceil(h / 10))
    g = math.ceil(h / 12)

    img_draw = ImageDraw.Draw(img)
    img_draw.rectangle([(g, h // 5), (w - g - 1, h // 5 + th - 1)], mode.value.type)
    img_draw.rectangle([(g, h // 5), (g + th - 1, h // 5 + h // 3)], mode.value.type)
    img_draw.rectangle([(w - g - th, h // 5), (w - g - 1, h // 5 + h // 3)], mode.value.type)

    img_draw.rectangle([(d - h // 8 - 1, d + g * 2 - h // 5), (d + h // 8, d + g * 2 + h // 5 - 1)], mode.value.type)

    return img


class UnitType(Enum):
    Generic = partial(_draw_type_generic)

    Air = partial(_draw_type_air)
    Antiair = partial(_draw_type_antiair)
    AirHq = partial(_draw_type_air_hq)

    Armored = partial(_draw_type_armored)

    Artillery = partial(_draw_type_artillery)
    Antiartillery = partial(_draw_type_antiartillery)

    Missile = partial(_draw_type_missile)
    Antimissile = partial(_draw_type_antimissile)

    Bomb = partial(_draw_type_bomb)

    Naval = partial(_draw_type_naval)
    Antinavy = partial(_draw_type_antinavy)
    NavalHq = partial(_draw_type_naval_hq)

    Intel = partial(_draw_type_intel)
    Counterintel = partial(_draw_type_counterintel)

    Land = partial(_draw_type_land)
    LandHq = partial(_draw_type_land_hq)

    DirectFire = partial(_draw_type_directfire)

    Mass = partial(_draw_type_mass)
    Energy = partial(_draw_type_energy)
    Engineer = partial(_draw_type_engineer)
    Energy_Storage = partial(_draw_type_energy_storage)

    Shield = partial(_draw_type_shield)
    Antishield = partial(_draw_type_antishield)

    Sniper = partial(_draw_type_sniper)
    Transport = partial(_draw_type_transport)

    @staticmethod
    def get_type_pic(type: UnitType, mode: IconMode) -> Image:
        if (type, mode) not in type_cache:
            img: Image = type.value(mode)
            # img.save(f'done_types\{type.name}-{mode.name}.png', 'png')
            type_cache[(type, mode)] = img

        return type_cache[(type, mode)]


def draw_type_icon(img: Image, mode: IconMode, type: UnitType, offset: int) -> Image:
    pic = type.get_type_pic(type, mode)
    img.alpha_composite(pic, (img.width // 2 - pic.width // 2, img.height // 2 - pic.height // 2 + offset))
