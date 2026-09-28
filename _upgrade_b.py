# -*- coding: utf-8 -*-
"""智慧版升级 B：智慧卡内容 + JS 逻辑（决策日志/卡片渲染/体检报告/新按钮）"""
import io, re

base = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
html = base + r'\韭菜大冒险.html'

with io.open(html, 'r', encoding='utf-8') as f:
    s = f.read()

# ---------- 1. 替换 CARDS（智慧卡：text 直觉 / formula 公式 / use 运用 / quote 原话） ----------
new_cards = '''const CARDS={
  c01:{no:'01',title:'风险与收益',src:'出自第 4 课 · 资产定价模型',text:'想要更高的收益，就得承受更大的波动。高收益从来不免费，它背后是实打实的风险——这叫风险溢价。',formula:'E(R) = Rf + β × [E(Rm) − Rf]（资本资产定价模型：收益 = 无风险利率 + 风险补偿）',use:'看到高收益产品先问一句：多赚的那部分，是用什么风险换来的？',quote:'“永远不要只买债券”——希勒'},
  c02:{no:'02',title:'分散投资',src:'出自第 4 课 · 资产定价模型',text:'别把鸡蛋放在一个篮子里。股票、债券、现金、房产搭配着来，波动小一半，觉都睡得香一点。',formula:'σ组合 = √( Σwi²σi² + 2·ΣΣwi·wj·ρij·σi·σj ) —— 只要相关系数 ρ < 1，组合波动就小于各项之和',use:'配置至少两类低相关资产；别让工资、基金、币全押在同一种涨跌上。',quote:'“组合里最重要的数字，是资产之间的相关性”'},
  c03:{no:'03',title:'羊群效应',src:'出自第 7 课 · 行为金融学',text:'别人赚钱，不等于你也能赚。追涨杀跌、一窝蜂上车，是散户亏钱的头号原因。',formula:'价格 P = 基本面 + 情绪 e(t)，而情绪会自我放大：涨 → 更多人买 → 更涨',use:'当身边人都在晒收益、催你上车时，先离场冷静三天再做决定。',quote:'“市场由人的情绪驱动，而非纯理性”'},
  c04:{no:'04',title:'有效市场',src:'出自第 6 课 · 有效市场只是一半的真相',text:'内幕消息轮不到你。长期看，大多数主动基金跑不赢指数——普通人的好朋友是指数基金。',formula:'EMH：价格 P(t) 已反映全部公开信息 → 主动管理超额收益的期望 ≈ 0',use:'内幕消息别信；长期买指数，省心还省手续费。',quote:'“想打败市场？先问问自己凭什么”'},
  c05:{no:'05',title:'黑天鹅',src:'出自第 2 课 · 在险价值、压力测试与黑天鹅',text:'罕见、影响巨大、无法预测的事件，总会在你毫无防备时到来。所以永远别满仓裸奔，留足缓冲。',formula:'尾部风险：VaR 只覆盖 95%/99% 的场景，剩下的 1% 才是真正的灾难',use:'永远留 3-6 个月应急金；不加杠杆，市场怎么跌都伤不到你的根基。',quote:'“黑天鹅无法预测，只能应对”'},
  c06:{no:'06',title:'泡沫',src:'出自第 1 课 · 金融市场简介',text:'郁金香、南海公司、互联网、楼市……每次泡沫破灭前，都有人说“这次不一样”。',formula:'泡沫：P(t) = 内在价值 V + 乐观溢价 B(t)，B 只增不减，直到最后一个买家进场',use:'房价/币价疯涨时，用「价格 ÷ 价值」问自己：这买卖到底值不值？',quote:'“泡沫的本质，是价格远远脱离价值”'},
  c07:{no:'07',title:'损失厌恶',src:'出自第 7 课 · 行为金融学',text:'亏 100 块的痛，比赚 100 块的乐强烈两倍。所以恐慌割肉、死扛亏损，都是情绪在替你做决定。',formula:'前景理论：v(收益)=x^α，v(损失)=−λ·(−x)^α，λ ≈ 2.25 —— 亏损的心理权重是收益的 2 倍多',use:'亏了想割肉、赚了想加仓时，先停一分钟：别让情绪下单。',quote:'“先处理情绪，再处理账户”'},
  c08:{no:'08',title:'杠杆',src:'出自第 8 课 · 利率、通胀与杠杆',text:'借钱投资，涨的时候赚得多，跌的时候亏得更多，还可能被强制平仓。杠杆是双刃剑，普通人慎用。',formula:'收益 = 杠杆倍数 × 资产涨跌；亏损同样被放大，还可能被强制平仓',use:'任何「借钱投资」的建议，直接划走——杠杆是给专业玩家的，不是给打工人的。',quote:'“杠杆放大收益，也放大毁灭”'},
  c09:{no:'09',title:'生命周期',src:'出自第 1 课 · 金融市场简介',text:'结婚、生娃、买房、养老，人生不同阶段花钱不一样。理财不是一次性操作，而是一辈子的规划。',formula:'储蓄率 s =（收入 − 消费）/ 收入 —— 理财 = 平滑一生的消费曲线',use:'结婚、生娃、买房前先算一笔账：这笔钱占你几年储蓄率？',quote:'“金融产品是帮你平滑一生的消费”'},
  c10:{no:'10',title:'人力资本',src:'出自第 1 课 · 金融市场简介',text:'对年轻人来说，最大的资产是工资。先升职加薪、提升自己，再谈钱生钱——本金来自你的双手。',formula:'PV = Σ CFᵗ / (1+r)ᵗ —— 未来几十年工资的现值，才是你最大的资产',use:'前 5 年最该投资的是技能和工资，而不是 K 线。',quote:'“你的技能才是第一桶金”'},
  c11:{no:'11',title:'保险',src:'出自第 3 课 · 金融市场之保险',text:'用一笔确定的小钱，去换不确定的大灾保障。保险的本质，是集合众人之力共担风险。',formula:'保费 P ≈ 期望损失 E(L) + 运营成本 —— 用确定的小钱换不确定的大灾',use:'先买重疾/医疗险，再买基金——顺序不能反。',quote:'“保险是风险管理，不是投资”'},
  c12:{no:'12',title:'投机 vs 投资',src:'出自第 1 课 · 金融市场简介',text:'投资是参与创造价值，投机是零和博弈。赌场里没有长期赢家——庄家抽水，散户买单。',formula:'零和博弈：你赚的 = 别人亏的 − 交易成本（庄家抽水）',use:'下单前分清楚：这笔钱是「参与创造」，还是「赌别人亏」？',quote:'“投机赚的是别人的亏空”'},
  c13:{no:'13',title:'郁金香泡沫',src:'出自第 7 课 · 行为金融学',text:'1637 年，一株郁金香能换一栋豪宅；2021 年，一个“币”能换一辆豪车。历史总是惊人地重复。',formula:'自我强化：P↑ → 更多买家 → P↑↑ —— 直到没有下一个买家',use:'看到「百年一遇的机会」时，想想郁金香和币圈的结局。',quote:'“人类从历史中学到的唯一教训，就是没学到教训”'},
  c14:{no:'14',title:'应急金与流动性',src:'出自第 1 课 · 金融市场简介',text:'失业、生病、突发意外，都得用现金。先备好 3-6 个月生活费，再谈投资——流动性是救命稻草。',formula:'应急金 = 3~6 × 月支出；流动性资产必须 ≥ 应急金',use:'发工资先划出应急金，剩下的才谈投资。',quote:'“现金流断裂，比亏损更致命”'},
  c15:{no:'15',title:'利率与通胀',src:'出自第 8 课 · 利率、通胀、真实利率',text:'央行一打喷嚏，市场就感冒。现金放着不动，每年被通胀悄悄吃掉 2-3%——钱躺着也会“缩水”。',formula:'真实利率 r ≈ 名义利率 i − 通胀率 π（费雪方程）',use:'现金别囤太多；每年被通胀吃掉的部分，等于你在无声地亏钱。',quote:'“名义利率减去通胀，才是你真正赚到的”'}
};'''

old_cards = re.search(r'const CARDS=\{.*?\n\};', s, re.S)
assert old_cards, 'CARDS block not found'
s = s.replace(old_cards.group(0), new_cards, 1)
print('ok: CARDS replaced')

def sub(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, f'FOUND {n} != {cnt}: {old[:60]}'
    s = s.replace(old, new, cnt)
    print('ok:', old[:34].replace('\n',' '))

# ---------- 2. newGame：初始化决策日志 ----------
sub('history:[],phase:\'event\',result:null,bankrupt:false,resolved:false};',
    'history:[],log:[],phase:\'event\',result:null,bankrupt:false,resolved:false};')

# ---------- 3. 选择点击：记录决策日志 ----------
sub('''      const c=ev.choices[+b.dataset.ci];c.f();
      if(c.q==='good')S.goodDec++;else if(c.q==='bad')S.badDec++;''',
    '''      const c=ev.choices[+b.dataset.ci];c.f();
      if(c.q==='good')S.goodDec++;else if(c.q==='bad')S.badDec++;
      S.log.push({yi:S.yi+1,t:ev.title,l:c.l,q:c.q});''')

# ---------- 4. showCard：渲染公式与运用 ----------
sub('''  $('card-body').textContent=c.text;
  $('card-quote').textContent=c.quote;''',
    '''  $('card-body').textContent=c.text;
  $('card-formula').innerHTML='<span class="fl">核心公式 · 生冷的逻辑</span>'+c.formula;
  $('card-use').innerHTML='<span class="fl">怎么用 · 落进你的钱包</span>'+c.use;
  $('card-quote').textContent=c.quote;''')

# ---------- 5. 体检报告函数 + 结局调用 ----------
sub('''  $('end-dec').textContent=dc;
  show('screen-game',false);show('screen-end',true);''',
    '''  $('end-dec').textContent=dc;
  renderEndReport();
  show('screen-game',false);show('screen-end',true);''')

sub('''/* ===== 初始化 ===== */''',
    '''/* ===== 理财体检报告 ===== */
function renderEndReport(){
  const el=$('end-report');if(!el)return;
  const nw=netWorth();const good=S.goodDec,bad=S.badDec;
  let verdict;
  if(!S.insured)verdict='最大漏洞：没有买保险。第 13 年大病差点击穿你的现金流——保险的公式是「保费 ≈ 期望损失 + 运营成本」，先补铠甲，再谈进攻。';
  else if(bad>good)verdict='决策手滑 '+bad+' 次、神操作 '+good+' 次。行为金融学说得对：损失厌恶（λ≈2.25）和羊群效应都在替你做决定——先处理情绪，再处理账户。';
  else if(nw>=CFG.goal)verdict='你跑通了「分散 + 长期持有」：E(R)=Rf+β·[E(Rm)−Rf] 说的正是——承受波动，市场才付你报酬。这是认知的胜利。';
  else if(nw>=1800000)verdict='稳健老钱路线成立：低相关资产把组合波动 σ 压了下来，剩下的交给时间复利。';
  else verdict='问题多半出在配置与流动性：先备足 3-6 个月应急金（应急金 = 3~6 × 月支出），再谈进攻。';
  let rows='';
  for(const e of S.log){
    const tag=e.q==='good'?'<span class="rep-tag good">神操作</span>':(e.q==='bad'?'<span class="rep-tag bad">骚操作</span>':'<span class="rep-tag neutral">中性</span>');
    rows+='<div class="rep-row"><span class="rep-y">第'+e.yi+'年</span><span style="flex:1">'+e.t+' · '+e.l+'</span>'+tag+'</div>';
  }
  el.innerHTML='<div class="rep-title">理财体检报告</div><div class="rep-verdict">'+verdict+'</div><div class="rep-list">'+(rows||'<div class="rep-row"><span class="rep-y">—</span><span style="flex:1">本局事件均为自动发生，没有留下手滑记录，也是一种本事。</span></div>')+'</div>';
}

/* ===== 初始化 ===== */''')

# ---------- 6. init：新按钮与配乐、短片 ----------
sub('''  $('btn-card-close').addEventListener('click',()=>{$('modal-card').hidden=true;});''',
    '''  $('btn-card-close').addEventListener('click',()=>{$('modal-card').hidden=true;});
  $('btn-video').addEventListener('click',()=>{$('modal-video').hidden=false;});
  $('btn-video-close').addEventListener('click',()=>{$('modal-video').hidden=true;var v=$('wisdom-video');if(v)v.pause();});
  $('modal-video').addEventListener('click',e=>{if(e.target===$('modal-video')){$('modal-video').hidden=true;var v=$('wisdom-video');if(v)v.pause();}});
  $('btn-graph').addEventListener('click',()=>{$('modal-graph').hidden=false;});
  $('btn-graph-close').addEventListener('click',()=>{$('modal-graph').hidden=true;});
  $('modal-graph').addEventListener('click',e=>{if(e.target===$('modal-graph'))$('modal-graph').hidden=true;});
  $('btn-music').addEventListener('click',()=>{
    const a=$('bgm');
    if(a.paused){a.volume=0.5;a.play();$('btn-music').textContent='配乐·关';}
    else{a.pause();$('btn-music').textContent='配乐';}
  });''')

with io.open(html, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('PHASE B done, chars:', len(s))
