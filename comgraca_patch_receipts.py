from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label, count=1):
    global s
    got = s.count(old)
    assert got >= count, f'{label}: expected at least {count}, got {got}'
    s = s.replace(old, new, count)

rep('''        method: form.method,\n        paid: paid,\n        qty: +form.qty,''','''        method: form.method,\n        paid: paid,\n        paidDate: paid ? form.date : null,\n        paidMethod: paid ? form.method : null,\n        qty: +form.qty,''','avulso receipt fields')
rep('''        method: form.method,\n        paid: paid,\n        qty: barsWillUse,''','''        method: form.method,\n        paid: paid,\n        paidDate: paid ? form.date : null,\n        paidMethod: paid ? form.method : null,\n        qty: barsWillUse,''','kit receipt fields')

old_toggle = '''  var togglePaid = function togglePaid(id) {\n    return setSales(function (s) {\n      return s.map(function (v) {\n        return v.id === id ? _objectSpread(_objectSpread({}, v), {}, {\n          paid: !v.paid\n        }) : v;\n      });\n    });\n  };'''
new_toggle = '''  var togglePaid = function togglePaid(id) {\n    var target = sales.find(function (v) { return v.id === id; });\n    if (!target) return;\n    if (target.paid) {\n      setSales(function (list) {\n        return list.map(function (v) {\n          return v.id === id ? _objectSpread(_objectSpread({}, v), {}, { paid: false, paidDate: null, paidMethod: null }) : v;\n        });\n      });\n      return;\n    }\n    var payMethod = window.prompt("Forma de recebimento (Pix ou Dinheiro):", "Pix");\n    if (payMethod === null) return;\n    payMethod = payMethod.trim() || "Pix";\n    var payDate = window.prompt("Data do recebimento (AAAA-MM-DD):", today());\n    if (payDate === null) return;\n    payDate = payDate.trim();\n    if (!/^\\d{4}-\\d{2}-\\d{2}$/.test(payDate)) { alert("Data inválida. Use AAAA-MM-DD."); return; }\n    setSales(function (list) {\n      return list.map(function (v) {\n        return v.id === id ? _objectSpread(_objectSpread({}, v), {}, { paid: true, paidDate: payDate, paidMethod: payMethod }) : v;\n      });\n    });\n  };'''
rep(old_toggle, new_toggle, 'togglePaid')

rep('''  var months = useMemo(function () {\n    var set = new Set(sales.map(function (s) {\n      return s.date.slice(0, 7);\n    }));\n    var sorted = _toConsumableArray(set).sort();''','''  var months = useMemo(function () {\n    var set = new Set();\n    sales.forEach(function (s) {\n      if (s.date) set.add(s.date.slice(0, 7));\n      if (s.paid && (s.paidDate || s.date)) set.add((s.paidDate || s.date).slice(0, 7));\n    });\n    var sorted = _toConsumableArray(set).sort();''','chart months')

rep('''      var paid = ms.filter(function (s) {\n        return s.paid;\n      }).reduce(function (a, s) {\n        return a + saleTotal(s, kits);\n      }, 0);''','''      var paid = sales.filter(function (s) {\n        return s.paid && (s.paidDate || s.date).startsWith(mo);\n      }).reduce(function (a, s) {\n        return a + saleTotal(s, kits);\n      }, 0);''','chart receipts')

rep('''  var mRev = mSales.filter(function (s) {\n    return s.paid;\n  }).reduce(function (a, s) {\n    return a + saleTotal(s, kits);\n  }, 0);''','''  var mRev = sales.filter(function (s) {\n    return s.paid && (s.paidDate || s.date).startsWith(cm);\n  }).reduce(function (a, s) {\n    return a + saleTotal(s, kits);\n  }, 0);''','dashboard receipts')

rep('''  var months = useMemo(function () {\n    var s = new Set([].concat(_toConsumableArray(sales.map(function (s) {\n      return s.date.slice(0, 7);\n    })), _toConsumableArray(prods.map(function (p) {\n      return p.date.slice(0, 7);\n    }))));\n    return _toConsumableArray(s).sort().reverse();\n  }, [sales, prods]);''','''  var months = useMemo(function () {\n    var s = new Set([].concat(_toConsumableArray(sales.map(function (sale) {\n      return sale.date.slice(0, 7);\n    })), _toConsumableArray(prods.map(function (p) {\n      return p.date.slice(0, 7);\n    }))));\n    sales.forEach(function (sale) {\n      if (sale.paid && (sale.paidDate || sale.date)) s.add((sale.paidDate || sale.date).slice(0, 7));\n    });\n    return _toConsumableArray(s).sort().reverse();\n  }, [sales, prods]);''','report months')

rep('''  var mPaidRev = mSales.filter(function (s) {\n    return s.paid;\n  }).reduce(function (a, s) {\n    return a + saleTotal(s, kits);\n  }, 0);''','''  var mPaidRev = sales.filter(function (s) {\n    return s.paid && (s.paidDate || s.date).startsWith(selMonth);\n  }).reduce(function (a, s) {\n    return a + saleTotal(s, kits);\n  }, 0);''','report receipts')

rep('''    var rows = [["Data", "Cliente", "Produto", "Quantidade", "Preço", "Total", "Forma", "Status"]];''','''    var rows = [["Data da venda", "Cliente", "Produto", "Quantidade", "Preço", "Total", "Forma na venda", "Status", "Recebido em", "Recebido via"]];''','csv header')
rep('''      rows.push([s.date, s.customer, label, s.qty, s.price.toFixed(2), saleTotal(s, kits).toFixed(2), s.method, s.paid ? "Pago" : "Pendente"]);''','''      rows.push([s.date, s.customer, label, s.qty, s.price.toFixed(2), saleTotal(s, kits).toFixed(2), s.method, s.paid ? "Pago" : "Pendente", s.paid ? (s.paidDate || s.date) : "", s.paid ? (s.paidMethod || s.method) : ""]);''','csv receipt fields')

rep('''  var exportBackup = function exportBackup() {\n    var json = JSON.stringify(allData, null, 2);''','''  var exportBackup = function exportBackup() {\n    var backupData = _objectSpread({\n      _backupMeta: {\n        app: "ComGraca",\n        version: 5,\n        exportedAt: new Date().toISOString()\n      }\n    }, allData);\n    var json = JSON.stringify(backupData, null, 2);''','backup export')

rep('''        var data = JSON.parse(ev.target.result);\n        if (data.sales || data.prods || data.recs) {\n          setAllData(data);\n          alert("✅ Dados restaurados com sucesso!");\n        } else {\n          alert("❌ Arquivo inválido.");\n        }''','''        var data = JSON.parse(ev.target.result);\n        var isObj = data && typeof data === "object" && !Array.isArray(data);\n        var requiredArrays = ["ingrs", "recs", "prods", "sales", "kits", "pack"];\n        var arraysOk = isObj && requiredArrays.every(function (key) { return Array.isArray(data[key]); });\n        var settingsOk = isObj && data.settings && typeof data.settings === "object" && !Array.isArray(data.settings);\n        var metaOk = !data._backupMeta || data._backupMeta.app === "ComGraca";\n        if (arraysOk && settingsOk && metaOk) {\n          setAllData(data);\n          alert("✅ Dados restaurados com sucesso!");\n        } else {\n          alert("❌ Arquivo inválido ou incompatível com o Com Graça.");\n        }''','backup import')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
assert 'const CACHE = "comgraca-v5-isolated-cache";' in w
w = w.replace('const CACHE = "comgraca-v5-isolated-cache";', 'const CACHE = "comgraca-v6-receipts-safe";', 1)
sw.write_text(w, encoding='utf-8')

s2 = p.read_text(encoding='utf-8')
for needle in [
    'paidDate: paid ? form.date : null',
    'paidDate: payDate',
    '(s.paidDate || s.date).startsWith(cm)',
    '(s.paidDate || s.date).startsWith(selMonth)',
    '"Recebido em", "Recebido via"',
    'requiredArrays.every',
    '_backupMeta'
]:
    assert needle in s2, needle
assert s2.count('paidDate: paid ? form.date : null') == 2
assert 'var mPaidRev = mSales.filter' not in s2
assert 'var mRev = mSales.filter' not in s2
assert 'k.startsWith(CACHE_PREFIX)' in sw.read_text(encoding='utf-8')
print('ComGraca patch verified')
