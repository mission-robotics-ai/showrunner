#!/usr/bin/env python3
"""QR make + verify. Run with: uv run --with "qrcode[pil]" --with opencv-python-headless qr.py

  qr.py make <url> <out.png> [--style dots]
  qr.py verify <image.png> <expected-url>

verify exits nonzero unless the decoded string equals expected exactly.
"""
import sys


def make(url, out, style=None):
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=24, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    if style == "dots":
        from qrcode.image.styledpil import StyledPilImage
        from qrcode.image.styles.moduledrawers.pil import CircleModuleDrawer
        img = qr.make_image(image_factory=StyledPilImage,
                            module_drawer=CircleModuleDrawer())
    else:
        img = qr.make_image(fill_color="black", back_color="white")
    img.save(out)
    print(f"wrote {out} ({'dots' if style == 'dots' else 'square'} modules, EC=H)")


def verify(image, expected):
    import cv2
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(image))
    ok = data == expected
    print(f"decoded: {data!r}\nexpected: {expected!r}\n{'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "make":
        make(sys.argv[2], sys.argv[3],
             "dots" if "--style" in sys.argv and "dots" in sys.argv else None)
    elif len(sys.argv) == 4 and sys.argv[1] == "verify":
        verify(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(2)
