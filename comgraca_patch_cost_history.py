from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label, count=1):
    global s
    got = s.count(old)
    assert got >= count, f'{label}: expected at least {count}, got {got}'
    s = s.replace(old, new, count)

# Freeze recipe identity and unit cost when production is created.
old_add = '''    setProds(function (prev) {
      return [].concat(_toConsumableArray(prev), [_objectSpread(_objectSpread({}, form), {}, {
        id: uid(),
        batches: +form.batches,
        bars: totalBars
      })]);
    });'''
new_add = '''    var prodCost = recipeCost(selRec);
    setProds(function (prev) {
      return [].concat(_toConsumableArray(prev), [_objectSpread(_objectSpread({}, form), {}, {
        id: uid(),
        batches: +form.batches,
        bars: totalBars,
        recipeName: selRec.name,
        costPerBar: prodCost.fullPerBar,
        costTotal: prodCost.fullPerBar * totalBars
      })]);
    });'''
rep(old_add, new_add, 'production cost snapshot')

# StockTab needs recipeCost to create the snapshot.
rep('''    lowStock = _ref12.lowStock,
    confirm = _ref12.confirm;''','''    lowStock = _ref12.lowStock,
    recipeCost = _ref12.recipeCost,
    confirm = _ref12.confirm;''','StockTab recipeCost prop')

# Historical production display keeps the original recipe name even if recipe is later removed/renamed.
old_hist = '''    }, (rec === null || rec === void 0 ? void 0 : rec.name) || /*#__PURE__*/React.createElement("span", {
      style: {
        color: "var(--mut)",
        fontStyle: "italic"
      }
    }, "Receita removida")),'''
new_hist = '''    }, p.recipeName || (rec === null || rec === void 0 ? void 0 : rec.name) || /*#__PURE__*/React.createElement("span", {
      style: {
        color: "var(--mut)",
        fontStyle: "italic"
      }
    }, "Receita removida")),'''
rep(old_hist, new_hist, 'stock history recipe name')

# Report cost prefers the frozen production snapshot. Old records keep backward-compatible fallback.
old_cost = '''  var mCost = useMemo(function () {
    return mProds.reduce(function (total, p) {
      var rec = recs.find(function (r) {
        return r.id === p.recipeId;
      });
      if (!rec) return total;
      var c = recipeCost(rec);
      return total + c.fullPerBar * p.bars;
    }, 0);
  }, [mProds, recs, recipeCost]);'''
new_cost = '''  var mCost = useMemo(function () {
    return mProds.reduce(function (total, p) {
      if (Number.isFinite(+p.costTotal)) return total + +p.costTotal;
      if (Number.isFinite(+p.costPerBar)) return total + +p.costPerBar * p.bars;
      var rec = recs.find(function (r) {
        return r.id === p.recipeId;
      });
      if (!rec) return total;
      var c = recipeCost(rec);
      return total + c.fullPerBar * p.bars;
    }, 0);
  }, [mProds, recs, recipeCost]);'''
rep(old_cost, new_cost, 'report frozen production cost')

# Report production table also keeps historical recipe name.
old_report_name = '''    }, (rec === null || rec === void 0 ? void 0 : rec.name) || "—"), /*#__PURE__*/React.createElement("td", null, p.batches),'''
new_report_name = '''    }, p.recipeName || (rec === null || rec === void 0 ? void 0 : rec.name) || "—"), /*#__PURE__*/React.createElement("td", null, p.batches),'''
rep(old_report_name, new_report_name, 'report recipe name')

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
w = sw.read_text(encoding='utf-8')
assert 'const CACHE = "comgraca-v6-receipts-safe";' in w
w = w.replace('const CACHE = "comgraca-v6-receipts-safe";', 'const CACHE = "comgraca-v7-cost-history";', 1)
sw.write_text(w, encoding='utf-8')

# Structural invariants.
s2 = p.read_text(encoding='utf-8')
for needle in [
    'recipeName: selRec.name',
    'costPerBar: prodCost.fullPerBar',
    'costTotal: prodCost.fullPerBar * totalBars',
    'Number.isFinite(+p.costTotal)',
    'p.recipeName || (rec === null',
]:
    assert needle in s2, needle
assert s2.count('recipeName: selRec.name') == 1
assert 'return total + c.fullPerBar * p.bars;' in s2  # fallback for legacy records only
w2 = sw.read_text(encoding='utf-8')
assert 'comgraca-v7-cost-history' in w2
assert 'k.startsWith(CACHE_PREFIX)' in w2
print('ComGraca production cost history patch OK')
