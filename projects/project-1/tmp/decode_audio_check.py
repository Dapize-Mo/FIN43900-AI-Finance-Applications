"""Prepare local comparison audio for Oladapo Olaniyan."""
from pathlib import Path
import av
import wave
zoom = Path(r'C:\Users\dolan\OneDrive\Documents\Zoom')
out = Path(__file__).parent / 'audio-check'
for number, ident in enumerate(['2766839541','1502154100','1988888967'], 1):
    source = next(zoom.glob(f'*/audio{ident}.m4a'))
    with av.open(str(source)) as container, wave.open(str(out / f'video-{number}.wav'), 'wb') as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(16000)
        resampler = av.AudioResampler(format='s16', layout='mono', rate=16000)
        for frame in container.decode(audio=0):
            for converted in resampler.resample(frame):
                target.writeframes(converted.to_ndarray().tobytes())
        for converted in resampler.resample(None):
            target.writeframes(converted.to_ndarray().tobytes())
    print(f'Converted Video {number}')
