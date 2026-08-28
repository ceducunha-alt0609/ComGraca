from pathlib import Path
import re

s = Path('index.html').read_text(encoding='utf-8')

checks = {}
patterns = {
    'uid_definition': r'var uid = function uid\(\)',
    'restore_validation': r'requiredArrays\.every',
    'duplicate_id_guard': r'duplicate|duplicad|Set\(.*id|new Set\(.*id',
    'negative_guard': r'<\s*0|<=\s*0|min:\s*"0"',
    'recipe_ref': r'recipeId',
    'kit_ref': r'kitId',
    'paid_date': r'paidDate',
    'production_snapshot': r'costPerBarSnapshot|totalCostSnapshot|recipeNameSnapshot',
    'dependency_guard': r'ingrediente está sendo usado|receita já foi usada em produção',
}
for name, pat in patterns.items():
    checks[name] = len(re.findall(pat, s, flags=re.I|re.S))

# Exact high-risk snippets around restore and stock.
def around(term, radius=500):
    i=s.find(term)
    if i<0: return 'NOT FOUND'
    return s[max(0,i-radius):i+radius]

parts=[]
parts.append('FINAL INTEGRITY AUDIT\n')
for k,v in checks.items():
    parts.append(f'{k}={v}\n')

for term in ['var uid = function uid', 'var stock = useMemo', 'var setAllData = function setAllData', 'var importBackup', 'requiredArrays', 'setProds(function', 'setSales(function']:
    parts.append('\n=== '+term+' ===\n'+around(term,900)+'\n')

Path('comgraca_final_integrity_report.txt').write_text(''.join(parts),encoding='utf-8')
print('audit report generated')
