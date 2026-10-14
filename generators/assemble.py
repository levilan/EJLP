# -*- coding: utf-8 -*-
import sys, json, re
import os
HERE=os.path.dirname(os.path.abspath(__file__)); DATA_DIR=os.path.join(HERE,'..','data')
sys.path.insert(0,HERE)
import eng_to_ipa as IPA
from stories import EN, JA
from gloss import EN_G, JA_G
from ja_vocab import JA_V
import ja_practice as J
src=open(os.path.join(HERE,'gen_days1-14.py'),encoding='utf-8').read().split('# ---------------------------------------------------------------- 主詞')[0]
ns={}; exec(src,ns); V=ns['V']
D=json.load(open(os.path.join(DATA_DIR,'phase0-days1-14.json'),encoding='utf-8'))
def jt(s): t,r=(s.split('|')+[''])[:2]; return [t,r]
# 英文單字卡加上日文
for d in D['days'].values():
    for it in d['blocks']['vocab_new']:
        if it['w'] in JA_V: it['ja']=jt(JA_V[it['w']])
# 日文平行練習
D['ja']={'meta':dict(level='N5'), 'days':{str(d):J.build(d,V,JA_V) for d in range(1,15)}}
# 中英混排空白
def fixzh(o):
    if isinstance(o,dict): return {k:fixzh(v) for k,v in o.items()}
    if isinstance(o,list): return [fixzh(v) for v in o]
    if isinstance(o,str) and re.search(r'[\u4e00-\u9fff]',o) and not re.search(r'[\u3040-\u30ff]',o):
        o=re.sub(r'([\u4e00-\u9fff])([A-Za-z])', r'\1 \2', o); o=re.sub(r'([A-Za-z])([\u4e00-\u9fff])', r'\1 \2', o)
    return o
D['ja']=fixzh(D['ja'])
# 詞彙表
ge={}
for line in EN_G.strip().split('\n'):
    w,pos,zh,jt_,jr,note=line.split('|')
    ipa=IPA.convert(w.replace("'s",'')) if not w.endswith("'s") else IPA.convert(w[:-2])+'z'
    if '*' in ipa: ipa=''
    ge[w]=dict(pos=pos,zh=zh,ja=[jt_,jr],note=note,ipa=ipa)
gj={}
for en,j in JA_V.items():
    t,r=jt(j); zh=next((z for d in V for w,p,z,e in V[d] if w==en),'')
    gj.setdefault(t,dict(r=r,pos='',zh=zh,en=en,note=''))
for line in JA_G.strip().split('\n'):
    t,r,pos,zh,en,note=line.split('|'); gj[t]=dict(r=r,pos=pos,zh=zh,en=en,note=note)
for t,r,pos,zh,en,note in [('さん','','接尾詞','先生／小姐（稱呼別人）','Mr./Ms.','不能用在自己身上'),('ではありません','','助動詞','不是','is not','名詞、な形容詞的否定；口語：じゃないです'),
    ('ありません','','動詞','沒有（物品）','there is not','ある 的否定'),('いません','','動詞','沒有；不在（人、動物）','is not (there)','いる 的否定'),('あります','','動詞','有（物品）','there is; have','物品用 あります'),
    ('います','','動詞','有；在（人、動物）','there is; is (there)','人、動物用 います'),('はじめまして','','感嘆詞','初次見面','nice to meet you',''),('そうです','','','是的；沒錯','that\'s right',''),('ちがいます','','動詞','不是；不對','that\'s wrong',''),
    ('これ','','代名詞','這個','this','近的東西'),('あれ','','代名詞','那個（遠）','that (over there)',''),('この','','連體詞','這個…','this ~','後面接名詞'),('来ました','きました','動詞','來了','came','来る 的過去式'),
    ('今日','きょう','名詞','今天','today',''),('人','ひと','名詞','人','person',''),('お名前','おなまえ','名詞','（您的）名字','(your) name',''),('仕事','しごと','名詞','工作','job',''),('トイレ','','名詞','廁所','toilet',''),
    ('家族','かぞく','名詞','家人','family',''),('写真','しゃしん','名詞','照片','photo',''),('四人','よにん','名詞','四個人','four people','特殊讀音')]:
    gj.setdefault(t,dict(r=r,pos=pos,zh=zh,en=en,note=note))
# 書庫
def enbook(b):
    return dict(id=b['id'],lang='en',title=b['title'],sub=b['zh'],level=b['level'],author=b['author'],color=b['color'],
        chapters=[dict(title=c['title'],zh=c['zh'],s=[dict(t=t,zh=z,ja=j) for t,z,j in c['s']],qs=[dict(q=q,opts=o,a=a) for q,o,a in c['qs']]) for c in b['chapters']])
def jabook(b):
    return dict(id=b['id'],lang='ja',title=b['title'],reading=b['reading'],sub=b['zh'],en=b['en'],level=b['level'],author=b['author'],color=b['color'],
        chapters=[dict(title=c['title'],reading=c['reading'],zh=c['zh'],s=[dict(toks=J.T(t),zh=z,en=e) for t,z,e in c['s']],
                       qs=[dict(q=J.T(q),opts=[J.T(o) for o in os],a=a,zh=qz) for q,os,a,qz in c['qs']]) for c in b['chapters']])
D['library']=dict(en=[enbook(b) for b in EN], ja=[jabook(b) for b in JA])
D['gloss']=dict(en=ge, ja=gj)
D['meta']['version']='days1-14 v2 (英日)'
json.dump(D, open(os.path.join(DATA_DIR,'phase0-days1-14-enja.json'),'w',encoding='utf-8'), ensure_ascii=False)
# 檢查故事中所有 token 都有詞彙
miss=set()
for b in D['library']['ja']:
    for c in b['chapters']:
        for s in c['s']:
            for t,r in s['toks']:
                if t not in '、。「」' and t not in gj: miss.add(t)
for b in D['library']['en']:
    for c in b['chapters']:
        for s in c['s']:
            for w in re.findall(r"[A-Za-z]+(?:'[a-z]+)?",s['t']):
                if w.lower() not in ge: miss.add(w)
print('missing gloss:',miss)
print({k:len(v) for k,v in D['gloss'].items()}, ge['influence'] if 'influence' in ge else ge['strange'])
print(os.path.getsize(os.path.join(DATA_DIR,'phase0-days1-14-enja.json'))//1024,'KB')
