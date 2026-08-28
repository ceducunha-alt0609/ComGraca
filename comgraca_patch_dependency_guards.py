from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    got=s.count(old)
    assert got>=count, f'{label}: expected {count}, got {got}'
    s=s.replace(old,new,count)

rep('''    setRecs = _ref4.setRecs,\n    recipeCost = _ref4.recipeCost,''','''    setRecs = _ref4.setRecs,\n    prods = _ref4.prods,\n    recipeCost = _ref4.recipeCost,''','RecTab prods')

old_ing='''  var delIngr = /*#__PURE__*/function () {\n    var _ref5 = _asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee(id) {\n      return _regenerator().w(function (_context) {\n        while (1) switch (_context.n) {\n          case 0:\n            _context.n = 1;\n            return confirm("Excluir este ingrediente?");\n          case 1:\n            if (!_context.v) {\n              _context.n = 2;\n              break;\n            }\n            setIngrs(ingrs.filter(function (x) {\n              return x.id !== id;\n            }));\n          case 2:\n            return _context.a(2);\n        }\n      }, _callee);\n    }));'''
new_ing='''  var delIngr = /*#__PURE__*/function () {\n    var _ref5 = _asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee(id) {\n      var inUse;\n      return _regenerator().w(function (_context) {\n        while (1) switch (_context.n) {\n          case 0:\n            inUse = recs.some(function (r) {\n              return (r.items || []).some(function (it) { return it.ingredientId === id; });\n            });\n            if (!inUse) {\n              _context.n = 1;\n              break;\n            }\n            alert("Este ingrediente está sendo usado em uma receita e não pode ser excluído.");\n            return _context.a(2);\n          case 1:\n            _context.n = 2;\n            return confirm("Excluir este ingrediente?");\n          case 2:\n            if (!_context.v) {\n              _context.n = 3;\n              break;\n            }\n            setIngrs(ingrs.filter(function (x) {\n              return x.id !== id;\n            }));\n          case 3:\n            return _context.a(2);\n        }\n      }, _callee);\n    }));'''
rep(old_ing,new_ing,'ingredient dependency guard')

old_rec='''  var delRec = /*#__PURE__*/function () {\n    var _ref6 = _asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee2(id) {\n      return _regenerator().w(function (_context2) {\n        while (1) switch (_context2.n) {\n          case 0:\n            _context2.n = 1;\n            return confirm("Excluir esta receita?");\n          case 1:\n            if (!_context2.v) {\n              _context2.n = 2;\n              break;\n            }\n            setRecs(recs.filter(function (r) {\n              return r.id !== id;\n            }));\n          case 2:\n            return _context2.a(2);\n        }\n      }, _callee2);\n    }));'''
new_rec='''  var delRec = /*#__PURE__*/function () {\n    var _ref6 = _asyncToGenerator(/*#__PURE__*/_regenerator().m(function _callee2(id) {\n      var inUse;\n      return _regenerator().w(function (_context2) {\n        while (1) switch (_context2.n) {\n          case 0:\n            inUse = (prods || []).some(function (p) { return p.recipeId === id; });\n            if (!inUse) {\n              _context2.n = 1;\n              break;\n            }\n            alert("Esta receita já foi usada em produção e não pode ser excluída. Você pode editar os dados para uso futuro sem perder o histórico.");\n            return _context2.a(2);\n          case 1:\n            _context2.n = 2;\n            return confirm("Excluir esta receita?");\n          case 2:\n            if (!_context2.v) {\n              _context2.n = 3;\n              break;\n            }\n            setRecs(recs.filter(function (r) {\n              return r.id !== id;\n            }));\n          case 3:\n            return _context2.a(2);\n        }\n      }, _callee2);\n    }));'''
rep(old_rec,new_rec,'recipe dependency guard')

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8')
assert 'const CACHE = "comgraca-v8-monthly-extra-costs";' in w
w=w.replace('const CACHE = "comgraca-v8-monthly-extra-costs";','const CACHE = "comgraca-v9-dependency-guards";',1)
sw.write_text(w,encoding='utf-8')

s2=p.read_text(encoding='utf-8')
for needle in [
    'prods = _ref4.prods',
    'Este ingrediente está sendo usado em uma receita',
    'Esta receita já foi usada em produção',
    'recs.some(function (r)',
    '(prods || []).some(function (p)'
]: assert needle in s2, needle
assert 'comgraca-v9-dependency-guards' in sw.read_text(encoding='utf-8')
print('ComGraca dependency guards patch OK')
