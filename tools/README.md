# Promo media tools

Scripts that turn a KDP book's cover and interior PDFs into Pinterest pins and Instagram reels.

- `colorize.py` auto-fills the closed regions of line art with a Halloween palette (used for "before/after" pins and the color-reveal reel).
- `lib.py` shared design helpers: purple starry background, outlined Chewy headlines, page cards.
- `pins.py` renders 1000x1500 pins. `reels.py A B C` renders 1080x1920 reels with original music from `music.py`.

Setup:
1. Render pages: `pdftoppm -r 150 -png Interior.pdf $KDP_WORK/hi/p` and `pdftoppm -r 200 -png Cover.pdf $KDP_WORK/hi/cover`
2. Fonts into `$KDP_FONTS`: Chewy (apache/chewy/Chewy-Regular.ttf) and Fredoka (ofl/fredoka) from github.com/google/fonts
3. `pip install numpy scipy pillow` and ffmpeg
4. Edit page numbers and headlines in `pins.py` / `reels.py` for the book, set `KDP_OUT=media/<book-slug>`, then run.

Media in `media/` is public (served via raw.githubusercontent.com) so Metricool can fetch it.
