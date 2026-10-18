# -*- coding: utf-8 -*-
"""現在進行式補充週（Day 57–61），輸出 EJLP 英文格式。

Day 57 肯定句與 -ing 拼字　Day 58 否定句　Day 59 問句與簡答／What are you doing?
Day 60 現在簡單式 vs 現在進行式　Day 61 總複習
"""
import random, re

rnd = random.Random(20261025)

# 動詞：原形, -ing, 中文（進行中）, 受詞/補語選項[(en, zh)], 日文, 讀音
VERBS = [  # (原形, -ing, 無受詞時的中文, [(受詞, 完整動作中文)], 日文, 讀音)
    ('read', 'reading', '讀書', [('a book', '讀書'), ('the news', '看新聞'), ('a letter', '讀一封信')], '読む', 'よむ'),
    ('write', 'writing', '寫字', [('an email', '寫電子郵件'), ('a report', '寫報告'), ('a story', '寫故事'), ('a message', '寫訊息')], '書く', 'かく'),
    ('eat', 'eating', '吃東西', [('lunch', '吃午餐'), ('breakfast', '吃早餐'), ('an apple', '吃蘋果')], '食べる', 'たべる'),
    ('drink', 'drinking', '喝東西', [('coffee', '喝咖啡'), ('tea', '喝茶'), ('water', '喝水')], '飲む', 'のむ'),
    ('cook', 'cooking', '煮飯', [('dinner', '煮晚餐'), ('soup', '煮湯'), ('lunch', '煮午餐')], '料理する', 'りょうりする'),
    ('watch', 'watching', '看', [('TV', '看電視'), ('a movie', '看電影'), ('the game', '看比賽')], '見る', 'みる'),
    ('play', 'playing', '玩', [('the guitar', '彈吉他'), ('basketball', '打籃球'), ('a game', '玩遊戲')], '遊ぶ', 'あそぶ'),
    ('listen', 'listening', '聽', [('to music', '聽音樂'), ('to the radio', '聽廣播'), ('to the teacher', '聽老師說話')], '聞く', 'きく'),
    ('study', 'studying', '讀書', [('English', '讀英文'), ('math', '讀數學'), ('for the test', '準備考試')], '勉強する', 'べんきょうする'),
    ('work', 'working', '工作', [('at home', '在家工作'), ('in the office', '在辦公室工作'), ('at the café', '在咖啡店工作')], '働く', 'はたらく'),
    ('make', 'making', '做東西', [('a cake', '做蛋糕'), ('coffee', '泡咖啡'), ('a video', '做影片')], '作る', 'つくる'),
    ('run', 'running', '跑步', [('in the park', '在公園跑步'), ('to the station', '跑去車站')], '走る', 'はしる'),
    ('swim', 'swimming', '游泳', [('in the pool', '在游泳池游泳'), ('in the sea', '在海裡游泳')], '泳ぐ', 'およぐ'),
    ('sit', 'sitting', '坐著', [('on the sofa', '坐在沙發上'), ('by the window', '坐在窗邊')], '座る', 'すわる'),
    ('shop', 'shopping', '買東西', [('at the mall', '在購物中心買東西'), ('online', '在網路上買東西')], '買い物する', 'かいものする'),
    ('wait', 'waiting', '等', [('for the bus', '等公車'), ('for my friend', '等我的朋友')], '待つ', 'まつ'),
    ('talk', 'talking', '說話', [('on the phone', '講電話'), ('to the teacher', '跟老師說話')], '話す', 'はなす'),
    ('sleep', 'sleeping', '睡覺', [('on the sofa', '在沙發上睡覺'), ('in the bedroom', '在臥室睡覺')], '寝る', 'ねる'),
    ('wash', 'washing', '洗', [('the dishes', '洗碗'), ('the car', '洗車')], '洗う', 'あらう'),
    ('clean', 'cleaning', '打掃', [('the kitchen', '打掃廚房'), ('my room', '打掃我的房間')], '掃除する', 'そうじする'),
    ('drive', 'driving', '開車', [('to work', '開車去上班'), ('home', '開車回家')], '運転する', 'うんてんする'),
    ('take', 'taking', '拿', [('photos', '拍照'), ('a shower', '洗澡')], '撮る', 'とる'),
    ('wear', 'wearing', '穿', [('jeans', '穿著牛仔褲'), ('glasses', '戴著眼鏡')], '着る', 'きる'),
    ('learn', 'learning', '學習', [('Japanese', '學日文'), ('to drive', '學開車')], '習う', 'ならう'),
    ('use', 'using', '用', [('the computer', '用電腦'), ('my phone', '用我的手機')], '使う', 'つかう'),
    ('get', 'getting', '準備', [('dressed', '穿衣服'), ('ready', '準備')], '準備する', 'じゅんびする'),
    ('rain', 'raining', '下雨', [], '雨が降る', 'あめがふる'),
]
SUBJ = [
    ('I', '我', 'am', 'I'), ('You', '你', 'are', 'you'), ('He', '他', 'is', 'he'), ('She', '她', 'is', 'she'),
    ('We', '我們', 'are', 'we'), ('They', '他們', 'are', 'they'), ('Tom', 'Tom', 'is', 'he'), ('Amy', 'Amy', 'is', 'she'),
    ('My mother', '我媽媽', 'is', 'she'), ('My father', '我爸爸', 'is', 'he'), ('My brother', '我哥哥', 'is', 'he'),
    ('The children', '孩子們', 'are', 'they'), ('My friends', '我的朋友們', 'are', 'they'), ('Ken and Lisa', 'Ken 和 Lisa', 'are', 'they'),
]
NOW = [('now', '現在'), ('right now', '此刻'), ('at the moment', '目前'), ('today', '今天')]
HABIT = [('every day', '每天'), ('every morning', '每天早上'), ('on Sundays', '每個星期日'), ('usually', '通常'), ('often', '常常')]
NEG = {'am': "am not", 'is': "isn't", 'are': "aren't"}
SPELL = [('make', 'making', '去 e 加 -ing', 'a cake'), ('write', 'writing', '去 e 加 -ing', 'an email'), ('drive', 'driving', '去 e 加 -ing', 'to work'),
         ('use', 'using', '去 e 加 -ing', 'the computer'), ('take', 'taking', '去 e 加 -ing', 'a shower'), ('run', 'running', '短母音＋子音：重複字尾再加 -ing', 'in the park'),
         ('swim', 'swimming', '短母音＋子音：重複字尾再加 -ing', 'in the pool'), ('sit', 'sitting', '短母音＋子音：重複字尾再加 -ing', 'on the sofa'),
         ('shop', 'shopping', '短母音＋子音：重複字尾再加 -ing', 'at the mall'), ('get', 'getting', '短母音＋子音：重複字尾再加 -ing', 'dressed'),
         ('lie', 'lying', 'ie 改 y 加 -ing', 'on the bed'), ('lie', 'lying', 'ie 改 y 加 -ing', 'on the sofa'), ('play', 'playing', '直接加 -ing', 'basketball'),
         ('study', 'studying', '直接加 -ing（y 不變）', 'English'), ('read', 'reading', '直接加 -ing', 'a book')]
THIRD = {'read': 'reads', 'write': 'writes', 'eat': 'eats', 'drink': 'drinks', 'cook': 'cooks', 'watch': 'watches', 'play': 'plays',
         'listen': 'listens', 'study': 'studies', 'work': 'works', 'make': 'makes', 'run': 'runs', 'swim': 'swims', 'sit': 'sits',
         'shop': 'shops', 'wait': 'waits', 'talk': 'talks', 'sleep': 'sleeps', 'wash': 'washes', 'clean': 'cleans', 'drive': 'drives',
         'take': 'takes', 'wear': 'wears', 'learn': 'learns', 'use': 'uses', 'get': 'gets', 'rain': 'rains'}


def pick(l, n):
    return rnd.sample(l, min(n, len(l)))


def low(s):
    return s if s in ('I',) or s[0].isupper() and s.split()[0] not in ('He', 'She', 'We', 'They', 'You', 'My', 'The') else s[0].lower() + s[1:]


def mid(s):
    first = s.split()[0]
    return s if first in ('I', 'Tom', 'Amy', 'Ken') else s[0].lower() + s[1:]


def phrase(v):
    base, ing, zh, objs, *_ = v
    if not objs:
        return ing, zh
    o = rnd.choice(objs)
    return '%s %s' % (ing, o[0]), o[1]


def prog(zh):
    """進行中：在讀書／在公園跑步／正坐在沙發上"""
    if zh.startswith('在'):
        return zh
    if zh.startswith(('坐在', '穿著', '戴著')):
        return '正' + zh
    return '在' + zh


def negz(zh):
    if zh.startswith(('坐在', '穿著', '戴著')):
        return '沒有' + zh.replace('著', '')
    return '沒有' + (zh if zh.startswith('在') else '在' + zh.replace('著', ''))


# ---------- 句子產生 ----------
def aff():
    s = rnd.choice(SUBJ); v = rnd.choice([x for x in VERBS if x[0] != 'rain']); t = rnd.choice(NOW)
    ph, phz = phrase(v)
    en = '%s %s %s %s.' % (s[0], s[2], ph, t[0])
    return dict(en=en, zh='%s%s%s。' % (s[1], t[1], prog(phz)), blank=len(s[0].split()), ans=s[2],
                cat='be', gp='現在進行式', why='%s 搭配 %s，再接 V-ing。' % (s[3] if s[0] != 'I' else 'I', s[2]), ing=v[1], base=v[0], subj=s)


def neg():
    s = rnd.choice(SUBJ); v = rnd.choice([x for x in VERBS if x[0] != 'rain']); t = rnd.choice(NOW)
    ph, phz = phrase(v)
    n = NEG[s[2]]
    en = '%s %s %s %s.' % (s[0], n, ph, t[0])
    k = len(s[0].split())
    return dict(en=en, zh='%s%s%s。' % (s[1], t[1], negz(phz)), blank=k, ans=n.split()[0] if s[2] == 'am' else n,
                cat='neg', gp='現在進行式', why='否定句：%s not＋V-ing。' % s[2], ing=v[1], base=v[0], subj=s)


def ques(short=True):
    s = rnd.choice([x for x in SUBJ if x[0] != 'I']); v = rnd.choice([x for x in VERBS if x[0] != 'rain']); t = rnd.choice(NOW)
    ph, phz = phrase(v)
    be = s[2].capitalize()
    q = '%s %s %s %s?' % (be, mid(s[0]), ph, t[0])
    if not short:
        return dict(en=q, zh='%s%s%s嗎？' % (s[1], t[1], prog(phz)), blank=0, ans=be, cat='beq', gp='現在進行式',
                    why='問句把 %s 移到句首。' % s[2], ing=v[1], base=v[0], subj=s)
    yes = rnd.random() < 0.5
    pr = 'I' if s[0] == 'You' else s[3]
    b = 'am' if pr == 'I' else ('is' if pr in ('he', 'she') else 'are')
    ansp = b if yes else ('am not' if pr == 'I' else NEG[b])
    en = '%s %s, %s %s.' % (q, 'Yes' if yes else 'No', pr, ansp)
    zh = '%s%s%s嗎？%s' % (s[1], t[1], prog(phz), '是的。' if yes else '不，沒有。')
    idx = len(q.split()) + 2
    return dict(en=en, zh=zh, blank=idx, ans=ansp.split()[0] if pr == 'I' else ansp, cat='sa', gp='現在進行式',
                why='簡答用 %s %s。' % (pr, ansp), ing=v[1], base=v[0], subj=s)


def what_doing():
    s = rnd.choice([x for x in SUBJ if x[0] != 'I']); v = rnd.choice([x for x in VERBS if x[0] != 'rain'])
    if v[0] == 'wear':  # 穿戴是狀態，不適合回答 What are you doing?（不多抽亂數，保持其他題目不變）
        v = VERBS[0]
    ph, phz = phrase(v)
    pr = 'I' if s[0] == 'You' else s[3].capitalize()
    b = 'am' if pr == 'I' else ('is' if pr in ('He', 'She') else 'are')
    en = 'What %s %s doing? %s %s %s.' % (s[2], mid(s[0]), pr, b, ph)
    zh = '%s在做什麼？%s%s。' % (s[1], '我' if pr == 'I' else s[1], prog(phz))
    alts = [] if pr == 'I' or s[0] in ('He', 'She', 'They', 'We') else ['What %s %s doing? %s %s %s.' % (s[2], mid(s[0]), s[0], s[2], ph)]
    return dict(en=en, zh=zh, alts=alts, blank=1, ans=s[2], cat='be', gp='現在進行式', why='What＋be＋主詞＋doing？', ing=v[1], base=v[0], subj=s)


def contrast():
    s = rnd.choice(SUBJ); v = rnd.choice([x for x in VERBS if x[0] not in ('rain', 'get', 'sit', 'sleep')])
    objs = v[3] or [('', v[2])]
    o = rnd.choice(objs)
    h = rnd.choice(HABIT); t = rnd.choice(NOW)
    while h[0] == 'every morning' and any(x in o[0] for x in ('lunch', 'dinner', 'late')):
        h = rnd.choice(HABIT)
    third = s[2] == 'is'
    simple = THIRD[v[0]] if third else v[0]
    if rnd.random() < 0.5:
        if h[0] in ('usually', 'often'):
            en = '%s %s %s %s.' % (s[0], h[0], simple, o[0])
            k = len(s[0].split()) + 1
        else:
            en = '%s %s %s %s.' % (s[0], simple, o[0], h[0])
            k = len(s[0].split())
        en = en.replace('  ', ' ')
        return dict(en=en, zh='%s%s%s。' % (s[1], h[1], o[1].replace('著', '')), blank=k, ans=simple,
                    cat='tense', gp='簡單式 vs 進行式', why='%s 是習慣，用現在簡單式%s。' % (h[0], '（第三人稱加 -s）' if third else ''),
                    ing=v[1], base=v[0], subj=s, alt=v[1], habit=True)
    en = ('%s %s %s %s %s.' % (s[0], s[2], v[1], o[0], t[0])).replace('  ', ' ')
    k = len(s[0].split())
    return dict(en=en, zh='%s%s%s。' % (s[1], t[1], prog(o[1])), blank=k, ans=s[2], cat='be', gp='簡單式 vs 進行式',
                why='%s 表示正在進行，用 be＋V-ing。' % t[0], ing=v[1], base=v[0], subj=s, alt='does' if s[2] == 'is' else 'do')


def spelling():
    b, ing, why, tail = rnd.choice(SPELL)
    s = rnd.choice(SUBJ)
    return dict(en='%s %s %s %s now.' % (s[0], s[2], ing, tail), zh='', blank=len(s[0].split()) + 1, ans=ing, cat='ing', gp='-ing 拼字',
                why='%s → %s：%s。' % (b, ing, why), ing=ing, base=b, subj=s)


GEN = {57: [aff] * 5 + [spelling] * 2, 58: [neg] * 5 + [aff] * 2, 59: [ques] * 4 + [lambda: ques(False)] * 2 + [what_doing] * 2,
       60: [contrast] * 6 + [aff, neg, ques], 61: [aff, neg, ques, what_doing, contrast, contrast, spelling]}
TOPIC = {57: '現在進行式肯定句與 -ing 拼字', 58: '現在進行式否定句', 59: '進行式問句與 What are you doing?',
         60: '現在簡單式 vs 現在進行式', 61: '現在進行式總複習'}


def sentences(day, n):
    out, seen = [], set()
    tries = 0
    while len(out) < n and tries < n * 30:
        tries += 1
        d = rnd.choice(GEN[day])()
        if d['en'] in seen:
            continue
        seen.add(d['en'])
        out.append(d)
    return out


def blank(en, i):
    t = en.split(' ')
    c = t[i].rstrip('.,?!'); p = t[i][len(c):]
    return ' '.join(t[:i] + ['___' + p] + t[i + 1:]), c


def opts_for(d):
    c = d['ans']
    pool = {'be': ['am', 'is', 'are', 'be'], 'neg': ["isn't", "aren't", 'not', "don't", "doesn't"], 'beq': ['Am', 'Is', 'Are', 'Do', 'Does'],
            'sa': ['am', 'is', 'are', "isn't", "aren't", 'do', 'does', "don't"],
            'ing': [d['base'], d['base'] + 'ing', d['base'] + d['base'][-1] + 'ing', d['base'][:-1] + 'ing'],
            'tense': [d['ans'], d['base'], d['base'] + 's' if not d['base'].endswith('s') else d['base'] + 'es', 'is ' + d['ing'], d['ing']]}[d['cat']]
    o = list(dict.fromkeys([x for x in pool if x != c]))
    rnd.shuffle(o)
    o = o[:3] + [c]
    rnd.shuffle(o)
    return o


VOCAB = [  # (en, pos, zh, ex, ja, r)
    ('now', 'adv.', '現在', 'I am reading now.', '今', 'いま'), ('right now', 'adv.', '此刻', 'She is busy right now.', '今すぐ', 'いますぐ'),
    ('at the moment', 'phr.', '目前', "He isn't working at the moment.", '今のところ', 'いまのところ'),
    ('look', 'int.', '看！', "Look! It's raining.", '見て', 'みて'), ('listen', 'int.', '聽！', 'Listen! The baby is crying.', '聞いて', 'きいて'),
    ('cry', 'v.', '哭', 'The baby is crying.', '泣く', 'なく'), ('smile', 'v.', '微笑', 'She is smiling at me.', 'ほほえむ', ''),
    ('laugh', 'v.', '笑', 'They are laughing.', '笑う', 'わらう'), ('dance', 'v.', '跳舞', 'We are dancing.', '踊る', 'おどる'),
    ('sing', 'v.', '唱歌', 'Amy is singing.', '歌う', 'うたう'), ('fly', 'v.', '飛', 'The birds are flying.', '飛ぶ', 'とぶ'),
    ('walk', 'v.', '走路', 'I am walking to school.', '歩く', 'あるく'), ('wait', 'v.', '等', 'We are waiting for the bus.', '待つ', 'まつ'),
    ('wear', 'v.', '穿著', 'He is wearing a hat.', '着る', 'きる'), ('carry', 'v.', '提；搬', 'She is carrying a bag.', '運ぶ', 'はこぶ'),
    ('hold', 'v.', '拿著', 'I am holding a cup.', '持つ', 'もつ'), ('rain', 'v.', '下雨', 'It is raining now.', '雨が降る', 'あめがふる'),
    ('snow', 'v.', '下雪', 'It is snowing in Tokyo.', '雪が降る', 'ゆきがふる'), ('shine', 'v.', '照耀', 'The sun is shining.', '照る', 'てる'),
    ('blow', 'v.', '吹', 'The wind is blowing.', '吹く', 'ふく'), ('busy', 'adj.', '忙碌的', "I'm busy. I'm cooking.", '忙しい', 'いそがしい'),
    ('phone', 'n.', '電話', 'She is talking on the phone.', '電話', 'でんわ'), ('message', 'n.', '訊息', 'He is writing a message.', 'メッセージ', ''),
    ('video', 'n.', '影片', 'They are watching a video.', '動画', 'どうが'), ('shower', 'n.', '淋浴', 'He is taking a shower.', 'シャワー', ''),
    ('dishes', 'n.', '碗盤', 'I am washing the dishes.', 'お皿', 'おさら'), ('sofa', 'n.', '沙發', 'Dad is sitting on the sofa.', 'ソファー', ''),
    ('pool', 'n.', '游泳池', 'The kids are swimming in the pool.', 'プール', ''), ('mall', 'n.', '購物中心', 'We are shopping at the mall.', 'ショッピングモール', ''),
    ('report', 'n.', '報告', 'She is writing a report.', 'レポート', ''), ('online', 'adv.', '在網路上', 'I am shopping online.', 'オンラインで', ''),
    ('dressed', 'adj.', '穿好衣服的', 'He is getting dressed.', '服を着た', 'ふくをきた'), ('ready', 'adj.', '準備好的', 'We are getting ready.', '準備ができた', 'じゅんびができた'),
    ('these days', 'phr.', '最近', 'I am learning Japanese these days.', '最近', 'さいきん'),
    ('this week', 'phr.', '這週', 'He is working late this week.', '今週', 'こんしゅう'),
]
DAY_VOCAB = {57: VOCAB[0:3] + VOCAB[5:17] + VOCAB[21:31], 58: VOCAB[0:3] + VOCAB[16:21] + VOCAB[21:31] + VOCAB[31:35] + VOCAB[3:5],
             59: VOCAB[3:20] + VOCAB[24:32], 60: VOCAB[0:3] + VOCAB[31:35] + VOCAB[5:23], 61: VOCAB[0:25]}


def readings(day):
    names = [('Mia', 'she', 'her'), ('Ken', 'he', 'his'), ('Lisa', 'she', 'her'), ('Ben', 'he', 'his')]
    out = []
    for i in range(4):
        n, p, ps = names[i]
        P = p.capitalize()
        f = rnd.choice(['mother', 'father', 'brother', 'sister'])
        IN = [(v[0], v[1], v[2], [o for o in v[3] if o[0] not in ('basketball', 'to the teacher', 'for the test')]) + tuple(v[4:])
              for v in (VERBS[j] for j in (0, 1, 2, 3, 4, 5, 6, 7, 8, 10))]
        me = rnd.choice(IN); mo = rnd.choice(me[3])
        fa = rnd.choice([x for x in IN if x[0] != me[0]]); fo = rnd.choice(fa[3])
        hb = rnd.choice([x for x in IN if x[0] not in (me[0], fa[0])]); ho = rnd.choice(hb[3])
        place = rnd.choice(['in the living room', 'in the kitchen', 'in the bedroom', 'at the café'])
        weather = rnd.choice([('raining', 'rainy'), ('snowing', 'snowy'), ('shining', 'sunny')])
        w_text = "It is raining outside." if weather[0] == 'raining' else ("It is snowing outside." if weather[0] == 'snowing' else 'The sun is shining.')
        text = (f"It is Saturday afternoon. {n} is {place}. {w_text} {P} is {me[1]} {mo[0]} now. "
                f"{P} usually {THIRD[hb[0]]} {ho[0]} on Saturdays, but today {p} isn't {hb[1]} {ho[0]}. "
                f"{ps.capitalize()} {f} is with {'him' if p == 'he' else 'her'}. The {f} is {fa[1]} {fo[0]}. "
                f"They are happy because they are not busy today.").replace('  ', ' ')
        def mc(q, c, pool):
            o = [c] + [x for x in pick([x for x in pool if x != c], 3)]
            rnd.shuffle(o)
            return {'q': q, 'opts': o, 'a': o.index(c)}
        acts = sorted({'%s %s' % (x[1], o[0]) for x in IN for o in x[3]})
        qs = [mc(f'What is {n} doing now?', f'{me[1]} {mo[0]}', acts),
              mc(f'Where is {n}?', place, ['in the living room', 'in the kitchen', 'in the bedroom', 'at the café', 'at school', 'at the park']),
              mc(f'What does {n} usually do on Saturdays?', f'{p.capitalize()} {THIRD[hb[0]]} {ho[0]}.',
                 sorted({f'{p.capitalize()} {THIRD[x[0]]} {o[0]}.' for x in IN for o in x[3]})),
              mc(f"What is {n}'s {f} doing?", f'{fa[1]} {fo[0]}', acts),
              mc('How is the weather?', weather[1], ['rainy', 'snowy', 'sunny', 'windy'])]
        out.append({'title': f'{n} 的星期六', 'text': text, 'qs': qs})
    return out


SPEAK = {57: ["I am reading a book now.", "She is cooking dinner.", "They are playing basketball.", "We are waiting for the bus.", "It is raining now.", "He is running in the park."],
         58: ["I am not working now.", "She isn't sleeping.", "They aren't watching TV.", "We aren't eating lunch.", "He isn't driving to work.", "It isn't raining today."],
         59: ["Are you studying now?", "Yes, I am.", "Is she cooking?", "No, she isn't.", "What are you doing?", "I'm listening to music."],
         60: ["I usually drink tea, but today I'm drinking coffee.", "She works in an office. Today she's working at home.", "Do you play the guitar? Are you playing it now?", "He doesn't swim every day. He's swimming now.", "We often eat at home. Tonight we're eating out.", "It rains a lot in June. It's raining now."],
         61: ["Look! The birds are flying.", "Listen! The baby is crying.", "What is your mother doing?", "She's washing the dishes.", "I'm not busy now.", "These days I'm learning Japanese."]}
WRITE = {57: ['看看四周，用現在進行式寫 5 句：家人或身邊的人「現在」正在做什麼。', "My mother is cooking dinner. My father is reading the news. My brother is playing a game. The cat is sleeping on the sofa. I am studying English."],
         58: ['寫 5 句：現在「沒有」在做的事，以及其實正在做的事（isn\'t / aren\'t … but …）。', "I'm not watching TV. I'm studying. My sister isn't sleeping. She is reading. It isn't raining now."],
         59: ['寫一段 3 組問答的對話：問朋友和家人現在在做什麼（Are you…? / What is … doing?）。', "Are you working now? No, I'm not. What are you doing? I'm watching a movie. Is your brother at home? Yes, he is. He's cooking."],
         60: ['用「平常 vs 今天」寫 5 句：usually / every day 用簡單式，today / now 用進行式。', "I usually take the bus, but today I'm driving. My father works in Taipei. This week he's working in Tainan. We often eat at home, but tonight we're eating out."],
         61: ['寫一段 6 句以上的短文：週末下午的現在情境，包含肯定、否定、問句和一句習慣（簡單式）。', "It's Sunday afternoon. I'm sitting in a café. I'm not working today. My friend is drinking tea. Is it raining? No, the sun is shining. I usually come here on Sundays."]}


TIMES = re.compile(r'\b(right now|at the moment|now)(?=[.?!])')
SWAPS = [['My mother', 'My mom'], ['My father', 'My dad'], ['my mother', 'my mom'],
         ['my father', 'my dad'], ['café', 'cafe', 'coffee shop'], ['working at home', 'working from home']]


def variants(answers):
    """中翻英：同義的時間說法、mom/dad、café 拼法等都收。"""
    out = []
    for a in answers:
        for t in (['now', 'right now', 'at the moment'] if TIMES.search(a) else [None]):
            v = TIMES.sub(t, a) if t else a
            if v not in out:
                out.append(v)
    for group in SWAPS:
        for a in list(out):
            for x in group:
                if x in a:
                    for y in group:
                        v = a.replace(x, y)
                        if v not in out:
                            out.append(v)
                    break
    out = [answers[0]] + [x for x in out if x != answers[0]]
    return out[:24]


def build_day(day):
    P = sentences(day, 180)
    mc, fill, err, trans, reo, dic = [], [], [], [], [], []
    for d in P[:50]:
        q, c = blank(d['en'], d['blank'])
        o = opts_for(d)
        if c not in o:
            o[-1] = c
        mc.append({'q': q, 'opts': o, 'a': o.index(c), 'gp': d['gp'], 'why': d['why'], **({'zh': d['zh']} if d['zh'] else {})})
    for d in P[50:100]:
        q, c = blank(d['en'], d['blank'])
        hint = {'be': 'am / is / are', 'neg': "am / is / are（空格後面已經有 not）" if c == 'am' else "isn't / aren't", 'beq': 'Am / Is / Are',
                'sa': 'am / is / are / isn\'t / aren\'t', 'ing': '寫出 %s 的 -ing 形' % d['base'],
                'tense': '用 %s：現在簡單式還是現在進行式？' % d['base']}[d['cat']]
        fill.append({'q': q, 'a': [c], 'hint': hint, 'gp': d['gp'], 'why': d['why'], **({'zh': d['zh']} if d['zh'] else {})})
    for d in P[100:115]:
        t = d['en'].split(' ')
        i = d['blank']
        c = t[i].rstrip('.,?!'); p = t[i][len(c):]
        if d['cat'] == 'ing':
            wrong = d['base'] + 'ing' if d['base'] + 'ing' != c else d['base']
        elif d['cat'] == 'tense' or d.get('alt'):
            wrong = d['alt']
        elif c in ('am', 'is', 'are'):
            wrong = rnd.choice([x for x in ('am', 'is', 'are') if x != c])
        elif c in ("isn't", "aren't"):
            wrong = "aren't" if c == "isn't" else "isn't"
        elif c in ('Am', 'Is', 'Are'):
            wrong = rnd.choice(['Do', 'Does'] + [x for x in ('Is', 'Are') if x != c])
        else:
            wrong = 'do' if c in ('am', 'is', 'are') else rnd.choice([x for x in ('is', 'are') if x != c])
        if wrong == c:
            wrong = 'be'
        t2 = t[:]; t2[i] = wrong + p
        err.append({'s': ' '.join(t2), 'wrong': i, 'fix': c, 'why': d['why'], 'full': d['en']})
    for d in [x for x in P[115:] if x['zh']][:20]:
        trans.append({'zh': d['zh'], 'a': variants([d['en']] + d.get('alts', [])), 'gp': d['gp']})
    short = [x for x in P[115:] if 4 <= len(x['en'].split()) <= 9 and '?' not in x['en'][:-1]]
    for d in short[:15]:
        ws = d['en'].split(' '); sh = ws[:]
        for _ in range(10):
            rnd.shuffle(sh)
            if sh != ws:
                break
        reo.append({'words': sh, 'a': d['en']})
    mid_ = [x for x in P[130:] if 4 <= len(x['en'].split()) <= 9 and ', ' not in x['en']]
    for d in mid_[:10]:
        dic.append({'s': d['en']})
    vocab = [{'w': v[0], 'pos': v[1], 'zh': v[2], 'ex': v[3], 'ja': [v[4], v[5]], **({'review': True} if day == 61 else {})} for v in DAY_VOCAB[day]]
    pool = VOCAB
    vr = []
    for i, c in enumerate(rnd.sample(pool, len(pool))):
        others = rnd.sample([x for x in pool if x[2] != c[2]], 3)
        if i % 2:
            o = [c[2]] + [x[2] for x in others]; rnd.shuffle(o); vr.append({'q': c[0], 'a': c[2], 'opts': o, 'dir': 'en2zh'})
        else:
            o = [c[0]] + [x[0] for x in others]; rnd.shuffle(o); vr.append({'q': c[2], 'a': c[0], 'opts': o, 'dir': 'zh2en'})
    sp = [{'prompt': s, 'model': s} for s in SPEAK[day]] + [{'prompt': d['en'], 'model': d['en']} for d in P[150:164]]
    w = WRITE[day]
    return {'week': 9, 'dayOfWeek': day - 56, 'weekTitle': '補充週：現在進行式', 'topic': TOPIC[day], 'review': day == 61, 'rest': False,
            'blocks': {'vocab_new': vocab, 'vocab_review': (vr * 2)[:60], 'mc': mc, 'fill': fill, 'translate': trans, 'error': err,
                       'reorder': reo, 'reading': readings(day), 'dictation': dic, 'speaking': sp,
                       'writing': [{'prompt': w[0], 'minWords': 20, 'sample': w[1]}] + [
                           {'prompt': p, 'minWords': 12, 'sample': s} for p, s in [
                               ('寫 3 句：現在窗外的情形（天氣、路上的人）。', "It's raining now. A man is walking with an umbrella. Two children are running to school."),
                               ('寫 3 句：你的朋友現在可能正在做什麼。', "Amy is probably working now. Ken is studying. Lisa is cooking lunch."),
                               ('寫一則傳給朋友的簡訊，說你現在在做什麼、不能接電話的原因。', "Sorry, I can't talk now. I'm driving to work. I'm calling you back later.")]]}}


GRAMMAR = {'point': '現在進行式：am / is / are + V-ing',
           'explain': '描述「說話的此刻正在進行」或「這陣子暫時」的動作。be 動詞跟著主詞變（I am / he is / they are），後面接動詞加 -ing。否定在 be 後面加 not；問句把 be 移到句首。和現在簡單式比較：every day / usually 是習慣，用簡單式；now / right now / at the moment / Look! / Listen! 是正在發生，用進行式。',
           'patterns': ['I am reading a book now.', "She isn't sleeping. She's studying.", 'Are you working at the moment? — Yes, I am.',
                        'What are they doing? — They are playing basketball.', 'He usually drives to work, but today he is taking the bus.']}


def build():
    days = {str(d): build_day(d) for d in range(57, 62)}
    # 補充週檢測：25 文法＋10 單字
    items = []
    for d in sentences(61, 60)[:25]:
        q, c = blank(d['en'], d['blank'])
        o = opts_for(d)
        if c not in o:
            o[-1] = c
        items.append({'type': 'mc', 'q': q, 'opts': o, 'a': o.index(c), 'gp': '現在進行式'})
    for c in rnd.sample(VOCAB, 10):
        o = [c[2]] + [x[2] for x in rnd.sample([x for x in VOCAB if x[2] != c[2]], 2)]
        rnd.shuffle(o)
        items.append({'type': 'mc', 'q': '「%s」是什麼意思？' % c[0], 'opts': o, 'a': o.index(c[2]), 'gp': '單字', 'speak': c[0]})
    week = {'id': 9, 'title': '補充週：現在進行式', 'subtitle': 'Present Continuous', 'focus': 'am/is/are + V-ing、否定、問句、與現在簡單式對比', 'grammar': GRAMMAR}
    return days, {'title': '補充週檢測（現在進行式）', 'items': items}, week


if __name__ == '__main__':
    import json
    days, test, week = build()
    for k, d in days.items():
        b = d['blocks']
        print(k, d['topic'], {x: len(y) for x, y in b.items()})
    b = days['60']['blocks']
    for x in b['mc'][:6]:
        print(x['q'], x['opts'], x['opts'][x['a']])
    for x in b['error'][:4]:
        print(x)
    print(b['translate'][:3]); print(b['reading'][0]['text']); print(b['reading'][0]['qs'][2])
