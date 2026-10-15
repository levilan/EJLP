# -*- coding: utf-8 -*-
"""把原 Phase 0 練習包（56 天）轉成 EJLP 的英文題庫格式。

輸入：source/p0_weeks.json、source/p0_tests.json（從原練習頁擷取）
      source/p0_vocab_ja.json（單字的日文對照，可缺）
輸出：回傳 dict，由 build_all.py 寫成 data/en.json
"""
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'source')
DAY1 = '2026-08-30'
AREA_ZH = {'be': 'be 動詞', 'poss': '所有格/have', 'present': '現在簡單式', 'there': 'there is/are',
           'count': '可數/some-any', 'past': '過去式', 'future': 'going to/can', 'vocab': '單字',
           'reading': '閱讀', 'cont': '現在進行式'}
CANDO = [
    ["A1", "我能用簡單句子自我介紹（姓名、國籍、職業）"], ["A1", "我能描述我的家人和他們的樣子/個性"],
    ["A1", "我能說出每天的作息，並用 usually/sometimes/never 描述習慣"], ["A1", "我能描述家裡有哪些房間、東西在哪裡"],
    ["A1", "我能在商店或餐廳詢問價錢、點餐、買東西"], ["A1", "我能簡單描述昨天或上週做過的事"],
    ["A1", "我能說出未來計畫，以及我會不會做某件事"], ["A1", "我能問路、給簡單的方向指示"],
    ["A1", "我能看懂簡單短文並回答問題；聽懂簡單句子並拼寫出來"], ["A1", "我能寫一段 5 句以上、包含多種時態的短文"],
    ["A2", "我能描述自己的教育背景、目前工作與居住環境"], ["A2", "我能用完整的段落敘述一段過去的經歷（不只單句）"],
    ["A2", "我能處理日常交易並理解價格、數量、時間表"], ["A2", "我能理解慢速清楚的短對話或公告的重點"],
    ["A2", "我能讀懂簡短的私人信件、廣告、菜單、時刻表"], ["A2", "我能寫簡短的便條、留言、感謝信"],
    ["A2", "我能簡單描述計畫與安排、表達喜好與意見並說明原因"], ["A2", "我能用 and/but/because/so 把想法連成較長的句子"],
    ["A2", "我能請對方重複或說慢一點，並讓簡單對話持續下去"], ["A2", "我能比較兩樣東西（比較級），談論習慣與頻率"],
]


def sample_every(arr, n):
    if len(arr) <= n:
        return list(arr)
    step = len(arr) / n
    return [arr[int(i * step)] for i in range(n)]


def words(s):
    return s.split(' ')


def core(tok):
    return re.sub(r'^[\"“(]+|[.,!?;:\"”)]+$', '', tok)


def conv_error(e):
    """原格式 {wrong, correct, hint} → 點字改錯；改不只一個字時改用整句改寫。"""
    w, c = words(e['wrong']), words(e['correct'])
    if len(w) == len(c):
        diff = [i for i in range(len(w)) if w[i] != c[i]]
        if len(diff) == 1:
            i = diff[0]
            return {'s': e['wrong'], 'wrong': i, 'fix': core(c[i]), 'why': e.get('hint', ''), 'full': e['correct']}
    return {'s': e['wrong'], 'correct': e['correct'], 'why': e.get('hint', ''), 'mode': 'rewrite'}


def make_reorder(cands, n, rnd):
    out, seen = [], set()
    for s in cands:
        s = s.strip()
        ws = s.split(' ')
        if not (4 <= len(ws) <= 10) or s in seen or '"' in s or '“' in s:
            continue
        seen.add(s)
        sh = ws[:]
        for _ in range(12):
            rnd.shuffle(sh)
            if sh != ws:
                break
        out.append({'words': sh, 'a': s})
        if len(out) >= n:
            break
    return out


def min_words(sample):
    return max(8, int(len(sample.split()) * 0.6))


def vocab_review(pool, n, rnd):
    uniq, seen = [], set()
    for v in pool:
        k = v['en'].lower()
        if k not in seen:
            seen.add(k)
            uniq.append(v)
    if len(uniq) < 4:
        return []
    picked = sample_every(uniq, min(n, len(uniq)))
    items = []
    for i, c in enumerate(picked):
        others = [x for x in uniq if x['zh'] != c['zh'] and x['en'].lower() != c['en'].lower()]
        ds = rnd.sample(others, min(3, len(others)))
        if i % 2 == 0:
            opts = [c['zh']] + [d['zh'] for d in ds]
            rnd.shuffle(opts)
            items.append({'q': c['en'], 'a': c['zh'], 'opts': opts, 'dir': 'en2zh'})
        else:
            opts = [c['en']] + [d['en'] for d in ds]
            rnd.shuffle(opts)
            items.append({'q': c['zh'], 'a': c['en'], 'opts': opts, 'dir': 'zh2en'})
    return items


def conv_day(d, ja, first_seen, prog_idx, prior_vocab, rnd):
    vocab = []
    for v in d.get('vocab', []):
        k = v['en'].lower().strip()
        item = {'w': v['en'], 'pos': '', 'zh': v['zh'], 'ex': v.get('example', '')}
        if first_seen.get(k, prog_idx) < prog_idx:
            item['review'] = True
        if v['en'] in ja:
            item['ja'] = ja[v['en']]
        vocab.append(item)
    reorder_src = [a for t in d.get('translate', []) for a in t['answers'][:1]] + [x['text'] for x in d.get('listening', [])]
    return {
        'vocab_new': vocab,
        'vocab_review': vocab_review(prior_vocab or d.get('vocab', []), 60, rnd),
        'mc': [{'q': m['q'], 'opts': m['options'], 'a': m['answer']} for m in d.get('mcq', [])],
        'fill': [{'q': f['q'], 'a': f['answers']} for f in d.get('fill', [])],
        'translate': [{'zh': t['zh'], 'a': t['answers']} for t in d.get('translate', [])],
        'error': [conv_error(e) for e in d.get('errorFix', [])],
        'reorder': make_reorder(reorder_src, 15, rnd),
        'reading': [{'title': '短文 %d' % (i + 1), 'text': r['text'],
                     'qs': [{'q': q['q'], 'opts': q['options'], 'a': q['answer']} for q in r['questions']]}
                    for i, r in enumerate(d.get('readings', []))],
        'dictation': [{'s': x['text']} for x in d.get('listening', [])],
        'speaking': [{'prompt': s, 'model': s} for s in d.get('speaking', [])],
        'writing': [{'prompt': w['prompt'], 'minWords': min_words(w.get('sample', '')), 'sample': w.get('sample', '')}
                    for w in d.get('writings', [])],
    }


def flatten(days, key):
    out = []
    for d in days:
        out += d.get(key, [])
    return out


def review_raw(days):
    return {
        'vocab': sample_every(flatten(days, 'vocab'), 30), 'mcq': sample_every(flatten(days, 'mcq'), 60),
        'fill': sample_every(flatten(days, 'fill'), 60), 'translate': sample_every(flatten(days, 'translate'), 30),
        'errorFix': sample_every(flatten(days, 'errorFix'), 20), 'readings': sample_every(flatten(days, 'readings'), 6),
        'listening': sample_every(flatten(days, 'listening'), 15), 'speaking': sample_every(flatten(days, 'speaking'), 25),
        'writings': sample_every(flatten(days, 'writings'), 5),
    }


def test_items_from(t, area_default=None):
    items = []
    for m in t.get('mcq', []):
        items.append({'type': 'mc', 'q': m['q'], 'opts': m['options'], 'a': m['answer'],
                      'gp': AREA_ZH.get(m.get('area', area_default), m.get('area', ''))})
    rd = t.get('reading')
    rds = rd if isinstance(rd, list) else ([rd] if rd else [])
    for r in rds:
        for q in r['questions']:
            items.append({'type': 'mc', 'q': q['q'], 'opts': q['options'], 'a': q['answer'], 'gp': '閱讀', 'passage': r['text']})
    return items


def vocab_test_items(pool, n, rnd):
    uniq, seen = [], set()
    for v in pool:
        k = v['en'].lower()
        if k not in seen:
            seen.add(k)
            uniq.append(v)
    out = []
    for c in sample_every(uniq, n):
        others = [x for x in uniq if x['zh'] != c['zh']]
        opts = [c['zh']] + [x['zh'] for x in rnd.sample(others, 2)]
        rnd.shuffle(opts)
        out.append({'type': 'mc', 'q': '「%s」是什麼意思？' % c['en'], 'opts': opts, 'a': opts.index(c['zh']), 'gp': '單字', 'speak': c['en']})
    return out


def build():
    rnd = random.Random(20260830)
    W = json.load(open(os.path.join(SRC, 'p0_weeks.json'), encoding='utf-8'))
    T = json.load(open(os.path.join(SRC, 'p0_tests.json'), encoding='utf-8'))
    jp = os.path.join(SRC, 'p0_vocab_ja.json')
    ja = json.load(open(jp, encoding='utf-8')) if os.path.exists(jp) else {}

    # 依日曆排出 56 天：每週 1–6 天課程、第 7 天總複習；第 8 週 1–5 天課程、第 6 天全程複習、第 7 天休息
    plan = []
    for w in W:
        for d in w['days']:
            plan.append((w, d['day'], 'authored', d))
        if w['id'] <= 7:
            plan.append((w, 7, 'review', review_raw(w['days'])))
        else:
            allw = [x for ww in W for x in ww['days']]
            cap = review_raw(allw)
            cap['vocab'] = sample_every(flatten(allw, 'vocab'), 25)
            plan.append((w, 6, 'capstone', cap))
            plan.append((w, 7, 'rest', None))
    assert len(plan) == 56, len(plan)

    first_seen = {}
    for i, (w, dn, kind, d) in enumerate(plan):
        if kind == 'authored':
            for v in d['vocab']:
                first_seen.setdefault(v['en'].lower().strip(), i)

    days = {}
    for i, (w, dn, kind, d) in enumerate(plan):
        n = i + 1
        info = {'week': w['id'], 'dayOfWeek': dn, 'weekTitle': w['title'],
                'review': kind in ('review', 'capstone'), 'rest': kind == 'rest'}
        if kind == 'rest':
            info['topic'] = '完賽休息'
            info['blocks'] = {}
        else:
            info['topic'] = d.get('label') if kind == 'authored' else ('本週總複習' if kind == 'review' else '全程總複習與自我檢測')
            prior = []
            for j in range(max(0, i - 10), i):
                pd = plan[j][3]
                if pd and plan[j][2] == 'authored':
                    prior += pd['vocab']
            rv = prior if kind == 'authored' else [v for ww in ([w] if kind == 'review' else W) for v in flatten(ww['days'], 'vocab')]
            info['blocks'] = conv_day(d, ja, first_seen, i, rv, rnd)
            if kind != 'authored':
                for v in info['blocks']['vocab_new']:
                    v['review'] = True
        days[str(n)] = info

    weeks = [{'id': w['id'], 'title': w['title'], 'subtitle': w.get('subtitle', ''), 'focus': w.get('focus', ''),
              'grammar': w.get('grammarWeek')} for w in W]

    week_vocab = {w['id']: flatten(w['days'], 'vocab') for w in W}
    weekly = {}
    for tw in T['weeks']:
        items = test_items_from(tw)
        reading = [x for x in items if x['gp'] == '閱讀']
        weekly[str(tw['week'])] = {'title': tw['title'],
                                   'items': [x for x in items if x['gp'] != '閱讀'] + vocab_test_items(week_vocab[tw['week']], 10, rnd) + reading}
    all_vocab = [v for w in W for v in flatten(w['days'], 'vocab')]
    fin = test_items_from(T['final'])
    final_items = [x for x in fin if x['gp'] != '閱讀'] + vocab_test_items(all_vocab, 10, rnd) + [x for x in fin if x['gp'] == '閱讀']
    diag = test_items_from(T['diagnostic'])
    diag_items = [x for x in diag if x['gp'] != '閱讀'] + vocab_test_items(week_vocab[1] + week_vocab[2], 10, rnd) + [x for x in diag if x['gp'] == '閱讀']

    pool = []
    seen = set()
    for i, (w, dn, kind, d) in enumerate(plan):
        if kind == 'authored':
            for v in d['vocab']:
                k = v['en'].lower()
                if k not in seen:
                    seen.add(k)
                    pool.append({'w': v['en'], 'zh': v['zh'], 'learnedDay': i + 1})

    return {
        'meta': {'day1': DAY1, 'weeks': weeks},
        'days': days,
        'tests': {
            'diagnostic': {'title': T['diagnostic']['title'], 'items': diag_items},
            'weekly': weekly,
            'final': {'title': T['final']['title'], 'items': final_items},
            'retention': {'pool': pool},
            'cefr': {'items': CANDO},
        },
    }


if __name__ == '__main__':
    D = build()
    from collections import Counter
    c = Counter()
    for d in D['days'].values():
        for k, v in d['blocks'].items():
            c[k] += len(v) if k != 'reading' else sum(len(r['qs']) for r in v)
    print(dict(c), sum(c.values()))
    print({k: len(v['items']) for k, v in D['tests']['weekly'].items()}, len(D['tests']['final']['items']), len(D['tests']['diagnostic']['items']))
