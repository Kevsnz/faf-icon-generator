# Supreme Commander: Forged Allience Forever
# Strategic Icons Generator

This application generates strategic icons of configurable sizes for the game "[Supreme Commander: Forged Alliance Forever](faforever.com)".

Generated icons size can be changed with ICON_HEIGHT constant in sizes.py source file.

## Usage

Change icon size and run the application with command:

```bash
python main.py
```

Generated icons will be placed into **done_icons** (PNGs) and **done_ddss** (DDSs) directories. Resulting DDS files are ready to be put into the game mod.

## Requirements

Application has two required packages to be installed into system on virtual python environment:

- [pillow](https://pypi.org/project/Pillow/)
- [wand](https://pypi.org/project/Wand/)

These can be installed with the following command:

```bash
pip install -r requirements.txt
```

However, _Wand_ requires additional libraries. More on that can be found on the _Wand_ PyPI page.
