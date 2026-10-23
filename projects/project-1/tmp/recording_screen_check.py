"""Extract review frames for Oladapo Olaniyan; source recordings remain unchanged."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'audio-check-env' / 'Lib' / 'site-packages'))
import av
from PIL import Image, ImageDraw
zoom = Path(r'C:\Users\dolan\OneDrive\Documents\Zoom')
out = Path(__file__).parent / 'audio-check'
for number, ident, times in [(1,'2766839541',[35,75,108]),(2,'1502154100',[18,155,200]),(3,'1988888967',[150,190,225])]:
    source = next(zoom.glob(f'*/video{ident}.mp4'))
    sheet = Image.new('RGB', (1100,660*len(times)), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, seconds in enumerate(times):
        with av.open(str(source)) as container:
            container.seek(int(seconds*av.time_base))
            frame = next(f for f in container.decode(video=0) if f.time >= seconds)
            img = frame.to_image()
            img.thumbnail((1100,630))
        sheet.paste(img,(0,660*i+25))
        draw.text((10,660*i+5),f'Video {number}, actual frame {frame.time:.2f} seconds',fill='black')
    sheet.save(out / f'video-{number}-screen-review.jpg')
    print(number, flush=True)
