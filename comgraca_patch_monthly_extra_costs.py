from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label, count=1):
    global s
    got = s.count(old)
    assert got >= count, f'{label}: expected at least {count}, got {got}'
    s = s.replace(old, new, count)

rep('''  monthGoal: 500,\n  extraCosts: "",\n  markupPct: 150''', '''  monthGoal: 500,\n  extraCosts: "",\n  extraCostsByMonth: {},\n  markupPct: 150''', 'default monthly extra costs')

rep('''    kits = _ref14.kits,\n    settings = _ref14.settings,\n    recipeCost = _ref14.recipeCost,''', '''    kits = _ref14.kits,\n    settings = _ref14.settings,\n    setSettings = _ref14.setSettings,\n    recipeCost = _ref14.recipeCost,''', 'ReportTab setSettings')

old_calc = '''  // custo extra\n  var extraCostVal = parseFloat((settings.extraCosts || "0").replace(",", ".")) || 0;\n  var totalCost = mCost + extraCostVal;'''
new_calc = '''  // custo extra por mês; o campo antigo só serve de compatibilidade para o mês atual\n  var extraCostsByMonth = settings.extraCostsByMonth || {};\n  var hasMonthlyExtra = Object.prototype.hasOwnProperty.call(extraCostsByMonth, selMonth);\n  var extraCostRaw = hasMonthlyExtra ? extraCostsByMonth[selMonth] : selMonth === curMonth() ? settings.extraCosts || "" : "";\n  var extraCostVal = parseFloat(String(extraCostRaw || "0").replace(",", ".")) || 0;\n  var setMonthExtraCost = function setMonthExtraCost(value) {\n    setSettings(function (current) {\n      var byMonth = _objectSpread({}, current.extraCostsByMonth || {});\n      if (value === "") delete byMonth[selMonth];else byMonth[selMonth] = value;\n      return _objectSpread(_objectSpread({}, current), {}, {\n        extraCostsByMonth: byMonth,\n        extraCosts: selMonth === curMonth() ? value : current.extraCosts\n      });\n    });\n  };\n  var totalCost = mCost + extraCostVal;'''
rep(old_calc, new_calc, 'monthly extra cost calculation')

anchor = '''  }, months.length === 0 && /*#__PURE__*/React.createElement("option", {\n    value: curMonth()\n  }, monthLabel(curMonth())), months.map(function (m) {\n    return /*#__PURE__*/React.createElement("option", {\n      key: m,\n      value: m\n    }, monthLabel(m));\n  }))), /*#__PURE__*/React.createElement("button", {'''
replacement = '''  }, months.length === 0 && /*#__PURE__*/React.createElement("option", {\n    value: curMonth()\n  }, monthLabel(curMonth())), months.map(function (m) {\n    return /*#__PURE__*/React.createElement("option", {\n      key: m,\n      value: m\n    }, monthLabel(m));\n  }))), /*#__PURE__*/React.createElement("div", {\n    style: {\n      minWidth: 170\n    }\n  }, /*#__PURE__*/React.createElement("div", {\n    className: "flbl",\n    style: {\n      marginBottom: 4\n    }\n  }, "⚡ Custo extra do mês (R$)"), /*#__PURE__*/React.createElement("input", {\n    className: "inp",\n    type: "number",\n    step: "5",\n    min: "0",\n    value: extraCostRaw,\n    placeholder: "Ex: 30",\n    onChange: function onChange(e) {\n      return setMonthExtraCost(e.target.value);\n    }\n  })), /*#__PURE__*/React.createElement("button", {'''
rep(anchor, replacement, 'report month extra-cost editor')

old_config = '''  }, "\\u26A1 Custos extras mensais (R$)"), /*#__PURE__*/React.createElement("input", {\n    className: "inp",\n    type: "number",\n    step: "5",\n    value: settings.extraCosts || "",\n    placeholder: "Ex: 30",\n    onChange: function onChange(e) {\n      return setSettings(function (s) {\n        return _objectSpread(_objectSpread({}, s), {}, {\n          extraCosts: e.target.value\n        });\n      });\n    }\n  }),'''
new_config = '''  }, "\\u26A1 Custo extra do mês atual (R$)"), /*#__PURE__*/React.createElement("input", {\n    className: "inp",\n    type: "number",\n    step: "5",\n    min: "0",\n    value: settings.extraCostsByMonth && Object.prototype.hasOwnProperty.call(settings.extraCostsByMonth, curMonth()) ? settings.extraCostsByMonth[curMonth()] : settings.extraCosts || "",\n    placeholder: "Ex: 30",\n    onChange: function onChange(e) {\n      var value = e.target.value;\n      return setSettings(function (current) {\n        var byMonth = _objectSpread({}, current.extraCostsByMonth || {});\n        if (value === "") delete byMonth[curMonth()];else byMonth[curMonth()] = value;\n        return _objectSpread(_objectSpread({}, current), {}, {\n          extraCosts: value,\n          extraCostsByMonth: byMonth\n        });\n      });\n    }\n  }),'''
rep(old_config, new_config, 'config current-month extra cost')

rep('''    kits: kits,\n    settings: settings,\n    recipeCost: recipeCost,''', '''    kits: kits,\n    settings: settings,\n    setSettings: setSettings,\n    recipeCost: recipeCost,''', 'ReportTab prop')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
assert 'const CACHE = "comgraca-v7-cost-history";' in w, 'expected v7 cache anchor'
w = w.replace('const CACHE = "comgraca-v7-cost-history";', 'const CACHE = "comgraca-v8-monthly-extra-costs";', 1)
sw.write_text(w, encoding='utf-8')

s2 = p.read_text(encoding='utf-8')
for needle in [
    'extraCostsByMonth: {}',
    'setSettings = _ref14.setSettings',
    'hasMonthlyExtra',
    'setMonthExtraCost',
    'Custo extra do mês (R$)',
    'Custo extra do mês atual (R$)',
    'setSettings: setSettings'
]:
    assert needle in s2, needle
assert 'var extraCostVal = parseFloat((settings.extraCosts || "0")' not in s2
assert 'comgraca-v8-monthly-extra-costs' in sw.read_text(encoding='utf-8')
print('ComGraca monthly extra cost patch OK')
