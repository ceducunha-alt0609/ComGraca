from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''    l: "Lucro Estimado",\n    v: R$(lucro),'''
new='''    l: "Resultado de Caixa Estimado",\n    v: R$(lucro),'''
assert old in s
s=s.replace(old,new,1)

old='''  }, "* Lucro calculado sobre receita confirmada menos custos estimados de produ\\xE7\\xE3o.")))'''
new='''  }, "* Resultado de caixa estimado: valores recebidos no mês menos custos estimados de produção do mês.")))'''
assert old in s
s=s.replace(old,new,1)

old='''        React.createElement("div",{style:{fontSize:11,color:"var(--mut)"}},ptDate(s.date)," \\xB7 ",label," \\xB7 ",s.method),'''
new='''        React.createElement("div",{style:{fontSize:11,color:"var(--mut)"}},ptDate(s.date)," \\xB7 ",label," \\xB7 ",s.method),\n        s.paid&&s.paidDate&&React.createElement("div",{style:{fontSize:10,color:"var(--sage)",marginTop:2,fontWeight:600}},"Recebido em ",ptDate(s.paidDate)," via ",s.paidMethod||s.method),'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
s2=p.read_text(encoding='utf-8')
assert 'Resultado de Caixa Estimado' in s2
assert 'Resultado de caixa estimado: valores recebidos no mês' in s2
assert 'Recebido em ",ptDate(s.paidDate)' in s2
print('labels and receipt visibility verified')
