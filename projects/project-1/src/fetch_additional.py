"""Additional public source snapshots; Oladapo Olaniyan, FIN-43900 Project 1."""
from pathlib import Path
import urllib.request, json, datetime, hashlib
ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
 'pep-2025-annual-report.pdf':'https://www.pepsico.com/docs/pepsico-5v9wci20/media/Files/investors/pepsico-2025-annual-report.pdf',
 'treasury-2026.html':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026',
 'ko-market.html':'https://stockanalysis.com/stocks/ko/history/',
 'mdlz-market.html':'https://stockanalysis.com/stocks/mdlz/history/',
 'ko-2026-q2.pdf':'https://investors.coca-colacompany.com/filings-reports/all-sec-filings/content/0001628280-26-050503/0001628280-26-050503.pdf',
}
records=[]
for name,url in SOURCES.items():
 target=ROOT/'sources'/name
 row=dict(analyst='Oladapo Olaniyan',url=url,file=name,access_date='2026-10-06')
 try:
  if target.exists(): raise FileExistsError('Existing source preserved')
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 AcademicFinanceResearch/1.0'})
  with urllib.request.urlopen(req,timeout=25) as r: data=r.read()
  target.write_bytes(data)
  row.update(status='retrieved',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e: row.update(status='failed',error=str(e))
 records.append(row)
 print(name,row['status'],row.get('error',row.get('bytes')))
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
(ROOT/'sources'/f'additional-retrieval-{stamp}.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
