"""The rolling release's files for RIPPS2's THEMES page (RIPPS2 build 162): one uncompressed tar a theme, and themes.txt.

    python3 tools/make_release_assets.py [out]      (default out: dist/)

Each themes/thm_<Name>/ becomes <asset>.tar holding thm_<Name>/ and its files (ustar, no compression, every date and owner zeroed,
so the same folder makes the same bytes and GitHub's digest only changes when the theme does). themes.txt names them, one line a
theme, tab apart: asset, folder, name, blurb. RIPPS2 lists them in that order. A theme with no line in THEMES below is left out.
Then upload: gh release upload rolling dist/*.tar dist/themes.txt --clobber -R akilluminati47/RIPPS2-themes
"""
import io
import os
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# folder: (name, blurb). Short: RIPPS2 shows the blurb as the row's tip, one or two lines
THEMES = {
    'thm_Adapt': ('Adapt', "Each game's art under frosted glass, its cover in RIPPS2's case with the disc, the list on clear glass "
                           'beside it, the sources as glyphs in a frosted side bar.'),
    'thm_Adapt Rx': ('Adapt Rx', 'Adapt mirrored: the list on the left, the case and its disc on the right, LAUNCH DISC at the '
                                 'right of the bar.'),
}


def asset_name(folder):
    return folder.replace(' ', '_') + '.tar'


def make_tar(folder_path, folder):
    b = io.BytesIO()
    with tarfile.open(fileobj=b, mode='w', format=tarfile.USTAR_FORMAT) as t:
        def add(path, arc):
            ti = t.gettarinfo(path, arc)
            ti.mtime = 0
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = ''
            ti.mode = 0o755 if ti.isdir() else 0o644
            if ti.isdir():
                t.addfile(ti)
            else:
                with open(path, 'rb') as f:
                    t.addfile(ti, f)
        add(folder_path, folder)
        for dirpath, dirnames, filenames in os.walk(folder_path):
            dirnames.sort()
            rel = os.path.relpath(dirpath, folder_path)
            for d in dirnames:
                add(os.path.join(dirpath, d), '/'.join(x for x in (folder, rel, d) if x != '.'))
            for f in sorted(filenames):
                add(os.path.join(dirpath, f), '/'.join(x for x in (folder, rel, f) if x != '.'))
    return b.getvalue()


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'dist')
    os.makedirs(out, exist_ok=True)
    lines = ['# RIPPS2-themes for RIPPS2\'s THEMES page (build 162 and later): asset, folder, name, blurb, tab apart']
    for folder, (name, blurb) in THEMES.items():
        path = os.path.join(REPO, 'themes', folder)
        if not os.path.isdir(path):
            print('missing', path)
            return 1
        assert '\t' not in blurb and '\n' not in blurb and len(blurb) < 200 and '—' not in blurb
        data = make_tar(path, folder)
        with open(os.path.join(out, asset_name(folder)), 'wb') as f:
            f.write(data)
        lines.append('\t'.join((asset_name(folder), folder, name, blurb)))
        print('%s  %d bytes' % (asset_name(folder), len(data)))
    with open(os.path.join(out, 'themes.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('themes.txt  %d themes' % (len(lines) - 1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
