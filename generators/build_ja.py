# -*- coding: utf-8 -*-
"""JLPT 日文課程（N5–N1 58 課＋五級模擬測驗）→ EJLP 日文資料。

需要 fugashi + unidic-lite（見 requirements.txt）。為閱讀、例句、跟讀、作文範例、
聽解稿加上「詞塊＋讀音」，讓前端顯示振假名並可點字查詢。
選擇題與填空不加讀音（避免讀音題洩題）。
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'source')

try:
    import fugashi
    TAGGER = fugashi.Tagger()
except Exception as e:  # pragma: no cover
    raise SystemExit('需要 fugashi 與 unidic-lite：pip install fugashi unidic-lite（%s）' % e)

OVERRIDE = {'私': 'わたし', '私達': 'わたしたち', '私たち': 'わたしたち', '何': 'なに', '一人': 'ひとり', '二人': 'ふたり',
            '一日': 'ついたち', '林': 'りん', '陳': 'ちん', '王': 'おう', '李': 'り', '林さん': 'りんさん', '陳さん': 'ちんさん', '王さん': 'おうさん', '李さん': 'りさん', '今日': 'きょう', '明日': 'あした', '昨日': 'きのう', '大人': 'おとな', '上手': 'じょうず', '下手': 'へた'}
KANJI = re.compile(r'[㐀-鿿々〆ヶ]')
ATTACH_POS = {'助動詞', '接尾辞'}
ATTACH_CONJ = {'て', 'で', 'ば', 'たり', 'だり', 'ながら', 'ちゃ', 'じゃ'}


def hira(s):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s or '')


def tokenize(text, known=None):
    """回傳 [[表層, 讀音(若有漢字), 原形]] 詞塊列表；保留換行為 ['\\n','','']。"""
    known = known or {}
    out = []
    for li, line in enumerate(text.split('\n')):
        if li:
            out.append(['\n', '', ''])
        prev_kind = None
        for w in TAGGER(line):
            surf = w.surface
            f = w.feature
            pos1, pos2 = f.pos1, f.pos2
            kana = hira(getattr(f, 'kana', '') or '')
            base = getattr(f, 'orthBase', None) or surf
            if base and '-' in base:
                base = base.split('-')[0]
            attach = out and out[-1][0] != '\n' and prev_kind in ('動詞', '形容詞', '助動詞', 'attach') and (
                pos1 in ATTACH_POS or (pos1 == '助詞' and pos2 == '接続助詞' and surf in ATTACH_CONJ)
                or (pos2 == '非自立可能' and pos1 in ('動詞', '形容詞') and out[-1][0][-1:] in 'てでくに'))
            if pos1 == '接尾辞' and out and out[-1][0] != '\n' and prev_kind in ('名詞', 'attach'):
                attach = True
            if attach:
                out[-1][0] += surf
                out[-1][1] += kana if kana else surf
                prev_kind = '名詞' if (pos1 == '接尾辞' and prev_kind == '名詞') else 'attach'
                continue
            out.append([surf, kana if kana else surf, base])
            prev_kind = pos1 if pos1 in ('動詞', '形容詞', '助動詞', '名詞') else pos1
    # 讀音修正與精簡：沒有漢字就不需要讀音
    for t in out:
        s = t[0]
        if s in known:
            t[1] = known[s]
        elif s in OVERRIDE:
            t[1] = OVERRIDE[s]
        if not KANJI.search(s):
            t[1] = ''
        if t[2] == s:
            t[2] = ''
    return out


def build():
    D = json.load(open(os.path.join(SRC, 'jlpt_data.json'), encoding='utf-8'))
    known = {}
    for lv in D.values():
        for u in lv['units']:
            for v in u['vocab']:
                if KANJI.search(v['w']) and v.get('r'):
                    known.setdefault(v['w'], v['r'])
    gloss = {}
    for lvname, lv in D.items():
        for u in lv['units']:
            for v in u['vocab']:
                gloss.setdefault(v['w'], {'r': v['r'] if KANJI.search(v['w']) else '', 'pos': v.get('pos', ''), 'zh': v['zh'],
                                          'en': '', 'note': '%s 第%d課' % (lvname, u['unit'])})
            for v in u['vocab']:
                if v.get('ex'):
                    v['exT'] = tokenize(v['ex'], known)
            for g in u['grammar']:
                for e in g['ex']:
                    e['jt'] = tokenize(e['ja'], known)
            rd = u['reading']
            rd['textT'] = tokenize(rd['text'], known)
            for l in u['listening']:
                l['scriptT'] = tokenize(l['script'], known)
            for s in u['shadow']:
                s['jt'] = tokenize(s['ja'], known)
            if u.get('write', {}).get('sample'):
                u['write']['sampleT'] = tokenize(u['write']['sample'], known)
        for it in lv['mock']['items']:
            if it.get('passage'):
                it['passageT'] = tokenize(it['passage'], known)
            if it.get('script'):
                it['scriptT'] = tokenize(it['script'], known)
    return D, gloss, known


if __name__ == '__main__':
    D, g, k = build()
    u = D['N5']['units'][0]
    print(u['grammar'][0]['ex'][1]['jt'])
    print(u['reading']['textT'][:30])
    print(D['N3']['units'][0]['shadow'][0]['jt'])
    print(len(g))
