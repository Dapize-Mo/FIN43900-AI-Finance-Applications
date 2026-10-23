"""Local audio comparison evidence for Oladapo Olaniyan, FIN-43900 Project 1."""
from pathlib import Path
import json
import os
import wave
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HUB_DISABLE_XET'] = '1'
from faster_whisper import WhisperModel
import av

out = ROOT / 'tmp' / 'audio-check'
out.mkdir(exist_ok=True)
model = WhisperModel(str(out / 'small.en'), device='cpu', compute_type='int8', cpu_threads=8)
pairs = [('1', '2766839541'), ('2', '1502154100'), ('3', '1988888967')]
zoom = Path(r'C:\Users\dolan\OneDrive\Documents\Zoom')
for number, ident in pairs:
    audio = next(zoom.glob(f'*/audio{ident}.m4a'))
    video = audio.with_name(f'video{ident}.mp4')
    with av.open(str(video)) as container:
        duration = container.duration / av.time_base
    print(f'VIDEO {number}: {duration:.2f}s; transcribing', flush=True)
    with wave.open(str(out / f'video-{number}.wav'), 'rb') as decoded:
        samples = np.frombuffer(decoded.readframes(decoded.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    segments, info = model.transcribe(samples, language='en', beam_size=1,
                                     word_timestamps=False, vad_filter=True)
    records = []
    for s in segments:
        records.append(dict(start=s.start, end=s.end, text=s.text,
                            words=[dict(start=w.start,end=w.end,word=w.word,probability=w.probability) for w in (s.words or [])]))
        print(f'{number} [{s.start:.1f}-{s.end:.1f}] {s.text}', flush=True)
    (out / f'video-{number}-asr.json').write_text(json.dumps(dict(
        analyst='Oladapo Olaniyan', audio=str(audio), video=str(video),
        measured_video_duration_seconds=duration, model='faster-whisper small.en int8',
        status='Machine transcription for comparison; not human-certified verbatim',
        segments=records), indent=2), encoding='utf-8')
    print(f'COMPLETE VIDEO {number}', flush=True)
