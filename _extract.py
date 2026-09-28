# -*- coding: utf-8 -*-
import io, re, json, sys

base = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
html = base + r'\韭菜大冒险.html'

with io.open(html, 'r', encoding='utf-8') as f:
    s = f.read()

m = re.search(r'<script id="game-config" type="application/json">(.*?)</script>', s, re.S)
assert m, 'config not found'
cfg = json.loads(m.group(1))

out = []
out.append('ruleset_id = ' + cfg['ruleset_id'])
out.append('start_age=%s total_years=%s goal=%s' % (cfg['start_age'], cfg['total_years'], cfg['goal']))
out.append('salary_start=%s salary_months=%s expense_start=%s' % (cfg['salary_start'], cfg['salary_months'], cfg['expense_start']))
out.append('salary_growth_base=%s salary_growth_jitter=%s inflation=%s' % (cfg['salary_growth_base'], cfg['salary_growth_jitter'], cfg['inflation']))
out.append('insurance_monthly=%s kid_extra_monthly=%s step=%s' % (cfg['insurance_monthly'], cfg['kid_extra_monthly'], cfg['step']))
out.append('house_price_start=%s down_ratio=%s loan_rate=%s loan_pay_ratio=%s' % (cfg['house_price_start'], cfg['house_down_ratio'], cfg['house_loan_rate'], cfg['house_loan_pay_ratio']))
out.append('market_script = ' + ','.join(cfg['market_script']))
out.append('returns = ' + json.dumps(cfg['returns'], ensure_ascii=False))
out.append('event_amounts = ' + json.dumps(cfg['event_amounts'], ensure_ascii=False))
out.append('ending_thresholds = ' + json.dumps(cfg['ending_thresholds'], ensure_ascii=False))

# EVENTS / CARDS 定义（内联 JS，取 EVENTS 数组与 CARDS 数量）
ev = re.search(r'const EVENTS=(\[.*?\]);', s, re.S)
cards = re.search(r'const CARDS=(\[.*?\]);', s, re.S)
if ev:
    arr = json.loads(ev.group(1))
    out.append('EVENTS count=%d' % len(arr))
    for e in arr:
        line = '  y%s t=%s' % (e['y'], e['t'])
        if e['t'] == 'choice':
            line += ' q=%s' % e['q']
            for c in e['choices']:
                line += ' | ' + c['label'] + ' ~ ' + str(c.get('score', ''))
        out.append(line)
if cards:
    arr = json.loads(cards.group(1))
    out.append('CARDS count=%d' % len(arr))
    for c in arr:
        out.append('  y%s: %s' % (c['y'], c['t']))

with io.open(base + r'\_extract.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('extracted to _extract.txt, lines:', len(out))
print('\n'.join(out[:12]))
