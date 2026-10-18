"""Public source snapshots for Oladapo Olaniyan, FIN-43900 Project 1.
Research utility only; model runs offline and does not require this script.
"""
from pathlib import Path
import urllib.request, json, hashlib, datetime

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'pep-2025-10k.html': 'https://www.sec.gov/Archives/edgar/data/77476/000007747626000007/pep-20251227.htm',
    'pep-2026-q2.html': 'https://www.sec.gov/Archives/edgar/data/77476/000007747626000035/pep-20260613.htm',
    'course-architecture.md': 'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/PROJECT-SUBMISSION-ARCHITECTURE.md',
    'course-checklist.md': 'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/projects/major-project-student-checklist.md',
    'course-manifest.csv': 'https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/projects/templates/project-submission-manifest-template.csv',
    'pep-market.html': 'https://stockanalysis.com/stocks/pep/history/',
}
def main():
    folder = ROOT / 'sources'
    folder.mkdir(exist_ok=True)
    records = []
    for name, url in SOURCES.items():
        target = folder / name
        if target.exists():
            raise FileExistsError(f'Preserve existing snapshot: {target}')
        row = dict(analyst='Oladapo Olaniyan', url=url, accessed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), file=name)
        try:
            request = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 AcademicFinanceResearch/1.0'})
            with urllib.request.urlopen(request, timeout=25) as response:
                data = response.read()
            target.write_bytes(data)
            row.update(status='retrieved', sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        except Exception as exc:
            row.update(status='failed', error=str(exc))
        records.append(row)
        print(name, row['status'], row.get('error', row.get('bytes')))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    (folder / f'retrieval-log-{stamp}.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
if __name__ == '__main__':
    main()
