"""Refresh the official Q4 archive for rulebook research - Oladapo Olaniyan, FIN-43900.
Same route as forecast-audit-2026-10-28/fetch_archives.py (official archive API, download via Modal).
Read-only: submits nothing, changes no deployment. Never prints credentials."""
from pathlib import Path
import sys, json, hashlib, gzip, modal, httpx
from dotenv import dotenv_values
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'agent'))
from modal_app import image
app = modal.App('fin439-archive-refresh')

@app.function(image=image, timeout=120, serialized=True)
def fetch(url):
    import urllib.request
    with urllib.request.urlopen(url, timeout=90) as response:
        return response.read()

if __name__ == '__main__':
    cfg = dotenv_values(HERE.parent / 'agent/.env')
    manifest = httpx.get('https://api.explainingmarkets.ai/v1/archive', headers={'X-API-Key': cfg['EM_API_KEY']}, timeout=30)
    manifest.raise_for_status()
    item = next(x for x in manifest.json()['files'] if x['quarter'] == '2026Q4' and x['event_type'] == 'EARNINGS_RELEASE')
    with app.run():
        data = fetch.remote(item['url'])
    records = [json.loads(x) for x in gzip.decompress(data).decode().splitlines() if x]
    (HERE / '2026Q4.jsonl.gz').write_bytes(data)
    last = max(r['event_datetime'] for r in records)
    (HERE / 'source.json').write_text(json.dumps({'author': 'Oladapo Olaniyan', 'quarter': '2026Q4', 'records': len(records),
        'last_event': last, 'sha256': hashlib.sha256(data).hexdigest(), 'source': 'https://api.explainingmarkets.ai/v1/archive',
        'built_at': item.get('built_at')}, indent=2), encoding='utf-8')
    print('OK records', len(records), 'last event', last)
