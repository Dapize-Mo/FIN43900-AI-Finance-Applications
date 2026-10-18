"""Display-only dashboard copy for Oladapo Olaniyan; no model changes."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'outputs/final-working-run/visible-output.html').read_text(encoding='utf-8')
for old,new in [('low','Low'),('base','Base'),('high','High'),('value_reset_failure','Value Reset Failure')]:
    text=text.replace(f'<td>{old}</td>',f'<td>{new}</td>')
for year in range(2026,2031):text=text.replace(f'<td>{year:,.1f}</td>',f'<td>{year}</td>')
for name in ['forecast-statements.csv','sensitivity.csv','checks.csv','results.json']:
    text=text.replace(f'href="{name}"',f'href="../outputs/final-working-run/{name}"')
with (ROOT/'presentation/Dashboard-review.html').open('x',encoding='utf-8') as f:f.write(text)
