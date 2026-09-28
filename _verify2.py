# -*- coding: utf-8 -*-
import io, re, subprocess, os

base = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
html = os.path.join(base, '韭菜大冒险.html')

with io.open(html, 'r', encoding='utf-8') as f:
    s = f.read()

scripts = re.findall(r'<script>(.*?)</script>', s, re.S)
assert len(scripts) == 1, f'found {len(scripts)} game scripts'
tmp = os.path.join(base, '_game.js')
with io.open(tmp, 'w', encoding='utf-8') as f:
    f.write(scripts[0])

r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
print('node exit:', r.returncode)
print(r.stderr[:2000] if r.returncode else 'syntax OK')

# CARDS 可解析性（含新字段）
m = re.search(r'const CARDS=\{(.*?)\n\};', s, re.S)
assert m, 'CARDS not found'
# 用 node 直接 eval 卡片对象
js = 'const CARDS={' + m.group(1) + '};const ks=Object.keys(CARDS);let bad=[];for(const k of ks){const c=CARDS[k];for(const f of ["no","title","src","text","formula","use","quote"]){if(!(f in c))bad.push(k+":"+f);}}console.log("cards="+ks.length+" bad="+JSON.stringify(bad));'
with io.open(os.path.join(base, '_cardcheck.js'), 'w', encoding='utf-8') as f:
    f.write(js)
r = subprocess.run(['node', os.path.join(base, '_cardcheck.js')], capture_output=True, text=True)
print(r.stdout.strip() if r.returncode == 0 else r.stderr[:1500])
