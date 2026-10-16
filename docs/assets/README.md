# Assets

- `social-preview.svg` → `social-preview.png` (1280×640): the repository's social preview (#46). Upload the PNG under Settings → General → Social preview.
- `icon.svg` → `icon.png` (512×512): the square plugin icon (#37).

The SVGs are the sources. They use system fonts (Inter, then Segoe UI or Helvetica Neue for text; JetBrains Mono, then Cascadia Code or Consolas for code), so a re-export looks the same only on a machine with the same fonts. To regenerate the PNGs on Windows with Edge (Chrome takes the same flags):

```
msedge --headless=new --hide-scrollbars --window-size=1280,640 --screenshot=social-preview.png file:///<path>/social-preview.svg
msedge --headless=new --hide-scrollbars --window-size=512,512 --screenshot=icon.png file:///<path>/icon.svg
```
