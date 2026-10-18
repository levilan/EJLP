# -*- coding: utf-8 -*-
"""英文題目的「說明」對照鍵。build_all 依同一套鍵把 source/explain_en.json 合併進題目。"""
import hashlib, re

def _h(*parts):
    return hashlib.sha1('␟'.join(parts).encode('utf-8')).hexdigest()[:10]

def norm(s):
    return re.sub(r'\s+', ' ', (s or '').strip())

def key_mc(q, ans):
    return 'm' + _h(norm(q), norm(ans))

def key_fill(q, a0):
    return 'f' + _h(norm(q), norm(a0))

def key_tr(zh):
    return 't' + _h(norm(zh))

def key_rd(passage, q, ans):
    return 'r' + _h(norm(passage)[:120], norm(q), norm(ans))

VOCAB_Q = re.compile(r'^「(.+)」是什麼意思？$')
