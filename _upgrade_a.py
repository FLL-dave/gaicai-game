# -*- coding: utf-8 -*-
"""智慧版升级：智慧卡/关系图谱/体检报告/短片+配乐入口"""
import io, re

base = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
html = base + r'\韭菜大冒险.html'

with io.open(html, 'r', encoding='utf-8') as f:
    s = f.read()

def sub(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, f'FOUND {n} != {cnt}: {old[:60]}'
    s = s.replace(old, new, cnt)
    print('ok:', old[:34].replace('\n',' '))

# ---------- 1. 开始屏文案 ----------
sub('<p class="sub">打工人财务自由模拟器 · 改编自耶鲁大学《金融市场》公开课（主讲：罗伯特·希勒，2013 年诺贝尔经济学奖得主）</p>',
    '<p class="sub">打工人财务自由模拟器 · 智慧版<br>改编自耶鲁大学《金融市场》公开课（主讲：罗伯特·希勒，2013 年诺贝尔经济学奖得主）</p>')
sub('<li>每年还会解锁一张「希勒小课堂」，把课程里的金融知识装进你的钱包。</li>',
    '<li>每年还会解锁一张「希勒智慧卡」：<b>直觉故事 + 核心公式 + 怎么用 + 希勒原话</b>，把课程里的关系和智慧装进你的钱包。</li>')

# ---------- 2. 开始屏按钮组 ----------
sub('''  <div class="start-wrap">
    <button class="btn btn-primary btn-big" id="btn-start">开始打工</button>
    <button class="btn btn-ghost btn-big" id="btn-help-start">玩法说明</button>
  </div>''',
    '''  <div class="start-wrap">
    <button class="btn btn-primary btn-big" id="btn-start">开始打工</button>
    <button class="btn btn-gold btn-big" id="btn-video">先看智慧短片（90 秒）</button>
    <button class="btn btn-ghost btn-big" id="btn-graph">金融关系图谱</button>
    <button class="btn btn-ghost btn-big" id="btn-help-start">玩法说明</button>
  </div>''')

# ---------- 3. 顶栏配乐开关 ----------
sub('<button class="btn btn-ghost" id="btn-help" style="padding:4px 12px;font-size:12.5px">帮助</button>',
    '<button class="btn btn-ghost" id="btn-music" style="padding:4px 12px;font-size:12.5px" title="播放/暂停原创配乐">配乐</button>\n    <button class="btn btn-ghost" id="btn-help" style="padding:4px 12px;font-size:12.5px">帮助</button>')

# ---------- 4. 课堂卡模态：加公式/运用 ----------
sub('''    <div class="card-body" id="card-body"></div>
    <div class="card-quote" id="card-quote"></div>''',
    '''    <div class="card-body" id="card-body"></div>
    <div class="card-formula" id="card-formula"></div>
    <div class="card-use" id="card-use"></div>
    <div class="card-quote" id="card-quote"></div>''')

# ---------- 5. 结局屏：体检报告 ----------
sub('''    <div class="end-actions">
      <button class="btn btn-primary btn-big" id="btn-restart">再玩一局</button>''',
    '''    <div class="end-report" id="end-report"></div>
    <div class="end-actions">
      <button class="btn btn-primary btn-big" id="btn-restart">再玩一局</button>''')

# ---------- 6. 新增模态（短片/图谱）与配乐 ----------
sub('''    <button class="btn btn-gold m-close" id="btn-help-close">知道了</button>
  </div>
</div>''',
    '''    <button class="btn btn-gold m-close" id="btn-help-close">知道了</button>
  </div>
</div>

<!-- ====== 智慧短片模态 ====== -->
<div class="modal-mask" id="modal-video" hidden>
  <div class="modal modal-wide">
    <div class="card-head"><div class="card-badge serif" style="background:var(--gold)">视</div><div><h3>金融智慧 · 90 秒</h3><div class="card-src">原创短片：画面、旁白、配乐均为原创</div></div></div>
    <video id="wisdom-video" controls preload="metadata" style="width:100%;border-radius:12px;background:#000" src="assets/wisdom.mp4" poster="assets/hero.jpg"></video>
    <p class="muted" style="font-size:13px;margin-top:8px">看一遍，再开始打工：先理解「关系」，再管理你的钱。</p>
    <button class="btn btn-gold m-close" id="btn-video-close">看完了，去打工</button>
  </div>
</div>

<!-- ====== 金融关系图谱模态 ====== -->
<div class="modal-mask" id="modal-graph" hidden>
  <div class="modal modal-wide">
    <div class="card-head"><div class="card-badge serif" style="background:var(--blue)">图</div><div><h3>金融关系图谱</h3><div class="card-src">把课程里的六条核心关系画成一张图：谁牵着谁</div></div></div>
    <svg id="graph-svg" viewBox="0 0 360 260" role="img" aria-label="金融关系图谱">
      <line x1="180" y1="130" x2="268" y2="130" stroke="#C9A227" stroke-width="1.2"/>
      <line x1="180" y1="130" x2="224" y2="208" stroke="#C9A227" stroke-width="1.2"/>
      <line x1="180" y1="130" x2="136" y2="208" stroke="#C9A227" stroke-width="1.2"/>
      <line x1="180" y1="130" x2="92" y2="130" stroke="#C9A227" stroke-width="1.2"/>
      <line x1="180" y1="130" x2="136" y2="52" stroke="#C9A227" stroke-width="1.2"/>
      <line x1="180" y1="130" x2="224" y2="52" stroke="#C9A227" stroke-width="1.2"/>
      <circle cx="180" cy="130" r="42" fill="#F6EDD8" stroke="#C9A227" stroke-width="2"/>
      <text x="180" y="124" text-anchor="middle" font-size="13" font-weight="900" fill="#6B5418">金融市场</text>
      <text x="180" y="141" text-anchor="middle" font-size="10" fill="#8A7F6A">关系与智慧</text>
      <circle cx="268" cy="130" r="30" fill="#FDFBF4" stroke="#D6C28A" stroke-width="1.4"/>
      <text x="268" y="126" text-anchor="middle" font-size="11.5" font-weight="700" fill="#24384A">风险 ⇄ 收益</text>
      <text x="268" y="142" text-anchor="middle" font-size="9" fill="#8A7F6A">承担波动才获报酬</text>
      <circle cx="224" cy="208" r="30" fill="#FDFBF4" stroke="#D6C28A" stroke-width="1.4"/>
      <text x="224" y="204" text-anchor="middle" font-size="11.5" font-weight="700" fill="#24384A">分散 ⇄ 波动</text>
      <text x="224" y="220" text-anchor="middle" font-size="9" fill="#8A7F6A">低相关降波动</text>
      <circle cx="136" cy="208" r="30" fill="#FDFBF4" stroke="#D6C28A" stroke-width="1.4"/>
      <text x="136" y="204" text-anchor="middle" font-size="11.5" font-weight="700" fill="#24384A">情绪 ⇄ 泡沫</text>
      <text x="136" y="220" text-anchor="middle" font-size="9" fill="#8A7F6A">羊群吹大价格</text>
      <circle cx="92" cy="130" r="30" fill="#FDFBF4" stroke="#D6C28A" stroke-width="1.4"/>
      <text x="92" y="126" text-anchor="middle" font-size="11.5" font-weight="700" fill="#24384A">杠杆 ⇄ 脆弱</text>
      <text x="92" y="142" text-anchor="middle" font-size="9" fill="#8A7F6A">放大收益与毁灭</text>
      <circle cx="136" cy="52" r="30" fill="#FDFBF4" stroke="#D6C28A" stroke-width="1.4"/>
      <text x="136" y="48" text-anchor="middle" font-size="11.5" font-weight="700" fill="#24384A">通胀 ⇄ 现金</text>
      <text x="136" y="64" text-anchor="middle" font-size="9" fill="#8A7F6A">钱躺着会缩水</text>
      <circle cx="224" cy="52" r="30" fill="#FDFBF4" stroke="#D6C28A" stroke-width="1.4"/>
      <text x="224" y="48" text-anchor="middle" font-size="11.5" font-weight="700" fill="#24384A">流动性 ⇄ 危机</text>
      <text x="224" y="64" text-anchor="middle" font-size="9" fill="#8A7F6A">应急金救命</text>
    </svg>
    <div class="graph-notes">六条关系对应课程：风险收益（第 4 课 CAPM）、分散化（第 4 课）、行为金融（第 7 课）、杠杆（第 8 课）、通胀（第 8 课）、流动性（第 1 课）。看图顺序：先看中心，再沿每条线问自己——这条关系里，谁是因、谁是果？想明白一条，你的钱就少亏一分。</div>
    <button class="btn btn-gold m-close" id="btn-graph-close">收下这张图</button>
  </div>
</div>

<audio id="bgm" loop preload="none" src="assets/music.mp3"></audio>''')

# ---------- 7. CSS ----------
sub('''/* 响应式 */''',
    '''/* ===== 智慧版 ===== */
.modal-wide{max-width:720px}
.card-formula{margin-top:10px;padding:10px 12px;background:#F3F7FB;border:1px solid #D6E2EC;border-radius:10px;font-size:13.5px;color:#24384A;line-height:1.55}
.card-formula .fl{font-size:11.5px;color:#3D5A77;font-weight:700;letter-spacing:1px;display:block;margin-bottom:4px}
.card-use{margin-top:8px;padding:9px 12px;background:#F6EDD8;border-radius:10px;font-size:13px;color:#6B5418;line-height:1.5}
.card-use .fl{font-size:11px;font-weight:700;letter-spacing:1px;display:block;margin-bottom:3px;color:#B98A2E}
#graph-svg{width:100%;height:auto;border:1px solid #E6DFCE;border-radius:12px;background:#FDFBF4}
.graph-notes{margin-top:10px;font-size:12.5px;color:var(--muted);line-height:1.6}
.end-report{margin-top:16px;text-align:left}
.rep-title{font-weight:900;font-size:15px;margin-bottom:8px}
.rep-verdict{padding:10px 12px;background:var(--gold-bg);border-radius:10px;font-size:13.5px;line-height:1.6;color:#6B5418;margin-bottom:10px}
.rep-list{max-height:210px;overflow:auto;border:1px solid #E6DFCE;border-radius:10px}
.rep-row{display:flex;gap:8px;align-items:flex-start;padding:7px 10px;border-bottom:1px solid #EFE9DA;font-size:12.5px;line-height:1.45}
.rep-row:last-child{border-bottom:none}
.rep-y{white-space:nowrap;color:var(--muted)}
.rep-tag{white-space:nowrap;font-size:11px;padding:1px 6px;border-radius:20px;font-weight:700}
.rep-tag.good{background:#DFEFE5;color:#1E7A4D}
.rep-tag.bad{background:#F7E3DF;color:#BE3B2E}
.rep-tag.neutral{background:#EFE9DA;color:#8A7F6A}

/* 响应式 */''')

with io.open(html, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('PHASE A done, chars:', len(s))
