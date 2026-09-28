# -*- coding: utf-8 -*-
"""数值验证：从游戏 HTML 提取配置 JSON，用同一套数值模拟 4 种玩家策略的结局分布。"""
import json, re, os, random, statistics

BASE = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
HTML = os.path.join(BASE, '韭菜大冒险.html')

with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script id="game-config" type="application/json">(.*?)</script>', html, re.S)
assert m, 'config not found'
CFG = json.loads(m.group(1))
print('ruleset:', CFG['ruleset_id'])
print('config keys:', list(CFG.keys()))

EAM = CFG['event_amounts']
MARKETS = CFG['market_script']
TOTAL = CFG['total_years']
R = CFG['returns']

# ---------------- 随机（与游戏 JS 的 mulberry32 逐位一致） ----------------
import math

def jround(x):
    """与 JS Math.round 一致的取整。"""
    return math.floor(x + 0.5)

def make_rng(a):
    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xffffffff
        t = (a ^ (a >> 15)) & 0xffffffff
        t = (t * ((1 | a) & 0xffffffff)) & 0xffffffff
        t = ((t + ((t ^ (t >> 7)) & 0xffffffff) * ((61 | t) & 0xffffffff)) & 0xffffffff) ^ t
        return ((t ^ (t >> 14)) & 0xffffffff) / 4294967296
    return nxt

class RNG:
    def __init__(self, seed):
        self.f = make_rng(seed & 0xffffffff)
    def next(self):
        return self.f()
    def uni(self, a, b):
        return a + self.f() * (b - a)
    def choice(self, pool):
        return pool[int(self.f() * len(pool))]

# ---------------- 状态 ----------------
def new_state(rng):
    return dict(yi=-1, salary=CFG['salary_start'], expense=CFG['expense_start'],
                cash=0, bond=0, stock=0, hot=0, crypto=0,
                house={'owned': False, 'value': 0, 'loan': 0}, housePrice=CFG['house_price_start'],
                insured=False, kid=False, unemployed=False, side=False, rateBonus=False,
                debt=None, relReturn=None, IV=0)

def netWorth(s):
    h = s['house']['value'] - s['house']['loan'] if s['house']['owned'] else 0
    return s['cash'] + s['bond'] + s['stock'] + s['hot'] + s['crypto'] + h

def downPay(s):
    return jround(s['housePrice'] * CFG['house_down_ratio'])

def buyHouse(s):
    p = jround(s['housePrice']); d = downPay(s)
    s['cash'] -= d
    s['house'] = {'owned': True, 'value': p, 'loan': jround(p * 0.7)}

def sellHouse(s):
    net = jround((s['house']['value'] - s['house']['loan']) * 0.98)
    s['cash'] += net
    s['house'] = {'owned': False, 'value': 0, 'loan': 0}

def forceSell(s):
    for k in ['hot', 'crypto', 'stock', 'bond']:
        if s['cash'] >= 0: break
        need = -s['cash']
        take = min(s[k], (need * 20 + 18) // 19)  # ceil(need/0.95)
        s['cash'] += jround(take * 0.95)
        s[k] -= take
        s['IV'] -= take

# ---------------- 事件效果（choice index 与游戏 JS 一一对应） ----------------
def apply_event(s, yi, choice):
    if yi == 0: return                                  # 工资条
    if yi == 1:
        if choice == 0: s['hot'] += EAM['fomo_hot']; s['cash'] -= EAM['fomo_hot']; s['IV'] += EAM['fomo_hot']
        elif choice == 1: s['stock'] += EAM['fomo_stock']; s['cash'] -= EAM['fomo_stock']; s['IV'] += EAM['fomo_stock']
    elif yi == 2:
        s['salary'] = jround(s['salary'] * (1 + EAM['raise1']))
    elif yi == 3:
        if choice == 0: s['cash'] += jround(s['stock'] * EAM['panic_sell_rate']); s['IV'] -= s['stock']; s['stock'] = 0
        elif choice == 1: s['stock'] += EAM['dip_invest']; s['cash'] -= EAM['dip_invest']; s['IV'] += EAM['dip_invest']
        elif choice == 2: s['stock'] += EAM['debt_borrow']; s['IV'] += EAM['debt_borrow']; s['debt'] = {'pay': EAM['debt_pay'], 'due': s['yi'] + 1}
    elif yi == 4:
        if choice == 0: s['cash'] -= EAM['wedding_big']
        elif choice == 1: s['cash'] -= EAM['wedding_small']
    elif yi == 5:
        if choice == 0: s['unemployed'] = True
        elif choice == 1:
            amt = jround(s['stock'] * EAM['unemployment_sell_ratio'])
            s['cash'] += jround(amt * EAM['unemployment_sell_rate']); s['stock'] -= amt; s['IV'] -= amt; s['unemployed'] = True
        elif choice == 2: s['cash'] += EAM['family_support']; s['unemployed'] = True
    elif yi == 6:
        if choice == 0: s['kid'] = True
    elif yi == 7:
        if choice == 0: s['hot'] += EAM['insider_hot']; s['cash'] -= EAM['insider_hot']; s['IV'] += EAM['insider_hot']
        elif choice == 2: s['hot'] += EAM['insider_try']; s['cash'] -= EAM['insider_try']; s['IV'] += EAM['insider_try']
    elif yi == 8:
        if choice == 0:
            if s['cash'] >= downPay(s): buyHouse(s)
            else: s['cash'] -= 5000
        elif choice == 2:
            if s['house']['owned']: sellHouse(s)
    elif yi == 9: pass                                   # 崩盘 auto
    elif yi == 10:
        if choice == 0: s['cash'] -= EAM['relative_borrow']; s['relReturn'] = s['yi'] + EAM['relative_return_year']
    elif yi == 11:
        if choice == 0: s['cash'] += jround(s['stock'] * EAM['panic2_sell_rate']); s['IV'] -= s['stock']; s['stock'] = 0
        elif choice == 1: s['stock'] += EAM['dip_invest']; s['cash'] -= EAM['dip_invest']; s['IV'] += EAM['dip_invest']
    elif yi == 12:
        pay = EAM['sick_insured_pay'] if s['insured'] else EAM['sick_cost']
        s['cash'] -= pay
        if s['cash'] < 0: forceSell(s)
    elif yi == 13:
        if choice == 0:
            if rng_ref.next() < EAM['lottery_p']: s['cash'] += EAM['lottery_win']
            else: s['cash'] -= EAM['lottery_cost']
        elif choice == 1: s['side'] = True
    elif yi == 14:
        if choice == 0: s['crypto'] += EAM['crypto_allin']; s['cash'] -= EAM['crypto_allin']; s['IV'] += EAM['crypto_allin']
        elif choice == 2: s['crypto'] += EAM['crypto_try']; s['cash'] -= EAM['crypto_try']; s['IV'] += EAM['crypto_try']
    elif yi == 15:
        s['crypto'] = jround(s['crypto'] * EAM['crypto_crash_mult'])
    elif yi == 16:
        if choice == 0: s['cash'] -= EAM['parents_sick_cost']
    elif yi == 17:
        s['rateBonus'] = True
    elif yi == 18:
        s['salary'] = jround(s['salary'] * (1 + EAM['raise2']))
    # yi 19,20: 无效果

rng_ref = RNG(1)  # lottery 用独立 rng 引用（在策略循环内重置）

# ---------------- 一年结算 ----------------
def settle_year(s, rng):
    yi = s['yi']; mkt = MARKETS[yi]; rr = R[mkt]
    income = (0 if s['unemployed'] else s['salary'] * CFG['salary_months']) + (EAM['side_income'] if s['side'] else 0)
    living = s['expense'] * 12
    ins = CFG['insurance_monthly'] * 12 if s['insured'] else 0
    mrtg = 0
    if s['house']['owned']:
        mrtg = jround(s['house']['loan'] * CFG['house_loan_pay_ratio'])
        s['house']['loan'] = jround(s['house']['loan'] * (1 + CFG['house_loan_rate'] - CFG['house_loan_pay_ratio']))
    s['cash'] += income - living - ins - mrtg
    if s['debt'] and s['debt']['due'] == yi:
        s['cash'] -= s['debt']['pay']; s['debt'] = None
    if s['relReturn'] is not None and s['relReturn'] == yi:
        s['cash'] += EAM['relative_back']; s['relReturn'] = None
    if s['cash'] < 0: forceSell(s)
    for k in ['bond', 'stock', 'hot', 'crypto']:
        if s[k] == 0: continue
        r = rng.uni(rr[k][0], rr[k][1])
        if k == 'bond' and s['rateBonus']: r += 0.01
        s[k] = jround(s[k] * (1 + r))
    if s['house']['owned']:
        hr = rng.uni(rr['house'][0], rr['house'][1])
        if s['rateBonus']: hr += 0.03
        s['house']['value'] = jround(s['house']['value'] * (1 + hr))
        s['housePrice'] = jround(s['housePrice'] * (1 + hr))
    else:
        hr = rng.uni(rr['house'][0], rr['house'][1])
        s['housePrice'] = jround(s['housePrice'] * (1 + hr))

# ---------------- 分配策略 ----------------
def rebalance(s, cash_share, bond_share, stock_share):
    total = s['cash'] + s['bond'] + s['stock'] + s['hot'] + s['crypto']
    ds = jround(stock_share * total) - s['stock']
    db = jround(bond_share * total) - s['bond']
    if ds > 0:
        d = min(ds, s['cash']); s['cash'] -= d; s['stock'] += d; s['IV'] += d
    else:
        d = min(-ds, s['stock']); s['stock'] -= d; s['cash'] += d; s['IV'] -= d
    if db > 0:
        d = min(db, s['cash']); s['cash'] -= d; s['bond'] += d; s['IV'] += d
    else:
        d = min(-db, s['bond']); s['bond'] -= d; s['cash'] += d; s['IV'] -= d

STRATEGIES = {
    'S1_保守现金党': dict(ins=True, choices={1:2,3:1,4:1,5:0,6:1,7:1,8:1,10:1,11:2,13:2,14:1,16:1}, house_after=None, alloc=lambda s, rng: rebalance(s, 0.80, 0.20, 0.00)),
    'S2_稳健定投党': dict(ins=True, choices={1:1,3:1,4:1,5:0,6:1,7:1,8:1,10:1,11:1,13:1,14:1,16:0}, house_after=7, alloc=lambda s, rng: rebalance(s, 0.10, 0.30, 0.60)),
    'S3_追热点赌徒': dict(ins=False, choices={1:0,3:2,4:0,5:1,6:0,7:0,8:0,10:0,11:0,13:0,14:0,16:1}, house_after=8, alloc='gamble'),
    'S4_随机玩家':  dict(ins=None, choices=None, house_after=7, alloc=None),
}

def run_strategy(name, cfg_s, seeds):
    res = []
    for seed in range(seeds):
        rng = RNG(seed + 1)
        rng_ref = RNG(seed + 99991)  # 彩票独立随机
        globals()['rng_ref'] = rng_ref
        s = new_state(rng)
        s['insured'] = cfg_s['ins'] if cfg_s['ins'] is not None else (rng.next() < 0.5)
        bankrupt = False
        for yi in range(TOTAL):
            s['yi'] = yi
            if yi > 0:
                s['salary'] = jround(s['salary'] * (1 + CFG['salary_growth_base'] + (rng.next() - 0.5) * 2 * CFG['salary_growth_jitter']))
            s['expense'] = jround(CFG['expense_start'] * (1 + CFG['inflation']) ** yi + (CFG['kid_extra_monthly'] if s['kid'] else 0))
            s['unemployed'] = False; s['side'] = False; s['rateBonus'] = False
            # 事件
            if name == 'S4_随机玩家':
                choice_pool = {1:[0,1,2],3:[0,1,2],4:[0,1,2],5:[0,1,2],6:[0,1],7:[0,1,2],8:[0,1,2],10:[0,1],11:[0,1,2],13:[0,1,2],14:[0,1,2],16:[0,1]}
                choice = rng.choice(choice_pool.get(yi, [0]))
            else:
                choice = cfg_s['choices'].get(yi, 0)
            apply_event(s, yi, choice)
            # 分配
            if name == 'S3_追热点赌徒':
                # 留 30% 现金，其余梭哈热点；币圈狂热时转一半币圈
                total = s['cash'] + s['hot'] + s['crypto']
                keep = jround(0.30 * total)
                excess = s['cash'] - keep
                if excess >= CFG['step'] and s['yi'] < 14:
                    s['hot'] += excess; s['IV'] += excess; s['cash'] -= excess
                if s['yi'] == 14:
                    mv = s['hot'] // 2
                    s['crypto'] += mv; s['hot'] -= mv
            elif name == 'S4_随机玩家':
                t = s['cash'] + s['bond'] + s['stock'] + s['hot'] + s['crypto']
                if t > 0:
                    cs, bs, st, ho, cr = 0.1, 0.1, 0.1, 0.1, 0.1
                    shares = [rng.next() for _ in range(5)]
                    tot = sum(shares)
                    shares = [x / tot for x in shares]
                    for k, sh in zip(['cash', 'bond', 'stock', 'hot', 'crypto'], shares):
                        if k == 'cash': continue
                        d = jround(sh * t) - s[k]
                        if d > 0:
                            dd = min(d, s['cash']); s['cash'] -= dd; s[k] += dd; s['IV'] += dd
                        else:
                            dd = min(-d, s[k]); s[k] -= dd; s['cash'] += dd; s['IV'] -= dd
            else:
                cfg_s['alloc'](s, rng)
            # 买房（策略时机后且买得起）
            ha = cfg_s.get('house_after')
            if ha is not None and not s['house']['owned'] and s['yi'] >= ha and s['cash'] >= downPay(s):
                if name != 'S4_随机玩家' or rng.next() < 0.3:
                    buyHouse(s)
            # 结算
            settle_year(s, rng)
            if netWorth(s) < 0:
                bankrupt = True
                break
        res.append((netWorth(s), bankrupt))
    return res

def report(name, res):
    nws = [r[0] for r in res]
    nws_sorted = sorted(nws)
    n = len(nws_sorted)
    med = nws_sorted[n // 2]
    p25 = nws_sorted[int(n * 0.25)]
    p75 = nws_sorted[int(n * 0.75)]
    br = sum(1 for r in res if r[1]) / n
    g120 = sum(1 for x in nws if x >= CFG['goal']) / n
    g180 = sum(1 for x in nws if x >= 1800000) / n
    g80 = sum(1 for x in nws if x >= 800000) / n
    g40 = sum(1 for x in nws if x >= 400000) / n
    print(f"{name}: 中位 {med/10000:.1f}万 | P25 {p25/10000:.1f}万 | P75 {p75/10000:.1f}万")
    print(f"   破产率 {br*100:.1f}% | ≥300万 {g120*100:.1f}% | ≥180万 {g180*100:.1f}% | ≥80万 {g80*100:.1f}%")
    return med

print()
for name, cfg_s in STRATEGIES.items():
    res = run_strategy(name, cfg_s, 3000)
    report(name, res)
