/* =========================================================
   EJLP — 英日雙語練習包
   英文：Phase 0 Day 1–61（2026-08-30 起）
   日文：JLPT N5–N1 58 課（2026-10-19 起）
   資料：data/*.json（由 generators/build_all.py 產生）
========================================================= */
'use strict';
const EN_DAY1 = '2026-08-30';
const JA_DAY1 = '2026-10-19';
const LEVELS_JA = ['N5', 'N4', 'N3', 'N2', 'N1'];
const EN_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1'];
const BLOCKS = [
  {id:'vocab_new', name:'新字', min:10}, {id:'vocab_review', name:'單字複習', min:15},
  {id:'mc', name:'選擇', min:15}, {id:'fill', name:'填空', min:20}, {id:'translate', name:'中譯英', min:15},
  {id:'error', name:'改錯', min:10}, {id:'reorder', name:'重組', min:8}, {id:'reading', name:'閱讀', min:15},
  {id:'dictation', name:'聽寫', min:8}, {id:'speaking', name:'口說', min:10}, {id:'writing', name:'寫作', min:15},
];
const JSECS = [
  {id:'jv', name:'單字', min:8}, {id:'jg', name:'文法', min:8}, {id:'jm', name:'選擇', min:8},
  {id:'jf', name:'填空', min:6}, {id:'jr', name:'讀解', min:8}, {id:'jl', name:'聽解', min:6},
  {id:'js', name:'跟讀', min:6}, {id:'jw', name:'作文', min:15}, {id:'jc', name:'單字卡', min:5},
];
const TASK2SEC = {vocab:'jv', grammar:'jg', mcq:'jm', fill:'jf', reading:'jr', listening:'jl', shadow:'js', write:'jw', flash:'jc', review:'jx', mock:'mock'};
const CONTR = [["can't","cannot"],["can not","cannot"],["won't","will not"],["isn't","is not"],["aren't","are not"],["wasn't","was not"],["weren't","were not"],
  ["don't","do not"],["doesn't","does not"],["didn't","did not"],["haven't","have not"],["hasn't","has not"],["i'm","i am"],["you're","you are"],["we're","we are"],
  ["they're","they are"],["he's","he is"],["she's","she is"],["it's","it is"],["that's","that is"],["what's","what is"],["where's","where is"],["there's","there is"],
  ["who's","who is"],["i've","i have"],["you've","you have"],["we've","we have"],["they've","they have"],["i'd","i would"],["i'll","i will"],["you'll","you will"],
  ["he'll","he will"],["she'll","she will"],["we'll","we will"],["they'll","they will"],["it'll","it will"],["let's","let us"]];

/* ---------- 儲存 ---------- */
const Store = {
  get(k, d){ try{ const v = localStorage.getItem('ejlp:'+k); return v == null ? d : JSON.parse(v); }catch(e){ return d; } },
  set(k, v){ try{ localStorage.setItem('ejlp:'+k, JSON.stringify(v)); }catch(e){} },
};
const DATA = {en:null, lib:null, gloss:null, jaIndex:null, ja:{}};
const state = {
  screen:'home', lang: Store.get('lang','en'),
  day: 1, jsel: Store.get('jsel', null),
  progress: Store.get('progress', {}), jprog: Store.get('jprog', {}), jwrong: Store.get('jwrong', {}), jtasks: Store.get('jtasks', {}),
  drafts: Store.get('drafts', {}), tests: Store.get('tests', {}), jmock: Store.get('jmock', {}), external: Store.get('external', []),
  cefr: Store.get('cefr', []), words: Store.get('words', {en:{}, ja:{}}), readTime: Store.get('readTime', {}), readPos: Store.get('readPos', {}),
  settings: Object.assign({voice:'', jaVoice:'', rate:0.95, amount:100, reviewMode:'choice', jaScript:'furigana', jaGap:true, trLang:'zh', rdfs:22, rdRate:0.9}, Store.get('settings', {})),
  shelf:{lang:'en', level:null}, testsLang:'en', runner:null, reader:null,
};
function persist(){
  for (const k of ['lang','jsel','progress','jprog','jwrong','jtasks','drafts','tests','jmock','external','cefr','words','readTime','readPos','settings']) Store.set(k, state[k]);
}

/* ---------- 日期 ---------- */
function ymd(d){ return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
function parseD(s){ const [y,m,d]=s.split('-').map(Number); return new Date(y, m-1, d); }
function todayD(){ try{ return parseD(new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Taipei'}).format(new Date())); }catch(e){ const d=new Date(); d.setHours(0,0,0,0); return d; } }
function addDays(d, n){ const x = new Date(d); x.setDate(x.getDate()+n); return x; }
function diffDays(a, b){ return Math.round((parseD(ymd(b)) - parseD(ymd(a))) / 86400000); }
function todayStr(){ return ymd(todayD()); }
function enTotal(){ return DATA.en ? Object.keys(DATA.en.days).length : 61; }
function enToday(){ return Math.min(enTotal(), Math.max(1, diffDays(parseD(EN_DAY1), todayD()) + 1)); }
function dayDate(day){ const d = addDays(parseD(EN_DAY1), day-1); return `${d.getMonth()+1} 月 ${d.getDate()} 日`; }

/* ---------- 小工具 ---------- */
function esc(s){ return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function rich(s){ return esc(s).replace(/&lt;u&gt;/g,'<u>').replace(/&lt;\/u&gt;/g,'</u>'); }
function q(s){ return JSON.stringify(s).replace(/"/g, '&quot;'); }
function toast(msg){ const t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 2000); }
function shuffle(a){ a = a.slice(); for (let i = a.length-1; i > 0; i--){ const j = Math.floor(Math.random()*(i+1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function norm(s){
  s = String(s||'').toLowerCase().replace(/[’‘`´]/g,"'").replace(/[“”]/g,'"').replace(/\s+/g,' ').trim().replace(/[.,!?;:"]+$/,'').trim();
  for (const [c,f] of CONTR) s = s.replace(new RegExp('(^|\\s)'+c+'(?=\\s|$)','g'), '$1'+f);
  return s.replace(/\s*,\s*/g, ', ').replace(/\s+/g,' ').trim();
}
function match(user, answers){ const u = norm(user); return (Array.isArray(answers) ? answers : [answers]).some(a => norm(a) === u); }
function jnorm(s){ return String(s||'').replace(/[\s　。、．，！？!?]/g,'').trim(); }
function wordCount(t){ return t.trim() ? t.trim().split(/\s+/).length : 0; }

/* ---------- 日文顯示 ---------- */
const RJ = (() => { const m = {}; const add = s => s.split(' ').forEach(p => { const [k,v] = p.split('='); m[k] = v; });
  add('きゃ=kya きゅ=kyu きょ=kyo しゃ=sha しゅ=shu しょ=sho ちゃ=cha ちゅ=chu ちょ=cho にゃ=nya にゅ=nyu にょ=nyo ひゃ=hya ひゅ=hyu ひょ=hyo みゃ=mya みゅ=myu みょ=myo りゃ=rya りゅ=ryu りょ=ryo ぎゃ=gya ぎゅ=gyu ぎょ=gyo じゃ=ja じゅ=ju じょ=jo びゃ=bya びゅ=byu びょ=byo ぴゃ=pya ぴゅ=pyu ぴょ=pyo ふぁ=fa てぃ=ti でぃ=di しぇ=she ちぇ=che じぇ=je');
  add('あ=a い=i う=u え=e お=o か=ka き=ki く=ku け=ke こ=ko さ=sa し=shi す=su せ=se そ=so た=ta ち=chi つ=tsu て=te と=to な=na に=ni ぬ=nu ね=ne の=no は=ha ひ=hi ふ=fu へ=he ほ=ho ま=ma み=mi む=mu め=me も=mo や=ya ゆ=yu よ=yo ら=ra り=ri る=ru れ=re ろ=ro わ=wa を=o ん=n が=ga ぎ=gi ぐ=gu げ=ge ご=go ざ=za じ=ji ず=zu ぜ=ze ぞ=zo だ=da ぢ=ji づ=zu で=de ど=do ば=ba び=bi ぶ=bu べ=be ぼ=bo ぱ=pa ぴ=pi ぷ=pu ぺ=pe ぽ=po ぁ=a ぃ=i ぅ=u ぇ=e ぉ=o ゔ=vu');
  return m; })();
function toHira(s){ return [...String(s||'')].map(c => { const o = c.charCodeAt(0); return (o >= 0x30A1 && o <= 0x30F6) ? String.fromCharCode(o-0x60) : c; }).join(''); }
function romaji(kana, tok){
  if (tok === 'は') return 'wa'; if (tok === 'へ') return 'e'; if (tok === 'を') return 'o';
  const s = toHira(kana); let out = '', dbl = false;
  for (let i = 0; i < s.length; i++){
    const two = s.substr(i,2), one = s[i];
    if (one === 'っ'){ dbl = true; continue; }
    if (one === 'ー'){ const v = out.match(/[aeiou]$/); out += v ? v[0] : ''; continue; }
    if (one === 'ん'){ out += /^[あいうえおやゆよ]/.test(s[i+1]||'') ? "n'" : 'n'; continue; }
    let r = RJ[two] ? (i++, RJ[two]) : (RJ[one] ?? one);
    if (dbl){ r = (r.startsWith('ch') ? 't' : r[0]) + r; dbl = false; }
    out += r;
  }
  return out;
}
const KANJI = /[㐀-鿿々〆ヶ]/;
function rubyTok(t, r){
  if (!r || !KANJI.test(t)) return esc(t);
  if (state.settings.jaScript === 'kana') return esc(r);
  const th = toHira(t);
  let a = 0; while (a < t.length && a < r.length && th[a] === r[a]) a++;
  let b = 0; while (b < t.length-a && b < r.length-a && th[t.length-1-b] === r[r.length-1-b]) b++;
  const pre = t.slice(0,a), mid = t.slice(a, t.length-b), suf = t.slice(t.length-b), rmid = r.slice(a, r.length-b);
  if (!mid || !rmid) return esc(t);
  return `${esc(pre)}<ruby>${esc(mid)}<rt>${esc(rmid)}</rt></ruby>${esc(suf)}`;
}
const PUNCT = '、。「」！？!?（）()…・ 　『』,.';
function jaLine(toks, opt = {}){
  if (!toks) return '';
  const html = toks.map((tk, i) => {
    if (tk === null) return `<span class="jtok">${opt.blank || '<span class="blank">&nbsp;</span>'}</span>`;
    const [t, r, base] = tk;
    if (t === '\n') return '<br>';
    if (PUNCT.includes(t)) return `<span>${esc(t)}</span>`;
    const inner = rubyTok(t, r);
    if (opt.tap) return `<span class="jtok w ${opt.saved && opt.saved(base || t) ? 'saved' : ''}" data-ja="${esc(t)}" data-base="${esc(base || '')}" data-r="${esc(r || '')}">${inner}</span>`;
    return `<span class="jtok">${inner}</span>`;
  }).join('');
  const rom = state.settings.jaScript === 'romaji' ? `<div class="romaji">${toks.filter(x => x && x[0] !== '\n' && !PUNCT.includes(x[0])).map(([t,r]) => romaji(r || t, t)).join(' ')}</div>` : '';
  return `<span class="${state.settings.jaGap ? 'jgap' : ''}">${html}</span>${rom}`;
}
function jaText(toks){ return (toks || []).filter(Boolean).map(t => t[0] === '\n' ? '\n' : t[0]).join(''); }
function jaTok1(tk){ return Array.isArray(tk) ? tk : [tk, '']; }

/* ---------- 語音 ---------- */
/* 語音：自動挑最自然的聲音，避開 macOS 的趣味語音；長文分句播放（避開 Chrome 約 15 秒截斷） */
const NOVELTY = /Eddy|Flo\b|Grandma|Grandpa|Reed|Rocko|Sandy|Shelley|Albert|Bad News|Bahh|Bells|Boing|Bubbles|Cellos|Good News|Jester|Organ|Superstar|Trinoids|Whisper|Wobble|Zarvox|Fred|Junior|Ralph|Kathy/i;
function rankVoice(v){
  const n = v.name; let s = 0;
  if (NOVELTY.test(n)) s -= 100;
  if (/Google/.test(n)) s += 15;
  if (/Natural|Online|Neural/.test(n)) s += 50;
  if (/Siri|Premium|Enhanced|プレミアム|拡張|高品質/.test(n)) s += 30;
  if (/Kyoko|O-ren|Otoya|Nanami|Keita|Haruka|Ayumi|Ichiro|Hattori|Samantha|Daniel|Karen|Moira|Serena|Aria|Libby|Sonia/.test(n)) s += 30;
  if (/^(ja[-_]JP|en[-_](GB|US))$/i.test(v.lang)) s += 5;
  if (v.localService) s += 10;
  return s;
}
const TTS = {
  voices:[], jvoices:[], _cancelAt:0,
  load(){
    if (!('speechSynthesis' in window)) return;
    const all = speechSynthesis.getVoices();
    const sortV = l => { const good = l.filter(v => !NOVELTY.test(v.name)); return (good.length ? good : l).sort((a, b) => rankVoice(b) - rankVoice(a)); };
    this.voices = sortV(all.filter(v => /^en/i.test(v.lang)));
    this.jvoices = sortV(all.filter(v => /^ja/i.test(v.lang)));
    const s = state.settings;
    if (this.voices.length && (!this.voices.find(v => v.name === s.voice))) s.voice = this.voices[0].name;
    if (this.jvoices.length && (!this.jvoices.find(v => v.name === s.jaVoice))) s.jaVoice = this.jvoices[0].name;
  },
  voiceFor(lang, name){
    const pool = lang === 'ja' ? this.jvoices : this.voices;
    return pool.find(v => v.name === (name || (lang === 'ja' ? state.settings.jaVoice : state.settings.voice))) || pool[0] || null;
  },
  chunks(text, lang){
    const parts = lang === 'ja' ? String(text).split(/(?<=[。！？!?\n])/) : String(text).split(/(?<=[.!?])\s+|\n+/);
    const out = [];
    for (let p of parts){
      p = p.trim(); if (!p) continue;
      while (p.length > 160){ const cut = Math.max(p.lastIndexOf(lang === 'ja' ? '、' : ',', 160), 80); out.push(p.slice(0, cut + 1)); p = p.slice(cut + 1).trim(); }
      if (p) out.push(p);
    }
    return out;
  },
  cancel(){ try{ speechSynthesis.cancel(); }catch(e){} this._cancelAt++; },
  /* items: [{text, lang, voice}] 依序播放 */
  play(items, rate, onend){
    if (!('speechSynthesis' in window)){ toast('此瀏覽器不支援朗讀'); return; }
    if (!this.voices.length || !this.jvoices.length) this.load();
    this.cancel();
    const us = [];
    items.forEach(it => this.chunks(it.text, it.lang).forEach(t => {
      const u = new SpeechSynthesisUtterance(t);
      const v = this.voiceFor(it.lang, it.voice);
      if (v){ u.voice = v; u.lang = v.lang; } else u.lang = it.lang === 'ja' ? 'ja-JP' : 'en-GB';
      u.rate = rate ?? state.settings.rate; u.pitch = 1;
      us.push(u);
    }));
    if (!us.length){ if (onend) onend(); return; }
    if (onend) us[us.length - 1].onend = onend;
    const stamp = this._cancelAt;
    /* Chrome：cancel 後立刻 speak 常常沒聲音，稍等一下再播 */
    setTimeout(() => { if (this._cancelAt !== stamp) return; try{ speechSynthesis.resume(); }catch(e){} us.forEach(u => speechSynthesis.speak(u)); }, 80);
  },
  speakEn(text, rate, onend){ this.play([{text, lang:'en'}], rate, onend); },
  speakJa(text, rate, onend){
    if (!this.jvoices.length && !this._warned){ this._warned = true; toast('找不到日文語音，請到「設定」看如何安裝'); }
    this.play([{text: {'は':'わ','へ':'え','を':'お'}[text] || text, lang:'ja'}], rate, onend);
  },
  /* 聽解稿：去掉「男：」「女：」標籤；有第二個好的日文語音就讓男女換人說 */
  script(text, rate){
    const male = this.jvoices.find(v => /Otoya|Keita|Ichiro|Hattori|Daichi|Naoki|Male/i.test(v.name));
    const female = this.jvoices.find(v => /Kyoko|O-ren|Nanami|Haruka|Ayumi|Female/i.test(v.name));
    const items = String(text).split('\n').map(line => {
      const m = line.match(/^(男|女)(の人)?[：:]\s*/);
      if (!m) return {text: line, lang:'ja'};
      const v = m[1] === '男' ? male : female;
      return {text: line.slice(m[0].length), lang:'ja', voice: v && v.name};
    }).filter(x => x.text.trim());
    this.play(items, rate);
  },
};
if ('speechSynthesis' in window){ TTS.load(); speechSynthesis.onvoiceschanged = () => { TTS.load(); if (state.screen === 'settings') render(); }; }
const spkLabel = l => l === '' ? '' : ' ' + (l || '播放');
const spkEn = (text, label, rate) => `<button class="spk${label === '' ? ' icon' : ''}" onclick="TTS.speakEn(${q(text)}${rate ? ','+rate : ''})" aria-label="朗讀">🔊${spkLabel(label)}</button>`;
const spkJa = (text, label, rate) => `<button class="spk${label === '' ? ' icon' : ''}" onclick="TTS.speakJa(${q(text)}${rate ? ','+rate : ''})" aria-label="朗讀">🔊${spkLabel(label)}</button>`;

/* =========================================================
   資料載入
========================================================= */
async function getJSON(p){ const r = await fetch(p); if (!r.ok) throw new Error(p + ' ' + r.status); return r.json(); }
async function ensureJa(lv){
  if (DATA.ja[lv]) return DATA.ja[lv];
  DATA.ja[lv] = await getJSON(`data/ja/${lv}.json`);
  return DATA.ja[lv];
}
async function boot(){
  document.getElementById('app').innerHTML = `<div class="loading"><div>載入題庫…</div><div class="bar"><b style="width:30%"></b></div></div>`;
  try{
    const [en, lib, gloss, jai] = await Promise.all([getJSON('data/en.json'), getJSON('data/library.json'), getJSON('data/gloss.json'), getJSON('data/ja/index.json')]);
    Object.assign(DATA, {en, lib, gloss, jaIndex: jai});
  }catch(e){
    document.getElementById('app').innerHTML = `<div class="screen"><h1>載入失敗</h1><p class="muted">${esc(e.message)}</p><p>請確認網路連線後重新整理。若是直接打開檔案，請改用網址 https://levilan.github.io/EJLP/ 。</p></div>`;
    return;
  }
  state.day = enToday();
  const cur = jaCurrent();
  if (!state.jsel || !state.jsel.lv) state.jsel = cur.unit ? {lv: cur.unit.lv, u: cur.unit.u} : {lv:'N5', u:1};
  if (state.lang === 'ja') await ensureJa(state.jsel.lv);
  render();
}

/* =========================================================
   路由
========================================================= */
function go(s){ state.screen = s; render(); window.scrollTo(0, 0); }
document.getElementById('nav').addEventListener('click', e => { const b = e.target.closest('button'); if (b) go(b.dataset.s); });
function render(){
  if (!DATA.en) return;
  document.querySelectorAll('#nav button').forEach(b => b.classList.toggle('on', b.dataset.s === state.screen));
  const fn = {home: renderHome, read: renderRead, progress: renderProgress, tests: renderTests, settings: renderSettings}[state.screen];
  document.getElementById('app').innerHTML = fn();
}
async function setLang(l){
  state.lang = l; persist();
  if (l === 'ja') await ensureJa(state.jsel.lv);
  render();
}
const langSw = () => `<div class="langsw"><button class="${state.lang==='en'?'sel':''}" onclick="setLang('en')">English</button><button class="${state.lang==='ja'?'sel':''}" onclick="setLang('ja')">日本語 JLPT</button></div>`;

/* =========================================================
   英文：今日
========================================================= */
function enDay(n){ return DATA.en.days[String(n)]; }
function enItems(day, block){
  const d = enDay(day); if (!d || !d.blocks[block]) return [];
  let items = d.blocks[block];
  if (block === 'reading') items = items.flatMap(p => p.qs.map(x => Object.assign({passageTitle: p.title, passage: p.text}, x)));
  const pct = state.settings.amount / 100;
  return pct < 1 ? items.slice(0, Math.max(1, Math.ceil(items.length * pct))) : items;
}
function prog(store, key, block){
  store[key] = store[key] || {};
  store[key][block] = store[key][block] || {done:0, correct:0, skipped:[], answers:{}};
  return store[key][block];
}
function blockStatus(n, done, correct, skipped){
  if (!n) return {kind:'none', n:0};
  if (!done) return {kind:'todo', n};
  if (done >= n) return {kind:'done', n, correct, answered: done - (skipped || 0)};
  return {kind:'part', n, done};
}
function enStatus(day, b){
  const items = enItems(day, b.id); const p = (state.progress[day] || {})[b.id];
  return blockStatus(items.length, p ? p.done : 0, p ? p.correct : 0, p ? p.skipped.length : 0);
}
function stripHTML(sts){
  return `<div class="strip" style="grid-template-columns:repeat(${sts.length},1fr)">${sts.map(s => `<i class="${s.kind==='done'?'done':s.kind==='part'?'part':''}"></i>`).join('')}</div>`;
}
function blockRow(name, s, min, onclick, noPct){
  return `<li><button onclick="${onclick}" ${s.kind==='none'?'disabled':''}>
    <span class="name">${name}</span><span class="n">${s.kind==='none'?'—':s.n}</span>
    <span class="st ${s.kind}">${s.kind==='done' ? `✓ ${s.answered && !noPct ? Math.round(s.correct/s.answered*100)+'%' : ''}` : s.kind==='part' ? `${s.done}/${s.n}` : s.kind==='todo' ? `${min} 分` : ''}</span></button></li>`;
}
function renderHome(){ return state.lang === 'ja' ? renderJaHome() : renderEnHome(); }
function renderEnHome(){
  const day = state.day, d = enDay(day), total = enTotal(), today = enToday();
  const wk = DATA.en.meta.weeks.find(w => w.id === d.week);
  const sts = BLOCKS.map(b => ({b, s: enStatus(day, b)}));
  const live = sts.filter(x => x.s.kind !== 'none');
  const doneCount = live.filter(x => x.s.kind === 'done').length;
  const remain = live.filter(x => x.s.kind !== 'done').reduce((m, x) => m + x.b.min * (x.s.kind === 'part' ? 1 - x.s.done / x.s.n : 1), 0);
  const next = live.find(x => x.s.kind === 'part') || live.find(x => x.s.kind === 'todo');
  const g = wk && wk.grammar;
  const gbox = g ? `<details class="gbox"><summary>${wk.id === 9 ? '補充週' : `第 ${wk.id} 週`}文法：${esc(g.point)}</summary><div class="gb"><p>${esc(g.explain)}</p>${(g.patterns||[]).map(p => `<div class="pat"><span>${esc(p)}</span>${spkEn(p,'')}</div>`).join('')}</div></details>` : '';
  const body = d.rest
    ? `<div class="restbox"><div class="big">🌿</div><h2>${esc(d.topic)}</h2><p class="muted">Phase 0 跑完了。今天休息；明天開始現在進行式補充週（Day 57–61）。也可以到「檢測」做結業測驗。</p></div>`
    : `${stripHTML(live.map(x => x.s))}
      <div class="row small muted"><span>${doneCount}/${live.length} 區塊完成</span><span>${remain > 0 ? `約 ${Math.round(remain)} 分鐘剩` : '今天做完了'}</span></div>
      ${next ? `<button class="primary" style="margin-top:18px" onclick="startEn(${day},'${next.b.id}')">${next.s.kind==='part' ? `繼續：${next.b.name} 第 ${next.s.done+1} 題` : `開始：${next.b.name}`}</button>`
             : `<div class="note">今天的區塊都完成了。可以到「閱讀」讀 10 分鐘，或到「檢測」做週檢測。</div>`}
      <ul class="blocks">${live.map(({b, s}) => blockRow(b.name + (b.id==='reading' ? `<span class="muted small" style="font-weight:400">　${d.blocks.reading.length} 篇</span>` : ''), s, b.min, `startEn(${day},'${b.id}')`, b.id === 'vocab_new')).join('')}</ul>`;
  return `<div class="screen">${langSw()}
    <div class="row" style="align-items:flex-end"><h1>Day ${day}</h1>
      <div class="muted small" style="text-align:right">${wk ? esc(wk.id === 9 ? '補充週' : `第 ${wk.id} 週`) : ''} 第 ${d.dayOfWeek} 天${d.review ? '<br>總複習' : ''}</div></div>
    <div class="muted">${dayDate(day)}　${esc(d.topic || '')}${day !== today ? '　<span class="tag">非今天</span>' : ''}</div>
    ${gbox}${body}
    <div class="daynav">
      <button class="ghost" onclick="state.day=Math.max(1,state.day-1);render()" ${day<=1?'disabled':''}>‹ 前一天</button>
      ${day !== today ? `<button class="ghost" onclick="state.day=enToday();render()">回到今天</button>` : ''}
      <button class="ghost" onclick="state.day=Math.min(${total},state.day+1);render()" ${day>=total?'disabled':''}>後一天 ›</button>
    </div></div>`;
}
function startEn(day, block){
  const items = enItems(day, block); if (!items.length) return;
  const b = BLOCKS.find(x => x.id === block);
  let its = items.slice();
  if (block === 'reorder') its = its.map(it => Object.assign({}, it, {tiles: shuffle(it.words.map(w => [w, '']))}));
  openRunner({title: b.name, block, items: its, p: prog(state.progress, day, block), back: null});
}

/* =========================================================
   日文：JLPT 時程
========================================================= */
const PLAN = (() => {
  const P = []; const blk = o => P.push(o);
  let d = parseD(JA_DAY1);
  for (let i = 1; i <= 12; i++){ blk({kind:'unit', lv:'N5', u:i, start:d, days:7}); d = addDays(d, 7); }
  d = parseD('2027-01-11');
  for (let i = 1; i <= 12; i++){ const n = i < 12 ? 14 : 7; blk({kind:'unit', lv:'N4', u:i, start:d, days:n}); d = addDays(d, n); }
  blk({kind:'sprint', lv:'N4', start:parseD('2027-06-21'), days:13}); blk({kind:'exam', lv:'N4', start:parseD('2027-07-04'), days:1});
  d = parseD('2027-07-05');
  for (let i = 1; i <= 10; i++){ blk({kind:'unit', lv:'N3', u:i, start:d, days:14}); d = addDays(d, 14); }
  blk({kind:'sprint', lv:'N3', start:parseD('2027-11-22'), days:13}); blk({kind:'exam', lv:'N3', start:parseD('2027-12-05'), days:1});
  blk({kind:'rest', lv:'N3', start:parseD('2027-12-06'), days:7});
  d = parseD('2027-12-13');
  for (let i = 1; i <= 12; i++){ blk({kind:'unit', lv:'N2', u:i, start:d, days:21}); d = addDays(d, 21); }
  blk({kind:'consol', lv:'N2', start:parseD('2028-08-21'), days:90}); blk({kind:'sprint', lv:'N2', start:parseD('2028-11-19'), days:14});
  blk({kind:'exam', lv:'N2', start:parseD('2028-12-03'), days:1});
  return P;
})();
const CYCLE_A = [[['vocab','單字 1–10：看、聽、唸出例句'],['grammar','文法①：讀說明，唸 3 個例句']],[['vocab','單字 11–20'],['grammar','文法②']],
  [['grammar','文法③'],['mcq','選擇題 12 題（看解析）']],[['fill','填空 10 題'],['review','錯題本：重做本課錯題']],[['reading','讀解：先讀一次再看中譯，答 4 題']],
  [['listening','聽解 4 題：先別看稿'],['shadow','跟讀 6 句，每句 3 遍']],[['write','作文：用本課文法寫'],['flash','單字卡自測 20 張']]];
const CYCLE_B = [[['flash','單字卡自測：遮讀音與中文']],[['review','錯題本：選擇＋填空重做']],[['reading','讀解精讀：跟著朗讀全文']],
  [['listening','聽解不看稿再聽一次，再對照稿'],['shadow','跟讀全部 6 句']],[['ext','外部教材：對應課的練習題 30 分鐘']],
  [['mcq','選擇題全部重做，目標 100%'],['fill','填空全部重做']],[['write','作文重寫，比對範例']]];
const CYCLE_C = [[['ext','NHK NEWS WEB EASY 或新聞讀 2 篇，抓出本課文法']],[['flash','單字卡自測'],['review','錯題本']],[['ext','外部教材（新完全マスター）文法練習']],
  [['ext','聽力：Podcast 或日劇片段 20 分鐘，跟讀 5 句']],[['shadow','本課跟讀全部'],['listening','聽解再做一次']],[['mock','模擬測驗做一部分（文法或讀解區）']],[['rest','休息或補進度']]];
const SPRINT = [[['mock','完整模擬測驗一次，計時']],[['review','錯題本全部清空']],[['ext','官方問題集／JLPT 範例題：文字語彙＋文法']],
  [['ext','官方問題集：讀解']],[['ext','官方問題集：聽解']],[['flash','整級單字卡：抽 3 課自測']],[['rest','休息']]];
function jaCurrent(day){
  day = day || todayD();
  const off0 = diffDays(parseD(JA_DAY1), day);
  if (off0 < 0) return {before: -off0, unit: {lv:'N5', u:1}, tasks: [], block: null};
  for (const b of PLAN){
    const o = diffDays(b.start, day);
    if (o >= 0 && o < b.days){
      let tasks = [];
      if (b.kind === 'unit'){ const c = o < 7 ? CYCLE_A : (o < 14 ? CYCLE_B : CYCLE_C); tasks = c[o % 7]; }
      else if (b.kind === 'sprint') tasks = SPRINT[o % 7];
      else if (b.kind === 'consol') tasks = [[['ext','外部教材 30–40 分鐘']],[['review','錯題本']],[['mock','模擬測驗一區']],[['ext','NHK 新聞 2 篇']],[['ext','聽力 20 分鐘＋跟讀']],[['flash','單字卡']],[['rest','休息']]][o % 7];
      else if (b.kind === 'rest') tasks = [['rest','休息週：只做 10 分鐘單字卡']];
      else tasks = [['exam','考試日。帶准考證、身分證、2B 鉛筆和橡皮擦']];
      return {day: off0 + 1, block: b, off: o, tasks, unit: b.kind === 'unit' ? {lv: b.lv, u: b.u} : null};
    }
  }
  return {day: off0 + 1, block: null, tasks: [['ext','N1：自主進度']], unit: null};
}
function jUnit(lv, u){ const d = DATA.ja[lv]; return d && d.units.find(x => x.unit === u); }
function jKey(lv, u){ return lv + '-' + u; }
function jItems(lv, u, sec){
  const U = jUnit(lv, u); if (!U) return [];
  switch (sec){
    case 'jv': return U.vocab;
    case 'jg': return U.grammar;
    case 'jm': return U.mcq;
    case 'jf': return U.fill;
    case 'jr': return U.reading.qs.map(x => Object.assign({passage: U.reading}, x));
    case 'jl': return U.listening;
    case 'js': return U.shadow;
    case 'jw': return [U.write];
    case 'jc': return U.vocab.map((v, i) => {
      const others = shuffle(U.vocab.filter(x => x.zh !== v.zh)).slice(0, 3);
      const o = shuffle([v, ...others]);
      return i % 2 ? {kind:'w2z', v, opts:o.map(x => x.zh), a:o.indexOf(v)} : {kind:'z2w', v, opts:o.map(x => [x.w, x.r]), a:o.indexOf(v)};
    });
    case 'jx': return (state.jwrong[jKey(lv, u)] || []).map(w => Object.assign({}, jItems(lv, u, w.sec)[w.i], {_wsec: w.sec, _wi: w.i})).filter(x => x._wsec);
  }
  return [];
}
function jStatus(lv, u, sec){
  const n = jItems(lv, u, sec).length; const p = (state.jprog[jKey(lv, u)] || {})[sec];
  return blockStatus(n, p ? p.done : 0, p ? p.correct : 0, p ? p.skipped.length : 0);
}
function renderJaHome(){
  const cur = jaCurrent();
  const sel = state.jsel; const U = jUnit(sel.lv, sel.u);
  if (!U) return `<div class="screen">${langSw()}<div class="loading">載入 ${sel.lv}…</div></div>`;
  const isToday = cur.unit && cur.unit.lv === sel.lv && cur.unit.u === sel.u;
  const tkey = todayStr();
  const tdone = state.jtasks[tkey] || {};
  const head = cur.before
    ? `<h1>日文</h1><div class="muted">課程 10/19（一）開始，還有 ${cur.before} 天。可以先預習 N5 第 1 課。</div>`
    : `<div class="row" style="align-items:flex-end"><h1>日文 Day ${cur.day}</h1><div class="muted small" style="text-align:right">${cur.block ? esc(blockLabel(cur)) : ''}</div></div>
       <div class="muted">${(() => { const d = todayD(); return `${d.getMonth()+1} 月 ${d.getDate()} 日`; })()}</div>`;
  const tasks = (cur.tasks.length && isToday) || (cur.tasks.length && !cur.unit) ? `<div class="sec-h">今天的任務</div><ul class="tasks">${cur.tasks.map(([k, label], i) => {
      const sec = TASK2SEC[k]; const can = sec && (sec === 'mock' || jItems(sel.lv, sel.u, sec).length);
      return `<li class="${tdone[i] ? 'done' : ''}"><input type="checkbox" ${tdone[i]?'checked':''} onchange="toggleTask(${i},this.checked)" aria-label="完成"><span>${esc(label)}</span>${can ? `<button class="go" onclick="jaTask('${k}')">開始</button>` : ''}</li>`;
    }).join('')}</ul>` : '';
  const sts = JSECS.map(s => ({s, st: jStatus(sel.lv, sel.u, s.id)}));
  const wrongN = (state.jwrong[jKey(sel.lv, sel.u)] || []).length;
  return `<div class="screen">${langSw()}${head}
    <div class="unitcard"><span class="lvtag">${sel.lv}</span><span class="muted small">第 ${sel.u} 課${isToday ? '　今天的課' : ''}</span>
      <h2>${esc(U.title)}</h2><div class="ja" lang="ja">${esc(U.titleJa)}</div><div class="th">${esc(U.theme)}</div>
      ${stripHTML(sts.map(x => x.st))}</div>
    ${tasks}
    <ul class="blocks">${sts.map(({s, st}) => blockRow(s.name, st, s.min, `startJa('${s.id}')`, ['jv','jg','js','jw'].includes(s.id))).join('')}
      <li><button onclick="startJa('jx')" ${wrongN ? '' : 'disabled'}><span class="name">錯題本</span><span class="n">${wrongN || '—'}</span><span class="st todo">${wrongN ? '重做' : ''}</span></button></li></ul>
    <div class="sec-h">選課</div>
    <div class="chips">${LEVELS_JA.map(lv => `<button class="${lv===sel.lv?'sel':''}" onclick="pickLevel('${lv}')">${lv}</button>`).join('')}</div>
    <ul class="ulist">${DATA.jaIndex.levels[sel.lv].map(x => {
      const done = JSECS.filter(s => jStatus(sel.lv, x.unit, s.id).kind === 'done').length;
      return `<li><button onclick="pickUnit('${sel.lv}',${x.unit})" ${x.unit===sel.u?'style="background:var(--marker-soft)"':''}><span class="no">${x.unit}</span><span class="tt">${esc(x.title)}<small lang="ja">${esc(x.titleJa)}</small></span><span class="pc">${done ? done + '/' + JSECS.length : ''}</span></button></li>`;
    }).join('')}</ul>
    ${cur.unit && !isToday ? `<div class="daynav"><button class="ghost" onclick="pickUnit('${cur.unit.lv}',${cur.unit.u})">回到今天的課</button></div>` : ''}
  </div>`;
}
function blockLabel(cur){
  const b = cur.block;
  if (b.kind === 'unit') return `${b.lv} 第 ${b.u} 課　第 ${cur.off + 1}/${b.days} 天`;
  return {sprint:`${b.lv} 考前衝刺`, exam:`JLPT ${b.lv} 考試日`, rest:'休息週', consol:'N2 鞏固期'}[b.kind] || '';
}
function toggleTask(i, v){ const k = todayStr(); state.jtasks[k] = state.jtasks[k] || {}; state.jtasks[k][i] = v; persist(); render(); }
async function pickLevel(lv){ await ensureJa(lv); state.jsel = {lv, u:1}; persist(); render(); }
async function pickUnit(lv, u){ await ensureJa(lv); state.jsel = {lv, u}; persist(); render(); window.scrollTo(0, 0); }
function jaTask(k){
  const sec = TASK2SEC[k];
  if (sec === 'mock'){ state.testsLang = 'ja'; go('tests'); return; }
  startJa(sec);
}
function startJa(sec){
  const {lv, u} = state.jsel;
  let items = jItems(lv, u, sec); if (!items.length) return;
  const name = sec === 'jx' ? '錯題本' : JSECS.find(s => s.id === sec).name;
  const p = sec === 'jx' ? {done:0, correct:0, skipped:[], answers:{}} : prog(state.jprog, jKey(lv, u), sec);
  if (sec === 'jx') p.done = 0;
  openRunner({title: `${lv} 第${u}課 ${name}`, block: sec, items: items.slice(), p, ctx: {lv, u}, temp: sec === 'jx'});
}
function addWrong(ctx, sec, i){
  if (!ctx || sec === 'jx') return;
  const k = jKey(ctx.lv, ctx.u); const L = state.jwrong[k] = state.jwrong[k] || [];
  if (!L.find(x => x.sec === sec && x.i === i)) L.push({sec, i});
}
function clearWrong(ctx, sec, i){
  const k = jKey(ctx.lv, ctx.u); const L = state.jwrong[k] || [];
  state.jwrong[k] = L.filter(x => !(x.sec === sec && x.i === i));
}

/* =========================================================
   Runner
========================================================= */
function openRunner(cfg){
  const p = cfg.exam ? {done:0, correct:0, skipped:[], answers:{}} : cfg.p;
  state.runner = Object.assign({idx: cfg.exam ? 0 : Math.min(p.done, cfg.items.length), phase:'answer', tmp:{}, p, startedAt: Date.now(), wrongs:[], examAnswers:[]}, cfg);
  document.getElementById('nav').classList.add('hidden');
  document.getElementById('reader').classList.add('hidden');
  document.getElementById('runner').classList.remove('hidden');
  renderRunner();
}
function closeRunner(){
  const r = state.runner;
  if (r && r.tmp && r.tmp.rec && r.tmp.rec.state === 'recording') r.tmp.rec.stop();
  if (r && r.p && !r.exam && !r.temp) r.p.done = r.idx;
  persist();
  const back = r && r.back;
  state.runner = null; TTS.cancel();
  document.getElementById('runner').classList.add('hidden');
  if (back === 'reader' && state.reader){ document.getElementById('reader').classList.remove('hidden'); renderReader(); return; }
  document.getElementById('nav').classList.remove('hidden');
  render();
}
function renderRunner(){
  const r = state.runner, el = document.getElementById('runner');
  if (r.idx >= r.items.length){ el.innerHTML = renderComplete(); return; }
  const item = r.items[r.idx];
  const type = r.exam ? 'exam' : (r.block === 'jx' ? item._wsec : r.block);
  const body = ITEM[type].render(item, r);
  el.innerHTML = `
    <div class="r-head"><div class="row"><button class="x" onclick="closeRunner()" aria-label="離開">✕</button><span class="title">${esc(r.title)}${r.exam ? '<span class="tag">考試</span>' : ''}</span><span class="count">${r.idx+1}/${r.items.length}</span></div>
      <div class="bar"><b style="width:${(r.idx / r.items.length * 100).toFixed(1)}%"></b></div></div>
    <div class="r-body">${body}${r.phase === 'feedback' ? renderFeedback() : ''}</div>
    <div class="r-foot">${renderFoot(type)}</div>`;
  const f = el.querySelector('[data-autofocus]'); if (f && r.phase === 'answer') setTimeout(() => f.focus(), 50);
  const nb = el.querySelector('#next-btn'); if (nb) setTimeout(() => nb.focus(), 50);
  el.querySelector('.r-body').scrollTop = 0;
}
const CHOICE = new Set(['vocab_review','mc','reading','jm','jr','jl','jc','rd_q','srs']);
function curType(r){ const it = r.items[r.idx]; return r.exam ? 'exam' : (r.block === 'jx' ? it._wsec : r.block); }
function isChoice(type){ return CHOICE.has(type) && !(type === 'vocab_review' && state.settings.reviewMode === 'typing' && state.runner.items[state.runner.idx].dir !== 'en2zh'); }
function renderFoot(type){
  const r = state.runner;
  if (r.phase === 'feedback'){
    const canOverride = !r.last.ok && !r.exam && ['translate','dictation','fill','error','jf'].includes(type);
    return `${canOverride ? `<button class="secondary" onclick="markRight()">我覺得算對</button>` : ''}<button id="next-btn" class="primary" onclick="nextItem()">${r.idx + 1 >= r.items.length ? '完成' : '下一題'}</button>`;
  }
  if (type === 'exam') return r.idx > 0 ? `<button class="secondary" onclick="prevItem()">‹ 上一題</button>` : `<div class="muted small" style="text-align:center;align-self:center">點選答案就會進入下一題</div>`;
  if (isChoice(type)) return `<button class="secondary" onclick="skipItem()">跳過</button>`;
  const def = ITEM[type];
  if (def.foot) return def.foot(r);
  return `${r.exam ? '' : `<button class="secondary" onclick="skipItem()">跳過</button>`}<button class="primary" onclick="checkItem()">${r.exam ? '下一題' : '檢查答案'}</button>`;
}
function renderFeedback(){
  const {ok, ans, why, extra} = state.runner.last;
  return `<div class="fb ${ok ? 'ok' : 'no'}"><strong>${ok ? '✓ 正確' : '✗ 正確答案'}</strong>${!ok && ans ? `<div class="ans">${esc(ans)}</div>` : ''}${why ? `<div class="why">${esc(why)}</div>` : ''}</div>${extra || ''}`;
}
function finish(ok, ans, why, userText, extra){
  const r = state.runner, item = r.items[r.idx];
  r.last = {ok, ans, why, extra};
  if (!r.exam){
    r.p.answers[r.idx] = userText ?? '';
    if (ok) r.p.correct++; else r.wrongs.push({item, ans, user: userText});
    if (r.ctx){
      const sec = r.block === 'jx' ? item._wsec : r.block, i = r.block === 'jx' ? item._wi : r.idx;
      if (!ok) addWrong(r.ctx, sec, i); else if (r.block === 'jx') clearWrong(r.ctx, sec, i);
    }
  }
  r.phase = 'feedback'; persist(); renderRunner();
  if (ok && isChoice(curType(r))){ const idx = r.idx; setTimeout(() => { if (state.runner === r && r.phase === 'feedback' && r.idx === idx) nextItem(); }, 700); }
}
function markRight(){ const r = state.runner; r.last.ok = true; r.p.correct++; r.wrongs = r.wrongs.filter(w => w.item !== r.items[r.idx]);
  if (r.ctx){ const it = r.items[r.idx]; clearWrong(r.ctx, r.block === 'jx' ? it._wsec : r.block, r.block === 'jx' ? it._wi : r.idx); } persist(); renderRunner(); }
function nextItem(){ const r = state.runner; r.idx++; r.phase = 'answer'; r.tmp = {}; if (!r.exam && !r.temp) r.p.done = Math.max(r.p.done, r.idx); persist(); renderRunner(); }
function skipItem(){ const r = state.runner; if (!r.p.skipped.includes(r.idx)) r.p.skipped.push(r.idx); nextItem(); }
function checkItem(){ const r = state.runner, it = r.items[r.idx]; ITEM[r.exam ? 'exam' : (r.block === 'jx' ? it._wsec : r.block)].check(it, r); }
function pickOpt(i){
  const r = state.runner; if (r.phase !== 'answer' || r.tmp.locked) return;
  r.tmp.pick = i; const type = curType(r);
  if (type === 'exam'){ r.tmp.locked = true; renderRunner(); const idx = r.idx; setTimeout(() => { if (state.runner === r && r.idx === idx) checkItem(); }, 250); return; }
  if (isChoice(type)){ checkItem(); return; }
  renderRunner();
}
function prevItem(){ const r = state.runner; if (!r || r.idx === 0) return; r.idx--; r.phase = 'answer'; const a = r.examAnswers[r.idx]; r.tmp = {pick: a ? a.pick : undefined}; renderRunner(); }
function againWord(){ const r = state.runner; r.items.push(r.items[r.idx]); nextItem(); }
function pick(i){ const r = state.runner; if (r.phase !== 'answer') return; r.tmp.picked = [...(r.tmp.picked || []), i]; renderRunner(); }
function unpick(k){ const r = state.runner; if (r.phase !== 'answer') return; r.tmp.picked.splice(k, 1); renderRunner(); }
function pickWord(i){ const r = state.runner; if (r.phase !== 'answer') return; r.tmp.pick = i; r.tmp.text = undefined; renderRunner(); }
function saveDraft(v){ const r = state.runner; if (!r) return; r.tmp.text = v; const k = r.ctx ? jKey(r.ctx.lv, r.ctx.u) : 'en' + (r.block); state.drafts[k] = state.drafts[k] || {}; state.drafts[k][r.idx] = v; persist();
  const h = document.querySelector('#runner .hint .wc'); if (h) h.textContent = r.ctx ? [...v.replace(/\s/g,'')].length : wordCount(v); }
async function toggleRec(){
  const r = state.runner;
  if (r.tmp.recording){ r.tmp.rec.stop(); return; }
  try{
    const stream = await navigator.mediaDevices.getUserMedia({audio:true});
    const rec = new MediaRecorder(stream), chunks = [];
    rec.ondataavailable = e => chunks.push(e.data);
    rec.onstop = () => { stream.getTracks().forEach(t => t.stop()); r.tmp.recording = false; r.tmp.url = URL.createObjectURL(new Blob(chunks, {type: rec.mimeType || 'audio/webm'})); renderRunner(); };
    rec.start(); r.tmp.rec = rec; r.tmp.recording = true; renderRunner();
  }catch(e){ toast('無法使用麥克風：' + e.message); }
}
function renderComplete(){
  const r = state.runner;
  if (r.exam) return renderExamResult();
  const answered = r.items.length - r.p.skipped.length;
  const pct = answered ? Math.round(r.p.correct / answered * 100) : null;
  const mins = Math.max(1, Math.round((Date.now() - r.startedAt) / 60000));
  const grading = !['vocab_new','speaking','writing','jv','jg','js','jw','srs_none'].includes(r.block);
  return `<div class="r-head"><div class="row"><span></span><span class="title">${esc(r.title)} 完成</span><span></span></div></div>
  <div class="r-body">
    <div class="done-box"><div class="big">${grading && pct !== null ? pct + '%' : '✓'}</div><div class="muted">${r.items.length} 題　約 ${mins} 分鐘${r.p.skipped.length ? `　跳過 ${r.p.skipped.length} 題` : ''}</div></div>
    ${r.p.skipped.length && !r.temp ? `<button class="secondary" onclick="redoSkipped()">回頭做跳過的 ${r.p.skipped.length} 題</button>` : ''}
    ${r.wrongs.length ? `<h2>這次錯的</h2><ul class="wrongs">${r.wrongs.map(w => `<li><div class="en">${esc(w.ans)}</div><div class="muted">你的答案：${esc(w.user || '（空白）')}</div></li>`).join('')}</ul>` : ''}
    ${r.ctx && r.wrongs.length ? '<p class="muted small">錯的題目已加入本課錯題本。</p>' : ''}
  </div>
  <div class="r-foot"><button class="primary" onclick="closeRunner()">${r.back === 'reader' ? '回到書' : '完成'}</button></div>`;
}
function redoSkipped(){ const r = state.runner; const sk = [...r.p.skipped].sort((a, b) => a - b); r.p.skipped = []; r.idx = sk[0]; r.tmp = {}; r.phase = 'answer'; renderRunner(); }

/* ---------- 共用選項 ---------- */
function optsHTML(opts, cls, chosen, result, label){
  const K = 'ABCD';
  return `<div class="opts">${opts.map((o, i) => {
    const c = result ? (i === result.correct ? 'right' : i === result.chosen ? 'wrong' : '') : (chosen === i ? 'sel' : '');
    return `<button class="opt ${cls || ''} ${c}" ${result ? 'disabled' : `onclick="pickOpt(${i})"`}><span class="k">${K[i]}</span><span>${label ? label(o) : esc(o)}</span></button>`;
  }).join('')}</div>`;
}
const fieldHTML = (val, ph, multi, lang) => multi
  ? `<textarea class="field ${lang==='ja'?'jp':''}" data-autofocus placeholder="${ph || ''}" oninput="state.runner.tmp.text=this.value" ${lang==='ja'?'lang="ja"':''}>${esc(val || '')}</textarea>`
  : `<input class="field ${lang==='ja'?'jp':''}" data-autofocus placeholder="${ph || ''}" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" enterkeyhint="go" value="${esc(val || '')}" oninput="state.runner.tmp.text=this.value" onkeydown="if(event.key==='Enter'){event.preventDefault();checkItem()}" ${lang==='ja'?'lang="ja"':''}>`;

/* =========================================================
   題型
========================================================= */
const ITEM = {
  /* ---------- 英文 ---------- */
  vocab_new: {
    render: it => `<div class="card"><div class="w">${esc(it.w)}${it.review ? '<span class="tag">複習</span>' : ''}</div>${it.pos ? `<div class="pos">${esc(it.pos)}</div>` : ''}<div class="zh">${esc(it.zh)}</div>
      ${it.ja ? `<div class="ja"><small>日本語</small><span lang="ja">${rubyTok(it.ja[0], it.ja[1])}</span> <button class="mini-spk" style="width:32px;height:32px;vertical-align:middle" onclick="TTS.speakJa(${q(it.ja[0])})" aria-label="唸日文">🔊</button></div>` : ''}
      ${it.ex ? `<div class="ex">${esc(it.ex)}</div>` : ''}</div>
      <div class="spkrow" style="margin-top:16px">${spkEn(it.w, '唸單字')}${it.ex ? spkEn(it.ex, '唸例句') : ''}</div>`,
    foot: () => `<button class="secondary" onclick="againWord()">再看一次</button><button class="primary" onclick="nextItem()">認識</button>`,
    check: () => nextItem(),
  },
  vocab_review: {
    render: (it, r) => {
      const toZh = it.dir === 'en2zh';
      if (state.settings.reviewMode === 'typing' && !toZh) return `<div class="q zh">${esc(it.q)}</div>${fieldHTML(r.tmp.text, '輸入英文')}`;
      const res = r.phase === 'feedback' ? {correct: it.opts.indexOf(it.a), chosen: r.tmp.pick} : null;
      return `<div class="q ${toZh ? '' : 'zh'}">${esc(it.q)}</div>${toZh ? `<div style="margin:-12px 0 16px">${spkEn(it.q, '聽')}</div>` : ''}${optsHTML(it.opts, toZh ? 'zh' : '', r.tmp.pick, res)}`;
    },
    check: (it, r) => {
      if (state.settings.reviewMode === 'typing' && it.dir !== 'en2zh') return finish(match(r.tmp.text, it.a), it.a, '', r.tmp.text);
      if (r.tmp.pick == null) return toast('先選一個答案');
      finish(it.opts[r.tmp.pick] === it.a, it.a, '', it.opts[r.tmp.pick]);
    },
  },
  mc: {
    render: (it, r) => `<div class="q">${esc(it.q)}</div>${optsHTML(it.opts, '', r.tmp.pick, r.phase === 'feedback' ? {correct: it.a, chosen: r.tmp.pick} : null)}`,
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); finish(r.tmp.pick === it.a, it.opts[it.a], it.why, it.opts[r.tmp.pick]); },
  },
  fill: {
    render: (it, r) => `<div class="q">${esc(it.q).replace(/_{2,}/, `<span class="blank ${r.tmp.text ? 'filled' : ''}">${esc(r.tmp.text || '')}&nbsp;</span>`)}</div>${fieldHTML(r.tmp.text, '填入空格')}${it.hint && (r.tmp.miss || r.phase === 'feedback') ? `<div class="hint">提示：${esc(it.hint)}</div>` : ''}`,
    check: (it, r) => { const ok = match(r.tmp.text, it.a); if (!ok && !r.tmp.miss && it.hint && !r.tmp.text){ r.tmp.miss = true; return renderRunner(); } finish(ok, it.a[0], it.why, r.tmp.text); },
  },
  translate: {
    render: (it, r) => `<div class="q zh">${esc(it.zh)}</div>${fieldHTML(r.tmp.text, '寫出英文句子', true)}`,
    check: (it, r) => { if (!norm(r.tmp.text)) return toast('先寫一句'); finish(match(r.tmp.text, it.a), it.a.join('　／　'), '', r.tmp.text); },
  },
  error: {
    render: (it, r) => {
      if (it.mode === 'rewrite') return `<div class="muted small" style="margin-bottom:8px">這句有錯，整句改寫成正確的句子</div><div class="rw">${esc(it.s)}</div>${fieldHTML(r.tmp.text ?? it.s, '改寫後的句子', true)}`;
      const ws = it.s.split(' ');
      const cls = i => r.phase === 'feedback' ? (i === it.wrong ? 'wrong' : '') : (r.tmp.pick === i ? 'sel' : '');
      return `<div class="muted small" style="margin-bottom:8px">點出錯的字，再輸入正確寫法</div>
        <div class="tap-words">${ws.map((w, i) => `<button class="${cls(i)}" onclick="pickWord(${i})">${esc(w)}</button>${r.phase === 'feedback' && i === it.wrong ? `<button class="fixed" disabled>${esc(it.fix)}</button>` : ''}`).join(' ')}</div>
        ${r.tmp.pick != null && r.phase === 'answer' ? `<div style="margin-top:20px">${fieldHTML(r.tmp.text ?? ws[r.tmp.pick].replace(/[.,!?]$/, ''), '改成…')}</div>` : ''}`;
    },
    check: (it, r) => {
      if (it.mode === 'rewrite'){ const t = r.tmp.text ?? it.s; if (norm(t) === norm(it.s)) return toast('還沒改喔'); return finish(match(t, it.correct), it.correct, it.why, t); }
      if (r.tmp.pick == null) return toast('先點出錯的字');
      const fixed = it.full || it.s;
      if (r.tmp.pick !== it.wrong){ if (!r.tmp.miss){ r.tmp.miss = true; toast('不是這個字，再找找'); return; } return finish(false, fixed, it.why, r.tmp.text); }
      finish(match(r.tmp.text, it.fix), fixed, it.why, r.tmp.text);
    },
  },
  reorder: {
    render: (it, r) => {
      const tiles = it.tiles, picked = r.tmp.picked || [];
      return `<div class="slot">${picked.map((i, k) => `<button class="chip ${r.phase === 'feedback' && !r.last.ok ? 'bad' : ''}" onclick="unpick(${k})">${esc(tiles[i][0])}</button>`).join('')}</div>
        <div class="words">${tiles.map((t, i) => `<button class="chip ${picked.includes(i) ? 'used' : ''}" onclick="pick(${i})" ${picked.includes(i) ? 'disabled' : ''}>${esc(t[0])}</button>`).join('')}</div>`;
    },
    check: (it, r) => { const s = (r.tmp.picked || []).map(i => it.tiles[i][0]).join(' '); if (!s) return toast('先拼句子'); finish(match(s, it.a), it.a, '', s); },
  },
  reading: {
    render: (it, r) => `<details class="passage" ${r.tmp.collapsed ? '' : 'open'} ontoggle="if(state.runner)state.runner.tmp.collapsed=!this.open"><summary>${esc(it.passageTitle || '短文')}</summary><div class="t">${esc(it.passage)} ${spkEn(it.passage, '')}</div></details>
      <div class="q" style="font-size:21px">${esc(it.q)}</div>${optsHTML(it.opts, '', r.tmp.pick, r.phase === 'feedback' ? {correct: it.a, chosen: r.tmp.pick} : null)}`,
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); finish(r.tmp.pick === it.a, it.opts[it.a], '', it.opts[r.tmp.pick]); },
  },
  dictation: {
    render: (it, r) => `<div class="muted small">聽一句，寫下來。可以重播。</div><div class="spkrow" style="margin-top:12px">${spkEn(it.s, '播放')}${spkEn(it.s, '🐢 慢速', 0.7)}</div>${fieldHTML(r.tmp.text, '寫下聽到的句子', true)}`,
    check: (it, r) => { if (!norm(r.tmp.text)) return toast('先寫下句子'); finish(match(r.tmp.text, it.s), it.s, '', r.tmp.text); },
  },
  speaking: {
    render: (it, r) => {
      const canRec = !!(navigator.mediaDevices && window.MediaRecorder);
      const same = it.prompt === it.model;
      return `<div class="muted small">${same ? '先聽，再大聲跟讀' : '用英文回答'}</div><div class="q" style="font-size:22px">${esc(it.prompt)}</div>
        <div class="spkrow">${spkEn(it.model, same ? '聽' : '聽範例')}${spkEn(it.model, '🐢', 0.7)}${canRec ? `<button class="spk ${r.tmp.recording ? 'on' : ''}" onclick="toggleRec()">${r.tmp.recording ? '⏹ 停止' : '⏺ 錄音'}</button>` : ''}${r.tmp.url ? `<audio controls src="${r.tmp.url}" style="width:100%;margin-top:8px"></audio>` : ''}</div>
        ${same ? '' : r.tmp.showModel ? `<div class="card" style="margin-bottom:18px"><div class="ex" style="border:0;padding:0;margin:0;color:var(--ink)">${esc(it.model)}</div></div>` : `<button class="ghost" onclick="state.runner.tmp.showModel=true;renderRunner()">看範例句子</button>`}
        <div class="muted small" style="margin:14px 0 8px">說完後自評</div>
        <div class="rate">${['不順','還可以','流利'].map((l, i) => `<button class="${r.tmp.rate === i ? 'sel' : ''}" onclick="state.runner.tmp.rate=${i};renderRunner()">${l}</button>`).join('')}</div>`;
    },
    foot: () => `<button class="secondary" onclick="skipItem()">跳過</button><button class="primary" onclick="checkItem()">下一題</button>`,
    check: (it, r) => { if (r.tmp.rate == null) return toast('先自評一下'); r.p.answers[r.idx] = r.tmp.rate; if (r.tmp.rate > 0) r.p.correct++; if (r.tmp.rec && r.tmp.rec.state === 'recording') r.tmp.rec.stop(); nextItem(); },
  },
  writing: {
    render: (it, r) => {
      const k = 'en' + r.block; const txt = r.tmp.text ?? ((state.drafts[k] || {})[r.idx]) ?? '';
      return `<div class="q zh">${esc(it.prompt)}</div>
        <textarea class="field" data-autofocus placeholder="用英文寫在這裡，會自動保存草稿" oninput="saveDraft(this.value)">${esc(txt)}</textarea>
        <div class="hint"><span class="wc">${wordCount(txt)}</span> 字${it.minWords ? `　（至少 ${it.minWords} 字）` : ''}</div>
        ${r.phase === 'feedback' ? `<div class="sec-h">範例</div><div class="card"><div class="ex" style="border:0;padding:0;margin:0;color:var(--ink)">${esc(it.sample || '')}</div></div>` : ''}`;
    },
    foot: r => r.phase === 'feedback' ? '' : `<button class="secondary" onclick="skipItem()">先跳過</button><button class="primary" onclick="checkItem()">完成</button>`,
    check: (it, r) => { const txt = r.tmp.text ?? ((state.drafts['en' + r.block] || {})[r.idx]) ?? ''; if (it.minWords && wordCount(txt) < it.minWords) return toast(`再寫一點，至少 ${it.minWords} 字`); finish(true, '', '', txt); },
  },
  /* ---------- 考試（英文與 JLPT 共用） ---------- */
  exam: {
    render: (it, r) => {
      const ja = r.examLang === 'ja';
      let head = '';
      if (it.passage) head = ja ? `<details class="passage" open><summary>讀解</summary><div class="t passage-j" lang="ja">${jaLine(it.passageT)}</div></details>`
                                : `<details class="passage" open><summary>短文</summary><div class="t">${esc(it.passage)}</div></details>`;
      if (it.script) head = `<div class="muted small">聽解：先聽，再作答（可重播）</div><div class="spkrow" style="margin-top:10px"><button class="spk" onclick="TTS.script(${q(it.script)})">🔊 播放</button><button class="spk" onclick="TTS.script(${q(it.script)},0.7)">🐢 慢速</button></div>`;
      if (it.speak) head += `<div style="margin-bottom:10px">${spkEn(it.speak, '聽')}</div>`;
      const qtext = ja ? `<div class="qj" lang="${it.script ? 'zh' : 'ja'}">${it.t ? `<span class="ttag">${esc(it.t)}</span>` : ''}${rich(it.q)}</div>` : `<div class="q" style="font-size:21px">${esc(it.q)}</div>`;
      return head + qtext + optsHTML(it.opts || it.o, ja && !it.script ? 'jp' : '', r.tmp.pick, null);
    },
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); r.examAnswers[r.idx] = {item: it, ok: r.tmp.pick === it.a, pick: r.tmp.pick}; nextItem(); },
  },
  /* ---------- 日文 ---------- */
  jv: {
    render: it => `<div class="card"><div class="w jp" lang="ja" style="font-family:var(--jps)">${rubyTok(it.w, it.r)}${it._rev ? '<span class="tag">複習</span>' : ''}</div>
      <div class="pos">${esc(romaji(it.r || it.w))}${it.pos ? '　' + esc(it.pos) : ''}</div><div class="zh">${esc(it.zh)}</div>
      ${it.ex ? `<div class="ex" lang="ja" style="font-family:var(--jps);color:var(--ink);font-size:18px;line-height:2.1">${it.exT ? jaLine(it.exT, {tap:true}) : esc(it.ex)}</div><div class="muted small">${esc(it.exZh || '')}</div>` : ''}</div>
      <div class="spkrow" style="margin-top:16px">${spkJa(it.w, '唸單字')}${spkJa(it.w, '🐢', 0.6)}${it.ex ? spkJa(it.ex, '唸例句') : ''}</div>`,
    foot: () => `<button class="secondary" onclick="againWord()">再看一次</button><button class="primary" onclick="nextItem()">記住了</button>`,
    check: () => nextItem(),
  },
  jg: {
    render: it => `<div class="gcard"><div class="gp" lang="ja">${esc(it.p)}</div><div class="conn" lang="ja">${esc(it.conn)}</div><div class="gz">${esc(it.zh)}</div>
      <ol>${it.ex.map(e => `<li><div class="jx" lang="ja">${jaLine(e.jt, {tap:true})} <button class="mini-spk" style="width:32px;height:32px;vertical-align:middle" onclick="TTS.speakJa(${q(e.ja)})" aria-label="唸">🔊</button></div><div class="zx">${esc(e.zh)}</div></li>`).join('')}</ol></div>`,
    foot: () => `<button class="primary" onclick="nextItem()">看懂了，下一個</button>`,
    check: () => nextItem(),
  },
  jm: {
    render: (it, r) => `<div class="qj" lang="ja"><span class="ttag">${esc(it.t)}</span>${rich(it.q)}</div>${optsHTML(it.o, 'jp', r.tmp.pick, r.phase === 'feedback' ? {correct: it.a, chosen: r.tmp.pick} : null)}`,
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); finish(r.tmp.pick === it.a, it.o[it.a], it.exp, it.o[r.tmp.pick]); },
  },
  jf: {
    render: (it, r) => `<div class="qj" lang="ja">${esc(it.q).replace('（　）', `<span class="blank ${r.tmp.text ? 'filled' : ''}">${esc(r.tmp.text || '')}&nbsp;</span>`)}</div>
      ${fieldHTML(r.tmp.text, '填入（可用平假名）', false, 'ja')}<div class="hint">提示：${esc(it.hint)}</div>${r.phase === 'feedback' ? `<div class="hint">${esc(it.zh)}</div>` : ''}`,
    check: (it, r) => { const t = jnorm(r.tmp.text); if (!t) return toast('先填答案'); finish(it.a.some(a => jnorm(a) === t || toHira(jnorm(a)) === toHira(t)), it.a.join('／'), '', r.tmp.text); },
  },
  jr: {
    render: (it, r) => `<details class="passage" ${r.tmp.collapsed ? '' : 'open'} ontoggle="if(state.runner)state.runner.tmp.collapsed=!this.open"><summary lang="ja">${esc(it.passage.title)}</summary>
        <div class="t passage-j" lang="ja">${jaLine(it.passage.textT, {tap:true})}<div style="margin-top:8px">${spkJa(it.passage.text, '朗讀全文')}</div></div></details>
      ${r.phase === 'feedback' ? `<details class="passage"><summary>中文翻譯</summary><div class="t" style="white-space:pre-wrap">${esc(it.passage.zh)}</div></details>` : ''}
      <div class="qj" lang="ja">${esc(it.q)}</div>${optsHTML(it.o, 'jp', r.tmp.pick, r.phase === 'feedback' ? {correct: it.a, chosen: r.tmp.pick} : null)}`,
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); finish(r.tmp.pick === it.a, it.o[it.a], it.exp, it.o[r.tmp.pick]); },
  },
  jl: {
    render: (it, r) => {
      const fb = r.phase === 'feedback';
      return `<div class="muted small">先別看稿，聽完再選。可以重播。</div>
        <div class="spkrow" style="margin-top:12px"><button class="spk" onclick="TTS.script(${q(it.script)})">🔊 播放</button><button class="spk" onclick="TTS.script(${q(it.script)},0.7)">🐢 慢速</button></div>
        <div class="q zh" style="font-size:20px">${esc(it.q)}</div>${optsHTML(it.o, 'zh', r.tmp.pick, fb ? {correct: it.a, chosen: r.tmp.pick} : null)}
        ${fb ? `<div class="script" lang="ja">${jaLine(it.scriptT, {tap:true})}<div class="zh" lang="zh-Hant">${esc(it.zh)}</div></div>` : ''}`;
    },
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); finish(r.tmp.pick === it.a, it.o[it.a], it.exp, it.o[r.tmp.pick]); },
  },
  js: {
    render: (it, r) => {
      const canRec = !!(navigator.mediaDevices && window.MediaRecorder);
      return `<div class="muted small">聽一遍，再跟讀 3 遍</div><div class="qj" lang="ja" style="font-size:24px">${jaLine(it.jt, {tap:true})}</div><div class="muted">${esc(it.zh)}</div>
        <div class="spkrow" style="margin-top:12px">${spkJa(it.ja, '聽')}${spkJa(it.ja, '🐢', 0.6)}${canRec ? `<button class="spk ${r.tmp.recording ? 'on' : ''}" onclick="toggleRec()">${r.tmp.recording ? '⏹ 停止' : '⏺ 錄音'}</button>` : ''}${r.tmp.url ? `<audio controls src="${r.tmp.url}" style="width:100%;margin-top:8px"></audio>` : ''}</div>
        <div class="muted small" style="margin:14px 0 8px">跟讀後自評</div>
        <div class="rate">${['不順','還可以','流利'].map((l, i) => `<button class="${r.tmp.rate === i ? 'sel' : ''}" onclick="state.runner.tmp.rate=${i};renderRunner()">${l}</button>`).join('')}</div>`;
    },
    foot: () => `<button class="secondary" onclick="skipItem()">跳過</button><button class="primary" onclick="checkItem()">下一句</button>`,
    check: (it, r) => ITEM.speaking.check(it, r),
  },
  jw: {
    render: (it, r) => {
      const k = jKey(r.ctx.lv, r.ctx.u); const txt = r.tmp.text ?? ((state.drafts[k] || {})[r.idx]) ?? '';
      return `<div class="q zh" style="font-size:18px">${esc(it.prompt)}</div>
        <textarea class="field jp" lang="ja" data-autofocus placeholder="用日文寫在這裡，會自動保存草稿" oninput="saveDraft(this.value)">${esc(txt)}</textarea>
        <div class="hint"><span class="wc">${[...txt.replace(/\s/g,'')].length}</span> 字</div>
        ${r.phase === 'feedback' ? `<div class="sec-h">範例</div><div class="card"><div class="passage-j" lang="ja">${jaLine(it.sampleT, {tap:true})}</div></div>` : ''}`;
    },
    foot: r => r.phase === 'feedback' ? '' : `<button class="secondary" onclick="skipItem()">先跳過</button><button class="primary" onclick="checkItem()">完成，看範例</button>`,
    check: (it, r) => { const k = jKey(r.ctx.lv, r.ctx.u); const txt = r.tmp.text ?? ((state.drafts[k] || {})[r.idx]) ?? ''; if (!txt.trim()) return toast('先寫一點'); finish(true, '', '', txt); },
  },
  jc: {
    render: (it, r) => {
      const fb = r.phase === 'feedback', v = it.v;
      if (it.kind === 'w2z') return `<div class="q jp" lang="ja" style="text-align:center;font-size:40px">${esc(v.w)}</div><div style="text-align:center;margin:-8px 0 16px">${spkJa(v.w, '聽')}</div>
        ${fb ? `<div style="text-align:center;margin-bottom:12px" lang="ja">${esc(v.r)}</div>` : ''}${optsHTML(it.opts, 'zh', r.tmp.pick, fb ? {correct: it.a, chosen: r.tmp.pick} : null)}`;
      return `<div class="q zh" style="text-align:center">${esc(v.zh)}</div>${optsHTML(it.opts, 'jp', r.tmp.pick, fb ? {correct: it.a, chosen: r.tmp.pick} : null, o => rubyTok(o[0], o[1]))}`;
    },
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); TTS.speakJa(it.v.w); finish(r.tmp.pick === it.a, `${it.v.w}（${it.v.r}）＝${it.v.zh}`, '', ''); },
  },
  /* ---------- 書本理解題、生字本 ---------- */
  rd_q: {
    render: (it, r) => {
      const fb = r.phase === 'feedback';
      if (it.lang === 'ja') return `<div class="zhhint">${esc(it.zh || '')}</div><div class="qj" lang="ja">${jaLine(it.q)}</div>${optsHTML(it.opts, 'jp', r.tmp.pick, fb ? {correct: it.a, chosen: r.tmp.pick} : null, o => jaLine(o))}`;
      return ITEM.mc.render(it, r);
    },
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); finish(r.tmp.pick === it.a, it.lang === 'ja' ? jaText(it.opts[it.a]) : it.opts[it.a], '', ''); },
  },
  srs: {
    render: (it, r) => {
      const fb = r.phase === 'feedback', g = it.g;
      const head = it.lang === 'ja' ? `<div class="q jp" lang="ja" style="text-align:center;font-size:40px">${rubyTok(it.w, g.r)}</div><div style="text-align:center;margin:-8px 0 16px">${spkJa(it.w, '聽')}</div>`
        : `<div class="q" style="text-align:center;font-family:var(--serif);font-size:38px">${esc(it.w)}</div><div style="text-align:center;margin:-8px 0 16px">${spkEn(it.w, '聽')}</div>`;
      return head + optsHTML(it.opts, 'zh', r.tmp.pick, fb ? {correct: it.a, chosen: r.tmp.pick} : null) + (fb && it.ex ? `<div class="hint" style="margin-top:14px">出自：${esc(it.ex)}</div>` : '');
    },
    check: (it, r) => { if (r.tmp.pick == null) return toast('先選一個答案'); const ok = r.tmp.pick === it.a; srsGrade(it.lang, it.w, ok); finish(ok, it.opts[it.a], '', ''); },
  },
};

/* =========================================================
   進度
========================================================= */
function enCompletion(day){
  let tot = 0, done = 0;
  BLOCKS.forEach(b => { const n = enItems(day, b.id).length; if (!n) return; tot += n; done += Math.min(n, ((state.progress[day] || {})[b.id] || {done:0}).done); });
  return tot ? done / tot : null;
}
function renderProgress(){
  const t = enToday(), total = enTotal();
  const cells = Array.from({length: total}, (_, i) => { const d = i + 1, c = enCompletion(d), rest = enDay(d).rest;
    return `<button class="cell ${d === t ? 'today' : ''} ${d > t ? 'future' : ''} ${c === 1 ? 'full' : ''}" onclick="state.day=${d};state.lang='en';go('home')" ${rest ? 'title="休息"' : ''}><b style="height:${Math.round((c || 0) * 100)}%"></b><span>${rest ? '休' : d}</span></button>`; }).join('');
  const weeks = Object.entries(state.tests.weekly || {});
  const jaDone = [];
  for (const lv of LEVELS_JA) for (const x of DATA.jaIndex.levels[lv]){ const p = state.jprog[jKey(lv, x.unit)]; if (p) jaDone.push(`${lv}-${x.unit}`); }
  return `<div class="screen">
    <h1>進度</h1>
    <div class="sec-h">英文 61 天（填色＝完成率）</div>
    <div class="grid">${cells}</div>
    <div class="legend"><span><i style="background:var(--green-soft)"></i>部分</span><span><i style="background:var(--green)"></i>完成</span><span><i style="border:2px solid var(--blue);width:9px;height:9px"></i>今天</span></div>
    <h2>英文週檢測</h2>
    ${weeks.length ? `<table class="tbl"><tr><th>週</th><th>分數</th><th>判定</th><th>日期</th></tr>${weeks.map(([w, r]) => `<tr><td>${w === '9' ? '補充週' : '第 ' + w + ' 週'}</td><td>${r.score}%</td><td>${r.score >= 80 ? '進下一週' : r.score >= 60 ? '做完 Day 7 再考' : '重做 Day 2–4'}</td><td>${r.date}</td></tr>`).join('')}</table>` : '<p class="muted">還沒有週檢測紀錄。</p>'}
    <h2>日文</h2>
    ${jaDone.length ? `<p>已開始 ${jaDone.length} 課：${jaDone.join('、')}</p>` : '<p class="muted">還沒開始日文課程。</p>'}
    ${Object.entries(state.jmock).length ? `<table class="tbl"><tr><th>模擬測驗</th><th>分數</th><th>結果</th><th>日期</th></tr>${Object.entries(state.jmock).map(([lv, r]) => `<tr><td>${lv}</td><td>${r.score}%</td><td>${r.pass ? '合格' : '未合格'}</td><td>${r.date}</td></tr>`).join('')}</table>` : ''}
  </div>`;
}

/* =========================================================
   檢測
========================================================= */
function renderTests(){
  const L = state.testsLang;
  const sw = `<div class="langsw"><button class="${L==='en'?'sel':''}" onclick="state.testsLang='en';render()">English</button><button class="${L==='ja'?'sel':''}" onclick="state.testsLang='ja';render()">日本語 JLPT</button></div>`;
  return `<div class="screen"><h1>檢測</h1>${sw}${L === 'ja' ? renderJaTests() : renderEnTests()}</div>`;
}
function renderEnTests(){
  const T = DATA.en.tests, today = enToday(), wk = Math.ceil(today / 7);
  const last = id => { const r = id.startsWith('w') ? (state.tests.weekly || {})[id.slice(1)] : state.tests[id]; return r ? r.score + '%' : '未做'; };
  const rows = [['diagnostic', T.diagnostic.title || '入門診斷', '開始前做一次，當基準線']].concat(
    Object.keys(T.weekly).map(w => ['w' + w, T.weekly[w].title || `第 ${w} 週週檢測`, w === '9' ? 'Day 61 之後' : `建議 Day ${(w - 1) * 7 + 6} 之後`])
  ).concat([['final', T.final.title || '結業測驗', 'Day 54 之後；混合七個文法點'], ['retention', '單字保留率', '每 2 週一次，只抽 7 天前學過的字'], ['cefr', 'CEFR 自評', 'Day 0 / 28 / 56']]);
  const ret = state.tests.retention, fin = state.tests.final;
  const lastCefr = state.cefr[state.cefr.length - 1];
  const a1ok = lastCefr && lastCefr.scores.slice(0, 10).every(x => x >= 2);
  const efOk = state.external.some(e => /EF/i.test(e.provider) && /A2|B1|B2|C1|C2/.test(e.level));
  const chk = (ok, label, v) => `<div class="gp"><span>${label}</span><span class="pill ${ok == null ? 'na' : ok ? 'ok' : 'no'}">${ok == null ? '未做' : v}</span></div>`;
  return `<div class="muted">考試模式不顯示對錯，交卷後才看分數與弱項</div>
    <ul class="list">${rows.map(([id, name, sub]) => `<li><button onclick="startTest('${id}')"><span><div>${esc(name)}</div><div class="sub">${esc(sub)}</div></span><span class="muted">${id === 'cefr' ? (lastCefr ? lastCefr.date : '未做') : last(id)}</span></button></li>`).join('')}</ul>
    <h2>外部驗證</h2>
    <div class="muted small">EF SET 在 Day 0 與 Day 56 各做一次；Cambridge / British Council 每月抽查</div>
    <div class="ext-form">
      <select id="ext-p" class="field"><option>EF SET</option><option>Cambridge</option><option>British Council</option></select>
      <input id="ext-d" class="field" type="date" value="${todayStr()}">
      <input id="ext-l" class="field" placeholder="等級（A1/A2…）">
      <input id="ext-s" class="field" placeholder="分數">
      <button class="secondary full" onclick="addExternal()">記錄一次結果</button>
    </div>
    ${state.external.length ? `<table class="tbl"><tr><th>測驗</th><th>日期</th><th>等級</th><th>分數</th></tr>${state.external.map(e => `<tr><td>${esc(e.provider)}</td><td>${esc(e.date)}</td><td>${esc(e.level)}</td><td>${esc(e.score)}</td></tr>`).join('')}</table>` : ''}
    <h2>進入 Phase 1 條件</h2>
    ${chk(fin ? fin.score >= 80 : null, '結業測驗 ≥ 80%', fin && fin.score + '%')}
    ${chk(ret ? ret.score >= 70 : null, '單字保留率 ≥ 70%', ret && ret.score + '%')}
    ${chk(lastCefr ? a1ok : null, 'A1 自評十項全部 ≥ 2', lastCefr && (a1ok ? '達成' : '未達成'))}
    ${chk(state.external.length ? efOk : null, 'EF SET 顯示 A2 以上', efOk ? '達成' : '未達成')}`;
}
function addExternal(){
  const g = id => document.getElementById(id).value;
  if (!g('ext-d')) return toast('請填日期');
  state.external.unshift({provider: g('ext-p'), date: g('ext-d'), level: g('ext-l'), score: g('ext-s')}); persist(); render(); toast('已記錄');
}
function startTest(id){
  const T = DATA.en.tests;
  if (id === 'cefr') return openCefr();
  let items, title;
  if (id === 'diagnostic'){ items = T.diagnostic.items; title = '入門診斷'; }
  else if (id === 'final'){ items = T.final.items; title = '結業測驗'; }
  else if (id === 'retention'){
    const today = enToday();
    const pool = T.retention.pool.filter(x => x.learnedDay <= today - 7);
    if (pool.length < 10) return toast('7 天前學過的字還不夠，過幾天再來');
    items = shuffle(pool).slice(0, 30).map(c => { const o = shuffle([c.zh, ...shuffle(pool.filter(x => x.zh !== c.zh)).slice(0, 3).map(x => x.zh)]); return {type:'mc', q:`「${c.w}」是什麼意思？`, opts:o, a:o.indexOf(c.zh), gp:'單字', speak:c.w}; });
    title = '單字保留率';
  } else { const w = id.slice(1); items = T.weekly[w].items; title = T.weekly[w].title || `第 ${w} 週週檢測`; }
  openRunner({title, block:'exam', items, exam:true, testId:id, examLang:'en'});
}
function renderExamResult(){
  const r = state.runner;
  const byGp = {};
  r.examAnswers = r.examAnswers.filter(Boolean);
  r.examAnswers.forEach(({item, ok}) => { const g = item.gp || item.sec || '其他'; byGp[g] = byGp[g] || {n:0, ok:0}; byGp[g].n++; if (ok) byGp[g].ok++; });
  const score = Math.round(r.examAnswers.filter(a => a.ok).length / r.items.length * 100);
  const rec = {score, byGp: Object.fromEntries(Object.entries(byGp).map(([g, v]) => [g, Math.round(v.ok / v.n * 100)])), date: todayStr()};
  let verdict = '';
  if (r.examLang === 'ja'){
    const pass = score >= r.pass && Object.values(rec.byGp).every(p => p >= 40);
    rec.pass = pass; state.jmock[r.level] = rec;
    verdict = `<div class="verdict ${pass ? 'pass' : 'fail'}">${pass ? '合格' : '未合格'}（合格線 ${r.pass}%，且每一區 ≥ 40%）</div>`;
  } else if (r.testId.startsWith('w')){ state.tests.weekly = state.tests.weekly || {}; state.tests.weekly[r.testId.slice(1)] = rec;
    verdict = `<div class="note">${score >= 80 ? '≥80%，進下一週' : score >= 60 ? '60–79%，做完 Day 7 再考一次' : '<60%，重做 Day 2–4 再考'}</div>`;
  } else state.tests[r.testId] = rec;
  persist();
  const wrong = r.examAnswers.filter(a => !a.ok);
  return `<div class="r-head"><div class="row"><span></span><span class="title">${esc(r.title)}</span><span></span></div></div>
    <div class="r-body"><div class="done-box"><div class="big">${score}%</div><div class="muted">${r.items.length} 題</div>${verdict}</div>
      <h2>${r.examLang === 'ja' ? '各區得分' : '各文法點正確率'}</h2>
      <div class="secbars">${Object.entries(rec.byGp).map(([g, p]) => `<div class="sb"><span>${esc(g)}</span><span class="tr"><i class="${p < (r.examLang === 'ja' ? 40 : 70) ? 'low' : ''}" style="width:${p}%"></i></span><span class="v">${p}%</span></div>`).join('')}</div>
      ${wrong.length ? `<h2>錯的題目</h2><ul class="wrongs">${wrong.map(w => `<li><div ${r.examLang === 'ja' ? 'lang="ja"' : ''}>${rich(w.item.q)}</div><div class="muted">正解：${esc((w.item.opts || w.item.o)[w.item.a])}${w.item.exp ? '　' + esc(w.item.exp) : ''}</div></li>`).join('')}</ul>` : ''}
    </div>
    <div class="r-foot"><button class="primary" onclick="closeRunner()">回檢測</button></div>`;
}
function openCefr(){
  const T = DATA.en.tests.cefr.items;
  const last = state.cefr[state.cefr.length - 1];
  const scores = last ? last.scores.slice() : T.map(() => 0);
  state.runner = {cefr: true, scores};
  const el = document.getElementById('runner');
  document.getElementById('nav').classList.add('hidden'); el.classList.remove('hidden');
  const draw = () => { el.innerHTML = `<div class="r-head"><div class="row"><button class="x" onclick="closeRunner()" aria-label="離開">✕</button><span class="title">CEFR 自評</span><span></span></div></div>
    <div class="r-body"><p class="muted small">0＝完全不行　1＝勉強　2＝大致可以　3＝很有把握。自評會偏高，要和測驗分數對照看。</p>
    ${T.map(([lv, t], i) => `<div class="cando"><span><span class="tag" style="margin:0 6px 0 0">${lv}</span>${esc(t)}</span><span class="seg">${[0,1,2,3].map(n => `<button class="${scores[i] === n ? 'sel' : ''}" onclick="state.runner.scores[${i}]=${n};this.parentNode.querySelectorAll('button').forEach((b,k)=>b.classList.toggle('sel',k===${n}))">${n}</button>`).join('')}</span></div>`).join('')}
    ${state.cefr.length ? `<h2>過去紀錄</h2><table class="tbl"><tr><th>日期</th><th>A1 平均</th><th>A2 平均</th></tr>${state.cefr.map(c => `<tr><td>${c.date}</td><td>${(c.scores.slice(0, 10).reduce((a, b) => a + b, 0) / 10).toFixed(1)}</td><td>${(c.scores.slice(10).reduce((a, b) => a + b, 0) / 10).toFixed(1)}</td></tr>`).join('')}</table>` : ''}</div>
    <div class="r-foot"><button class="primary" onclick="saveCefr()">儲存這次自評</button></div>`; };
  draw();
}
function saveCefr(){ state.cefr.push({date: todayStr(), scores: state.runner.scores.slice()}); persist(); toast('已儲存'); closeRunner(); }
function renderJaTests(){
  return `<div class="muted">五級模擬測驗各 40 題（文字語彙 12／文法 12／讀解 8／聽解 8）。合格：總分達合格線，且每一區 ≥ 40%。</div>
    <ul class="list">${LEVELS_JA.map(lv => { const r = state.jmock[lv]; return `<li><button onclick="startMock('${lv}')"><span><div>JLPT ${lv} 模擬測驗</div><div class="sub">40 題・約 40–60 分鐘</div></span><span class="muted">${r ? r.score + '%' + (r.pass ? ' 合格' : '') : '未做'}</span></button></li>`; }).join('')}</ul>
    <h2>考試日程（推估）</h2>
    <div class="gp"><span>JLPT N4</span><span>2027/7/4</span></div><div class="gp"><span>JLPT N3</span><span>2027/12/5</span></div><div class="gp"><span>JLPT N2</span><span>2028/12/3</span></div>
    <p class="muted small">考期依「每年 7 月與 12 月第一個週日」推估，報名前以 LTTC 公告為準。</p>`;
}
async function startMock(lv){
  const D = await ensureJa(lv); const m = D.mock;
  const items = m.items.map(x => Object.assign({gp: x.sec, opts: x.o}, x));
  openRunner({title:`JLPT ${lv} 模擬測驗`, block:'exam', items, exam:true, testId:'mock-' + lv, examLang:'ja', level: lv, pass: m.pass});
}

/* =========================================================
   設定
========================================================= */
function renderSettings(){
  const s = state.settings;
  const voiceSel = (list, key, sample, fn) => `<select class="sel-input" onchange="state.settings.${key}=this.value;persist();${fn}(${q(sample)})">${list.length ? list.map(v => `<option ${v.name === s[key] ? 'selected' : ''} value="${esc(v.name)}">${esc(v.name)}</option>`).join('') : '<option>（無）</option>'}</select>`;
  return `<div class="screen"><h1>設定</h1>
    <h2>英文</h2><ul class="list">
      <li><label><span><div>英文語音</div></span>${voiceSel(TTS.voices, 'voice', 'My aunt lives in Taichung.', 'TTS.speakEn')}</label></li>
      <li><label><span><div>語速</div><div class="sub" id="rate-v">${s.rate}×</div></span><input type="range" min="0.7" max="1.2" step="0.05" value="${s.rate}" oninput="state.settings.rate=+this.value;document.getElementById('rate-v').textContent=this.value+'×'" onchange="persist();TTS.speakEn('My uncle has a big house.')"></label></li>
      <li><label><span><div>每日量</div><div class="sub">完成率低於 60% 就降</div></span><span class="seg">${[100,75,50].map(a => `<button class="${s.amount === a ? 'sel' : ''}" onclick="state.settings.amount=${a};persist();render()">${a}%</button>`).join('')}</span></label></li>
      <li><label><span><div>單字複習模式</div></span><span class="seg"><button class="${s.reviewMode === 'choice' ? 'sel' : ''}" onclick="state.settings.reviewMode='choice';persist();render()">四選一</button><button class="${s.reviewMode === 'typing' ? 'sel' : ''}" onclick="state.settings.reviewMode='typing';persist();render()">打字</button></span></label></li>
    </ul>
    <h2>日文</h2><ul class="list">
      <li><label><span><div>日文顯示</div><div class="sub">漢字上方標假名</div></span><span class="seg">${[['furigana','注音'],['kana','只用假名'],['romaji','＋拼音']].map(([k, l]) => `<button class="${s.jaScript === k ? 'sel' : ''}" onclick="state.settings.jaScript='${k}';persist();render()">${l}</button>`).join('')}</span></label></li>
      <li><label><span><div>詞間空格</div></span><span class="seg"><button class="${s.jaGap ? 'sel' : ''}" onclick="state.settings.jaGap=true;persist();render()">開</button><button class="${!s.jaGap ? 'sel' : ''}" onclick="state.settings.jaGap=false;persist();render()">關</button></span></label></li>
      <li><label><span><div>日文語音</div><div class="sub">${TTS.jvoices.length ? '選了會試播一句。聲音不自然就換一個。' : '沒有找到日文語音'}</div></span>${voiceSel(TTS.jvoices, 'jaVoice', '桃太郎は川へ行きました。', 'TTS.speakJa')}</label></li>
      <li><div class="note" style="margin:10px 0">日文語音建議：Mac 到「系統設定 → 輔助使用 → 朗讀內容 → 系統聲音 → 管理聲音」下載日文的 Kyoko 或 O-Ren（加強版更自然）；iPhone 到「設定 → 輔助使用 → 朗讀內容 → 聲音 → 日文」下載；Chrome 也可以選「Google 日本語」。</div></li>
    </ul>
    <h2>進度</h2>
    <div class="muted small">進度存在這支手機的瀏覽器裡。換裝置或清除瀏覽資料前，先匯出。</div>
    <button class="secondary" style="margin-top:10px" onclick="exportProgress()">匯出進度 JSON</button>
    <label class="secondary" style="margin-top:10px;display:block;text-align:center;cursor:pointer">匯入進度 JSON<input type="file" accept=".json" style="display:none" onchange="importProgress(this.files[0])"></label>
    <button class="secondary" style="margin-top:10px;color:var(--red)" onclick="if(confirm('清除所有進度、草稿、錯題與檢測紀錄？'))resetAll()">重置所有進度</button>
    <p class="muted small" style="margin-top:20px">題庫版本：英文 ${enTotal()} 天、日文 ${LEVELS_JA.map(lv => DATA.jaIndex.levels[lv].length).reduce((a, b) => a + b, 0)} 課、讀物 ${DATA.lib.en.length + DATA.lib.ja.length} 本</p>
  </div>`;
}
const SAVE_KEYS = ['progress','jprog','jwrong','jtasks','drafts','tests','jmock','external','cefr','words','readTime','readPos','settings'];
function exportProgress(){
  const o = {version: 3}; SAVE_KEYS.forEach(k => o[k] = state[k]);
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(o, null, 1)], {type:'application/json'}));
  a.download = `ejlp-progress-${todayStr()}.json`; a.click();
}
function importProgress(f){ if (!f) return; f.text().then(t => { try{ const o = JSON.parse(t); SAVE_KEYS.forEach(k => { if (o[k] !== undefined) state[k] = o[k]; }); persist(); render(); toast('進度已匯入'); }catch(e){ toast('JSON 格式錯誤'); } }); }
function resetAll(){ SAVE_KEYS.filter(k => k !== 'settings').forEach(k => state[k] = Array.isArray(state[k]) ? [] : (k === 'words' ? {en:{}, ja:{}} : {})); persist(); render(); toast('已重置'); }

/* =========================================================
   生字本（間隔重複 1、2、4、7、15、30 天）與閱讀時間
========================================================= */
const SRS_INT = [0, 1, 2, 4, 7, 15, 30];
function addDaysStr(n){ return ymd(addDays(todayD(), n)); }
function isSaved(lang, w){ return !!(state.words[lang] || {})[w]; }
function toggleSave(lang, w, ex){ state.words[lang] = state.words[lang] || {}; if (state.words[lang][w]) delete state.words[lang][w]; else state.words[lang][w] = {added: todayStr(), box: 0, due: todayStr(), ex: ex || ''}; persist(); }
function srsGrade(lang, w, ok){ const e = (state.words[lang] || {})[w]; if (!e) return; e.box = ok ? Math.min(SRS_INT.length - 1, e.box + 1) : 0; e.due = addDaysStr(ok ? SRS_INT[e.box] : 1); persist(); }
function dueWords(lang){ const t = todayStr(); return Object.entries(state.words[lang] || {}).filter(([w, e]) => e.due <= t).map(([w]) => w); }
function glossOf(lang, w){ const G = DATA.gloss[lang]; return G[w] || (lang === 'ja' && state.words.ja[w] && state.words.ja[w].g) || null; }
function startSrs(lang){
  const due = dueWords(lang); if (!due.length) return toast('目前沒有到期的生字');
  const all = Object.entries(DATA.gloss[lang]).filter(([k, g]) => g.zh);
  const items = due.slice(0, 30).map(w => { const g = glossOf(lang, w) || {zh:'?', r:''};
    const o = shuffle([g.zh, ...shuffle(all.filter(([k, x]) => x.zh !== g.zh)).slice(0, 3).map(([k, x]) => x.zh)]);
    return {lang, w, g, opts:o, a:o.indexOf(g.zh), ex: state.words[lang][w].ex}; });
  openRunner({title: lang === 'ja' ? '日文生字複習' : '英文生字複習', block:'srs', items, p:{done:0, correct:0, skipped:[], answers:{}}, temp:true});
}
function addReadSec(n){ const t = todayStr(); state.readTime[t] = (state.readTime[t] || 0) + n; }
setInterval(() => { if (state.reader && !document.hidden && Date.now() - (state.reader.lastAct || 0) < 120000){ addReadSec(5); if (Math.random() < .2) persist(); const el = document.getElementById('rd-tm'); if (el) el.innerHTML = timerHTML(); } }, 5000);
function readMin(){ return Math.floor((state.readTime[todayStr()] || 0) / 60); }
function streak(){ let n = 0; for (let i = 0; i < 400; i++){ const k = ymd(addDays(todayD(), -i)); if ((state.readTime[k] || 0) >= 600) n++; else if (i > 0) break; } return n; }
function timerHTML(){ const m = readMin(); return `今日 ${Math.min(m, 99)}/10 分${m >= 10 ? ' ✓' : ''}`; }

/* =========================================================
   閱讀：書架與閱讀器
========================================================= */
function renderRead(){
  const L = state.shelf.lang, books = DATA.lib[L] || [], levels = L === 'ja' ? LEVELS_JA : EN_LEVELS;
  const lv = state.shelf.level, shown = books.filter(b => !lv || b.level === lv);
  const m = readMin(), pct = Math.min(1, m / 10), C = 2 * Math.PI * 22;
  const words = Object.keys(state.words[L] || {}), due = dueWords(L).length;
  return `<div class="screen"><h1>閱讀</h1>
    <div class="goal"><svg width="56" height="56" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="22" fill="none" stroke="var(--rule)" stroke-width="6"/><circle cx="28" cy="28" r="22" fill="none" stroke="var(--tr)" stroke-width="6" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - pct)}" transform="rotate(-90 28 28)"/></svg>
      <div><b>${m}</b> / 10 分鐘<div class="muted small">每天讀 10 分鐘${streak() ? `　連續 ${streak()} 天` : ''}</div></div></div>
    <div class="langsw"><button class="${L === 'en' ? 'sel' : ''}" onclick="state.shelf={lang:'en',level:null};render()">English</button><button class="${L === 'ja' ? 'sel' : ''}" onclick="state.shelf={lang:'ja',level:null};render()">日本語</button></div>
    <div class="lv"><button class="${!lv ? 'sel' : ''}" onclick="state.shelf.level=null;render()">全部</button>${levels.map(x => { const n = books.filter(b => b.level === x).length; return `<button class="${lv === x ? 'sel' : ''} ${n ? '' : 'empty'}" onclick="state.shelf.level='${x}';render()">${x}${n ? '' : ' 製作中'}</button>`; }).join('')}</div>
    ${shown.length ? `<div class="books">${shown.map(b => { const done = (state.readPos[b.id] || {}).done || []; const p = done.length / b.chapters.length;
      return `<button class="book" onclick="openBook('${L}','${b.id}')"><div class="cover ${L}" style="background:linear-gradient(160deg,${b.color[0]},${b.color[0]} 55%,${b.color[1]})"><span class="lvb">${b.level}</span>
          <div class="ct">${L === 'ja' ? rubyTok(b.title, b.reading) : esc(b.title)}</div><div class="ca">${esc(b.author)}</div></div>
        <div class="bt">${esc(b.sub)}</div><div class="bp">${b.chapters.length} 章　${done.length ? `已讀 ${done.length}` : '未開始'}</div><div class="pbar"><b style="width:${p * 100}%"></b></div></button>`; }).join('')}</div>`
      : `<p class="muted">${lv} 的書還在製作中。先讀 ${levels[0]}–${levels[1]} 的書，程度到了這裡會補上。</p>`}
    <h2>生字本</h2>
    <div class="row"><span class="muted small">${words.length} 個字　${due} 個到期</span><button class="ghost" onclick="startSrs('${L}')" ${due ? '' : 'disabled'}>複習到期的字</button></div>
    ${words.length ? `<ul class="wl">${words.slice(-30).reverse().map(w => { const g = glossOf(L, w) || {}; return `<li><button style="text-align:left;flex:1" onclick="openSheet('${L}',${q(w)},'',null)"><span class="w1 ${L === 'ja' ? 'jp' : ''}">${L === 'ja' ? rubyTok(w, g.r) : esc(w)}</span></button><span class="w2">${esc(g.zh || '')}<br>${L === 'en' ? rubyTok(...(g.ja || ['', ''])) : esc(g.en || '')}</span></li>`; }).join('')}</ul>`
      : `<p class="muted small">閱讀時點單字，按「加入生字本」就會出現在這裡，並依遺忘曲線排程複習。</p>`}
  </div>`;
}
function openBook(lang, id, ch){
  const b = DATA.lib[lang].find(x => x.id === id); const pos = state.readPos[id] || {};
  state.reader = {lang, b, ch: ch ?? Math.min(pos.ch || 0, b.chapters.length - 1), mode: pos.mode || 'tr', cur: -1, playing: false, lastAct: Date.now()};
  document.getElementById('nav').classList.add('hidden'); document.getElementById('reader').classList.remove('hidden'); renderReader();
}
function closeReader(){ stopPlay(); persist(); state.reader = null; document.getElementById('reader').classList.add('hidden'); document.getElementById('nav').classList.remove('hidden'); render(); }
function setMode(m){ const R = state.reader; R.mode = m; R.lastAct = Date.now(); state.readPos[R.b.id] = Object.assign(state.readPos[R.b.id] || {}, {mode: m}); persist(); if (m === 'listen'){ R.cur = Math.max(0, R.cur); renderReader(); startPlay(); } else { stopPlay(); renderReader(); } }
function enTokens(t){
  return t.split(/([A-Za-z]+(?:'[a-z]+)?)/).map((p, i) => {
    if (i % 2 === 0) return esc(p);
    const k = p.toLowerCase(); if (!DATA.gloss.en[k]) return esc(p);
    return `<span class="w ${isSaved('en', k) ? 'saved' : ''}" data-en="${esc(k)}">${esc(p)}</span>`;
  }).join('');
}
function renderReader(){
  const R = state.reader, b = R.b, c = b.chapters[R.ch], L = R.lang, el = document.getElementById('reader');
  const trOn = R.mode === 'tr' || R.mode === 'listen';
  const trKey = L === 'en' ? (state.settings.trLang === 'ja' ? 'ja' : 'zh') : (state.settings.trLang === 'en' ? 'en' : 'zh');
  const sents = c.s.map((s, i) => {
    const tr = trOn ? `<div class="tr ${trKey === 'ja' ? 'jp' : ''}">${esc(s[trKey] || s.zh)}</div>` : '';
    const tx = L === 'en' ? `<div class="tx">${enTokens(s.t)}</div>` : `<div class="tx jp" lang="ja">${jaLine(s.toks, {tap: true, saved: w => isSaved('ja', w)})}</div>`;
    return `<div class="sent ${i === R.cur ? 'cur' : ''}" id="s${i}" data-i="${i}">${tr}${tx}<button class="sp" onclick="playOne(${i})" aria-label="朗讀這句">🔊</button></div>`;
  }).join('');
  const last = R.ch >= b.chapters.length - 1;
  el.style.setProperty('--rdfs', state.settings.rdfs + 'px');
  const trBtns = L === 'en' ? [['zh','中文'],['ja','日本語']] : [['zh','中文'],['en','English']];
  el.innerHTML = `
    <div class="rd-head"><button onclick="closeReader()" aria-label="離開">✕</button>
      <div class="t">${L === 'ja' ? rubyTok(b.title, b.reading) : esc(b.title)}<small>第 ${R.ch + 1}／${b.chapters.length} 章　${b.level}</small></div>
      <button onclick="cycleFont()" aria-label="字級" style="font-family:var(--serif);font-weight:700">Aa</button></div>
    <div class="modes"><button class="${R.mode === 'read' ? 'sel' : ''}" onclick="setMode('read')">📖 閱讀</button><button class="${R.mode === 'listen' ? 'sel' : ''}" onclick="setMode('listen')">🎧 收聽</button><button class="${R.mode === 'tr' ? 'sel' : ''}" onclick="setMode('tr')">🌐 翻譯</button></div>
    <div class="rd-body" id="rd-body">
      <div class="chap-t ${L === 'ja' ? 'jp' : ''}">${L === 'ja' ? rubyTok(c.title, c.reading) : esc(c.title)}</div><div class="chap-s">${esc(c.zh)}　·　點單字看${L === 'en' ? '中、日文' : '中、英文'}與發音</div>
      ${sents}
      <div class="rd-end">
        <button class="primary" onclick="chapterQuiz()">讀完了，做 ${c.qs.length} 題理解題</button>
        <div class="daynav">${R.ch > 0 ? `<button class="ghost" onclick="gotoCh(${R.ch - 1})">‹ 上一章</button>` : '<span></span>'}${!last ? `<button class="ghost" onclick="gotoCh(${R.ch + 1})">下一章 ›</button>` : '<span></span>'}</div>
        <div class="muted small" style="margin-top:8px">翻譯語言：${trBtns.map(([k, l]) => `<button class="ghost" onclick="setTr('${k}')" ${trKey === k ? 'style="text-decoration:underline"' : ''}>${l}</button>`).join('')}</div>
      </div>
    </div>
    <div class="player"><div>
      <button onclick="stepSent(-1)" aria-label="上一句">⏮</button><button class="pp" onclick="togglePlay()" aria-label="播放">${R.playing ? '⏸' : '▶'}</button><button onclick="stepSent(1)" aria-label="下一句">⏭</button>
      <button class="spd" onclick="cycleRate()">${state.settings.rdRate}×</button><div class="tm" id="rd-tm">${timerHTML()}</div>
    </div></div>`;
  const body = document.getElementById('rd-body');
  body.onclick = e => { R.lastAct = Date.now(); const w = e.target.closest('.w'); if (!w) return;
    const sent = c.s[+w.closest('.sent').dataset.i];
    if (L === 'en') openSheet('en', w.dataset.en, sent.t, w); else openSheetJa(w, jaText(sent.toks)); };
  body.onscroll = () => { R.lastAct = Date.now(); };
}
function gotoCh(i){ stopPlay(); const R = state.reader; R.ch = i; R.cur = -1; state.readPos[R.b.id] = Object.assign(state.readPos[R.b.id] || {}, {ch: i}); persist(); renderReader(); document.getElementById('rd-body').scrollTop = 0; }
function setTr(k){ state.settings.trLang = k; persist(); renderReader(); }
function cycleFont(){ const s = [18, 20, 22, 25, 28]; state.settings.rdfs = s[(s.indexOf(state.settings.rdfs) + 1) % s.length]; persist(); renderReader(); }
function cycleRate(){ const s = [0.6, 0.75, 0.9, 1.0]; state.settings.rdRate = s[(s.indexOf(state.settings.rdRate) + 1) % s.length]; persist(); renderReader(); }
function sentText(i){ const R = state.reader, s = R.b.chapters[R.ch].s[i]; return R.lang === 'en' ? s.t.replace(/["“”]/g, '') : jaText(s.toks); }
function markCur(i){ const R = state.reader; R.cur = i; document.querySelectorAll('#reader .sent').forEach(e => e.classList.toggle('cur', +e.dataset.i === i)); const el = document.getElementById('s' + i); if (el) el.scrollIntoView({block:'center', behavior: matchMedia('(prefers-reduced-motion:reduce)').matches ? 'auto' : 'smooth'}); }
function speakSent(i, onend){ const R = state.reader; R.lastAct = Date.now(); markCur(i); (R.lang === 'en' ? TTS.speakEn : TTS.speakJa).call(TTS, sentText(i), state.settings.rdRate, onend); }
function playOne(i){ stopPlay(); speakSent(i); }
function startPlay(){ const R = state.reader; R.playing = true; const n = R.b.chapters[R.ch].s.length;
  const run = i => { if (!state.reader || !R.playing) return; if (i >= n){ R.playing = false; renderPlayerBtn(); return; } speakSent(i, () => { if (R.playing) setTimeout(() => run(i + 1), 350); }); };
  run(Math.max(0, R.cur)); renderPlayerBtn(); }
function stopPlay(){ const R = state.reader; if (R) R.playing = false; TTS.cancel(); renderPlayerBtn(); }
function togglePlay(){ const R = state.reader; if (R.playing) stopPlay(); else { if (R.cur < 0) R.cur = 0; startPlay(); } }
function stepSent(d){ const R = state.reader; const n = R.b.chapters[R.ch].s.length; const i = Math.min(n - 1, Math.max(0, (R.cur < 0 ? 0 : R.cur) + d)); const was = R.playing; stopPlay(); R.cur = i; if (was) startPlay(); else speakSent(i); }
function renderPlayerBtn(){ const b = document.querySelector('#reader .pp'); if (b && state.reader) b.textContent = state.reader.playing ? '⏸' : '▶'; }
function chapterQuiz(){
  stopPlay(); const R = state.reader, c = R.b.chapters[R.ch];
  const done = new Set((state.readPos[R.b.id] || {}).done || []); done.add(R.ch); state.readPos[R.b.id] = Object.assign(state.readPos[R.b.id] || {}, {done: [...done]}); persist();
  openRunner({title:'理解題', block:'rd_q', items: c.qs.map(x => Object.assign({lang: R.lang}, x)), p:{done:0, correct:0, skipped:[], answers:{}}, temp:true, back:'reader'});
}

/* ---------- 單字面板 ---------- */
function openSheetJa(node, sentence){
  const t = node.dataset.ja, base = node.dataset.base, r = node.dataset.r;
  const key = (DATA.gloss.ja[t] && t) || (base && DATA.gloss.ja[base] && base) || (base || t);
  openSheet('ja', key, sentence, node, {r, surface: t});
}
function openSheet(lang, w, sentence, node, extra){
  if (state.reader) state.reader.lastAct = Date.now();
  document.querySelectorAll('.w.on').forEach(e => e.classList.remove('on')); if (node) node.classList.add('on');
  let g = glossOf(lang, w);
  if (!g && lang === 'ja') g = {r: extra && extra.r && KANJI.test(w) ? extra.r : '', pos:'', zh:'', en:'', note:'詞彙表還沒收錄這個字'};
  if (!g){ toast('這個字還沒有詞彙資料'); return; }
  const sh = document.getElementById('sheet'); const saved = isSaved(lang, w);
  let body;
  if (lang === 'en'){
    body = `<div class="hw">${esc(w)}</div><div class="ph">${g.ipa ? `/${esc(g.ipa)}/　` : ''}${esc(g.pos)}</div>
      <div class="spkrow" style="margin:0 0 6px">${spkEn(w, '發音')}${spkEn(w, '🐢 慢速', 0.55)}</div>
      <div class="line"><span class="k">中文</span><span class="v">${esc(g.zh)}</span><span></span></div>
      <div class="line"><span class="k">日本語</span><span class="v jp" lang="ja">${rubyTok(g.ja[0], g.ja[1])}${g.ja[1] ? `<div class="romaji" style="font-size:13px">${esc(romaji(g.ja[1]))}</div>` : ''}</span><button class="mini-spk" onclick="TTS.speakJa(${q(g.ja[0])})" aria-label="唸日文">🔊</button></div>`;
  } else {
    const rd = g.r || '';
    body = `<div class="hw jp" lang="ja">${rubyTok(w, rd)}</div><div class="ph">${esc(romaji(rd || w, w))}${g.pos ? '　' + esc(g.pos) : ''}${extra && extra.surface && extra.surface !== w ? `　原文：<span lang="ja">${esc(extra.surface)}</span>` : ''}</div>
      <div class="spkrow" style="margin:0 0 6px">${spkJa(w, '發音')}${spkJa(w, '🐢 慢速', 0.55)}</div>
      ${g.zh ? `<div class="line"><span class="k">中文</span><span class="v">${esc(g.zh)}</span><span></span></div>` : ''}
      ${g.en ? `<div class="line"><span class="k">English</span><span class="v" style="font-family:var(--serif)">${esc(g.en)}</span><button class="mini-spk" onclick="TTS.speakEn(${q((g.en || '').replace(/\(.*?\)/g, '').split(';')[0])})" aria-label="唸英文">🔊</button></div>` : ''}`;
  }
  const canSave = !!(g.zh);
  sh.innerHTML = `<div class="sh" role="dialog" aria-label="單字"><div class="grab"></div>${body}
    ${g.note ? `<div class="note small">${esc(g.note)}</div>` : ''}${sentence ? `<div class="ex ${lang === 'ja' ? 'jp' : ''}" ${lang === 'ja' ? 'lang="ja"' : ''}>${esc(sentence)}</div>` : ''}
    <div class="acts">${canSave ? `<button class="${saved ? 'secondary' : 'primary'}" onclick="toggleSave('${lang}',${q(w)},${q(sentence || '')});closeSheet();if(state.reader)renderReader();else if(!state.runner)render()">${saved ? '從生字本移除' : '加入生字本'}</button>` : ''}<button class="secondary" onclick="closeSheet()">關閉</button></div></div>`;
  sh.classList.remove('hidden');
  (lang === 'en' ? TTS.speakEn : TTS.speakJa).call(TTS, lang === 'ja' && extra && extra.surface ? extra.surface : w);
}
function closeSheet(){ document.getElementById('sheet').classList.add('hidden'); document.querySelectorAll('.w.on').forEach(e => e.classList.remove('on')); }
document.getElementById('sheet').addEventListener('click', e => { if (e.target.id === 'sheet') closeSheet(); });
document.getElementById('runner').addEventListener('click', e => { const w = e.target.closest('.w[data-ja]'); if (w) openSheetJa(w, ''); });

/* ---------- 啟動 ---------- */
if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('sw.js').catch(() => {});
boot();
