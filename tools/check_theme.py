"""Check a RIPPS2 theme folder before it goes near a PS2.

    python3 tools/check_theme.py "themes/thm_Adapt"

Checks conf_theme.cfg the way RIPPS2's theme engine reads it (src/themes.c, RIPPS2 build 98):
- main and info are numbered 0, 1, 2... with no gap (the engine stops reading at the first missing
  number); every other family (appsMain, vcdInfo...) replaces its base family's element of the same
  number, so a number past the base family's last is never read;
- every element type is one the engine knows;
- every image the theme names (default=, overlay=, bg/attribute folders) and every font exists, or is one of
  RIPPS2's own (build 115: an image a theme names but does not ship is RIPPS2's of that name, unless use_default=0);
- RIPPS2 keys are where they work (blur/tint/tint_color/frame on Ripps2PanelGlass, columns/rows/spacing/back_pattern
  on Grid, widecrop on Background) and in range (tint 0-128, tint_color #RRGGBB);
- a Grid or Coverflow page also declares an ItemsList (hidden=1), else the engine adds a visible one;
- source_name, color_theme, category_bar, button_hints, dpad_glyphs, category_order, the hint, glyph, category
  bar and launch disc keys, page_buttons and a Grid's coverless hold values RIPPS2 knows;
- every PNG is an 8-bit palette PNG (a warning: RGBA ones cost four times the VRAM; tools/png8.py).
Exit code 1 on an error; warnings do not fail.
"""
import os
import re
import struct
import sys

# fonts compiled into RIPPS2 (src/fntsys.c): a theme names them as builtin:<name> and ships nothing
BUILTIN_FONTS = {"builtin:ripps2", "builtin:ripps2sleek", "builtin:ripps2sleekbold", "builtin:ripps2sleekcase",
                 "builtin:ripflow", "builtin:ripflowbold", "builtin:roboto",  # roboto: build 114, variable (weights)
                 "builtin:ripps2condensed"}  # build 115: Planet N Condensed (Adapt's list face)
# RIPPS2's own images (RiptOPL src/textures.c's table): from build 115 a theme may name one it does not ship
BUILTIN_IMAGES = set("""load0 load1 load2 load3 load4 load5 load6 load7 usb usb_bd ilk_bd m4s_bd hdd_bd mmce hdd eth udp_bd app Index_0 Index_1 Index_2 Index_3 Index_4 left right cross triangle circle square select start L3 R3 fav fav_mark cover disc screen coverapp missing no_Rating screens ELF HDL ISO VCD ZSO UL APP CD DVD Aspect_s Aspect_w Aspect_w1 Aspect_w2 Rating_0 Rating_1 Rating_2 Rating_3 Rating_4 Rating_5 Scan_240p Scan_240p1 Scan_480i Scan_480p Scan_480p1 Scan_480p2 Scan_480p3 Scan_480p4 Scan_480p5 Scan_576i Scan_576p Scan_720p Scan_1080i Scan_1080i2 Scan_1080p Vmode_multi Vmode_ntsc Vmode_pal logo logo0 logo1 logo2 logo3 logo4 logo5 logo6 case apps_case PS1 PS2 case_overlay udp_fs L1 R1 ripps2_glass ripps2_mark ripps2_mark_glow L2R2 ripps2_ps1logo ripps2_ps2logo ripps2_grid_icons ripps2_up ripps2_down hint_badge launch_disc ripps2_sidebar_icons Players_1 Players_2 Players_3 Players_4 Parental_3 Parental_10 Parental_17 Parental_18 Parental_e Parental_teen psbbn_bg ra_mark""".split())


def builtin_image(name):
    """RIPPS2 has this image: by its own name, or as a badge folder names it (rating/0_Rating is Rating_0)"""
    if name in BUILTIN_IMAGES:
        return True
    m = re.match(r"^[^/]+/(.+)_([A-Za-z]+)$", name)
    return bool(m) and ("%s_%s" % (m.group(2), m.group(1))) in BUILTIN_IMAGES

TYPES = {"AttributeText", "StaticText", "AttributeImage", "GameImage", "StaticImage", "Background", "MenuIcon",
         "MenuText", "ItemsList", "ItemIcon", "ItemCover", "ItemText", "HintText", "InfoHintText", "LoadingIcon",
         "BdmIndex", "GameCountText", "Coverflow", "Ripps2PanelGlass", "Grid",
         "PSBBNFlow", "SaveIcon"}  # build 103 (RiptOPL upstream 3cd7f89): PSBBN Flow's perspective fan, the save icon
FAMILIES = ["main", "info", "appsMain", "appsInfo", "favsMain", "favsInfo", "vcdMain", "vcdInfo", "favsVcdMain",
            "favsVcdInfo", "favsAppsMain", "favsAppsInfo"]
# main and info are read 0, 1, 2... until a number is missing; every other family replaces the element of
# the same number in its base family, and only numbers the base family has are read
BASE = {f: ("info" if f.endswith("Info") else "main") for f in FAMILIES if f not in ("main", "info")}
GRID_KEYS = {"columns", "rows", "spacing", "back_pattern"}
GLASS_KEYS = {"blur", "tint", "tint_color", "frame"}  # build 78-79
LIST_IMAGES = ("star_image", "decorator_all", "decorator_ps2", "decorator_ps1", "decorator_app")  # build 106
LIST_KEYS = {"star", "highlight"} | set(LIST_IMAGES)


def parse(path):
    glob, elems, cur = {}, {}, None
    for n, raw in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        line = raw.rstrip("\r\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z]+)(\d+):\s*$", line.strip())
        if m and not line.startswith(("\t", " ")):
            cur = (m.group(1), int(m.group(2)))
            elems.setdefault(cur, {"_line": n})
            continue
        if "=" in line:
            k, v = line.strip().split("=", 1)
            if line.startswith(("\t", " ")) and cur:
                elems[cur][k.strip()] = v.strip()
            else:
                glob[k.strip()] = v.strip()
                cur = None
    return glob, elems


def main(folder):
    cfg = os.path.join(folder, "conf_theme.cfg")
    errors, warnings = [], []
    if not os.path.isfile(cfg):
        print("ERROR no conf_theme.cfg in %s" % folder)
        return 1
    glob, elems = parse(cfg)

    def img(name):
        if any(os.path.isfile(os.path.join(folder, name + ext)) for ext in (".png", ".jpg", "")):
            return True
        return glob.get("use_default", "1") != "0" and builtin_image(name)  # build 115

    for k, v in glob.items():
        if (k == "default_font" or re.match(r"font\d+$", k)) and v.startswith("builtin:"):
            if v not in BUILTIN_FONTS:
                errors.append("font %s=%s: RIPPS2 has no such built-in font (%s)" % (k, v, ", ".join(sorted(BUILTIN_FONTS))))
            continue
        if (k == "default_font" or re.match(r"font\d+$", k)) and not os.path.isfile(os.path.join(folder, v)):
            errors.append("font %s=%s is missing" % (k, v))
    # Colors and More from the theme (build 81; source_name=pop since 80): each must be a value RIPPS2 knows
    CHOICES = {"source_name": ("pop", "shown", "fade", "hidden"), "category_bar": ("shown", "fade", "hidden"),
               "button_hints": ("shown", "fade", "hidden"),
               "dpad_glyphs": ("hidden", "shown", "fade_in", "fade_out", "guidance"),  # build 115: guidance
               "category_order": ("launch_disc_first", "memory_files_first"),
               "color_theme": ("ripps2", "ember", "blood", "ectoplasm", "amethyst", "bone",
                               "tangerine", "flamingo", "turquoise", "moonlight"),  # build 114's four
               # build 90: hints and glyphs; 91: the launch disc; 92: the category bar; 96: page buttons
               "hints_labels": ("1", "0", "badge"), "hints_layout": ("row", "column"),
               "glyph_set": ("theme", "ripps2", "standard", "white"), "launch_disc": ("pop", "spin", "zoom", "off"),
               "category_font": ("ripps2", "theme"),
               "category_layout": ("row", "column", "sidebar", "menu"),  # build 115: menu; unset is menu too
               "category_transition": ("none", "fade", "flash"), "page_buttons": ("l2r2", "l1r1"),
               "bg_blur": ("off", "weak", "normal", "strong"),  # build 98
               # build 113: the categories a theme shows and the sidebar's bar
               "categories": ("three", "storage"), "sidebar_bar": ("always", "pages", "never"),
               # build 115: the hint glyphs' fade-in, the sidebar's style
               "hints_fade": ("1", "0"), "sidebar_style": ("split", "one_piece"),
               # build 115: RIPPS2's badges, where its busy mark sits
               "badge_set": ("theme", "ripps2"), "loading_mark": ("corner", "center"),
               "sidebar_left": ("sidebar", "list"), "sidebar_hide": ("0", "1"),  # build 115: RIPFLOW's sidebar
               "hints_flank": ("0", "1"),  # build 115: OSDSYS-style hints
               "flowtilt": ("0", "1"),  # build 117: RIPFLOW's case tilt on Up / Down
               "info_sidebar": ("0", "1")}  # build 119: the info page leaves the sidebar its room
    for key, values in CHOICES.items():
        if key in glob and glob[key].lower() not in values:
            errors.append("%s=%s: one of %s" % (key, glob[key], ", ".join(values)))
    # build 115: category_layout alone says where the categories go; build 113's categories= still reads, but only
    # where category_layout is not set, and a theme that says neither shows them in the START menu
    if "categories" in glob:
        warnings.append("categories=%s: build 115 reads category_layout (row, sidebar or menu); %s" % (
            glob["categories"], "drop categories=" if "category_layout" in glob else
            "say category_layout=%s instead" % ("row" if glob["categories"].lower() == "three" else "menu")))
    elif "category_layout" not in glob:
        warnings.append("no category_layout: RIPPS2 shows the categories in the START menu (menu); say row or sidebar "
                        "for the bar")
    # build 113: the sidebar's place, its glass and its accent strip (the engine's own ranges)
    for key, lo, hi in (("sidebar_x", 0, 560), ("sidebar_width", 16, 80), ("sidebar_drawer", 120, 400)):
        if key in glob and not (glob[key].isdigit() and lo <= int(glob[key]) <= hi):
            errors.append("%s=%s: %d to %d pixels" % (key, glob[key], lo, hi))
    for key in ("sidebar_color", "sidebar_accent_color"):
        if key in glob and not re.match(r"^#[0-9A-Fa-f]{6}$", glob[key]):
            errors.append("%s=%s: #RRGGBB" % (key, glob[key]))
    for key in ("sidebar_tint", "sidebar_accent_tint"):
        if key in glob and not (glob[key].isdigit() and 0 <= int(glob[key]) <= 128):
            errors.append("%s=%s: 0-128" % (key, glob[key]))
    # build 115: the option names on STATUS and ACHIEVEMENTS, and the notifications, in a slot of the theme's own
    if "hints_flank_gap" in glob and not (glob["hints_flank_gap"].isdigit() and int(glob["hints_flank_gap"]) <= 200):
        errors.append("hints_flank_gap=%s: 0 to 200 pixels" % glob["hints_flank_gap"])
    for key in ("row_font", "notice_font", "message_font"):  # message_font: build 115
        if key in glob and not (glob[key].isdigit() and 0 <= int(glob[key]) <= 15):
            errors.append("%s=%s: a font slot, 0-15" % (key, glob[key]))
    if glob.get("use_settings_bg") == "1" and not img("settings_bg"):
        errors.append("use_settings_bg=1 but settings_bg.png is missing")

    for fam in FAMILIES:
        nums = sorted(i for f, i in elems if f == fam)
        if fam in BASE:
            base = len([1 for f, i in elems if f == BASE[fam]])
            for i in nums:
                if i >= base:
                    warnings.append("%s%d is never read: %s has only %d elements (0-%d)" % (fam, i, BASE[fam], base, base - 1))
        elif nums and nums != list(range(len(nums))):
            gap = next(i for i, n in enumerate(nums) if n != i)
            errors.append("%s: numbering breaks at %s%d (the engine stops reading there)" % (fam, fam, gap))
        types = []
        for i in nums:
            e = elems[(fam, i)]
            t = e.get("type")
            where = "%s%d (line %d)" % (fam, i, e["_line"])
            if t is None:
                if e.get("enabled") != "0":
                    warnings.append("%s has no type (it inherits main's element of that number)" % where)
                continue
            types.append(t)
            if t not in TYPES:
                errors.append("%s: unknown type %s" % (where, t))
            for key in ("default", "overlay", "overlay2"):
                if key in e and not img(e[key]):
                    errors.append("%s: %s=%s is missing" % (where, key, e[key]))
            if GLASS_KEYS & set(e) and t != "Ripps2PanelGlass":
                warnings.append("%s: blur/tint/tint_color/frame work only on Ripps2PanelGlass" % where)
            if "widecrop" in e and t != "Background":
                warnings.append("%s: widecrop works only on Background" % where)
            if "tint" in e and not (e["tint"].isdigit() and 0 <= int(e["tint"]) <= 128):
                errors.append("%s: tint is 0-128 (got %s)" % (where, e["tint"]))
            if "tint_color" in e and not re.match(r"^#[0-9A-Fa-f]{6}$", e["tint_color"]):
                errors.append("%s: tint_color is #RRGGBB (got %s)" % (where, e["tint_color"]))
            if t == "Grid" and "default" in e:
                warnings.append("%s: a Grid default= puts that picture on every game without art (build 79 shows a glass tile with the name)" % where)
            if LIST_KEYS & set(e) and t != "ItemsList":  # build 106
                warnings.append("%s: star/star_image/highlight/decorator_* work only on ItemsList" % where)
            if e.get("star", "left") not in ("left", "right", "hidden"):
                errors.append("%s: star is left, right or hidden (got %s)" % (where, e["star"]))
            if e.get("highlight", "bar") not in ("bar", "line", "none"):
                errors.append("%s: highlight is bar, line or none (got %s)" % (where, e["highlight"]))
            for key in LIST_IMAGES:
                if key in e and not img(e[key]):
                    errors.append("%s: %s=%s is missing" % (where, key, e[key]))
            if e.get("pattern") == "SCRn":  # build 108: every shot in turn
                if t != "GameImage":
                    warnings.append("%s: pattern=SCRn works only on GameImage (it shows nothing here)" % where)
            elif re.match(r"^SCR\d+$", e.get("pattern", "")) and int(e["pattern"][3:]) > 2:
                warnings.append("%s: pattern=%s shows that one shot; pattern=SCRn (build 108) shows them all in turn" % (where, e["pattern"]))
            if GRID_KEYS & set(e) and t != "Grid":
                warnings.append("%s: columns/rows/spacing/back_pattern work only on Grid" % where)
            if t == "Grid":
                c, r = int(e.get("columns", 4)), int(e.get("rows", 2))
                if not (1 <= c <= 8 and 1 <= r <= 4):
                    errors.append("%s: columns 1-8 and rows 1-4 (got %d x %d)" % (where, c, r))
                if "back_pattern" in e and not re.match(r"^(0|[A-Za-z0-9]+)$", e["back_pattern"]):
                    errors.append("%s: back_pattern is an art suffix such as COV2 or SCR, or 0 (got %s)" % (where, e["back_pattern"]))
                if e.get("coverless", "title") not in ("title", "serial"):  # build 92
                    errors.append("%s: coverless is title or serial (got %s)" % (where, e["coverless"]))
        scrn = [i for i in nums if elems[(fam, i)].get("pattern") == "SCRn"]
        if len(scrn) > 4:  # build 108: four SCRn boxes show their own shots; the rest show their default
            warnings.append("%s: %d SCRn boxes; only the first four show shots" % (fam, len(scrn)))
        if fam in ("main", "appsMain") and ({"Grid", "Coverflow"} & set(types)) and "ItemsList" not in types:
            errors.append("%s: a Grid/Coverflow page needs an ItemsList (hidden=1), else a visible default list is added" % fam)

    for root, _, files in os.walk(folder):  # RIPPS2 keeps 8-bit palette PNGs as 8-bit textures
        for name in sorted(files):
            if name.lower().endswith(".png"):
                with open(os.path.join(root, name), "rb") as fh:
                    head = fh.read(26)
                if len(head) == 26 and (head[25], head[24]) != (3, 8):  # colour type 3 (palette), 8-bit
                    warnings.append("%s is not an 8-bit palette PNG (4x the VRAM; tools/png8.py converts it)"
                                    % os.path.relpath(os.path.join(root, name), folder))

    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print("%s: %d error(s), %d warning(s)" % (folder, len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    folders = [f for f in sys.argv[1:] if os.path.isdir(f)]
    sys.exit(max(main(f) for f in folders) if folders else 2)
