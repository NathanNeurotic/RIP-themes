# What a RIPPS2 theme can do (build 117)

*Updated 10/26/2026. Every key below, one line each, is in [key_glossary.cfg](key_glossary.cfg): `#` comments ready
to sit at the top of a `conf_theme.cfg`, as they do in Adapt and Adapt Rx. RIPGRID and RIPFLOW are built into RIPPS2.*

A RIPPS2 theme is a folder, `THM/thm_<Name>/`, on any drive RIPPS2 reads (USB, HDD, MMCE, a memory
card's `OPL/THM`). Everything on this page is driven from that folder: `conf_theme.cfg`, its images,
fonts and sounds. **Nothing here needs RIPPS2 rebuilt.** Make the folder, copy it, pick it.

RIPPS2 reads OPL / RiptOPL themes, so everything in [THEME_ENGINE_RiptOPL.md](THEME_ENGINE_RiptOPL.md)
works too (element blocks, families, attributes, Coverflow). This page is what RIPPS2 adds on top, and
how RIPPS2's own pages meet a theme. The build each key arrived in is given; an older build ignores a
key it does not know, so a theme stays usable on it.

**Contents:** [the folder](#the-folder) · [coordinates](#coordinates) · [global keys](#global-keys) ·
[Colors and More from the theme](#colors-and-more-from-the-theme-build-81) ·
[hints and glyphs](#hints-and-glyphs-build-90) · [fonts](#fonts) ·
[element types](#element-types-ripps2-adds) · [keys on existing elements](#keys-ripps2-adds-to-existing-elements) ·
[effects and tricks](#effects-and-tricks) · [replacing RIPPS2's own images](#replacing-ripps2s-own-images) ·
[sounds and music](#sounds-and-music) · [what every theme gets](#what-every-theme-gets) ·
[what a theme cannot change](#what-a-theme-cannot-change-yet)

## The folder

| File | What it is |
|---|---|
| `conf_theme.cfg` | The layout and the keys below. Plain `key=value`; element blocks are `main0:` and indented keys. |
| `*.png` | Images. **8-bit palette PNGs**: RIPPS2 keeps those as 8-bit textures with a 32-bit palette (alpha included), a quarter of the VRAM of RGBA and quicker to load. `tools/png8.py` converts. 640x480 for full-screen pieces. |
| `*.ttf` | Fonts, named in the font keys. |
| *(nothing else)* | Build 115: a theme can be `conf_theme.cfg` alone, or with its own pictures. An image it names but leaves out is RIPPS2's own of that name (see [a theme of two files](#a-theme-of-two-files-build-115)). Adapt and Adapt Rx are `conf_theme.cfg` and `SCR43.png`. |
| `sound/*.adp` | The theme's sounds, by event (see [sounds](#sounds-and-music)). |
| `sound/bgm.ogg` | The theme's music. |
| `<name>.png` | Any of RIPPS2's own images, replaced by name (see [replacing](#replacing-ripps2s-own-images)). |

## Coordinates
RIPPS2 lays out in a 640x480 space, scaled to the video mode (720p and 1080i included, build 75).
`x` / `y` count from the left / top; a negative value counts from the right / bottom. `POS_MID` is the
centre. `aligned=1` (the default for most elements) centres the element on `x`,`y`; `aligned=0` makes
`x`,`y` its top-left corner. `scaled=1` narrows width for 16:9 so shapes stay true (covers, cases,
screenshots).

## Global keys

| Key | Values | Build | What it does |
|---|---|---|---|
| `bg_color` | `#RRGGBB` | OPL | The page colour behind everything (shows where there is no art and `towers=0`). |
| `text_color`, `ui_text_color`, `sel_text_color`, `title_color` | `#RRGGBB` | OPL | Text, menu text, the selection (also the Grid's glow), titles. |
| `default_font`, `font1` ... `font15` | a `.ttf` in the folder, or a `builtin:` font | OPL / 59 | The 16 font slots. See [fonts](#fonts). |
| `<font>_size` | pixels | OPL | `font4_size=20`. |
| `<font>_caps` | `0` / `1` | 70 | `1`: that font draws in capitals. |
| `towers` | `0` / `1` (default 1) | 78 | `0`: the game pages never show RIPPS2's pillars. Where a page has no image (a game without art, or art still fading in) `bg_color` shows instead. Settings keep the pillars behind glass unless the theme ships `settings_bg`. |
| `bg_blur` | `off`, `weak`, `normal`, `strong` (default strong) | 98 | How hard frosted glass (`Ripps2PanelGlass` with `blur=1`) blurs the game's art: the blurred copy is laid over the sharp art at 0, 33, 66 or 100 %. A theme default: Artwork settings > Background Blur overrides it. RIPGRID and Adapt use `weak`. |
| `source_name` | `pop`, `shown`, `fade`, `hidden` | 80 / 81 | How the source's name (ALL GAMES, HDD GAMES...) appears. `pop` (build 81): not drawn over the list, it plays as a toast in the middle of the page, the whole name in big capitals, on the first list after boot, on a source change and on coming back to Storage, then fades. `shown` / `fade` (with the category bar's idle fade) / `hidden` (build 81). A theme default: [the user wins](#colors-and-more-from-the-theme-build-81). |
| `source_name_sidebar` | `pop`, `pop_name` | 136 | The Source Name while the sidebar is on (Category Layout: Sidebar, or a sidebar theme). `pop_name`: the toast and the name over the list too. Adapt, Adapt Rx and RIPGRID: `source_name=pop` with the categories across the top, `source_name_sidebar=pop_name` with the sidebar. A theme default: the user wins. |
| `use_settings_bg` | `0` / `1` | OPL | `1` + `settings_bg.png`: Settings over that picture. Leave it out for the pillars behind RIPPS2's glass page panel. |
| `use_default` | `0` / `1` (default 1) | OPL | `0`: an image the theme does not ship stays empty instead of falling back to RIPPS2's own (build 115: images named in `default=` and `overlay=` too). |
| `badge_set` | `theme` (default), `ripps2` | 115 | `ripps2`: the info page's badges are RIPPS2's own (RIPFLOW's set, with Players and the ESRB ratings added), so the theme ships no badge folders. Hints and Glyphs > Badge Set overrides it on any theme. |
| `loading_mark` | `corner`, `center` (default: the `LoadingIcon` element's place) | 115 | Where RIPPS2's busy mark (the PS2 logo) sits: the bottom-right corner (544, 426) or centred over the hints (320, 426). The theme's `load0`...`load7` are not drawn. |
| `message_font` | a font slot, `0` to `15` | 115 | Every message box and wait screen. Unset: the built-in Roboto Condensed at 400, in the text's own case (Text Weight does not change it). |
| `coverflow_cover_offset` | pixels | RiptOPL | Coverflow's cover offset (see the engine reference). |

## Colors and More from the theme (build 81)

Colors and More (Settings > Interface) is the user's: colour theme, category bar, hints, D-pad glyphs,
category order, source name. A theme can choose its own for each, so it arrives looking the way it was
made:

| Key | Values | The Colors and More row |
|---|---|---|
| `color_theme` | `ripps2`, `ember`, `blood`, `ectoplasm`, `amethyst`, `bone`, and from build 114 `tangerine`, `flamingo`, `turquoise`, `moonlight` | Color Theme: one colour matrix over everything RIPPS2 draws itself (towers, orbs, glass, its pages). Greys and art never change, only the blues move. |
| `category_bar` | `shown`, `fade`, `hidden` | LAUNCH DISC, STORAGE, MEMORY FILES along the top. `fade`: fades after 6 s idle, back on a press. |
| `button_hints` | `shown`, `fade`, `hidden` | The button hints along the bottom of the three tabs. |
| `dpad_glyphs` | `hidden`, `shown`, `fade_in`, `fade_out`, `guidance` | The D-pad glyphs beside a drive's name. Build 115: `guidance` brings them in after 4.2 s with no press (and, on RIPFLOW in sidebar mode, L1/R1 beside the centre cover). |
| `hints_fade` | `1` (default), `0` | Build 115: a hint glyph that changes fades in, as the covers do; one that stays is left alone. Settings > Interface > Layout > Hints and Glyphs Fade overrides it. |
| `category_order` | `launch_disc_first`, `memory_files_first` | Which end of the bar Memory Files sits. RIPFLOW uses `memory_files_first`. |
| `source_name` | `pop`, `shown`, `fade`, `hidden` | Source Name (above). |
| `page_buttons` | `l2r2`, `l1r1` (default: none) | Build 96: which shoulder buttons turn the game list's pages. `l2r2`: L2 / R2 turn pages and L1 / R1 switch categories; `l1r1` the other way round. Without it L2 goes to the top and R2 to the end. Controller Settings > Page Buttons overrides it. RIPGRID uses `l2r2`. |

**The user always wins.** RIPPS2 remembers which of these rows the user has changed (saved as
`ripps2_userset`). A theme's value shows only on a row the user has never touched that still holds its
own default; anything the user picks, the default included, stays theirs on every theme. Colors and More
shows what is in effect, so the user sees the theme's choice and can change it.

## Hints and glyphs (build 90)

The hint bar and the button glyphs. Each key is the theme's default for a row of Controller Settings >
Hints and Glyphs, where every row starts on **Theme** (this key) and anything else the user picks wins.

| Key | Values | What it does |
|---|---|---|
| `hints_hide` | hint names, comma separated | Leaves those hints off the bar. The buttons still work. |
| `hints_order` | hint names, comma separated | The hints named come first, in that order; the rest follow in the order the page adds them. |
| `hints_labels` | `1` (default), `0`, `badge` | `0`: glyphs only, for glyph art that carries its own words (a hint whose glyph the theme lacks keeps its label). `badge`: each hint is one badge, its glyph and title together on a pill (`hint_badge.png`, or the glyph set's own), the pill's ends kept round and its middle stretched to the title. Never on unless a theme sets it or the user picks Badges. |
| `hints_layout` | `row` (default), `column` | `column`: one hint a line, from the hint element's `x`/`y` down. A column that would run off the bottom ends on the bar's line instead, so the default hint element gives a column in the bottom left corner. |
| `hints_spacing` | 12 to 96 (default 28) | A column's line pitch. |
| `hints_flank` | `0` (default), `1` | Build 115, OSDSYS style: the confirm button's RUN stands left of the source name (a centred `MenuText`, e.g. `x=POS_MID`, `aligned=1`) and the cancel button's SOURCE right of it, and the hint row leaves the two out. `hints_flank_gap` (0 to 200, default 18) is the room between the name and each hint. RIPFLOW sets it. With the categories as the sidebar the two go back to the hint row. |
| `<name>_sidebar_font` (on a `MenuText`) | a font slot, `0` to `15` | Build 136: the face the source name is drawn in while the sidebar is on (RIPGRID: Planet N, `font9=builtin:ripps2`). Unset: the element's own `font`. With the categories across the top, a `MenuText` set in their row (y above the PS2 mark) is drawn just below the mark instead. |
| `glyph_set` | `theme` (default), `ripps2`, `standard`, `white` | The glyphs on every page. `theme` is the theme's own PNGs (below); `ripps2` is RIPPS2's outlined set; `standard` is the Adapt theme's dark glossy buttons; `white` is the Grunge theme's solid white. The built-in sets cover every glyph, the shoulder buttons, sticks and D-pad included. |

Hint names: `menu` `run` `info` `options` `refresh` `star` `view` `source` (`source` is Coverflow and
Grid's source cycling). Their buttons name them too: `start` `select` `r3` `l3` `cross` `circle` `square`
`triangle`. For example, a sidebar theme:

```
hints_layout=column
hints_spacing=30
hints_order=run,info,options
hints_hide=refresh
```

## The category bar (build 92)

LAUNCH DISC, STORAGE and MEMORY FILES are drawn in RIPPS2's own face on every theme, so they look alike
everywhere. A theme can change that, move them, and reword them:

| Key | Values | What it does |
|---|---|---|
| `category_font` | `ripps2` (default), `theme` | `theme`: the bar uses the theme's font2 (the current category) and font7 (the others). |
| `category_layout` | `row`, `sidebar`, `menu` (default) | Build 115: the one key for where the three categories go, and **a theme must say `row` or `sidebar` to have them**. `row`: their names across the top. `sidebar` (build 113): glyphs down a bar on the left; Left on a list (the cancel button on Launch Disc and Memory Files) focuses them, Up / Down opens each one's drawer with its name first (Storage's lists the sources), Cross enters it and Cross on an item goes there; no page titles. `menu` (or no key, as a theme made for OPL): no bar, Storage alone, Launch Disc and Memory Files in the START menu (backing out of either returns to Storage), L1 / R1 turn the list's pages. Layout > Category Layout overrides it. `column` means `sidebar`. Build 113's `categories=three` / `storage` still reads as `row` / `menu` where `category_layout` is not set. |
| `category_x`, `category_y` | 0 to 640, 0 to 480 | A column's left edge and first line (40, 140). In a row, `category_y` moves the bar down (30). |
| `category_spacing` | 12 to 120 | A column's line pitch (34). |
| `category_label_launch`, `category_label_storage`, `category_label_files` | text | The words on the bar (RIPPS2's if not set). |
| `category_transition` | `none`, `fade`, `flash` | How a new page comes in as the category changes: from the theme's `bg_color`, or out of a flash. Colors and More > Page Transition overrides it. |

### Where the row and the sidebar sit (measurements)

Lay a theme out around these, in the 640 x 480 space:

| | Row (`category_layout=row`) | Sidebar (`category_layout=sidebar`) |
|---|---|---|
| Where | Across the top | Down the left edge, the whole height |
| Pieces | The three names centred at x **128, 320, 512** (192 apart), on **y 30** (`category_y` moves the line); the PS2 mark under the lit one at **y 53**, 96 x 20 | The bar at `sidebar_x` (**0**), `sidebar_width` wide (**26**), its accent strip **14** more; three glyphs, `sidebar_width` - 8 square (**18**; 14 to 28), centred in the bar, the middle one at **y 240**, a glyph and **22** px apart |
| Room a name gets | **184** px; a wider name (FICHIERS MÉMOIRE) is drawn at 15, 13 or 12 px | The drawer, out to `sidebar_drawer` (**216**), **26** px rows |
| Keep the theme's own content | Below **y 70** (Adapt's glass starts at 76) | Right of **x 40** (`sidebar_x` + `sidebar_width` + 14) |
| Moves with | `category_y`, `category_font`, `category_label_*` | `sidebar_x`, `sidebar_width`, `sidebar_drawer`, `sidebar_style` |

### The sidebar's bar (build 113)

With `category_layout=sidebar` the glyphs sit in a bar on the left, Adapt's by default (its `main2` and `main3`
frosted panels), and the drawer opens out of it, frosted on Storage like the bar.

| Key | Values | What it does |
|---|---|---|
| `sidebar_x`, `sidebar_width` | 0 to 560, 16 to 80 | The bar the glyphs sit in (0, 26). |
| `sidebar_drawer` | 120 to 400 | The drawer's right edge (216). |
| `sidebar_bar` | `always` (default), `pages`, `never` | Where RIPPS2 draws the bar: every page, every page but Storage (the theme draws its own there, as Adapt does), or nowhere. |
| `sidebar_left` | `sidebar` (default), `list` | Build 115: `list` keeps Left / Right and L1 / R1 the list's while the categories are the sidebar (RIPFLOW keeps its covers on them); Circle brings the sidebar out. |
| `sidebar_hide` | `0` (default), `1` | Build 115: `1` keeps the sidebar out of sight, sliding out when Circle calls it and away when it is done. RIPFLOW sets both. |
| `sidebar_style` | `split` (default), `one_piece` | Build 115: the glyphs in the dark bar with the accent strip beside it, or one bar of the same overall width with the glyphs in its middle. Layout > Sidebar Style overrides it. |
| `flowtilt` | `0` (default), `1` | Build 117: on a coverflow theme with the categories as the sidebar, Up / Down (and the left stick) tip the centre case back and forth instead of changing the source; the sources are the sidebar's (Circle). RIPFLOW sets it. |
| `info_sidebar` | `0` (default), `1` | Build 119, the newest key: with the categories as the sidebar, the info page is the game's. By default the sidebar is out of sight there until Left brings it out; Circle or Right put it away and the page stays, Up / Down step the games, and Circle with it away goes back to the list. `1` draws it on the info page all the time, for a theme whose info page leaves it room on the left. No built-in theme sets it; Adapt and Adapt Rx do (their info pages leave the bar its margin). |

Build 117: with the categories as the sidebar, every theme's keys are alike, a theme made for OPL included (Layout > Category Layout > Sidebar). Circle opens the sidebar on every page, and Left on a list; Right steps no source. L1 / R1 are the theme's own: a list's pages as OPL turns them (unless `page_buttons=l2r2` gives the pages to L2 / R2), RIPFLOW's covers. RIPFLOW and RIPGRID walk their covers on Left / Right, round their ends, and never open the sidebar with Left. Launch Disc and the info page leave L1 / R1 alone; Memory Files turns its orbs with them. The RIPDISC and theme boxes start flush with the sidebar's bar, and the sidebar is drawn over everything on the page.
| `row_font`, `notice_font` | a font slot, `0` to `15` | Build 115: the slot STATUS's and ACHIEVEMENTS' option names, and every notification, are drawn in. Unset: the Settings rows' Roboto, and the built-in Roboto Condensed Bold. |
| `sidebar_color`, `sidebar_tint` | `#RRGGBB`, 0 to 128 | The bar's glass (`#01040F`, 88). The drawer's is deeper. |
| `sidebar_accent_color`, `sidebar_accent_tint` | `#RRGGBB`, 0 to 128 | The strip beside the bar (`#28C5F9`, 22); tint 0 draws none. |

## The Grid's extras (build 92)

On a `Grid` element (`main4` below stands for its name):

From build 97 Right on a row's last cover turns to the next page (Left on its first, back), instead of wrapping to the next row; the chosen case turns over to its back cover on a 0.42 s hold of the right stick (RIPFLOW's centre cover too), and the grid is centred on its `x`.

| Key | Values | What it does |
|---|---|---|
| `coverless` | `title` (default), `serial` | `serial`: a game with no cover shows only its serial (SLUS-20482) on its case, in the in-game menu's pixel font, one line or two, as large as fits. |
| `title` | `0` (default), `1` | The chosen game's name on a line of its own under the grid; the highlight stays on the case. |
| `title_y` | 0 to 480 | That line (418). |
| `title_font` | a font slot | Its face (0). RIPGRID uses RIPPS2 Sleek Bold at 22 (font7) from build 97. |
| `wide_columns`, `wide_rows`, `wide_width`, `wide_height`, `wide_spacing` | as their standard keys | Build 98: the page on a 16:9 picture only (widescreen, 720p, 1080i), where a cover draws at three quarters of its width so more fit across; each key left out keeps the standard value. Flow and Grid > Widescreen Grid Layout can override it (Same as Grid Layout, 6 x 2, 7 x 2, 5 x 2 Large, 8 x 3 Compact). RIPGRID uses `wide_columns=6`. |

## The launch disc (build 91)

| Key | Values | What it does |
|---|---|---|
| `launch_disc` | `pop`, `spin`, `zoom`, `off` (default: `pop` from RIPPS2 build 122, none before) | As a game launches, its disc comes in over the middle of the screen: the game's ICO art, else `launch_disc.png` (yours, or RIPPS2's disc). `pop` settles in like the L3 logos and fades; `spin` settles in, then turns faster and faster and never fades; `zoom` (build 122) settles in, then grows smoothly to read clearly and stays. The user can override it in Flow and Grid > Launch Disc. RIPGRID and the default theme use `spin`, RIPFLOW, Adapt and Adapt Rx `zoom`. |

## Fonts

A theme has 16 font slots: `default_font` (slot 0) and `font1` to `font15`, each a `.ttf` in the folder
or one of RIPPS2's built-in faces:

| `builtin:` | Face |
|---|---|
| `builtin:ripps2` | RIPPS2's text face (the built-in theme's default) |
| `builtin:ripps2sleek` | RIPPS2 Sleek: hints, menus, settings |
| `builtin:ripps2sleekbold` | its bold weight: text beside big glyphs, the view word |
| `builtin:ripps2sleekcase` | bold with a true lowercase: typed text, tooltips |
| `builtin:ripflow` | Roboto Condensed (RIPFLOW's text; from build 114 the variable Roboto at 400) |
| `builtin:ripflowbold` | Roboto Bold Condensed (RIPFLOW's menus; from build 114 the variable Roboto at 700) |
| `builtin:roboto` | build 114: Roboto Condensed 3.015, variable, drawn at the slot's `font<N>_weight` |
| `builtin:ripps2condensed` | build 115: Planet N Condensed (Iconian Fonts), Adapt's list face |

**`font1_weight` ... `font15_weight`** (and `default_font_weight`), build 114: the weight a slot is drawn at, 100 to 900.
`builtin:roboto` is variable from 400 to 700; any other face is grown to the weight asked. Adapt and Adapt Rx (edition
114) use `builtin:roboto` at 700 and 400 and `builtin:ripps2` in place of their own b.ttf, c.ttf and d.ttf; a build
before 114 draws those slots in its default font.

Elements pick a slot with `font=<n>`. RIPPS2's own pages (menus, the category bar, Memory Files, the CD
player...) draw in fixed slots too, so **setting these restyles RIPPS2 itself**. A slot a theme leaves
out falls back to its `default_font`.

| Slot | RIPPS2 draws with it |
|---|---|
| `font2` | the selected category on the bar |
| `font3` | Launch Disc's line about the disc in the drive |
| `font4` | menus and message boxes (RIPPS2's UI font). From build 96 Settings and its dialogs read in one plain face on every theme (Roboto Condensed Bold 19, tooltips Roboto Condensed 16), whatever the theme sets. |
| `font5` | small text: About, the CD player's details |
| `font6` | text beside a button glyph (the START prompts) |
| `font7` | the other categories on the bar |
| `font8` | rows in Memory Files and the CD player's track list |
| `font9` | a title in true case (RetroAchievements) |
| `font10` | About's small print |
| `font11` | the CD player's track title |
| `font14` | the Achievements page's big numbers. A theme without `font14` gets RIPPS2 Sleek Bold at 64 px here (build 81; `font14_size` still sets it), not its default font. (Up to build 80 it also drew L3's view word; from build 81 L3's ALL / PS1 / PS2 and the Pop In toast draw in RIPPS2 Sleek Bold 64 on every theme, so they move the same everywhere.) |
| `font15` | typed text and tooltips, in true lowercase |

## Element types RIPPS2 adds

### `Ripps2PanelGlass` (build 55; blur in 78; tint, tint_color, frame in 79)
A glass panel: by default a navy tint, light at the top and deepening from about a third down, with a
thin frame. Put it after the backdrop and before the text it sits under. With `tint=` it is clear glass
instead: one even tint over the whole panel.

| Key | Values | Build | What it does |
|---|---|---|---|
| `x`,`y`,`width`,`height`,`aligned` | | 55 | The panel's rectangle. |
| `blur` | `0` / `1` | 78 | Frosted glass: what is behind shows through softened. The source is the page's `Background` (the game's own art once loaded, else the theme's `default=`) shrunk to 80x60 and drawn stretched with bilinear filtering, made again only when the game or its art changes. Cheap enough for every page. |
| `tint` | 0-128 | 79 | One constant tint instead of the gradient (128 opaque; 20-50 reads as glass). |
| `tint_color` | `#RRGGBB` (default `#040C2E`) | 79 | The tint's colour. Dark and high makes a strip (Adapt's side bar); light and low a highlight rule. |
| `frame` | `0` / `1` (default 1) | 79 | The thin frame line. `0` for layers that are not panels. |
| `tilt*` | | 70 | Right-stick tilt (below). |

### `Grid` (build 78)
The game list as a page of covers in rows, backed by the cover art (`COV`).

| Key | Default | What it does |
|---|---|---|
| `x` | `POS_MID` | The grid's horizontal centre. |
| `y` | 60 | The top of the first row. |
| `width`,`height` | 104 x 146 | One cover. |
| `columns` | 4 (1-8) | Covers across. |
| `rows` | 2 (1-4) | Rows on a page. Build 82: the grid moves by whole pages, the new page sliding in as the old one slides away (eased like RIPFLOW's carousel; off when Coverflow's animation speed is 0). |
| `spacing` | 14 | Pixels between covers. |
| `default` | none | A placeholder for games without art. Leave it out: those games get a clear glass tile with their name instead (build 79). |
| `overlay`, `overlay_*`, `reflection` | | As on `ItemCover` (case art, a mirror under the selection). |
| `font` | | The name on a no-art tile. |
| `tilt*` | | Build 80: tips only the chosen cover, about its own centre (its glow with it). `tilt_scale` lets one cover turn further than a page. |
| `back_pattern` | `COV2` | Build 82: the art on the back of a turned case. Hold the right stick to one side (0.42 s from build 97, 2 s before) and the chosen case turns over to it; it stays turned until held again. Any art suffix works (`SCR` puts a screenshot on the back); `0` leaves the cases unturnable. The back is asked for as soon as the front is in, from a cache of its own. |

Controls on a Grid theme: Left / Right one cover, Up / Down one row, past the top or bottom row a new
press switches drive, the cancel button cycles the sources (the hint row says *Source*), and a 0.42 s
right-stick hold turns the chosen case over (build 97; 2 s from build 82). From build 97 Right on a row's last
cover turns the page instead of wrapping. A Grid
page **must also declare an `ItemsList` with `hidden=1`**: the engine adds a visible list to any page
without one.

## Keys RIPPS2 adds to existing elements

| Key | On | Build | What it does |
|---|---|---|---|
| `tilt` | any image or panel, text too | 70 | `1`: the element tips with the right stick on the game list and info page. |
| `tilt_x`, `tilt_y` | | 70 | The pivot. Elements sharing a pivot tip together as one plane. |
| `tilt_scale` | | 70 | The angle in percent of the default (1-400, default 100). |
| `overlay2` | `ItemCover`, `GameImage`, `Grid` | RiptOPL | A second overlay drawn over the art (RIPPS2's case: `overlay=case overlay2=case_overlay`). |
| `reflection`, `reflection_offset` | cover elements | RiptOPL | A mirror image under the art, fading out; the offset moves it down. |
| `alpha` | `GameImage` | 66 | Opacity 0-128. |
| `widecrop` | `Background` | 79 | `1`: on a 16:9 picture 4:3 art zooms (its middle three quarters of height) instead of stretching. Frosted panels follow the crop. |
| `valign` | `GameImage` | 102 | `bottom`: the art's lowest visible row stands on the box's bottom edge, however much clear space the image has round it. For logos set just above a panel: every game's logo sits the same distance above it. |
| `pattern=SCRn` | `GameImage` | 108 | Every screenshot in turn: the game's `_SCR`, `_SCR2` .. `_SCR9` (RIPSHOT's ART shots and any the art set has), each for 5 s with a 1 s crossfade, as the slides do. A second `SCRn` box on the page starts one shot later (a third two later, up to four), so two boxes never show the same shot; a box with no shot of its own shows its `default`. As a `slide`, an `SCRn` element shows the next shot each time the show comes round (two `SCRn` slides: two new shots a round), as RIPPS2's own info page does. Shots count from `_SCR` with no gap. On builds before 108 the box shows its `default`. |
| `slide` | `GameImage` | 59 | Slideshow position 1-4: the page's slides take turns (5 s each, a 1 s crossfade), each in its own place with its own overlay and reflection. Any page: the info page's art (BG, SCR, SCR2), or a game list's case showing the front cover (`COV`) then the back (`COV2`), as Adapt does (build 81). A game without a slide's art skips it. |
| `hidden` | `ItemsList` | RiptOPL | The list drives selection but is not drawn (Coverflow, Grid). |
| `line_height`, `vcenter` | `AttributeText` | 59 | Wrapped text's line step; centre the block in its height. With either set, text longer than its box **rolls** through it. One-line text always scrolls in its room. |
| `item_height` | `ItemsList` | 59 | Row pitch. The highlighted row's bar fills the row, and from build 83 every title is centred on its row by its own font's centreline (measured from the face), so any font sits in the middle of the bar with nothing to adjust. |
| `star` | `ItemsList` | 106 | Where a starred game's star sits. `left` (the default, in every built-in theme and Adapt): its own column at the start of every row, so the titles stay lined up. `right`: after the title. `hidden`: none. The user's **Settings > Game Sources > Starred Games Star** wins. With the star on the left, the row icon (`decorator`) moves to the row's right end, so the two never overlap. |
| `star_image` | `ItemsList` | 106 | The star's picture for this list. Without it: the theme's `fav_mark.png`, else RIPPS2's. |
| `highlight` | `ItemsList` | 106 | The selected row: `bar` (the default: the PS2-blue bar with its light leading edge), `line` (a line under the row) or `none` (the selected title's colour alone). |
| `decorator_all` | `ItemsList` | 106 | One picture drawn as every row's icon, for a list without per-game icons. |
| `decorator_ps2`, `decorator_ps1`, `decorator_app` | `ItemsList` | 106 | A row icon for each kind of row: a PS2 game, a PS1 game, an app. A game's own icon (`decorator=ICO`, its `ART/<ID>_ICO`) comes first, then its kind's, then `decorator_all`, then the decorator's `default`. |
| `devices` | any element | RiptOPL | Show the element only on some devices (see the engine reference). |

## Effects and tricks

- **The frosted screen** (build 79). A full-screen panel straight after the `Background`,
  `x=0 y=0 width=640 height=480 aligned=0 blur=1 tint=24 frame=0`, puts every game's art under frosted
  glass: no hard edges, no stretched pixels, and what sits on it stays readable. Panels after it frost
  the same art, so they read as one sheet. Adapt and RIPGRID do this.
- **A side bar** is two frameless panels: a dark strip (`tint=88 tint_color=#01040F`) and a light rule
  beside it (`tint=22 tint_color=#28C5F9`).
- **Page transitions.** RIPPS2 morphs one page's glass into the next between the game list and the info
  page (and into menus), using the **first framed** `Ripps2PanelGlass` of `main` and of `info`. Declare
  one on each page and the theme gets the full transition. A theme with none keeps its backdrop and
  switches the content (RIPFLOW's way).
- **One-sheet tilt.** Give every element of the info page the same `tilt=1 tilt_x=320 tilt_y=260` and
  the page tips as one plane with the right stick, text included. A cover and its disc sharing a pivot
  tip together.
- **RIPPS2's case**: an `ItemCover` at 143 x 201 with `overlay=case overlay2=case_overlay`, overlay
  corners at the four corners and `reflection=1`. `scaled=1` keeps it true on 16:9.
- **4:3 screenshots on any screen**: a `GameImage` with `scaled=1` in a frame overlay (Adapt's `SCR43.png`).
  `pattern=SCRn` (build 108) on two boxes shows every shot the game has, two at a time; `SCR` and `SCR2` show
  just those two.
- **Art eases in** as it arrives; the info page's pieces appear as one group (up to 0.8 s).
- **Rolling descriptions**: set `line_height` on a wrapped `AttributeText` and a long description rolls.
- **Settings over the pillars**: leave out `use_settings_bg`.
- **No towers**: `towers=0` and a `bg_color`, for a theme that is all art.
- **The source as a toast**: `source_name=pop`.
- **Arrive in your colours**: `color_theme=` and the other Colors and More keys.
- **Left / right variants**: `tools/mirror_theme.py` drafts the other side; the Adapt family keeps its
  side bar left and swaps the content (`tools/gen_adapt_family.py`).

## A theme of two files (build 115)

A theme names its pictures (`default=`, `overlay=`, `overlay2=`, an `AttributeImage`'s badge folder); from build 115
any it leaves out of its folder is RIPPS2's own of that name, unless `use_default=0`. A badge folder's name reads as
RIPPS2's (`rating/0_Rating` is `Rating_0`). With the built-in fonts, `glyph_set`, `badge_set` and `loading_mark`, a
theme can be `conf_theme.cfg` alone, plus whatever pictures make it its own. Adapt and Adapt Rx (edition 115) are
`conf_theme.cfg` and `SCR43.png`:

| Was a file | Now |
|---|---|
| `a.ttf` | `default_font=builtin:ripps2condensed` |
| `case.png`, `case_overlay.png` | RIPPS2's own (RiptOPL's case, the same pictures) |
| `cross.png` ... `right.png` | `glyph_set=standard` (RIPPS2 carries the set) |
| `load0.png` ... `load7.png` | `loading_mark=corner` (RIPPS2's busy mark; the frames were never drawn) |
| `aspect/`, `esrb/`, `players/`, `rating/`, `scan/`, `vmode/` | `badge_set=ripps2` |

A theme that keeps its own pictures loses nothing: a file in the folder always wins.

## Replacing RIPPS2's own images

Any of these, shipped in the theme folder as `<name>.png`, replaces RIPPS2's own (8-bit palette, alpha
kept). Leave one out and RIPPS2 uses its own, unless `use_default=0`.

| Group | Names |
|---|---|
| Launch disc | `launch_disc` (build 91: the disc `launch_disc=pop|spin|zoom` brings in when a game has no ICO art; square, round, transparent outside) |
| Button glyphs | `cross` `circle` `square` `triangle` `select` `start` `L1` `R1` `L3` `R3` `L2R2` `left` `right` `ripps2_up` `ripps2_down` `hint_badge` (build 90: the pill for `hints_labels=badge`; make it 40 x 28 or so with a flat middle) |
| Loading | `load0` ... `load7` (not drawn: RIPPS2's busy mark is, placed by `loading_mark`) |
| Devices | `usb` `usb_bd` `ilk_bd` `m4s_bd` `hdd_bd` `hdd` `mmce` `eth` `udp_bd` `udp_fs` `app` `Index_0` ... `Index_4` `no_Device` `Device_1` ... `Device_6` `Device_all` |
| Badges | `ELF` `HDL` `ISO` `VCD` `ZSO` `UL` `APP` `CD` `DVD` `PS1` `PS2` `Aspect_s` `Aspect_w` `Aspect_w1` `Aspect_w2` `Rating_0` ... `Rating_5` `no_Rating` `Scan_240p` `Scan_240p1` `Scan_480i` `Scan_480p` ... `Scan_480p5` `Scan_576i` `Scan_576p` `Scan_720p` `Scan_1080i` `Scan_1080i2` `Scan_1080p` `Vmode_multi` `Vmode_ntsc` `Vmode_pal`; build 115: `Players_1` ... `Players_4` `Parental_3` `Parental_10` `Parental_17` `Parental_18` `Parental_e` `Parental_teen` |
| Art stand-ins | `cover` `disc` `screen` `screens` `coverapp` `missing` `case` `case_overlay` `apps_case` `logo` `logo0` ... `logo6` `fav` `fav_mark` `settings_bg` |
| RIPPS2's marks | `ripps2_mark` (the PS2 mark that flies along the category bar) `ripps2_mark_glow` `ripps2_glass` `ripps2_ps1logo` `ripps2_ps2logo` (L3's view word) `ripps2_grid_icons` `ra_mark` |

## Sounds and music

A theme's `sound/` folder gives the theme its own sounds while it is on: any of the 15 events, as
`.adp` (mono SPU2 ADPCM; RIPPS2 Audio Studio converts any sound). RIPPS2 has no sounds of its own from
build 95: the user rips theirs into the AUDIO folder. From build 98 an event the theme leaves out plays
the AUDIO folder's (builds 95 to 97 played nothing for it). From build 100 the AUDIO folder fills only
what the theme's set leaves silent: an event the theme covers through the sound it falls back to (its
`transition` for page in and out, its `message` for error and save, its `cursor` for random) keeps the
theme's. Adapt and Adapt Rx ship no sounds (10/12/2026), so every sound with them on is the user's own rip.

From build 102 `sounds=audio` makes that certain: the theme always plays the AUDIO folder's sounds and never a
`sound/` folder of its own, even one an older edition left behind when a new one was copied over it (Adapt
shipped six sounds up to build 99). Adapt and Adapt Rx set it.

| File | Plays |
|---|---|
| `boot.adp` | as the towers rise at power on |
| `cursor.adp` | moving the cursor |
| `confirm.adp` | choosing something |
| `cancel.adp` | going back |
| `message.adp` | a message box opens |
| `transition.adp` | switching tabs |
| `bd_connect.adp`, `bd_disconnect.adp` | a drive arrives, a drive is removed |
| `page_in.adp`, `page_out.adp` | opening a page, closing it |
| `error.adp` | an error message |
| `save.adp` | settings saved |
| `launch.adp` | a game launching |
| `disc.adp` | a disc read in Launch Disc |
| `random.adp` | L2 + R2 picks a random game |

`sound/bgm.ogg` is the theme's music (Ogg Vorbis at a fixed bitrate, no tags). It plays instead of the
user's AUDIO music while the theme is on. Every sound
is loaded into the SPU2's 2 MB at once (music streams), so keep the set small.

## What every theme gets
- Art fades in as it arrives; covers on a Grid ease in once per game.
- Hold **SELECT** on the game list for the themes (build 114's list): from 1 s the THEMES window comes up with a
  wheel filling, and at 4.2 s the themes fill it (build 115). Let go before and it fades away and the list refreshes,
  as a short press does. Settings > Interface > Hold SELECT: Cycle steps to the next theme instead (build 79's).
- L3's view word and the Pop In toast in RIPPS2 Sleek Bold 64 (build 81), the same on every theme, and the category bar's flying mark.
- Colors and More, with the theme's own defaults where it gives them.
- Hints and Glyphs (build 90): the user can hide, reorder or relabel the hints and pick a glyph set on any theme.
- 720p and 1080i in one pass at full detail (build 75).
- Build 102: the Colours page edits the theme's own colours too (kept for that theme; Reset gives back its
  file's), an app's case is a PS1 square unless its menu (Triangle > Case Shape) says PS2 or Theme, a
  reflection fades with its cover, long text slides smoothly, and About and STATUS read in RIPPS2's own faces.
- Build 115: a PS1 game's cover in the square PS1 case, every message in Roboto at normal weight, the towers in the
  Color Theme (or the Color Sweep) from the first boot frame, and Hints and Glyphs > Badge Set.

## What a theme cannot change (yet)
These are RIPPS2's own and need an engine change (`elf/patches` in RIPPS2), not a theme: the towers'
and orbs' shapes and motion (a theme can turn the towers off and recolour them with `color_theme`), the
layout of Launch Disc, Memory Files, STATUS and the Achievements pages (they take the theme's fonts and
colours; About and STATUS keep RIPPS2's own faces from build 102), where the view word and toasts sit, and the Grid glow's timing. If a look needs one of these,
ask for a key in RIPPS2's issues: new keys land here with the build that brings them.
