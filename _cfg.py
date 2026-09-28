# -*- coding: utf-8 -*-
import io, re, json

base = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
html = base + r'\韭菜大冒险.html'

with io.open(html, 'r', encoding='utf-8') as f:
    s = f.read()

m = re.search(r'<script id="game-config" type="application/json">(.*?)</script>', s, re.S)
cfg = json.loads(m.group(1))

def n(v):
    return '{:,}'.format(v) if isinstance(v, int) else v

lines = []
lines.append('ruleset_id=' + cfg['ruleset_id'])
lines.append('start_age=%d total_years=%d goal=%s' % (cfg['start_age'], cfg['total_years'], n(cfg['goal'])))
lines.append('salary_start=%s salary_months=%d expense_start=%s' % (n(cfg['salary_start']), cfg['salary_months'], n(cfg['expense_start'])))
lines.append('salary_growth_base=%s salary_growth_jitter=%s inflation=%s' % (cfg['salary_growth_base'], cfg['salary_growth_jitter'], cfg['inflation']))
lines.append('insurance_monthly=%s kid_extra_monthly=%s step=%s' % (n(cfg['insurance_monthly']), n(cfg['kid_extra_monthly']), n(cfg['step'])))
lines.append('house_price_start=%s down_ratio=%s loan_rate=%s loan_pay_ratio=%s' % (n(cfg['house_price_start']), cfg['house_down_ratio'], cfg['house_loan_rate'], cfg['house_loan_pay_ratio']))
lines.append('market_script=' + ','.join(cfg['market_script']))
lines.append('returns=' + json.dumps(cfg['returns'], ensure_ascii=False))
lines.append('event_amounts=' + json.dumps(cfg['event_amounts'], ensure_ascii=False))
lines.append('ending_thresholds=' + json.dumps(cfg['ending_thresholds'], ensure_ascii=False))

with io.open(base + r'\_cfg.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('\n'.join(lines))
