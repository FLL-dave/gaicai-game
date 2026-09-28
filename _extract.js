// -*- coding: utf-8 -*-
const fs = require('fs');
const path = 'C:/Users/Administrator/DoubaoWork/chats/2026-09-28/new-chat/gaicai-game/韭菜大冒险.html';
const s = fs.readFileSync(path, 'utf8');

function extract(name) {
  const re = new RegExp('const ' + name + '=\\s*(\\[.*?\\]);', 's');
  const m = s.match(re);
  if (!m) throw new Error('not found ' + name);
  // 函数体替换为空对象，保持数组可序列化
  // 函数体替换为 f:null（按花括号配平扫描）
  let clean = '';
  let i = 0;
  while (i < m[1].length) {
    const idx = m[1].indexOf('f(){', i);
    if (idx === -1) { clean += m[1].slice(i); break; }
    clean += m[1].slice(i, idx) + 'f:null';
    let depth = 1, j = idx + 4;
    for (; j < m[1].length; j++) {
      if (m[1][j] === '{') depth++;
      else if (m[1][j] === '}') { depth--; if (depth === 0) { j++; break; } }
    }
    i = j;
  }
  return eval('(' + clean + ')');
}

function extractObj(name) {
  const re = new RegExp('const ' + name + '=\\s*(\\{.*?\\});', 's');
  const m = s.match(re);
  if (!m) throw new Error('not found ' + name);
  let clean = '';
  let i = 0;
  while (i < m[1].length) {
    const idx = m[1].indexOf('f(){', i);
    if (idx === -1) { clean += m[1].slice(i); break; }
    clean += m[1].slice(i, idx) + 'f:null';
    let depth = 1, j = idx + 4;
    for (; j < m[1].length; j++) {
      if (m[1][j] === '{') depth++;
      else if (m[1][j] === '}') { depth--; if (depth === 0) { j++; break; } }
    }
    i = j;
  }
  return eval('(' + clean + ')');
}

const EVENTS = extract('EVENTS');
const CARDS = extractObj('CARDS');

const lines = [];
lines.push('EVENTS count=' + EVENTS.length);
EVENTS.forEach(e => {
  let line = 'y' + String(e.y).padStart(2) + ' [' + e.t + '] ' + e.title;
  if (e.choices) {
    e.choices.forEach(c => { line += ' || ' + c.l + ' (' + c.q + ')'; });
  }
  lines.push(line);
});
lines.push('CARDS count=' + Object.keys(CARDS).length);
Object.keys(CARDS).forEach(id => { const c = CARDS[id]; lines.push(id + ' | ' + c.title + ' | ' + c.src); });
fs.writeFileSync('C:/Users/Administrator/DoubaoWork/chats/2026-09-28/new-chat/gaicai-game/_events.txt', lines.join('\n'), 'utf8');
console.log(lines.join('\n'));
