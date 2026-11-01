"""Write conf_theme.cfg for the Adapt themes (Adapt, Adapt Rx) from one layout, so the shared pieces -- the
frosted screen, the side bar, the info page -- stay in step. RIPGRID is built into RIPPS2 (since build 91, as
<RIPGRID>), so it is no longer written here.

Each conf_theme.cfg opens with its creation header, then the key glossary (docs/key_glossary.cfg: every key a
RIPPS2 theme can use), then the theme itself. Change EDITION_DATE and EDITION_BUILD when the themes change.

    python3 tools/gen_adapt_family.py

Layers, back to front, on the game list and the info page alike:
  Background (each game's art, widecrop in 16:9) -> a full-screen frosted layer (blur, low tint, no
  frame) -> the side bar (a dark frosted strip and a light rule, frameless) -> the framed glass panel
  under the text -> the art and text.

The whole info page (panel, logo, badges, text, screenshots) tips with the right stick as one plane about
the page's centre; the hint row and the backdrop hold still. Adapt's cover is RIPPS2's case (case +
case_overlay, its reflection below), tipping with the disc; on the game list the case shows the front
cover, then the back (COV2), crossfading as the info page's slideshow does (slide=1, 2). The info page
sits on the other side from the game list's text: Adapt's text right, Adapt Rx's left.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "themes")

EDITION_DATE = "11/01/2026"  # the date the RIPPS2 edition last changed: the theme pack's release date
EDITION_BUILD = 128          # the RIPPS2 build it was made and checked on
GLOSSARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "key_glossary.cfg")

RULE = "# " + "=" * 102
HEAD = RULE + """
# Theme Name: {name}
# Made by: akilluminati47
# Created: 8/27/2026 (Adapt, for RiptOPL)
# Updated: {date} (the RIPPS2 edition, made on RIPPS2 build {build}; needs RIPPS2 build 115 or later)
# Files: this one and SCR43.png (Adapt's screenshot frame cut to 4:3). Everything else is RIPPS2's own from build
#   115: the case (case, case_overlay: RiptOPL's), the glyphs (glyph_set=standard), the badges (badge_set=ripps2),
#   the busy mark (loading_mark=corner) and Adapt's fonts, Planet N Condensed by Iconian Fonts
#   (builtin:ripps2condensed, its a.ttf), Roboto Condensed (builtin:roboto at 700 and 400) and Planet N Compact
#   (builtin:ripps2). An edition before 115 shipped those as files.
# Look: each game's art under frosted glass (a full-screen Ripps2PanelGlass, blur=1), a frosted side bar on
#   the left, clear glass panels under the text, page morphs between the list and the info page, the pillars
#   behind Settings (no settings_bg), right-stick tilt on the art. Art eases in; no stock disc or case.
#   {side}
# Written by tools/gen_adapt_family.py (github.com/akilluminati47/RIPPS2-themes): change the layout there.
""" + RULE + """
#
{glossary}
#
# ---- THIS THEME: the global keys, then the elements ---------------------------------------------------
bg_color=#050A1C
sel_text_color=#0064FF
text_color=#FFFFFF
ui_text_color=#C4DAFF
towers=0
bg_blur=weak
source_name=pop
# RIPPS2 build 102: the Standard glyph set (L3 and R3 included), and the AUDIO folder's sounds (the ripped map)
# even where an older Adapt left a sound folder in the theme
glyph_set=standard
sounds=audio
# RIPPS2 build 113: the three categories, as the sidebar: their glyphs in the frosted bar on the left, a drawer
# opening out of it for each (Left on the list); RIPPS2 draws the bar on Launch Disc and Memory Files, this theme's
# main2 / main3 are the bar on Storage. Build 115: category_layout alone says it (a theme that says neither row nor
# sidebar gets the categories in the START menu, as a theme made for OPL)
category_layout=sidebar
sidebar_bar=always
# RIPPS2 build 115: a hint glyph that changes fades in, as the covers do (on is RIPPS2's default; said here so the key
# is in front of anyone making a theme from this one), and the sidebar as Adapt draws it: the dark bar and its strip
hints_fade=1
# edition 115 (the user, 10/26): the one-piece bar, RIPPS2's on every page
sidebar_style=one_piece
# RIPPS2 build 119: the sidebar stays on the info page (the user, 10/27: Adapt's info page leaves the bar its margin,
# in both themes); a theme without that room leaves the key out and the sidebar waits for Left there
info_sidebar=1
# edition 122 (the user, 10/28): the main page shows covers, no disc, so the game's disc comes in as it launches
# and zooms up to read clearly (RIPPS2 build 122; earlier builds pop it in); Flow and Grid > Launch Disc can change it
launch_disc=zoom
# RIPPS2 build 115: RIPPS2's own badges (RIPFLOW's set, with Players and the ESRB ratings), and its busy mark in the
# corner, so the theme ships no badge folders and no loading frames
badge_set=ripps2
loading_mark=corner
{fonts}"""

SIDES = {
    0: "Adapt: the case and disc left, under LAUNCH DISC, the list right; the info page's text right.",
    1: "Adapt Rx: the list left, the case and disc right, under LAUNCH DISC; the info page's text left.",
}

# Adapt's own type. Edition 114 (the font audit): Roboto Condensed Bold and Regular (b.ttf, c.ttf) are RIPPS2's built-in
# variable Roboto at 700 and 400, Planet N Compact (d.ttf) its built-in menu face. Edition 115: Planet N Condensed (a.ttf)
# is built in too (builtin:ripps2condensed), so the theme ships no font.
# The fonts RIPPS2 carries, for any theme: builtin:ripps2 (Planet N Compact, the menus), builtin:ripps2sleek,
# builtin:ripps2sleekbold, builtin:ripps2sleekcase (RIPPS2 Sleek: hints, bold, typed text), builtin:roboto (Roboto
# Condensed 3.015, variable: font<N>_weight 400 to 700), builtin:ripflow (it at 400), builtin:ripflowbold (at 700) and
# builtin:ripps2condensed (Planet N Condensed, build 115).
ADAPT_FONTS = """default_font=builtin:ripps2condensed
default_font_size=17
font1=builtin:roboto
font1_weight=700
font2=builtin:roboto
font2_weight=400
font3=builtin:ripps2
font4=builtin:roboto
font4_size=20
font4_weight=700
font15=builtin:ripps2sleekcase
font15_size=15
font6=builtin:ripps2sleekcase
font6_size=18
"""
# font15 (build 102): RIPPS2 Sleek Case, the hints' face on every page (the hint rows, the menus' hints, RIPPS2's own
# pages) as on RIPPS2's other themes; Adapt's own faces were hard to read that small. font6 (edition 115): the text
# beside a glyph on RIPPS2's own pages (START BROWSER, START LASER, the drawers' hints) in the same face
FROST_TINT, PANEL_TINT, BAR_TINT, RULE_TINT = 24, 44, 88, 22
INFO_TILT = dict(tilt=1, tilt_x=320, tilt_y=260, tilt_scale=75)  # the info page: one plane
BADGE = dict(width=46, height=23)  # edition 115: RIPPS2's 64 x 32 badges at Adapt's size


def case(w=143, h=201, **kv):
    """RIPPS2's case around the cover (143 x 201: true scale beside RIPPS2's 127 px disc), with its reflection (the
    built-in theme's own keys)."""
    return dict(kv, width=w, height=h, aligned=1, scaled=1, reflection=1, overlay="case", overlay2="case_overlay",
                overlay_ulx=0, overlay_uly=0, overlay_urx=w, overlay_ury=0,
                overlay_llx=0, overlay_lly=h, overlay_lrx=w, overlay_lry=h)


def square_case(side=160, **kv):
    """Build 102: an app's case, square as a PS1 game's (user: "apps cases should display as ps1 square by default").
    The app's Case Shape (its menu, Triangle) can make it a PS2 case."""
    return case(side, side, **kv)


# Build 102 (user: "adapt would look nicer if its disc and case were lined up lower instead of sitting proud above the
# other content, but I want them to have proportions to each other like in real life"): a 120 mm disc over a
# 135 x 190 mm case, as tall together as the list's glass (76 to 385) with 9 between: 0.97 px a millimetre, so the
# disc 116, the case 131 x 184. The disc's top is the glass's top, the case's foot the glass's foot. Up to edition
# 100 the disc (112, a size of its own) stood at 44, up by the category bar, over a 143 x 201 case.
GLASS_TOP, GLASS_BOTTOM = 76, 385
DISC, CASE_W, CASE_H, DISC_GAP = 116, 131, 184, 9
DISC_Y = GLASS_TOP + DISC // 2           # the disc's centre: 134
CASE_Y = GLASS_BOTTOM - CASE_H // 2      # the case's centre: 293
GROUP_Y = (GLASS_TOP + GLASS_BOTTOM) // 2  # the pair tips about its own middle


def block(name, **kv):
    out = [name + ":"]
    for k, v in kv.items():
        out.append("\t%s=%s" % (k, v))
    return "\n".join(out)


def backdrop(fam):
    """Background, the frosted screen, the side bar's strip and rule: indices 0-3 of main and info. The
    side bar is on the left in every theme of the family, Adapt Rx included (it mirrors the content)."""
    bar_x, rule_x = 0, 28  # the strip 0-26, the rule 28-40: content starts at x 40
    return [
        block(fam + "0", type="Background", pattern="BG", widecrop=1),
        block(fam + "1", type="Ripps2PanelGlass", aligned=0, x=0, y=0, width=640, height=480,
              blur=1, tint=FROST_TINT, frame=0),
        # edition 115: the side bar is RIPPS2's on every page (sidebar_bar=always), in the style picked (Layout > Sidebar
        # Style), and it stays through the list <-> info morph; the theme's own strip and rule (2, 3) stand down, kept as
        # numbers so the elements after them keep theirs
        block(fam + "2", type="Ripps2PanelGlass", enabled=0),
        block(fam + "3", type="Ripps2PanelGlass", enabled=0),
    ]


def screenshot(name, pattern, x, y):
    # 4:3: the SCR43 frame at 160 x 120 (its window 6,4 to 156,116); scaled=1 keeps it 4:3 on a 16:9 picture, as the
    # case is. Build 102: two of them stand flush with the text's glass (160 to 415), 15 apart (they were 170 x 128,
    # 6 above the glass and 11 below it)
    return block(name, type="GameImage", pattern=pattern, scaled=1, x=x, y=y, width=160, height=120, overlay="SCR43",
                 overlay_ulx=6, overlay_uly=4, overlay_urx=156, overlay_ury=4,
                 overlay_llx=6, overlay_lly=116, overlay_lrx=156, overlay_lry=116, **INFO_TILT)


def info(rx):
    # the text panel and the screenshots side by side, clear of the side bar. Rx swaps them, the side bar
    # staying left: screenshots 56-226 (16 px from the bar), glass 242-622 (16 px gap, 18 px to the edge)
    gw = 380 if rx else 395   # glass width
    gx = 242 if rx else 45    # glass left
    tw = gw - 20              # text width
    tx = gx + 10              # text left
    ax = gx + 15              # first attribute icon
    sx = 141 if rx else 540   # screenshots' centre: the middle of the room beside the glass (40-242, 440-640)
    els = backdrop("info") + [
        block("info4", type="Ripps2PanelGlass", aligned=0, x=gx, y=160, width=gw, height=255,
              blur=1, tint=PANEL_TINT, frame=1, **INFO_TILT),
        # build 102 (user: "the logos should not run into the info boxes on any theme, have them just above"): the
        # logo's box ends at 158, 2 above the glass (160), and valign=bottom stands its lowest visible row there,
        # however much clear space its image has round it
        block("info5", type="GameImage", pattern="LGO", x="POS_MID", y=95, aligned=1, width=300,
              height=125, valign="bottom", **INFO_TILT),
        # edition 115: RIPPS2's badges (badge_set=ripps2), 64 x 32 drawn at 46 x 23 on Adapt's 50 px pitch; default=
        # names RIPPS2's own no-stars picture. Edition 126 (the user, 10/31: "stars on info pages too small"): the stars
        # (256 x 32) at RIPFLOW's 143 x 18, their right end where it was (ax + 112, short of Players) and on the same
        # middle (188), so they grow to the left into the glass
        block("info6", type="AttributeImage", attribute="Rating", default="Rating_0", aligned=0, x=ax - 31, y=179,
              width=143, height=18, **INFO_TILT),
        block("info7", type="AttributeImage", attribute="Scan", aligned=0, x=ax + 172, y=176, **BADGE, **INFO_TILT),
        block("info8", type="AttributeImage", attribute="Players", aligned=0, x=ax + 122, y=176, **BADGE, **INFO_TILT),
        # line_height: a description longer than its box rolls through it instead of running on
        block("info9", type="AttributeText", attribute="Description", aligned=0, display=2, x=tx, y=210,
              width=tw, height=100, wrap=1, line_height=19, font=1, **INFO_TILT),
        block("info10", type="AttributeText", attribute="Developer", aligned=0, display=2, x=tx, y=330,
              width=tw, wrap=0, font=2, **INFO_TILT),
        block("info11", type="AttributeText", attribute="Release", aligned=0, display=2, x=tx, y=358,
              width=tw, font=3, **INFO_TILT),
        block("info12", type="AttributeText", attribute="Genre", display=2, aligned=0, x=tx, y=385,
              width=tw, font=2, **INFO_TILT),
        block("info13", type="InfoHintText", aligned=1, x="POS_MID", y=-41, font=15),
        # the screenshots flush with the glass (160 to 415), 15 apart, the lower one still clear of the hints
        screenshot("info14", "SCRn", sx, 220),  # build 108: every shot in turn, the lower box one shot later
        screenshot("info15", "SCRn", sx, 355),
        # the badge (54 px) 16 px inside the panel's right edge, whichever width the panel is
        block("info16", type="AttributeImage", attribute="Parental", aligned=0, scaled=1, x=gx + gw - 70, y=330, **INFO_TILT),
        block("info17", type="AttributeImage", attribute="Vmode", aligned=0, x=ax + 272, y=176, **BADGE, **INFO_TILT),
        block("info18", type="AttributeImage", attribute="Aspect", aligned=0, x=ax + 222, y=176, **BADGE, **INFO_TILT),
    ]
    # apps: the app's case in the screenshots' place (build 102: a PS1 square, centred on the glass), no screenshots
    apps = [
        block("appsInfo5", type="ItemCover", **square_case(x=sx, y=287, **INFO_TILT)),
        block("appsInfo14", type="GameImage", enabled=0),
        block("appsInfo15", type="GameImage", enabled=0),
    ]
    return els, apps


def common_tail(fam, start):
    return [
        block("%s%d" % (fam, start), type="LoadingIcon", x=-60, y=-31),
        block("%s%d" % (fam, start + 1), type="HintText", aligned=1, x="POS_MID", y=-41, font=15),
        block("%s%d" % (fam, start + 2), type="MenuText", x="POS_MID", y=25, aligned=1, width=225, font=2),
    ]


# RIPPS2's category bar: LAUNCH DISC, STORAGE, MEMORY FILES at these x (ripps2ui.c categoryX), labels at y 30
BAR_X = (128, 320, 512)


def adapt(rx):
    # The disc and its case sit right under LAUNCH DISC: Adapt's at the bar's left end (x 128); Rx puts
    # LAUNCH DISC at the right end (category_order=memory_files_first, build 81) and its disc under it
    # (x 512). The list glass takes the rest, 16 px from the bar's rule (x 40), from the case and from the
    # edge: Adapt 216-624, Rx 56-424.
    cx = BAR_X[2] if rx else BAR_X[0]  # cover and disc centre, under LAUNCH DISC
    gx = 56 if rx else 216    # list glass left
    gw = 368 if rx else 408   # list glass width
    lw = gw - 24              # the list inside the glass
    main = backdrop("main") + [
        block("main4", type="Ripps2PanelGlass", aligned=0, x=gx, y=GLASS_TOP, width=gw, height=GLASS_BOTTOM - GLASS_TOP,
              blur=1, tint=PANEL_TINT, frame=1),
        # the case: the front cover, then the back, crossfading (the slideshow; a game with no back
        # cover keeps its front). The front is the list's cover (COV), so it still loads first.
        block("main5", type="GameImage", pattern="COV", slide=1,
              **case(CASE_W, CASE_H, x=cx, y=CASE_Y, tilt=1, tilt_x=cx, tilt_y=GROUP_Y)),
        block("main6", type="GameImage", pattern="COV2", slide=2,
              **case(CASE_W, CASE_H, x=cx, y=CASE_Y, tilt=1, tilt_x=cx, tilt_y=GROUP_Y)),
        # the disc over its case, true to it (DISC above)
        block("main7", type="ItemIcon", aligned=1, scaled=1, x=cx, y=DISC_Y, width=DISC, height=DISC,
              tilt=1, tilt_x=cx, tilt_y=GROUP_Y),
        block("main8", type="ItemsList", x=gx + 12, y=88, aligned=0, width=lw, height=285, font=4, star="left"),
    ] + common_tail("main", 9)
    # apps (build 102: "adapts apps viewport needs to be refit"): the games' page, its glass and list (main4, main8:
    # under the category bar, where the apps' own wide glass from y 40 ran into it), with the app's case under LAUNCH
    # DISC, a PS1 square as wide as the games' case and standing where it stands (its foot on the glass's), no back
    # cover and no disc
    apps = [
        block("appsMain5", type="GameImage", pattern="COV",
              **square_case(CASE_W, x=cx, y=GLASS_BOTTOM - CASE_W // 2, tilt=1, tilt_x=cx, tilt_y=GROUP_Y)),
        block("appsMain6", type="GameImage", enabled=0),
        block("appsMain7", type="ItemIcon", enabled=0),
    ]
    return main, apps


def write(folder, name, rx, main, mainApps, infoEls, infoApps, extra=""):
    glossary = open(GLOSSARY, encoding="utf-8").read().rstrip("\n")
    for n, line in enumerate(glossary.split("\n"), 1):
        if line and not line.startswith("#"):
            raise SystemExit("docs/key_glossary.cfg line %d is not a comment: %r" % (n, line[:60]))
    text = HEAD.format(name=name, date=EDITION_DATE, build=EDITION_BUILD, side=SIDES[rx], glossary=glossary,
                       fonts=ADAPT_FONTS) + extra + "\n" + "\n".join(main + infoEls + mainApps + infoApps) + "\n"
    with open(os.path.join(ROOT, folder, "conf_theme.cfg"), "w", newline="\n") as f:
        f.write(text)
    print("wrote", folder)


if __name__ == "__main__":
    for folder, name, rx in (("thm_Adapt", "Adapt", 0), ("thm_Adapt Rx", "Adapt Rx", 1)):
        m, ma = adapt(rx)
        # the info page puts its text on the other side from the game list's: Adapt (list right) gets
        # text right and pictures left, Adapt Rx (list left) the reverse
        i, ia = info(1 - rx)
        # Rx: LAUNCH DISC at the bar's right end, over its disc (a default: the user's own order wins)
        extra = "category_order=memory_files_first\n" if rx else ""
        write(folder, name, rx, m, ma, i, ia, extra)
