import math
import os
from PIL.Image import Image, new
from PIL import ImageDraw

import icon_mode as im
import shapes
import sizes
import unit_type as ut
from colors import COLOR_BG, COLOR_WHITE, COLOR_BLACK


tech_levels = [  # black, white
    [[-2, 1], [-1, 0]],  # 1
    [[-4, -1, 0, 3], [-3, -2, 1, 2]],  # 2
    [[-5, -2, 1, 4], [-4, -3, -1, 0, 2, 3]],  # 3
]


def save_dds(filename: str):
    from wand import image

    with image.Image(filename=os.path.join('done_icons', f'{filename}.png')) as img:
        img.format = 'DDS'
        img.compression = 'dxt5'
        img.save(filename=os.path.join('done_ddss', f'{filename}.dds'))


# Extend image so that it's dimensions are a multiple of 4
def bring_to_four(img: Image) -> Image:
    w, h = img.size
    w = int(math.ceil(w / 4)) * 4
    h = int(math.ceil(h / 4)) * 4
    new_img = new('RGBA', (w, h), (0, 0, 0, 0))
    new_img.paste(img, ((w - img.width) // 2, (h - img.height) // 2))
    return new_img


def draw_tech_level(img: Image, mode: im.IconMode, tech_level):
    if tech_level == 0:
        return
    tech_level -= 1

    # get image size
    w, h = img.size
    d = w // 2

    img_draw = ImageDraw.Draw(img)
    img_draw.line(
        [(d + tech_levels[tech_level][0][0], h - sizes.TECH_LEVEL_HEIGHT - 3), (d + tech_levels[tech_level][0][-1], h - sizes.TECH_LEVEL_HEIGHT - 3)],
        COLOR_BLACK,
    )
    img_draw.line(
        [(d + tech_levels[tech_level][0][0], h - 1), (d + tech_levels[tech_level][0][-1], h - 1)],
        COLOR_BLACK,
    )

    for x in tech_levels[tech_level][0]:
        img_draw.line([(d + x, h - 2), (d + x, h - sizes.TECH_LEVEL_HEIGHT - 2)], COLOR_BLACK)

    for x in tech_levels[tech_level][1]:
        img_draw.line([(d + x, h - 2), (d + x, h - sizes.TECH_LEVEL_HEIGHT - 2)], COLOR_WHITE)


def draw_icon(mode: im.IconMode, unit_shape: shapes.Shape, tech_level: int, unit_type: ut.UnitType):
    if tech_level == 0:
        img = new('RGBA', unit_shape.value.size, COLOR_BG)
    else:
        img = new('RGBA', (unit_shape.value.size[0], unit_shape.value.size[1] + sizes.TECH_LEVEL_HEIGHT * 2), COLOR_BG)

    # draw the icon
    icon = new('RGBA', unit_shape.value.size, COLOR_BG)
    shapes.draw_shape(icon, mode, unit_shape)
    ut.draw_type_icon(icon, mode, unit_type, unit_shape.value.offset)

    draw_tech_level(img, mode, tech_level)
    img.alpha_composite(icon, (0, 0 if tech_level == 0 else sizes.TECH_LEVEL_HEIGHT))

    img = bring_to_four(img)
    img.save(f'done_icons\\icon_{unit_shape.name}{tech_level if tech_level > 0 else ""}_{unit_type.name}_{mode.name}.png'.lower(), 'PNG')
    save_dds(f'icon_{unit_shape.name}{tech_level if tech_level > 0 else ""}_{unit_type.name}_{mode.name}'.lower())


def draw_experimental(mode: im.IconMode):
    img = new('RGBA', sizes.ICON_SIZE_EXPERIMENTAL, COLOR_BG)
    shapes.draw_experimental(img, mode)

    img = bring_to_four(img)
    img.save(f'done_icons\\icon_experimental_generic_{mode.name}.png'.lower(), 'PNG')
    save_dds(f'icon_experimental_generic_{mode.name}'.lower())


def draw_wall(mode: im.IconMode):
    img = new('RGBA', sizes.ICON_SIZE_WALL, COLOR_BG)
    shapes.draw_wall(img, mode)

    img = bring_to_four(img)
    img.save(f'done_icons\\icon_structure_wall_{mode.name}.png'.lower(), 'PNG')
    save_dds(f'icon_structure_wall_{mode.name}'.lower())


def draw_nuke():
    img = new('RGBA', sizes.ICON_SIZE_NUKE, COLOR_BG)
    shapes.draw_nuke(img)

    img = bring_to_four(img)
    img.save(f'done_icons\\icon_strategic_nuke.png'.lower(), 'PNG')
    save_dds(f'icon_strategic_nuke'.lower())


def draw_antinuke():
    img = new('RGBA', sizes.ICON_SIZE_ANTINUKE, COLOR_BG)
    shapes.draw_antinuke(img)

    img = bring_to_four(img)
    img.save(f'done_icons\\icon_strategic_antinuke.png'.lower(), 'PNG')
    save_dds(f'icon_strategic_antinuke'.lower())


def draw_commanders():
    for mode in (im.IconMode.Rest, im.IconMode.Over, im.IconMode.Selected, im.IconMode.SelectedOver):
        img = new('RGBA', sizes.ICON_SIZE_COMMANDER, COLOR_BG)
        shapes.draw_commander(img, mode)

        img = bring_to_four(img)
        img.save(f'done_icons\\icon_commander_generic_{mode.name}.png'.lower(), 'PNG')
        img.save(f'done_icons\\icon_subcommander_{mode.name}.png'.lower(), 'PNG')
        save_dds(f'icon_commander_generic_{mode.name}'.lower())
        save_dds(f'icon_subcommander_{mode.name}'.lower())


def main():
    os.makedirs('done_icons', exist_ok=True)
    os.makedirs('done_ddss', exist_ok=True)

    bombers = (
        ut.UnitType.Antinavy,
        ut.UnitType.DirectFire,
        ut.UnitType.Generic,
    )
    bots = (
        ut.UnitType.Antiair,
        ut.UnitType.Artillery,
        ut.UnitType.DirectFire,
        ut.UnitType.Engineer,
        ut.UnitType.Generic,
        ut.UnitType.Intel,
    )
    factories = (
        ut.UnitType.Air,
        ut.UnitType.Generic,
        ut.UnitType.Land,
        ut.UnitType.Naval,
    )
    fighters = (
        ut.UnitType.Antiair,
        ut.UnitType.Bomb,
        ut.UnitType.DirectFire,
        ut.UnitType.Generic,
        ut.UnitType.Intel,
        ut.UnitType.Missile,
    )
    gunships = (
        ut.UnitType.Antiair,
        ut.UnitType.DirectFire,
        ut.UnitType.Generic,
        ut.UnitType.Transport,
    )
    land = (
        ut.UnitType.Antiair,
        ut.UnitType.Antishield,
        ut.UnitType.Artillery,
        ut.UnitType.Bomb,
        ut.UnitType.Counterintel,
        ut.UnitType.DirectFire,
        ut.UnitType.Engineer,
        ut.UnitType.Generic,
        ut.UnitType.Intel,
        ut.UnitType.Missile,
        ut.UnitType.Shield,
    )
    ships = (
        ut.UnitType.Air,
        ut.UnitType.Antiair,
        ut.UnitType.Antinavy,
        ut.UnitType.Counterintel,
        ut.UnitType.DirectFire,
        ut.UnitType.Generic,
        ut.UnitType.Intel,
        ut.UnitType.Missile,
        ut.UnitType.Shield,
    )
    structures = (
        ut.UnitType.Air,
        ut.UnitType.Antiair,
        ut.UnitType.Antiartillery,
        ut.UnitType.Antimissile,
        ut.UnitType.Antinavy,
        ut.UnitType.Artillery,
        ut.UnitType.Counterintel,
        ut.UnitType.DirectFire,
        ut.UnitType.Energy,
        ut.UnitType.Engineer,
        ut.UnitType.Generic,
        ut.UnitType.Intel,
        ut.UnitType.Land,
        ut.UnitType.Mass,
        ut.UnitType.Missile,
        ut.UnitType.Naval,
        ut.UnitType.Shield,
        ut.UnitType.Transport,
    )
    subs = (
        ut.UnitType.Antinavy,
        ut.UnitType.DirectFire,
        ut.UnitType.Generic,
        ut.UnitType.Intel,
        ut.UnitType.Missile,
    )

    units = {
        shapes.Shape.Bomber: bombers,
        shapes.Shape.Bot: bots,
        shapes.Shape.Factory: factories,
        shapes.Shape.Fighter: fighters,
        shapes.Shape.Gunship: gunships,
        shapes.Shape.Land: land,
        shapes.Shape.Ship: ships,
        shapes.Shape.Structure: structures,
        shapes.Shape.Sub: subs,
    }

    tech_levels2draw = (0, 1, 2, 3)
    modes2draw = (
        im.IconMode.Rest,
        im.IconMode.Over,
        im.IconMode.Selected,
        im.IconMode.SelectedOver,
    )

    for mode in modes2draw:
        for tech_level in tech_levels2draw:
            for unit_shape, unit_types in units.items():
                for unit_type in unit_types:
                    draw_icon(mode, unit_shape, tech_level, unit_type)

        draw_icon(mode, shapes.Shape.Bot, 3, ut.UnitType.Armored)
        draw_icon(mode, shapes.Shape.Bot, 3, ut.UnitType.Sniper)
        draw_icon(mode, shapes.Shape.Land, 1, ut.UnitType.Sniper)
        draw_icon(mode, shapes.Shape.Structure, 0, ut.UnitType.Energy_Storage)

        for tech_level in (2, 3):
            draw_icon(mode, shapes.Shape.FactoryHq, tech_level, ut.UnitType.Air)
            draw_icon(mode, shapes.Shape.FactoryHq, tech_level, ut.UnitType.Land)
            draw_icon(mode, shapes.Shape.FactoryHq, tech_level, ut.UnitType.Naval)

        draw_experimental(mode)
        draw_wall(mode)

    draw_nuke()
    draw_antinuke()
    draw_commanders()


if __name__ == '__main__':
    print('Welcome!')
    main()
    print('Done!')
