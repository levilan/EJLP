# -*- coding: utf-8 -*-
"""產生網站用的全部資料檔。

    pip install -r requirements.txt
    python generators/build_all.py

輸出：
  data/en.json          英文 Day 1–61（Phase 0 56 天＋現在進行式補充週）與檢測題庫
  data/ja/index.json    JLPT 各級課程目錄
  data/ja/N5.json…N1.json 各級課程（單字、文法、選擇、填空、讀解、聽解、跟讀、作文、模擬測驗）
  data/library.json     分級讀物（英文 A1/A2、日文 N5/N4）
  data/gloss.json       點字查詢用詞彙表（英文、日文）
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data')
sys.path.insert(0, HERE)

import eng_to_ipa as IPA
import build_en, gen_cont, build_ja, explain
from stories import EN as EN_OLD, JA as JA_OLD
from books_en_new import EN_NEW
from books_ja_new import JA_NEW
from gloss import EN_G, JA_G
from gloss_en_new import EN_G_NEW
from gloss_ja_new import JA_G_NEW

CJK = re.compile(r'[一-鿿]')


def zh_space(o):
    """中英混排加空格（只處理不含日文假名的中文字串）。"""
    if isinstance(o, dict):
        return {k: zh_space(v) for k, v in o.items()}
    if isinstance(o, list):
        return [zh_space(v) for v in o]
    if isinstance(o, str) and CJK.search(o) and not re.search(r'[぀-ヿ]', o):
        o = re.sub(r'([一-鿿])([A-Za-z])', r'\1 \2', o)
        o = re.sub(r'([A-Za-z])([一-鿿])', r'\1 \2', o)
    return o


def dump(name, obj):
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    return os.path.getsize(p)


def en_data():
    D = build_en.build()
    days, test, week = gen_cont.build()
    for k, d in days.items():
        d['blocks'] = zh_space(d['blocks'])
    D['days'].update(days)
    D['meta']['weeks'].append(week)
    D['tests']['weekly']['9'] = test
    D['meta']['days'] = len(D['days'])
    st = explain.merge(D, zh_space)
    print('錯題說明', st)
    return D


def T(s):
    out = []
    for tok in s.split(' '):
        if tok:
            p = tok.split('|')
            out.append([p[0], p[1] if len(p) > 1 else ''])
    return out


def library():
    def enbook(b):
        return dict(id=b['id'], lang='en', title=b['title'], sub=b['zh'], ja=b.get('ja', ''), level=b['level'], author=b['author'],
                    color=b['color'], chapters=[dict(title=c['title'], zh=c['zh'], s=[dict(t=t, zh=z, ja=j) for t, z, j in c['s']],
                                                     qs=[dict(q=q, opts=o, a=a) for q, o, a in c['qs']]) for c in b['chapters']])

    def jabook_old(b):
        return dict(id=b['id'], lang='ja', title=b['title'], reading=b['reading'], sub=b['zh'], en=b['en'], level=b['level'],
                    author=b['author'], color=b['color'],
                    chapters=[dict(title=c['title'], reading=c['reading'], zh=c['zh'], s=[dict(toks=T(t), zh=z, en=e) for t, z, e in c['s']],
                                   qs=[dict(q=T(q), opts=[T(o) for o in os_], a=a, zh=qz) for q, os_, a, qz in c['qs']])
                              for c in b['chapters']])

    def jabook_new(b):
        tk = build_ja.tokenize
        return dict(id=b['id'], lang='ja', title=b['title'], reading=b['reading'], sub=b['zh'], en=b['en'], level=b['level'],
                    author=b['author'], color=b['color'],
                    chapters=[dict(title=c['title'], reading=c['reading'], zh=c['zh'], s=[dict(toks=tk(t), zh=z, en=e) for t, z, e in c['s']],
                                   qs=[dict(q=tk(q), opts=[tk(o) for o in os_], a=a, zh=qz) for q, os_, a, qz in c['qs']])
                              for c in b['chapters']])
    lv = {'A1': 0, 'A2': 1, 'N5': 0, 'N4': 1}
    en = sorted([enbook(b) for b in EN_OLD + EN_NEW], key=lambda b: lv[b['level']])
    ja = sorted([jabook_old(b) for b in JA_OLD] + [jabook_new(b) for b in JA_NEW], key=lambda b: lv[b['level']])
    return {'en': en, 'ja': ja}


def gloss(ja_from_jlpt):
    en = {}
    for line in (EN_G.strip() + '\n' + EN_G_NEW.strip()).split('\n'):
        w, pos, zh, jt, jr, note = line.split('|')
        base = w[:-2] if w.endswith("'s") else w
        ipa = IPA.convert(base)
        if w.endswith("'s"):
            ipa += 'z'
        if '*' in ipa:
            ipa = ''
        en[w] = {'pos': pos, 'zh': zh, 'ja': [jt, jr], 'note': note, 'ipa': ipa}
    ja = dict(ja_from_jlpt)
    for line in (JA_G.strip() + '\n' + JA_G_NEW.strip()).split('\n'):
        t, r, pos, zh, e, note = line.split('|')
        ja[t] = {'r': r, 'pos': pos, 'zh': zh, 'en': e, 'note': note}
    for t, r, pos, zh, e, note in [
        ('さん', '', '接尾詞', '先生／小姐（稱呼別人）', 'Mr./Ms.', '不能用在自己身上'),
        ('ではありません', '', '助動詞', '不是', 'is not', '名詞、な形容詞的否定；口語：じゃないです'),
        ('ありません', '', '動詞', '沒有（物品）', 'there is not', 'ある 的否定'),
        ('いません', '', '動詞', '沒有；不在（人、動物）', 'is not (there)', 'いる 的否定'),
        ('あります', '', '動詞', '有（物品）', 'there is; have', '物品用 あります'),
        ('います', '', '動詞', '有；在（人、動物）', 'there is; is (there)', '人、動物用 います'),
        ('ある', '', '動詞', '有；在（物品）', 'there is; have', ''), ('いる', '', '動詞', '有；在（人、動物）', 'there is', ''),
        ('です', '', '助動詞', '是', 'is; am; are', '禮貌的斷定'), ('はじめまして', '', '感嘆詞', '初次見面', 'nice to meet you', ''),
        ('そうです', '', '', '是的；沒錯', "that's right", ''), ('ちがいます', '', '動詞', '不是；不對', "that's wrong", ''),
    ]:
        ja.setdefault(t, {'r': r, 'pos': pos, 'zh': zh, 'en': e, 'note': note})
    return {'en': en, 'ja': ja}


def main():
    sizes = {}
    E = en_data()
    sizes['en.json'] = dump('en.json', E)
    J, jg, _ = build_ja.build()
    index = {}
    for lv, d in J.items():
        sizes['ja/%s.json' % lv] = dump('ja/%s.json' % lv, d)
        index[lv] = [{'unit': u['unit'], 'title': u['title'], 'titleJa': u['titleJa'], 'theme': u['theme']} for u in d['units']]
    sizes['ja/index.json'] = dump('ja/index.json', {'levels': index, 'start': '2026-10-19'})
    sizes['library.json'] = dump('library.json', library())
    sizes['gloss.json'] = dump('gloss.json', gloss(jg))
    for k, v in sizes.items():
        print('%-18s %7.0f KB' % (k, v / 1024))
    print('英文天數', E['meta']['days'])


if __name__ == '__main__':
    main()
