"""Save audio comparison and revised topic timestamps for Oladapo Olaniyan."""
from pathlib import Path
import re
import json
import difflib
import csv

root = Path(__file__).resolve().parents[1]
evidence = root / 'tmp/audio-check'
out = root / 'docs/audio-check'
out.mkdir(exist_ok=True)
metadata = json.loads((evidence/'recording-metadata.json').read_text())
alignment = []

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def stamp(seconds):
    value = int(seconds)
    return f'{value//60:02d}:{value%60:02d}'

for number in range(1,4):
    source = root / f'docs/transcript-drafts/Video_{number}_Transcript_FINAL.txt'
    draft = source.read_text(encoding='utf-8-sig')
    raw = json.loads((evidence/f'video-{number}-asr.json').read_text())
    stream = []
    for segment in raw['segments']:
        words = tokens(segment['text'])
        for i, word in enumerate(words):
            stream.append((word,segment['start']+(segment['end']-segment['start'])*i/max(1,len(words))))
    floor = 0
    paragraphs = re.findall(r'\[(\d\d:\d\d)\]\s*(.*?)(?=\n\n|\Z)', draft, re.S)
    revised = []
    for index,(old,paragraph) in enumerate(paragraphs):
        anchor = tokens(paragraph)[:12]
        candidates = []
        for pos in range(floor,max(floor+1,len(stream)-len(anchor)+1)):
            window = [w for w,_ in stream[pos:pos+len(anchor)]]
            score = difflib.SequenceMatcher(None,anchor,window).ratio()
            candidates.append((score,-pos,pos))
        score,_,pos = max(candidates)
        second = stream[pos][1]
        # Use the directly observed segment boundary for this short anchor;
        # the generic fuzzy match otherwise starts inside the preceding sentence.
        if number == 2 and index == 4:
            second = 124.5
        floor = pos+len(anchor)
        alignment.append(dict(video=number,old_timestamp=old,audio_aligned_timestamp=stamp(second),
                              seconds=round(second,2),anchor_score=round(score,3),anchor=' '.join(anchor)))
        revised.append(f'[{stamp(second)}] {paragraph.strip()}')
    notes = draft.split('FACTUAL / TRANSCRIPTION NOTES',1)[1]
    notes = re.sub(r'^\s*\(NOT SPOKEN\)\s*:?\s*','',notes)
    if number == 1:
        notes = notes.replace('- 117.29 - 111.41 = 5.88. Percentage relative to 117.29 is about 5.01%; approximately 5.02% is a minor rounding discrepancy.',
            '- Correct model calculation: unrounded baseline 117.2940729555 minus changed value 111.4096394030 = 5.8844335525, a 5.0168208881% decline, correctly rounded to $5.88 and 5.02%. The rounded display values alone give about 5.01%; the original model percentage was correct.')
    if number == 3:
        notes += '\n- Local recognition also detects a brief stumble around 01:51-02:00 ("it is required if it requires"). The supplied draft smooths this passage. Exact filler/repetition should be checked in playback if a strictly verbatim transcript is required; its financial meaning is unchanged.'
    header = (f'FIN-43900 PROJECT 1 - VIDEO {number}\nOladapo Olaniyan\n'
              f'Recording: {metadata[number-1]["video"]["path"]}\n'
              f'Matching audio: {metadata[number-1]["audio"]["path"]}\n'
              f'Measured video duration: {raw["measured_video_duration_seconds"]:.3f} seconds\n'
              'Status: audio-compared transcript draft; no human word-for-word certification.\n'
              'Method: supplied speech draft compared with independent local faster-whisper small.en recognition. '
              'Topic times are estimated within recognized audio segments and rounded down to seconds; they are not exact caption timings. '
              'Draft wording is retained where machine recognition is uncertain; discrepancies are recorded separately.\n\n')
    text = header+'\n\n'.join(revised)+'\n\nEDITORIAL NOTES - NOT SPOKEN\n'+notes.strip()+'\n'
    (out/f'transcript-video-{number}-audio-compared.txt').write_text(text,encoding='utf-8')

with (out/'topic-timestamp-comparison.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=list(alignment[0]));writer.writeheader();writer.writerows(alignment)
(out/'recording-metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
print(json.dumps(alignment,indent=2))
