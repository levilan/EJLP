# -*- coding: utf-8 -*-
"""把錯題說明合併進英文題目。

source/explain_en.json：{鍵: {"x": 為什麼對, "w": {錯誤選項: 為什麼錯}, "g": 文法分類}}
鍵的算法見 explain_keys.py。單字題的說明直接由詞彙表產生。

合併後題目多出：
  why  正確答案的說明
  wn   與 opts 對齊的陣列，每個錯誤選項為什麼不行（正確答案位置為空字串）
  g    文法分類（錯題分析用）
"""
import json, os, re
from explain_keys import key_mc, key_fill, key_tr, key_rd, VOCAB_Q, norm

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'source', 'explain_en.json')
FIX = os.path.join(HERE, '..', 'source', 'fixes_en.json')

WEEK_TAG = {1: 'be 動詞', 2: '代名詞／所有格', 3: '現在簡單式', 4: 'there is/are', 5: '可數／不可數', 6: '過去式', 7: 'be going to', 9: '現在進行式'}


def load():
    if not os.path.exists(SRC):
        return {}
    return json.load(open(SRC, encoding='utf-8'))


def load_fix():
    if not os.path.exists(FIX):
        return {}
    return json.load(open(FIX, encoding='utf-8'))


def apply_fix(kind, it, ops, e):
    """依 QA 修正指令改題目（kind: mc / fill / tr / rd），回傳套用後的說明 e。"""
    e = dict(e or {})
    if e.get('w'):
        e['w'] = dict(e['w'])
    for op in ops:
        n = op['op']
        if n == 'set_q':
            it['q'] = op['q']
        elif n in ('set_zh', 'set_prompt'):
            it['zh'] = op['zh']
        elif n == 'add_answers':
            for a in op['answers']:
                if a not in it['a']:
                    it['a'].append(a)
        elif n == 'set_answers':
            it['a'] = list(op['answers'])
        elif n == 'replace_option':
            if op['old'] in it['opts'] and op['new'] not in it['opts']:
                it['opts'][it['opts'].index(op['old'])] = op['new']
                e.setdefault('w', {})[op['new']] = op['w']
        elif n == 'set_answer':
            if op['answer'] in it['opts']:
                it['a'] = it['opts'].index(op['answer'])
        elif n == 'set_item':
            it['q'] = op['q']
            if kind == 'mc':
                pos = min(it['a'], len(op['wrong']))
                it['opts'] = list(op['wrong'][:len(it['opts']) - 1])
                it['opts'].insert(pos, op['answer'])
                it['a'] = pos
            else:
                it['a'] = list(op['answers'])
        elif n == 'set_x':
            e['x'] = op['x']
        elif n == 'set_w':
            e.setdefault('w', {}).update(op['w'])
    return e


def vocab_maps(days):
    w2 = {}
    z2w = {}
    for d in days.values():
        for v in (d.get('blocks') or {}).get('vocab_new', []) if isinstance(d.get('blocks'), dict) else []:
            w2.setdefault(v['w'], {'zh': v['zh'], 'ex': v.get('ex', '')})
            z2w.setdefault(v['zh'], v['w'])
    return w2, z2w


def merge(E, zh_space):
    X = load()
    F = load_fix()
    w2, z2w = vocab_maps(E['days'])
    stats = {'hit': 0, 'miss': 0, 'fixed': 0}

    def look(kind, k, it):
        e = X.get(k)
        f = F.get(k)
        if f:
            stats['fixed'] += 1
            e = apply_fix(kind, it, f['ops'], e)
        return e

    def put(it, e, opts=None, ans=None):
        if not e:
            stats['miss'] += 1
            return
        stats['hit'] += 1
        it['why'] = zh_space(e['x'])
        if e.get('g'):
            it['g'] = e['g']
        if opts is not None and e.get('w'):
            it['wn'] = [('' if o == ans else zh_space(e['w'].get(o, ''))) for o in opts]

    def vocab_mc(it, word, ans_zh, opts):
        v = w2.get(word, {})
        why = '%s＝%s' % (word, ans_zh) + ('。例句：%s' % v['ex'] if v.get('ex') else '')
        it['why'] = zh_space(why)
        it['wn'] = [('' if o == ans_zh else zh_space('「%s」是 %s' % (o, z2w[o]) if o in z2w else '')) for o in opts]
        it['g'] = '單字'

    def mc(it):
        m = VOCAB_Q.match(it['q'])
        if m:
            return vocab_mc(it, m.group(1), it['opts'][it['a']], it['opts'])
        e = look('mc', key_mc(it['q'], it['opts'][it['a']]), it)
        put(it, e, it['opts'], it['opts'][it['a']])

    for d in E['days'].values():
        b = d.get('blocks')
        if not isinstance(b, dict):
            continue
        wk = d.get('week')
        for it in b.get('mc', []):
            mc(it)
        for it in b.get('fill', []):
            put(it, look('fill', key_fill(it['q'], it['a'][0]), it))
        tr_by_ans = {}
        for it in b.get('translate', []):
            e = look('tr', key_tr(it['zh']), it)
            put(it, e)
            if e:
                for a in it['a']:
                    tr_by_ans[norm(a).lower()] = e
        for it in b.get('reorder', []):
            e = tr_by_ans.get(norm(it['a']).lower())
            if e:
                it['why'] = zh_space(e['x'])
                it['g'] = e.get('g', '語序')
            else:
                it['g'] = WEEK_TAG.get(wk, '語序')
        for rd in b.get('reading', []):
            for qq in rd['qs']:
                e = look('rd', key_rd(rd['text'], qq['q'], qq['opts'][qq['a']]), qq)
                put(qq, e, qq['opts'], qq['opts'][qq['a']])
                qq['g'] = '閱讀'
        for it in b.get('error', []):
            it.setdefault('g', WEEK_TAG.get(wk, '綜合'))
        for it in b.get('vocab_review', []):
            if it.get('dir') == 'en2zh':
                v = w2.get(it['q'], {})
                it['why'] = zh_space('%s＝%s' % (it['q'], it['a']) + ('。例句：%s' % v['ex'] if v.get('ex') else ''))
                it['wn'] = [('' if o == it['a'] else zh_space('「%s」是 %s' % (o, z2w[o]) if o in z2w else '')) for o in it['opts']]
            else:
                v = w2.get(it['a'], {})
                it['why'] = zh_space('%s＝%s' % (it['q'], it['a']) + ('。例句：%s' % v['ex'] if v.get('ex') else ''))
                it['wn'] = [('' if o == it['a'] else zh_space('%s 是「%s」' % (o, w2[o]['zh']) if o in w2 else '')) for o in it['opts']]
            it['g'] = '單字'
    T = E['tests']
    for items in [T['diagnostic']['items'], T['final']['items']] + [t['items'] for t in T['weekly'].values()]:
        for it in items:
            if it.get('passage'):
                e = look('rd', key_rd(it['passage'], it['q'], it['opts'][it['a']]), it)
                put(it, e, it['opts'], it['opts'][it['a']])
                it['g'] = '閱讀'
            else:
                mc(it)
    return stats
