
/* ===== 常量与工具 ===== */
const CFG = JSON.parse(document.getElementById('game-config').textContent);
const $ = id => document.getElementById(id);
const EAM = CFG.event_amounts;
const MARKETS = CFG.market_script;
const TOTAL_YEARS = CFG.total_years;

function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
let rng = mulberry32(1);
function rnd(a,b){return a+rng()*(b-a);}
function wan(n){const w=Math.round(Math.abs(n)/10000*10)/10;return (n<0?'-':'')+w+'万';}
function full(n){return n.toLocaleString('zh-CN')+' 元';}
function pct(n){return (n>=0?'+':'')+(n*100).toFixed(1)+'%';}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function show(id,on){$(id).hidden=!on;}

const MKT_LABEL={bull:['疯牛','mkt-bull'],bear:['大熊','mkt-bear'],flat:['震荡','mkt-flat'],bubble:['楼市泡沫','mkt-bubble'],crash:['崩盘','mkt-crash']};
const MKT_FLAVOR={
  bull:'今年是疯牛行情，市场一片欢腾，人人都是股神。',
  bear:'今年大熊出没，账户绿得发慌，新闻里全是坏消息。',
  flat:'今年是震荡市，涨涨跌跌来回磨人，适合静观其变。',
  bubble:'今年楼市狂热，房价疯涨，泡沫越吹越大。',
  crash:'今年崩盘时刻，资产价格一地鸡毛。'
};
const ASSET_ORDER=['bond','stock','hot','crypto'];
const ASSET_LABEL={
  cash:{n:'现金 / 余额宝',h:'活期灵活，随时可用',c:'#3D5A77',bg:'#E4EBF2'},
  bond:{n:'债券基金',h:'稳稳的幸福',c:'#B98A2E',bg:'#F6EDD8'},
  stock:{n:'指数基金',h:'长期主力，波动中等',c:'#1E7A4D',bg:'#DFEFE5'},
  hot:{n:'热点股票',h:'刺激，但九死一生',c:'#BE3B2E',bg:'#F7E3DF'},
  crypto:{n:'币圈 / 合约',h:'赌场，谨慎进入',c:'#7A4FA0',bg:'#EFE6F6'}
};
const ICON={
  cash:'<path d="M4 7h13a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h12"/><path d="M16 13h1.5a1 1 0 0 0 0-2H16v2z"/>',
  bond:'<path d="M5 19V12"/><path d="M10 19V6"/><path d="M15 19v-5"/><path d="M20 19V9"/>',
  stock:'<path d="M3 17l6-6 4 4 7-8"/><path d="M14 7h7v7"/>',
  hot:'<path d="M12 3c1 3 5 4.5 5 9a5 5 0 0 1-10 0c0-2 1-3.5 2-5 .5 1 1 1.5 1 2 .5-2 1-4 2-6z"/>',
  crypto:'<circle cx="12" cy="12" r="9"/><path d="M9.5 8.5v7"/><path d="M9.5 12h5.5a1.5 1.5 0 0 0 0-3H9.5"/><path d="M10.5 15h5a1.5 1.5 0 0 1 0 3h-5"/>'
};

/* ===== 知识卡（15 张，对应课程） ===== */
const CARDS={
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
};

/* ===== 年度事件（21 个财年，对应课程知识） ===== */
const EVENTS=[
  {t:'auto',title:'工资条到账',desc:'24 岁，你正式成为都市打工人。月薪 8000，交完房租水电、还完花呗，每个月能攒下小几千。记住：理财的第一桶金，就从今天开始攒。',f(){},card:'c01'},
  {t:'choice',title:'牛市来了！朋友圈都在晒收益',desc:'“基金一天赚了三个月工资！” 同事老王晒收益截图，你刷了十条朋友圈，全是红。你有点心动。',choices:[
    {l:'跟风追热点，投 5 万进热点股',tip:'可能大赚，也可能接盘',q:'bad',f(){S.hot+=EAM.fomo_hot;S.cash-=EAM.fomo_hot;IV+=EAM.fomo_hot;}},
    {l:'分批定投 5 万指数基金',tip:'不预测市场，慢慢来',q:'good',f(){S.stock+=EAM.fomo_stock;S.cash-=EAM.fomo_stock;IV+=EAM.fomo_stock;}},
    {l:'按兵不动，继续攒钱',tip:'市场涨跌与我无关',q:'neutral',f(){}}
  ],card:'c03'},
  {t:'auto',title:'升职加薪！',desc:'努力被看见，领导给你升职，月薪 +20%。工资是年轻人最重要的资产——先提高它，再谈理财。',f(){S.salary=Math.round(S.salary*(1+EAM.raise1));},card:'c10'},
  {t:'choice',title:'黑天鹅来袭：金融危机',desc:'某大型机构突然暴雷，市场闪崩，新闻滚动播放“熊市来了”。你的账户一片绿。',choices:[
    {l:'恐慌清仓，保住本金',tip:'把指数基金都卖了，落袋为安',q:'bad',f(){S.cash+=Math.round(S.stock*EAM.panic_sell_rate);IV-=S.stock;S.stock=0;}},
    {l:'按兵不动，坚持定投',tip:'危机也是机会',q:'good',f(){S.stock+=EAM.dip_invest;S.cash-=EAM.dip_invest;IV+=EAM.dip_invest;}},
    {l:'向亲戚借 10 万抄底！',tip:'高利贷，明年要还 12 万',q:'bad',f(){S.stock+=EAM.debt_borrow;IV+=EAM.debt_borrow;S.debt={pay:EAM.debt_pay,due:S.yi+1};}}
  ],card:'c05'},
  {t:'choice',title:'要结婚了',desc:'另一半想办一场体面的婚礼。两边家长都在催：一辈子就一次，不能省！',choices:[
    {l:'大操大办，花 15 万',tip:'面子有了，钱包空了',q:'bad',f(){S.cash-=EAM.wedding_big;}},
    {l:'简办，花 5 万',tip:'把钱留给小家庭',q:'good',f(){S.cash-=EAM.wedding_small;}},
    {l:'裸婚领证，一分不花',tip:'真爱不需要排场',q:'neutral',f(){}}
  ],card:'c02'},
  {t:'choice',title:'公司裁员，你失业了',desc:'行业寒冬，你被“优化”了。今年没有工资收入，房贷、房租、饭钱一样不少。',choices:[
    {l:'动用存款硬扛',tip:'现金为王，先活下来',q:'neutral',f(){S.unemployed=true;}},
    {l:'卖 30% 指数基金应急',tip:'割肉换现金流',q:'bad',f(){const amt=Math.round(S.stock*EAM.unemployment_sell_ratio);S.cash+=Math.round(amt*EAM.unemployment_sell_rate);S.stock-=amt;IV-=amt;S.unemployed=true;}},
    {l:'找父母支援 3 万',tip:'啃老一时，不丢人',q:'neutral',f(){S.cash+=EAM.family_support;S.unemployed=true;}}
  ],card:'c14'},
  {t:'choice',title:'要不要生娃？',desc:'家里开始催了。孩子是甜蜜的负担，有了娃每月多花 2500 奶粉钱。',choices:[
    {l:'生！',tip:'每月支出 +2500',q:'neutral',f(){S.kid=true;}},
    {l:'先打拼几年再说',tip:'把精力留给事业',q:'neutral',f(){}}
  ],card:'c09'},
  {t:'choice',title:'“内幕消息”？',desc:'“我表哥的同事的邻居说，某只股票下个月翻倍，内部人透露的！” 对方信誓旦旦。',choices:[
    {l:'信了！重仓 5 万',tip:'天上掉馅饼？',q:'bad',f(){S.hot+=EAM.insider_hot;S.cash-=EAM.insider_hot;IV+=EAM.insider_hot;}},
    {l:'无视，继续按计划',tip:'有效市场：便宜消息轮不到你',q:'good',f(){}},
    {l:'小打小闹试 1 万',tip:'忍不住手痒',q:'bad',f(){S.hot+=EAM.insider_try;S.cash-=EAM.insider_try;IV+=EAM.insider_try;}}
  ],card:'c04'},
  {t:'choice',title:'楼市泡沫：房价暴涨！',desc:'房价一年涨了 40%，中介天天轰炸：“现在不上车，永远上不了车！” 首付 30 万起步。',choices:[
    {l:'加杠杆上车买房',tip:'首付需现金 ≥ 房价 30%',q:'bad',f(){if(S.cash>=downPay()){buyHouse();}else{S.cash-=5000;}}},
    {l:'观望，不追高',tip:'泡沫总会破',q:'good',f(){}},
    {l:'趁机卖房套现',tip:'如果有房的话',q:'neutral',f(){if(S.house.owned){sellHouse();}}}
  ],card:'c06'},
  {t:'auto',title:'崩盘时刻：楼市腰斩 + 股灾',desc:'调控落地，房价大跌，股市跟着遭殃。当初加杠杆上车的人，正在被按揭按在地上摩擦。',f(){},card:'c08'},
  {t:'choice',title:'亲戚来借钱',desc:'“哥/姐，最近急用钱，借 5 万周转一下？下个月就还！” 你们关系还不错。',choices:[
    {l:'借！都是亲戚',tip:'大概率两年后还你 1 万',q:'bad',f(){S.cash-=EAM.relative_borrow;S.relReturn=S.yi+EAM.relative_return_year;}},
    {l:'委婉拒绝',tip:'救急不救穷，量力而行',q:'good',f(){}}
  ],card:'c15'},
  {t:'choice',title:'大熊市，账户又绿了',desc:'指数跌了 30%，基金评论区全是“割肉离场”“再也不玩了”。你握着亏损的账户，夜不能寐。',choices:[
    {l:'割肉清仓，再也不玩了',tip:'损失厌恶：亏了就想逃',q:'bad',f(){S.cash+=Math.round(S.stock*EAM.panic2_sell_rate);IV-=S.stock;S.stock=0;}},
    {l:'坚持定投，越跌越买',tip:'微笑曲线的秘密',q:'good',f(){S.stock+=EAM.dip_invest;S.cash-=EAM.dip_invest;IV+=EAM.dip_invest;}},
    {l:'躺平不动，不看账户',tip:'时间是好资产的朋友',q:'neutral',f(){}}
  ],card:'c07'},
  {t:'auto',title:'突发大病住院',desc:'一场重病，医疗费 25 万。',f(){const pay=S.insured?EAM.sick_insured_pay:EAM.sick_cost;S.cash-=pay;if(S.cash<0){forceSell();}},card:'c11'},
  {t:'choice',title:'彩票店 + 副业机会',desc:'下班路过彩票店，老板说今晚头奖 500 万；同事又介绍了个靠谱副业，每月能多赚 2000。',choices:[
    {l:'花 200 块买张彩票',tip:'5% 概率中 5 万',q:'bad',f(){if(rng()<EAM.lottery_p){S.cash+=EAM.lottery_win;}else{S.cash-=EAM.lottery_cost;}}},
    {l:'接个靠谱副业',tip:'今年收入 +24000',q:'good',f(){S.side=true;}},
    {l:'算了，好好休息',tip:'休息也是投资',q:'neutral',f(){}}
  ],card:'c12'},
  {t:'choice',title:'币圈狂欢：一夜暴富神话',desc:'“XX币三天翻倍！” 群里有人晒出百万收益截图，配文：感谢币圈，改变命运。',choices:[
    {l:'梭哈 5 万进场',tip:'赌场里没有长期赢家',q:'bad',f(){S.crypto+=EAM.crypto_allin;S.cash-=EAM.crypto_allin;IV+=EAM.crypto_allin;}},
    {l:'不碰，赚认知内的钱',tip:'投机不是投资',q:'good',f(){}},
    {l:'小额 1 万试试水',tip:'手痒，但控制风险',q:'neutral',f(){S.crypto+=EAM.crypto_try;S.cash-=EAM.crypto_try;IV+=EAM.crypto_try;}}
  ],card:'c13'},
  {t:'auto',title:'币圈崩盘：归零时刻',desc:'“XX币”价格归零，群主退群，暴富神话碎了一地。你的币，只剩四分之一的残值。',f(){S.crypto=Math.round(S.crypto*EAM.crypto_crash_mult);},card:'c13'},
  {t:'choice',title:'父母生病住院',desc:'爸/妈需要手术，医保报销后仍需自付 10 万。',choices:[
    {l:'出钱，倾力救治',tip:'家庭责任，义不容辞',q:'good',f(){S.cash-=EAM.parents_sick_cost;}},
    {l:'先保守治疗凑合',tip:'省了钱，亏了心',q:'bad',f(){}}
  ],card:'c11'},
  {t:'auto',title:'央行降息',desc:'央行下调基准利率，债券价格上涨，房贷压力也小了。金融市场的每一次呼吸，都跟利率有关。',f(){S.rateBonus=true;},card:'c15'},
  {t:'auto',title:'升职加薪！',desc:'十年磨一剑，你升到了管理层，月薪 +25%。',f(){S.salary=Math.round(S.salary*(1+EAM.raise2));},card:'c10'},
  {t:'auto',title:'慢牛收官',desc:'市场走了几年慢牛，账户曲线缓缓向上。时间，果然是复利的朋友。',f(){},card:'c01'},
  {t:'auto',title:'45 岁：年终盘点',desc:'21 年打工生涯结束。是财务自由，还是继续搬砖？答案就在你的账户里。',f(){}}
];

/* ===== 状态与核心引擎 ===== */
let S=null, IV=0;
function netWorth(){const h=S.house.owned?S.house.value-S.house.loan:0;return S.cash+S.bond+S.stock+S.hot+S.crypto+h;}
function downPay(){return Math.round(S.housePrice*CFG.house_down_ratio);}
function buyHouse(){const p=Math.round(S.housePrice);const d=downPay();S.cash-=d;S.house={owned:true,value:p,loan:Math.round(p*0.7)};}
function sellHouse(){const net=Math.round((S.house.value-S.house.loan)*0.98);S.cash+=net;S.house={owned:false,value:0,loan:0};}
function forceSell(){for(const k of ['hot','crypto','stock','bond']){if(S.cash>=0)break;const need=-S.cash;const take=Math.min(S[k],Math.ceil(need/0.95));S.cash+=Math.round(take*0.95);S[k]-=take;IV-=take;}}

function newGame(){
  const seed=(Date.now()^Math.floor(Math.random()*1e9))>>>0;
  rng=mulberry32(seed);
  S={seed:seed,yi:-1,age:CFG.start_age,salary:CFG.salary_start,expense:CFG.expense_start,cash:0,bond:0,stock:0,hot:0,crypto:0,
     house:{owned:false,value:0,loan:0},housePrice:CFG.house_price_start,
     insured:false,kid:false,unemployed:false,side:false,rateBonus:false,
     debt:null,relReturn:null,goodDec:0,badDec:0,cards:new Set(),totalIncome:0,
     history:[],log:[],phase:'event',result:null,bankrupt:false,resolved:false};
  IV=0;
  $('ins-toggle').checked=false;
  show('screen-start',false);show('screen-game',true);show('screen-end',false);
  startYear();
}

function startYear(){
  S.yi++;
  if(S.yi>=TOTAL_YEARS){showEnding(false);return;}
  S.age=CFG.start_age+S.yi;
  S.unemployed=false;S.side=false;S.rateBonus=false;S.resolved=false;S.result=null;
  if(S.yi>0){
    S.salary=Math.round(S.salary*(1+CFG.salary_growth_base+(rng()-0.5)*2*CFG.salary_growth_jitter));
  }
  S.expense=Math.round(CFG.expense_start*Math.pow(1+CFG.inflation,S.yi)+(S.kid?CFG.kid_extra_monthly:0));
  const ev=EVENTS[S.yi];
  if(ev.t==='auto'){ev.f();}
  S.phase='event';
  renderAll();
}

function settleYear(){
  if(S.phase!=='alloc')return;
  const yi=S.yi,mkt=MARKETS[yi];
  const R=CFG.returns[mkt];
  const income=(S.unemployed?0:S.salary*CFG.salary_months)+(S.side?EAM.side_income:0);
  const living=S.expense*12;
  const ins=S.insured?CFG.insurance_monthly*12:0;
  let mrtg=0;
  if(S.house.owned){
    mrtg=Math.round(S.house.loan*CFG.house_loan_pay_ratio);
    S.house.loan=Math.round(S.house.loan*(1+CFG.house_loan_rate-CFG.house_loan_pay_ratio));
  }
  S.cash+=income-living-ins-mrtg;
  S.totalIncome+=income;
  let debtPaid=0;
  if(S.debt&&S.debt.due===yi){debtPaid=S.debt.pay;S.cash-=S.debt.pay;S.debt=null;}
  if(S.relReturn!==null&&S.relReturn===yi){S.cash+=EAM.relative_back;S.relReturn=null;}
  if(S.cash<0){forceSell();}
  const nwStart=netWorth();
  const rows=[];
  for(const k of ASSET_ORDER){
    const a0=S[k];
    if(a0===0){rows.push({k,a0:0,a1:0,d:0,p:0});continue;}
    let r=rnd(R[k][0],R[k][1]);
    if(k==='bond'&&S.rateBonus)r+=0.01;
    const a1=Math.round(a0*(1+r));
    S[k]=a1;rows.push({k,a0,a1,d:a1-a0,p:r});
  }
  const houseRow={};
  if(S.house.owned){
    let hr=rnd(R.house[0],R.house[1]);
    if(S.rateBonus)hr+=0.03;
    const v0=S.house.value;
    S.house.value=Math.round(v0*(1+hr));
    S.housePrice=Math.round(S.housePrice*(1+hr));
    houseRow.v0=v0;houseRow.v1=S.house.value;houseRow.d=S.house.value-v0;houseRow.p=hr;
  }else{
    const hr=rnd(R.house[0],R.house[1]);
    S.housePrice=Math.round(S.housePrice*(1+hr));
  }
  const nwEnd=netWorth();
  S.history.push({age:S.age,nw:nwEnd,mkt});
  S.result={yi,mkt,income,living,ins,mrtg,debtPaid,rows,houseRow,nwStart,nwEnd};
  S.phase='result';
  renderAll();
  if(nwEnd<0){S.bankrupt=true;setTimeout(()=>showEnding(true),900);return;}
  const ev=EVENTS[yi];
  if(ev.card&&!S.cards.has(ev.card)){showCard(ev.card);}
}

/* ===== 渲染 ===== */
function renderAll(){renderTop();renderNw();renderEventArea();renderAlloc();renderChart();renderStats();}

function renderTop(){
  $('chip-age').textContent='年龄 '+S.age;
  $('chip-year').textContent='第 '+(S.yi+1)+' / '+TOTAL_YEARS+' 年';
  $('chip-mkt').textContent='行情：'+MKT_LABEL[MARKETS[S.yi]][0];
  $('chip-salary').textContent='月薪 '+full(S.salary);
  $('chip-cash').textContent='现金 '+wan(S.cash);
}
function renderNw(){
  const nw=netWorth();
  $('nw-num').textContent=wan(nw);
  const prev=S.history.length?S.history[S.history.length-1].nw:null;
  const d=prev!==null?nw-prev:null;
  const dEl=$('nw-delta');
  if(d===null){dEl.textContent='--';dEl.className='delta flat';}
  else if(d>=0){dEl.textContent='+'+wan(d);dEl.className='delta up';}
  else{dEl.textContent='-'+wan(-d);dEl.className='delta down';}
  const p=clamp(nw/CFG.goal*100,0,100);
  $('goal-fill').style.width=p.toFixed(1)+'%';
  $('goal-txt').textContent='进度 '+p.toFixed(1)+'%'+(nw>=CFG.goal?' · 已达成财务自由！':'');
}

function renderEventArea(){
  const el=$('event-area');
  if(S.phase==='result'){renderResult();return;}
  const ev=EVENTS[S.yi];
  const mc=MKT_LABEL[MARKETS[S.yi]][1];
  let html='<div class="card">';
  html+='<div class="yr-tag"><span class="yr serif">第 '+(S.yi+1)+' 年 · '+S.age+' 岁</span><span class="mkt '+mc+'">'+MKT_LABEL[MARKETS[S.yi]][0]+'</span></div>';
  html+='<h3 class="serif">'+ev.title+'</h3><div class="desc">'+ev.desc+'</div>';
  if(ev.t==='choice'&&!S.resolved){
    ev.choices.forEach((c,i)=>{
      html+='<button class="choice" data-ci="'+i+'"><div class="c-label">'+c.l+'</div><div class="c-tip">'+c.tip+'</div></button>';
    });
    html+='</div>';
    el.innerHTML=html;
    el.querySelectorAll('.choice').forEach(b=>b.addEventListener('click',()=>{
      const c=ev.choices[+b.dataset.ci];c.f();
      if(c.q==='good')S.goodDec++;else if(c.q==='bad')S.badDec++;
      S.log.push({yi:S.yi+1,t:ev.title,l:c.l,q:c.q});
      S.resolved=true;S.phase='alloc';renderAll();
    }));
  }else if(!S.resolved){
    html+='</div>';
    el.innerHTML=html;
    const btn=document.createElement('button');
    btn.className='btn btn-gold';btn.style.cssText='margin-top:4px';btn.textContent='知道了，继续';
    btn.addEventListener('click',()=>{S.resolved=true;S.phase='alloc';renderAll();});
    el.querySelector('.card').appendChild(btn);
  }else{
    html+='<div class="muted">事件已处理，调整好配置后点右下角「结算这一年」。</div></div>';
    el.innerHTML=html;
  }
}

function renderResult(){
  const el=$('event-area');const R=S.result;
  const mc=MKT_LABEL[R.mkt][1];
  let html='<div class="card">';
  html+='<div class="yr-tag"><span class="yr serif">第 '+(R.yi+1)+' 年结算</span><span class="mkt '+mc+'">'+MKT_LABEL[R.mkt][0]+'</span></div>';
  html+='<p class="muted" style="margin-bottom:10px">'+MKT_FLAVOR[R.mkt]+'</p>';
  html+='<div class="result-block"><div class="rb-title">年度收支</div>';
  html+='<div class="line"><span>工资收入'+(R.income===0?'（失业年）':'')+'</span><span class="amt pos">+'+full(R.income)+'</span></div>';
  html+='<div class="line"><span>生活支出'+(S.kid?'（含养娃）':'')+'</span><span class="amt neg">-'+full(R.living)+'</span></div>';
  if(R.ins>0)html+='<div class="line"><span>保险保费</span><span class="amt neg">-'+full(R.ins)+'</span></div>';
  if(R.mrtg>0)html+='<div class="line"><span>房贷（本息）</span><span class="amt neg">-'+full(R.mrtg)+'</span></div>';
  if(R.debtPaid>0)html+='<div class="line"><span>偿还高息借款</span><span class="amt neg">-'+full(R.debtPaid)+'</span></div>';
  html+='</div>';
  html+='<div class="result-block"><div class="rb-title">资产涨跌</div>';
  const lk={bond:'债券基金',stock:'指数基金',hot:'热点股票',crypto:'币圈'};
  for(const row of R.rows){
    if(row.a0===0)continue;
    const cls=row.d>=0?'pos':'neg';const sign=row.d>=0?'+':'';
    html+='<div class="line"><span>'+lk[row.k]+' <span class="muted num">'+full(row.a0)+'</span></span><span class="amt '+cls+' num">'+sign+full(row.d)+' ('+pct(row.p)+')</span></div>';
  }
  if(R.houseRow.v0!==undefined){
    const h=R.houseRow;const cls=h.d>=0?'pos':'neg';const sign=h.d>=0?'+':'';
    html+='<div class="line"><span>房产（市值） <span class="muted num">'+full(h.v0)+'</span></span><span class="amt '+cls+' num">'+sign+full(h.d)+' ('+pct(h.p)+')</span></div>';
    html+='<div class="line"><span>房贷余额</span><span class="amt num">'+full(S.house.loan)+'</span></div>';
  }
  if(R.rows.every(r=>r.a0===0)&&R.houseRow.v0===undefined){
    html+='<div class="muted">你还没买入任何投资资产——全是现金，很安全，但也跑不赢通胀。</div>';
  }
  html+='</div>';
  const d=R.nwEnd-R.nwStart;const cls=d>=0?'pos':'neg';const sign=d>=0?'+':'';
  html+='<div class="res-summary"><div class="nw-line"><span>今年净资产变动</span><span class="amt '+cls+' num">'+sign+wan(d)+'</span></div>';
  html+='<div class="nw-line" style="font-size:15px;margin-top:4px"><span>累计净资产</span><span class="amt serif num">'+wan(R.nwEnd)+'</span></div></div>';
  html+='<div class="next-row">';
  if(R.yi<TOTAL_YEARS-1){html+='<button class="btn btn-gold" id="btn-next">下一年 ▶</button>';}
  else{html+='<button class="btn btn-primary" id="btn-finish">45 岁 · 查看人生结算</button>';}
  html+='</div></div>';
  el.innerHTML=html;
  const nb=el.querySelector('#btn-next');if(nb)nb.addEventListener('click',startYear);
  const fb=el.querySelector('#btn-finish');if(fb)fb.addEventListener('click',()=>showEnding(false));
}

function renderAlloc(){
  const locked=S.phase==='result';
  const monthly=Math.round(S.salary*CFG.salary_months/12)+(S.side?2000:0);
  const mExp=S.expense+(S.insured?CFG.insurance_monthly:0)+(S.house.owned?Math.round(S.house.loan*CFG.house_loan_pay_ratio/12):0);
  $('cashflow-line').innerHTML='<span>月收入 ≈ <b class="num">'+full(monthly)+'</b></span><span>月支出 ≈ <b class="num">'+full(mExp)+'</b></span><span>月结余 ≈ <b class="num" style="color:var(--blue)">'+(monthly-mExp>=0?'+':'')+full(monthly-mExp)+'</b></span>';
  const rows=$('asset-rows');
  let html='';
  for(const k of ['bond','stock','hot','crypto']){
    const a=ASSET_LABEL[k];const v=S[k];
    html+='<div class="asset-row" data-k="'+k+'">'
      +'<div class="asset-ic" style="background:'+a.bg+'"><svg viewBox="0 0 24 24" fill="none" stroke="'+a.c+'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+ICON[k]+'</svg></div>'
      +'<div class="asset-meta"><div class="asset-name">'+a.n+'</div><div class="asset-hint">'+a.h+'</div></div>'
      +'<span class="asset-amt num">'+wan(v)+'</span>'
      +'<button class="step-btn" data-d="-1" '+(locked||v<CFG.step?'disabled':'')+'>−</button>'
      +'<button class="step-btn" data-d="1" '+(locked||S.cash<CFG.step?'disabled':'')+'>+</button>'
      +'</div>';
  }
  html+='<div class="asset-row"><div class="asset-ic" style="background:'+ASSET_LABEL.cash.bg+'"><svg viewBox="0 0 24 24" fill="none" stroke="'+ASSET_LABEL.cash.c+'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+ICON.cash+'</svg></div>'
    +'<div class="asset-meta"><div class="asset-name">现金 / 余额宝</div><div class="asset-hint">活期灵活，随时可用</div></div>'
    +'<span class="asset-amt num" style="color:var(--blue)">'+wan(S.cash)+'</span></div>';
  rows.innerHTML=html;
  rows.querySelectorAll('.step-btn').forEach(b=>b.addEventListener('click',()=>{
    if(S.phase==='result')return;
    const row=b.closest('.asset-row');const k=row.dataset.k;const d=+b.dataset.d;
    if(d>0){if(S.cash<CFG.step)return;S.cash-=CFG.step;S[k]+=CFG.step;IV+=CFG.step;}
    else{if(S[k]<CFG.step)return;S[k]-=CFG.step;S.cash+=CFG.step;IV-=CFG.step;}
    renderAll();
  }));
  const hb=$('house-box');
  if(!S.house.owned){
    const dp=downPay();const can=!locked&&S.cash>=dp;
    hb.innerHTML='<div class="hb-line"><span>当前房价</span><span class="num"><b>'+wan(S.housePrice)+'</b></span></div>'
      +'<div class="hb-line"><span>首付 30%（按揭 4.5%）</span><span class="num">'+wan(dp)+'</span></div>'
      +'<button class="btn btn-ghost" style="width:100%;margin-top:8px;font-size:13px" id="btn-buy" '+(can?'':'disabled')+'>'+(locked?'结算中，下一年再操作':(S.cash>=dp?'买入房产（付首付）':'现金不足，攒够首付再来'))+'</button>';
    const b=$('btn-buy');if(b)b.addEventListener('click',()=>{if(S.phase==='result'||S.cash<downPay())return;buyHouse();renderAll();});
  }else{
    hb.innerHTML='<div class="hb-line"><span>房产市值</span><span class="num"><b>'+wan(S.house.value)+'</b></span></div>'
      +'<div class="hb-line"><span>房贷余额</span><span class="num">'+wan(S.house.loan)+'</span></div>'
      +'<div class="hb-line"><span>房产净值</span><span class="num" style="color:var(--gold)">'+wan(S.house.value-S.house.loan)+'</span></div>'
      +'<button class="btn btn-ghost" style="width:100%;margin-top:8px;font-size:13px" id="btn-sell" '+(locked?'disabled':'')+'>'+(locked?'结算中，下一年再操作':'卖出房产套现')+'</button>';
    const sb=$('btn-sell');if(sb)sb.addEventListener('click',()=>{if(S.phase==='result')return;sellHouse();renderAll();});
  }
  const sb=$('btn-settle');
  if(S.phase==='event'){sb.textContent='先处理年度事件';sb.disabled=true;}
  else if(S.phase==='alloc'){sb.textContent='结算这一年';sb.disabled=false;}
  else{sb.textContent='已结算';sb.disabled=true;}
  $('ins-toggle').disabled=locked;
}

function renderChart(){
  const svg=$('nw-chart');const W=300,H=150,pad=8;
  const pts=S.history;
  let maxN=CFG.goal,minN=0;
  for(const p of pts){if(p.nw>maxN)maxN=p.nw;if(p.nw<minN)minN=p.nw;}
  if(maxN===minN)maxN=minN+1;
  const X=i=>pad+(W-2*pad)*(i/(TOTAL_YEARS-1));
  const Y=n=>H-pad-(H-2*pad)*((n-minN)/(maxN-minN));
  let g='';
  for(let i=0;i<=4;i++){const y=pad+(H-2*pad)*i/4;g+='<line x1="'+pad+'" y1="'+y+'" x2="'+(W-pad)+'" y2="'+y+'" stroke="#E0D4B8" stroke-width="0.5"/>';}
  g+='<line x1="'+pad+'" y1="'+Y(CFG.goal)+'" x2="'+(W-pad)+'" y2="'+Y(CFG.goal)+'" stroke="#B98A2E" stroke-width="1.5" stroke-dasharray="5 4"/>';
  if(pts.length>1){
    let d='M'+X(0)+' '+Y(pts[0].nw);
    for(let i=1;i<pts.length;i++)d+=' L'+X(i)+' '+Y(pts[i].nw);
    g+='<path d="'+d+'" fill="none" stroke="#2B261E" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>';
    const last=pts[pts.length-1];
    g+='<circle cx="'+X(pts.length-1)+'" cy="'+Y(last.nw)+'" r="4" fill="#BE3B2E" stroke="#FDF9EE" stroke-width="2"/>';
  }else{
    g+='<circle cx="'+X(0)+'" cy="'+Y(0)+'" r="3" fill="#8C7F67"/>';
  }
  svg.innerHTML=g;
}

function renderStats(){
  $('stat-good').textContent=S.goodDec;
  $('stat-bad').textContent=S.badDec;
  const n=S.cards.size;
  $('stat-cards').textContent=n+'/15';
  $('cp-txt').textContent=n+'/15';
  $('cp-fill').style.width=(n/15*100).toFixed(1)+'%';
}

/* ===== 课堂卡与结局 ===== */
function showCard(id){
  const c=CARDS[id];if(!c||S.cards.has(id))return;
  S.cards.add(id);
  $('card-badge').textContent=c.no;
  $('card-title').textContent=c.title;
  $('card-src').textContent=c.src;
  $('card-body').textContent=c.text;
  $('card-formula').innerHTML='<span class="fl">核心公式 · 生冷的逻辑</span>'+c.formula;
  $('card-use').innerHTML='<span class="fl">怎么用 · 落进你的钱包</span>'+c.use;
  $('card-quote').textContent=c.quote;
  $('modal-card').hidden=false;
  renderStats();
}

function showEnding(bankrupt){
  const nw=netWorth();
  let title=(CFG.ending_thresholds.find(t=>nw>=t.min)||{title:'破产 · 纯纯大韭菜'}).title;
  if(bankrupt)title='破产 · 纯纯大韭菜';
  if(!bankrupt&&nw>=CFG.goal&&(S.goodDec-S.badDec)<5)title='暴富神话 · 天选韭菜';
  if(!bankrupt&&nw>=1800000&&nw<CFG.goal&&(S.goodDec-S.badDec)<0)title='赌狗上岸 · 惊险保本';
  const COMMENTS={
    '财务自由 · 巴菲特中国分巴':'从 24 岁的打工人，到 45 岁自己的基金经理。分散投资、稳住心态、尊重市场——希勒教授看了都忍不住给你点赞。',
    '暴富神话 · 天选韭菜':'钱是赚到了，但按你的操作方式……这属于统计学奇迹。建议把运气换成认知，否则迟早还回去。',
    '富足退休 · 稳健老钱':'没暴富，但很从容。你证明了：不追热点、不恐慌、好好配置，时间真的会替你打工。',
    '普通打工人 · 稳稳的幸福':'人生没有暴富，但也没被收割。记住：理财是场长跑，45 岁不是终点，是新的起点。',
    '月光族本族 · 消费主义战士':'钱都去哪了？可能是奶茶、可能是购物车、可能是追热点时的手滑。下一局记得：先买保险，再攒本金。',
    '赌狗上岸 · 惊险保本':'市场没把你清零，也没奖励你的骚操作——这次纯属运气好。赶紧把运气换成认知，否则迟早还回去。',
    '破产 · 纯纯大韭菜':'被市场狠狠教育了。学费已经交了，下一局记得：分散投资、别上杠杆、先存 3-6 个月应急金。'
  };
  $('end-badge').textContent=title;
  $('end-comment').textContent=COMMENTS[title];
  $('end-nw').textContent=wan(nw);
  $('end-income').textContent=full(S.totalIncome);
  const inv=S.bond+S.stock+S.hot+S.crypto-IV;
  $('end-invest').textContent=(inv>=0?'+':'')+full(inv);
  const dc=S.goodDec+S.badDec>0?Math.round(S.goodDec/(S.goodDec+S.badDec)*100)+'%':'—';
  $('end-dec').textContent=dc;
  renderEndReport();
  show('screen-game',false);show('screen-end',true);
}

/* ===== 理财体检报告 ===== */
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

/* ===== 初始化 ===== */
function init(){
  $('btn-start').addEventListener('click',newGame);
  $('btn-help-start').addEventListener('click',()=>{$('modal-help').hidden=false;});
  $('btn-help').addEventListener('click',()=>{$('modal-help').hidden=false;});
  $('btn-help-close').addEventListener('click',()=>{$('modal-help').hidden=true;});
  $('modal-help').addEventListener('click',e=>{if(e.target===$('modal-help'))$('modal-help').hidden=true;});
  $('btn-card-close').addEventListener('click',()=>{$('modal-card').hidden=true;});
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
  });
  $('modal-card').addEventListener('click',e=>{if(e.target===$('modal-card'))$('modal-card').hidden=true;});
  $('ins-toggle').addEventListener('change',e=>{if(S)S.insured=e.target.checked;renderAll();});
  $('btn-settle').addEventListener('click',()=>{if(S&&S.phase==='alloc')settleYear();});
  $('btn-restart').addEventListener('click',newGame);
  $('btn-detail').addEventListener('click',()=>{show('screen-end',false);show('screen-game',true);renderAll();});
  $('help-ruleset').textContent=CFG.ruleset_id;
}
init();
