import os
import glob
from PIL import Image

def generate_webp_for_all_posts():
    img_dir = '/home/merolhack/fl/mach-playbook/assets/img/posts'
    pngs = glob.glob(os.path.join(img_dir, '*.png'))
    print(f"Converting {len(pngs)} PNG images to WebP in {img_dir}...")

    total_png = 0
    total_webp = 0

    for path in pngs:
        webp_path = os.path.splitext(path)[0] + '.webp'
        png_sz = os.path.getsize(path)
        total_png += png_sz
        try:
            with Image.open(path) as img:
                rgb = img.convert('RGB')
                # Resize to max 600px width for sharp crisp mobile & desktop preview cards
                if rgb.width > 600:
                    new_h = int(rgb.height * 600 / rgb.width)
                    rgb = rgb.resize((600, new_h), Image.Resampling.LANCZOS)
                
                rgb.save(webp_path, 'WEBP', quality=75, method=6)
                webp_sz = os.path.getsize(webp_path)
                total_webp += webp_sz
        except Exception as e:
            print(f"Error converting {path}: {e}")

    saved = total_png - total_webp
    pct = (saved / total_png) * 100 if total_png > 0 else 0
    print("==================================================")
    print("   WEBP IMAGE GENERATION COMPLETE")
    print("==================================================")
    print(f"  Total PNG Size:  {total_png / (1024*1024):.2f} MB")
    print(f"  Total WebP Size: {total_webp / (1024*1024):.2f} MB")
    print(f"  Payload Saved:   {saved / (1024*1024):.2f} MB ({pct:.1f}% reduction)")
    print("==================================================")

if __name__ == '__main__':
    generate_webp_for_all_posts()
