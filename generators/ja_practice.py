# -*- coding: utf-8 -*-
"""日文 N5 平行練習：Day 1–14，文法與英文同日對應"""
import random
rnd = random.Random(20260912)
def T(s):
    """'私|わたし は 学生|がくせい です 。' -> [[t,r],...]"""
    out=[]
    for tok in s.split(' '):
        if not tok: continue
        p=tok.split('|'); out.append([p[0], p[1] if len(p)>1 else ''])
    return out
def pick(l,n): return rnd.sample(l, min(n,len(l)))

# ---------- 名詞與主詞 ----------
SUBJ1 = [('私|わたし','我'),('あなた','你')]
SUBJ3 = [('彼|かれ','他'),('彼女|かのじょ','她'),('父|ちち','我爸爸'),('母|はは','我媽媽'),('兄|あに','我哥哥'),('姉|あね','我姊姊'),('先生|せんせい','老師'),('友達|ともだち','我的朋友'),
         ('トム さん','Tom'),('エイミー さん','Amy'),('ケン さん','Ken'),('メイ さん','Mei')]
SUBJP = [('私たち|わたしたち','我們'),('彼ら|かれら','他們'),('両親|りょうしん','我的父母'),('子供たち|こどもたち','孩子們'),('トム さん と エイミー さん','Tom 和 Amy')]
NAMES = [('トム','Tom'),('エイミー','Amy'),('ケン','Ken'),('メイ','Mei'),('リサ','Lisa'),('ジャック','Jack'),('アンナ','Anna'),('レオ','Leo')]
JOBS = [('先生|せんせい','老師'),('学生|がくせい','學生'),('医者|いしゃ','醫生'),('看護師|かんごし','護理師'),('エンジニア','工程師'),('コック','廚師'),('運転手|うんてんしゅ','司機'),('農家|のうか','農夫'),('歌手|かしゅ','歌手'),('会社員|かいしゃいん','上班族')]
IADJ = [('忙しい|いそがしい','忙しくない|いそがしくない','很忙','不忙'),('うれしい','うれしくない','很開心','不開心'),('悲しい|かなしい','悲しくない|かなしくない','很難過','不難過'),
        ('若い|わかい','若くない|わかくない','很年輕','不年輕'),('強い|つよい','強くない|つよくない','很強壯','不強壯'),('面白い|おもしろい','面白くない|おもしろくない','很有趣','不有趣'),('優しい|やさしい','優しくない|やさしくない','很溫柔','不溫柔')]
NADJ = [('元気|げんき','很有精神','沒精神'),('親切|しんせつ','很親切','不親切'),('静か|しずか','很安靜','不安靜'),('きれい','很漂亮','不漂亮'),('有名|ゆうめい','很有名','不有名')]
THINGS = [('車|くるま','這台車'),('部屋|へや','房間'),('かばん','包包'),('家|いえ','房子'),('本|ほん','書'),('携帯|けいたい','手機'),('自転車|じてんしゃ','腳踏車'),('パソコン','電腦')]
TADJ = [('大きい|おおきい','大きくない|おおきくない','很大','不大'),('小さい|ちいさい','小さくない|ちいさくない','很小','不小'),('新しい|あたらしい','新しくない|あたらしくない','是新的','不是新的'),
        ('古い|ふるい','古くない|ふるくない','很舊','不舊'),('高い|たかい','高くない|たかくない','很貴','不貴')]
COUNTRIES = [('台湾|たいわん','台湾人|たいわんじん','台灣'),('日本|にほん','日本人|にほんじん','日本'),('韓国|かんこく','韓国人|かんこくじん','韓國'),('中国|ちゅうごく','中国人|ちゅうごくじん','中國'),
             ('アメリカ','アメリカ人|アメリカじん','美國'),('イギリス','イギリス人|イギリスじん','英國'),('フランス','フランス人|フランスじん','法國'),('ドイツ','ドイツ人|ドイツじん','德國'),('カナダ','カナダ人|カナダじん','加拿大')]
PLACES = [('家|いえ','家'),('学校|がっこう','學校'),('会社|かいしゃ','公司'),('病院|びょういん','醫院'),('公園|こうえん','公園'),('店|みせ','商店'),('銀行|ぎんこう','銀行'),('駅|えき','車站'),('図書館|としょかん','圖書館'),('台所|だいどころ','廚房'),('部屋|へや','房間')]
AGES = [('八歳|はっさい','八歲'),('十歳|じゅっさい','十歲'),('十二歳|じゅうにさい','十二歲'),('十五歳|じゅうごさい','十五歲'),('十八歳|じゅうはっさい','十八歲'),('二十歳|はたち','二十歲'),('三十歳|さんじゅっさい','三十歲')]
FAM = [('父|ちち','お父さん|おとうさん','爸爸'),('母|はは','お母さん|おかあさん','媽媽'),('兄|あに','お兄さん|おにいさん','哥哥'),('姉|あね','お姉さん|おねえさん','姊姊'),
       ('祖父|そふ','おじいさん','爺爺'),('祖母|そぼ','おばあさん','奶奶'),('弟|おとうと','弟さん|おとうとさん','弟弟'),('妹|いもうと','妹さん|いもうとさん','妹妹')]
OBJ = [('鍵|かぎ','鑰匙'),('財布|さいふ','錢包'),('時計|とけい','時鐘'),('帽子|ぼうし','帽子'),('傘|かさ','雨傘'),('かばん','包包'),('本|ほん','書'),('ペン','筆'),('車|くるま','車'),
       ('自転車|じてんしゃ','腳踏車'),('携帯|けいたい','手機'),('カメラ','相機'),('眼鏡|めがね','眼鏡'),('靴|くつ','鞋子'),('家|いえ','房子'),('写真|しゃしん','照片')]
POSS = [('私|わたし','我'),('あなた','你'),('彼|かれ','他'),('彼女|かのじょ','她'),('私たち|わたしたち','我們'),('彼ら|かれら','他們'),('先生|せんせい','老師'),('トム さん','Tom'),('メイ さん','Mei')]
HAVE_THING = [('車|くるま','車'),('自転車|じてんしゃ','腳踏車'),('パソコン','電腦'),('カメラ','相機'),('時間|じかん','時間'),('お金|おかね','錢'),('傘|かさ','雨傘'),('辞書|じしょ','字典'),
              ('地図|ちず','地圖'),('宿題|しゅくだい','功課'),('切符|きっぷ','票'),('携帯|けいたい','手機'),('予定|よてい','計畫'),('質問|しつもん','問題')]
HAVE_ANIM = [('犬|いぬ','狗'),('猫|ねこ','貓'),('兄|あに','哥哥'),('姉|あね','姊姊'),('弟|おとうと','弟弟'),('妹|いもうと','妹妹'),('子供|こども','孩子'),('友達|ともだち','朋友'),('ペット','寵物')]
FOOD = [('水|みず','水'),('お茶|おちゃ','茶'),('コーヒー','咖啡'),('牛乳|ぎゅうにゅう','牛奶'),('ジュース','果汁'),('パン','麵包'),('ケーキ','蛋糕'),('りんご','蘋果'),('卵|たまご','蛋')]
OWNERS = [('トム さん','Tom'),('エイミー さん','Amy'),('ケン さん','Ken'),('先生|せんせい','老師'),('父|ちち','我爸爸'),('母|はは','我媽媽'),('姉|あね','我姊姊'),('兄|あに','我哥哥'),('友達|ともだち','我朋友')]

def S(toks, zh, blanks, gp):
    return dict(toks=T(toks), zh=zh, blanks=blanks, gp=gp)
def idx_of(toks, word, start=0):
    t=T(toks); w=word.split('|')[0]
    for i in range(start,len(t)):
        if t[i][0]==w: return i
    raise ValueError(word+' not in '+toks)
P_WA = (['は','が','を','に'], '「〜は〜です」：は 標出主題，念 wa。')
P_NO = (['の','は','を','に'], 'の＝「…的」，接在名詞之間。')
P_GA = (['が','を','は','で'], '「〜が あります／います」前面用 が 標出存在的東西。')
P_KA = (['か','の','よ','ね'], '句尾加 か 就變成問句。')
P_KARA = (['から','へ','を','が'], 'から＝從；「〜から 来ました」＝來自…')
def B(toks, word, opts, why, start=0):
    return (idx_of(toks, word, start), opts, why)

def gen(day):
    P=[]
    if day==1:
        for s,sz in SUBJ1:
            for j,jz in JOBS:
                t=f"{s} は {j} です 。"; P.append(S(t, f"{sz}是{jz}。", [B(t,'は',*P_WA), B(t,'です',['です','ます','か','の'],'名詞結尾用 です＝「是」。')], 'です'))
            for n,nz in NAMES:
                nm = n if s.startswith('私') else n+' さん'
                t=f"{s} は {nm} です 。"; P.append(S(t, f"{sz}是 {nz}。", [B(t,'は',*P_WA)], 'です'))
        for n,nz in NAMES:
            t=f"はじめまして 。 私|わたし は {n} です 。"; P.append(S(t, f"初次見面。我是 {nz}。", [B(t,'は',*P_WA), B(t,'です',['です','ます','か','の'],'名詞結尾用 です。')], 'です'))
            t=f"私|わたし の 名前|なまえ は {n} です 。"; P.append(S(t, f"我的名字是 {nz}。", [B(t,'の',*P_NO), B(t,'は',*P_WA)], 'です'))
    elif day==2:
        for s,sz in SUBJ3:
            for j,jz in pick(JOBS,5):
                t=f"{s} は {j} です 。"; P.append(S(t, f"{sz}是{jz}。", [B(t,'は',*P_WA)], 'です'))
            for a,_,az,_ in IADJ:
                t=f"{s} は {a} です 。"; P.append(S(t, f"{sz}{az}。", [B(t,'は',*P_WA), B(t,'です',['です','だです','ます','か'],'い形容詞＋です 就是禮貌的說法。')], '形容詞'))
            for a,az,_ in NADJ:
                t=f"{s} は {a} です 。"; P.append(S(t, f"{sz}{az}。", [B(t,'は',*P_WA)], '形容詞'))
        for th,tz in THINGS:
            for a,_,az,_ in TADJ:
                t=f"この {th} は {a} です 。"; P.append(S(t, f"這個{tz}{az}。".replace('這個這台','這台'), [B(t,'は',*P_WA), B(t,'この',['この','これ','ここ','この人'],'この＋名詞＝這個…；これ 單獨使用。')], '形容詞'))
        for w,wz in [('暑い|あつい','很熱'),('寒い|さむい','很冷')]:
            t=f"今日|きょう は {w} です 。"; P.append(S(t, f"今天{wz}。", [B(t,'は',*P_WA)], '形容詞'))
    elif day==3:
        for s,sz in SUBJP+SUBJ1+SUBJ3[:6]:
            for c,cn,cz in COUNTRIES:
                t=f"{s} は {cn} です 。"; others=[x[1].split('|')[0] for x in COUNTRIES if x[0]!=c]
                P.append(S(t, f"{sz}是{cz}人。", [B(t,cn.split('|')[0],[cn.split('|')[0], c.split('|')[0], rnd.choice(others), c.split('|')[0]+'語'],'國名＋人（じん）＝…國人。')], '〜人'))
                t=f"{s} は {c} から 来ました|きました 。"; P.append(S(t, f"{sz}來自{cz}。", [B(t,'から',*P_KARA), B(t,'は',*P_WA)], 'から'))
            if s in [x[0] for x in SUBJP]:
                for j,jz in pick(JOBS,4):
                    t=f"{s} は {j} です 。"; P.append(S(t, f"{sz}是{jz}。", [B(t,'は',*P_WA)], 'です'))
    elif day==4:
        for s,sz in SUBJ1+SUBJ3+SUBJP[:3]:
            for j,jz in pick(JOBS,3):
                t=f"{s} は {j} ではありません 。"; P.append(S(t, f"{sz}不是{jz}。", [B(t,'ではありません',['ではありません','くないです','いません','です'],'名詞的否定：〜ではありません（口語 じゃないです）。')], '否定'))
            for a,n,az,nz in pick(IADJ,3):
                t=f"{s} は {n} です 。"; base=a.split('|')[0]
                P.append(S(t, f"{sz}{nz}。", [B(t,n.split('|')[0],[n.split('|')[0], base+'ではありません', base, base[:-1]+'くありました'],'い形容詞否定：去い＋くない。不能說「〜いではありません」。')], '否定'))
            for a,az,nz in pick(NADJ,2):
                t=f"{s} は {a} ではありません 。"; P.append(S(t, f"{sz}{nz}。", [B(t,'ではありません',['ではありません','くないです','いません','です'],'な形容詞否定和名詞一樣：〜ではありません。')], '否定'))
            for p,pz in pick(PLACES,3):
                t=f"{s} は {p} に いません 。"; P.append(S(t, f"{sz}不在{pz}。", [B(t,'いません',['いません','ありません','ではありません','です'],'人、動物「不在」用 いません；物品用 ありません。'), B(t,'に',['に','で','を','が'],'存在的地點用 に。')], '否定'))
        for th,tz in THINGS:
            for a,n,az,nz in pick(TADJ,2):
                t=f"この {th} は {n} です 。"; base=a.split('|')[0]
                P.append(S(t, f"這個{tz}{nz}。".replace('這個這台','這台'), [B(t,n.split('|')[0],[n.split('|')[0], base+'ではありません', base, base[:-1]+'くありました'],'い形容詞否定：去い＋くない。')], '否定'))
    elif day==5:
        for s,sz in [('あなた','你')]+SUBJ3:
            ans = '私|わたし' if s=='あなた' else s
            for j,jz in pick(JOBS,3):
                t=f"{s} は {j} です か 。 はい 、 そうです 。"; P.append(S(t, f"{sz}是{jz}嗎？是的，沒錯。", [B(t,'か',*P_KA), B(t,'そうです',['そうです','ちがいます','あります','います'],'「是的」回答 はい、そうです。')], '問句'))
                t=f"{s} は {j} です か 。 いいえ 、 ちがいます 。"; P.append(S(t, f"{sz}是{jz}嗎？不，不是。", [B(t,'ちがいます',['ちがいます','そうです','ありません','いません'],'「不是」回答 いいえ、ちがいます。')], '問句'))
            for a,n,az,nz in pick(IADJ,2):
                t=f"{s} は {a} です か 。 いいえ 、 {n} です 。"; base=a.split('|')[0]
                P.append(S(t, f"{sz}{az}嗎？不，{nz}。", [B(t,'か',*P_KA), B(t,n.split('|')[0],[n.split('|')[0], base+'ではありません', 'ちがいます', base],'形容詞問句的否定回答用 〜くないです。')], '問句'))
            for p,pz in pick(PLACES,2):
                t=f"{s} は {p} に います か 。 はい 、 います 。"; P.append(S(t, f"{sz}在{pz}嗎？是的，在。", [B(t,'か',*P_KA), B(t,'います',['います','あります','です','そうです'],'人在不在：います。',8 if True else 0)], '問句'))
        for w,wz in [('月曜日|げつようび','星期一'),('金曜日|きんようび','星期五'),('日曜日|にちようび','星期日'),('誕生日|たんじょうび','生日')]:
            t=f"今日|きょう は {w} です か 。"; P.append(S(t, f"今天是{wz}嗎？", [B(t,'か',*P_KA)], '問句'))
    elif day==6:
        for s,sz in [('あなた','你')]+SUBJ3:
            t=f"{s} は どこ です か 。"; P.append(S(t, f"{sz}在哪裡？", [B(t,'どこ',['どこ','何|なに','だれ','何歳|なんさい'],'問地點用 どこ。')], '疑問詞'))
            t=f"{s} は 何歳|なんさい です か 。"; P.append(S(t, f"{sz}幾歲？", [B(t,'何歳',['何歳','どこ','だれ','何'],'問年齡用 何歳（なんさい）。')], '疑問詞'))
            t=f"{s} は どこ から 来ました|きました か 。"; P.append(S(t, f"{sz}來自哪裡？", [B(t,'どこ',['どこ','だれ','何','何歳'],'問「從哪裡」用 どこから。'), B(t,'から',*P_KARA)], '疑問詞'))
        for s,sz in SUBJ3[:2]+[('あの 人|ひと','那個人')]:
            t=f"{s} は だれ です か 。"; P.append(S(t, f"{sz}是誰？", [B(t,'だれ',['だれ','どこ','何','何歳'],'問人用 だれ。')], '疑問詞'))
        for a,az in AGES:
            t=f"私|わたし は {a} です 。"; P.append(S(t, f"我{az}。", [B(t,'は',*P_WA)], '疑問詞'))
        for q,qz in [('お名前|おなまえ','你的名字'),('仕事|しごと','工作'),('これ','這個')]:
            t=f"{q} は 何|なん です か 。"; P.append(S(t, f"{qz}是什麼？", [B(t,'何',['何','どこ','だれ','何歳'],'問「什麼」用 何（なん）。')], '疑問詞'))
        for p,pz in PLACES:
            t=f"トイレ は どこ です か 。"; break
        for p,pz in pick(PLACES,6):
            t=f"{p} は どこ です か 。"; P.append(S(t, f"{pz}在哪裡？", [B(t,'どこ',['どこ','何','だれ','何歳'],'問地點用 どこ。')], '疑問詞'))
    elif day in (7,14):
        src = (1,2,3,4,5,6) if day==7 else (8,9,10,11,12,13)
        for d in src: P += pick(gen(d), 30)
    elif day==8:
        for h,o,z in FAM:
            for j,jz in pick(JOBS,3):
                t=f"私|わたし の {h} は {j} です 。"; others=[x[0].split('|')[0] for x in FAM if x[0]!=h]
                P.append(S(t, f"我的{z}是{jz}。", [B(t,'の',*P_NO), B(t,h.split('|')[0],[h.split('|')[0], o.split('|')[0], rnd.choice(others), rnd.choice([x[1].split('|')[0] for x in FAM if x[1]!=o])],'說自己的家人用謙稱：父、母、兄、姉…')], '家人'))
            for a,_,az,_ in pick(IADJ,2):
                t=f"あなた の {o} は {a} です 。"
                P.append(S(t, f"你的{z}{az}。", [B(t,'の',*P_NO), B(t,o.split('|')[0],[o.split('|')[0], h.split('|')[0], rnd.choice([x[1].split('|')[0] for x in FAM if x[1]!=o]), rnd.choice([x[0].split('|')[0] for x in FAM if x[0]!=h])],'說別人的家人用尊稱：お父さん、お母さん…')], '家人'))
        t="これ は 私|わたし の 家族|かぞく の 写真|しゃしん です 。"; P.append(S(t, "這是我家人的照片。", [B(t,'の',*P_NO)], 'の'))
        t="私|わたし の 家族|かぞく は 四人|よにん です 。"; P.append(S(t, "我家有四個人。", [B(t,'の',*P_NO)], 'の'))
        t="両親|りょうしん は 元気|げんき です 。"; P.append(S(t, "我父母都很好。", [B(t,'は',*P_WA)], '家人'))
    elif day==9:
        for o,oz in OBJ:
            for p,pz in pick(POSS,3):
                for k,kz in [('これ','這'),('あれ','那')]:
                    t=f"{k} は {p} の {o} です 。"
                    P.append(S(t, f"{kz}是{pz}的{oz}。", [B(t,'の',*P_NO), B(t,k,[k,'あれ' if k=='これ' else 'これ','ここ','あそこ'],'これ＝這個；あれ＝那個（遠處）；ここ／あそこ 是地點。')], 'これ・あれ'))
            p,pz = rnd.choice(POSS); a,_,az,_ = rnd.choice(TADJ)
            t=f"{p} の {o} は {a} です 。"; P.append(S(t, f"{pz}的{oz}{az}。", [B(t,'の',*P_NO)], 'の'))
    elif day==10:
        for s,sz in SUBJ1+SUBJ3[:8]+SUBJP[:2]:
            for o,oz in pick(HAVE_THING,4):
                t=f"{s} は {o} が あります 。"; P.append(S(t, f"{sz}有{oz}。", [B(t,'が',*P_GA), B(t,'あります',['あります','います','です','ありません'],'物品「有」用 あります。')], 'あります・います'))
            for o,oz in pick(HAVE_ANIM,3):
                t=f"{s} は {o} が います 。"; P.append(S(t, f"{sz}有{oz}。", [B(t,'が',*P_GA), B(t,'います',['います','あります','です','いません'],'人、動物「有」用 います。')], 'あります・います'))
        for s,sz in SUBJ3[:6]:
            for part,pz,a,az in [('髪|かみ','頭髮','長い|ながい','很長'),('目|め','眼睛','大きい|おおきい','很大'),('背|せ','個子','高い|たかい','很高'),('髪|かみ','頭髮','短い|みじかい','很短')]:
                t=f"{s} は {part} が {a} です 。"; P.append(S(t, f"{sz}的{pz}{az}。", [B(t,'が',['が','を','の','で'],'「AはBが形容詞」描述外表特徵。')], 'あります・います'))
    elif day==11:
        for s,sz in SUBJ1+SUBJ3[:8]+SUBJP[:2]:
            for o,oz in pick(HAVE_THING,4):
                t=f"{s} は {o} が ありません 。"; P.append(S(t, f"{sz}沒有{oz}。", [B(t,'ありません',['ありません','いません','ではありません','あります'],'物品「沒有」用 ありません。'), B(t,'が',*P_GA)], 'ありません・いません'))
            for o,oz in pick(HAVE_ANIM,2):
                t=f"{s} は {o} が いません 。"; P.append(S(t, f"{sz}沒有{oz}。", [B(t,'いません',['いません','ありません','ではありません','います'],'人、動物「沒有」用 いません。')], 'ありません・いません'))
        for w,wz in [('今日|きょう','今天'),('明日|あした','明天')]:
            for o,oz in [('時間|じかん','時間'),('宿題|しゅくだい','功課'),('予定|よてい','計畫')]:
                t=f"{w} は {o} が ありません 。"; P.append(S(t, f"{wz}沒有{oz}。", [B(t,'ありません',['ありません','いません','ではありません','あります'],'物品、事情「沒有」用 ありません。')], 'ありません・いません'))
    elif day==12:
        for o,oz in HAVE_THING+FOOD:
            t=f"{o} が あります か 。 はい 、 あります 。"; P.append(S(t, f"有{oz}嗎？有。", [B(t,'か',*P_KA), B(t,'が',*P_GA)], '〜ありますか'))
            t=f"{o} が あります か 。 いいえ 、 ありません 。"; P.append(S(t, f"有{oz}嗎？沒有。", [B(t,'ありません',['ありません','いません','ちがいます','そうです'],'物品的否定回答：いいえ、ありません。')], '〜ありますか'))
        for s,sz in [('あなた','你')]+SUBJ3[:6]:
            for o,oz in pick(HAVE_ANIM,3):
                ans='はい 、 います 。' if rnd.random()<.5 else 'いいえ 、 いません 。'
                t=f"{s} は {o} が います か 。 {ans}"; P.append(S(t, f"{sz}有{oz}嗎？{'有。' if 'はい' in ans else '沒有。'}", [B(t,'か',*P_KA), B(t,'います' if 'はい' in ans else 'いません',['います','あります','いません','ありません'] if 'はい' in ans else ['いません','ありません','います','あります'],'人、動物用 います／いません。',6)], '〜いますか'))
    elif day==13:
        for o,oz in OBJ:
            for w,wz in pick(OWNERS,3):
                t=f"これ は だれ の {o} です か 。 {w} の です 。"
                P.append(S(t, f"這是誰的{oz}？是{wz}的。", [B(t,'だれ',['だれ','何|なん','どこ','いつ'],'問「誰的」用 だれの。'), B(t,'の',['の','は','が','を'],'「Xの」＝X的（東西）。',idx_of(t,'か'))], 'だれの'))
                t=f"これ は {w} の {o} です 。"; P.append(S(t, f"這是{wz}的{oz}。", [B(t,'の',*P_NO)], 'の'))
            t=f"その {o} は 私|わたし の です 。"; P.append(S(t, f"那個{oz}是我的。", [B(t,'の',['の','は','が','を'],'「私の」＝我的（東西），後面名詞可省略。',3)], 'の'))
    # 去重
    seen=set(); out=[]
    for d in P:
        k=''.join(t for t,_ in d['toks'])
        if k in seen: continue
        seen.add(k); out.append(d)
    rnd.shuffle(out); return out

TOPIC = {1:'私は〜です',2:'〜は〜です（形容詞）',3:'〜人です・〜から来ました',4:'〜ではありません・〜くないです',5:'〜ですか・はい／いいえ',6:'疑問詞 何・どこ・だれ・何歳',7:'第 1 週總複習',
         8:'私の〜・家人稱謂',9:'これ・あれ・〜の',10:'あります・います',11:'ありません・いません',12:'〜がありますか',13:'だれの〜ですか',14:'第 2 週總複習'}

# ---------- 假名 ----------
H = dict(a='あ',i='い',u='う',e='え',o='お',ka='か',ki='き',ku='く',ke='け',ko='こ',sa='さ',shi='し',su='す',se='せ',so='そ',ta='た',chi='ち',tsu='つ',te='て',to='と',
         na='な',ni='に',nu='ぬ',ne='ね',no='の',ha='は',hi='ひ',fu='ふ',he='へ',ho='ほ',ma='ま',mi='み',mu='む',me='め',mo='も',ya='や',yu='ゆ',yo='よ',ra='ら',ri='り',ru='る',re='れ',ro='ろ',wa='わ',wo='を',n='ん',
         ga='が',gi='ぎ',gu='ぐ',ge='げ',go='ご',za='ざ',ji='じ',zu='ず',ze='ぜ',zo='ぞ',da='だ',de='で',do='ど',ba='ば',bi='び',bu='ぶ',be='べ',bo='ぼ',pa='ぱ',pi='ぴ',pu='ぷ',pe='ぺ',po='ぽ',
         kya='きゃ',kyu='きゅ',kyo='きょ',sha='しゃ',shu='しゅ',sho='しょ',cha='ちゃ',chu='ちゅ',cho='ちょ',nya='にゃ',ryo='りょ',gya='ぎゃ',ja='じゃ',ju='じゅ',jo='じょ',hyo='ひょ',myo='みょ')
def kata(s): return ''.join(chr(ord(c)+0x60) if 'ぁ'<=c<='ゖ' else c for c in s)
ROWS = {1:['a','i','u','e','o','ka','ki','ku','ke','ko','sa','shi','su','se','so'],
        2:['ta','chi','tsu','te','to','na','ni','nu','ne','no','ha','hi','fu','he','ho'],
        3:['ma','mi','mu','me','mo','ya','yu','yo','ra','ri','ru','re','ro'],
        4:['wa','wo','n','ga','gi','gu','ge','go','za','ji','zu','ze','zo'],
        5:['da','de','do','ba','bi','bu','be','bo','pa','pi','pu','pe','po'],
        6:['kya','kyu','kyo','sha','shu','sho','cha','chu','cho','nya','ryo','ja','ju','jo']}
ROWS[8]=ROWS[1]; ROWS[9]=ROWS[2]; ROWS[10]=ROWS[3]+['wa','wo','n']; ROWS[11]=ROWS[4][3:]+ROWS[5]; ROWS[12]=ROWS[6]
KATA_WORDS = [('テレビ','terebi','電視'),('コーヒー','kōhī','咖啡'),('パン','pan','麵包'),('バス','basu','公車'),('タクシー','takushī','計程車'),('カメラ','kamera','相機'),('ケーキ','kēki','蛋糕'),('ペン','pen','筆'),
              ('ノート','nōto','筆記本'),('メール','mēru','郵件'),('ホテル','hoteru','飯店'),('レストラン','resutoran','餐廳'),('アメリカ','amerika','美國'),('ジュース','jūsu','果汁'),('シャツ','shatsu','襯衫'),('パソコン','pasokon','電腦')]
def kana_items(day):
    items=[]
    if day in (7,14):
        pool=list(dict.fromkeys(r for d in ((1,2,3,4,5,6) if day==7 else (8,9,10,11,12)) for r in ROWS[d])); sel=pick(pool,15); katak = day==14
    else:
        sel=ROWS.get(day,[]); katak = day>=8
        if day==13:
            for w,ro,z in KATA_WORDS:
                others=[x[1] for x in KATA_WORDS if x[0]!=w]; opts=[ro]+pick(others,3); rnd.shuffle(opts)
                items.append(dict(k=w,a=ro,opts=opts,dir='k2r',zh=z))
            return items
    allr=[r for d in range(1,7) for r in ROWS[d]]
    for r in sel:
        k=H[r]; k = kata(k) if katak else k
        sim=[x for x in sel if x!=r] or allr
        opts=[r]+pick([x for x in sim if x!=r],3); rnd.shuffle(opts)
        items.append(dict(k=k,a=r,opts=opts,dir='k2r'))
        opts2=[k]+[kata(H[x]) if katak else H[x] for x in pick([x for x in sim if x!=r],3)]; rnd.shuffle(opts2)
        items.append(dict(k=r,a=k,opts=opts2,dir='r2k'))
    rnd.shuffle(items); return items

# ---------- 組裝 ----------
def build(day, V, JA_V):
    P = gen(day)
    mc=[]; reorder=[]; listen=[]; speak=[]
    for d in P[:25]:
        bi,opts,why = rnd.choice(d['blanks'])
        ct=d['toks'][bi]; correct=ct[0]
        rd={x.split('|')[0]:(x.split('|')+[''])[1] for x in opts}; rd[correct]=ct[1]
        o=list(dict.fromkeys([x.split('|')[0] for x in opts]))
        for f in ['は','が','を','に','で','も']:
            if len(o)>=4: break
            if f not in o: o.append(f)
        o=o[:4]
        if correct not in o: o[-1]=correct
        rnd.shuffle(o)
        q=[t[:] for t in d['toks']]; q[bi]=None
        mc.append(dict(q=q, opts=[[x,rd.get(x,'')] for x in o], a=o.index(correct), zh=d['zh'], gp=d['gp'], why=why, full=d['toks']))
    short=[d for d in P if 3<=len([t for t in d['toks'] if t[0] not in '、。'])<=9]
    for d in pick(short,15):
        toks=[t for t in d['toks'] if t[0] not in '。']
        bi,opts,_=rnd.choice(d['blanks']); wrong=[x.split('|')[0] for x in opts if x.split('|')[0]!=d['toks'][bi][0]][:1]
        tiles=list(range(len(toks)))
        reorder.append(dict(zh=d['zh'], toks=toks, extra=[[w,''] for w in wrong], gp=d['gp']))
    for d in pick(P,10):
        others=[x['zh'] for x in P if x['zh']!=d['zh']]; opts=[d['zh']]+pick(others,3); rnd.shuffle(opts)
        listen.append(dict(s=d['toks'], opts=opts, a=opts.index(d['zh'])))
    for d in pick(P,10): speak.append(dict(s=d['toks'], zh=d['zh']))
    # 單字
    def vocab_of(dd):
        out=[]
        for w,p,z,e in V.get(dd,[]):
            j=JA_V[w]; t,r=(j.split('|')+[''])[:2]; out.append(dict(w=t,r=r,zh=z,en=w))
        return out
    if day in (7,14):
        pool=[x for dd in range(day-6,day) for x in vocab_of(dd)]; new=pick(pool,15)
        for x in new: x['review']=True
    else:
        new=vocab_of(day)[:15]
    rpool=[x for dd in range(max(1,day-10), day+1 if day<=2 else day) for x in vocab_of(dd)]
    review=[]
    for x in pick(rpool,30):
        others=[y for y in rpool if y['w']!=x['w'] and y['zh']!=x['zh']]
        if rnd.random()<.5:
            o=[x]+pick(others,3); rnd.shuffle(o); review.append(dict(q=[x['w'],x['r']], opts=[y['zh'] for y in o], a=o.index(x), dir='ja2zh'))
        else:
            o=[x]+pick(others,3); rnd.shuffle(o); review.append(dict(q=x['zh'], opts=[[y['w'],y['r']] for y in o], a=o.index(x), dir='zh2ja'))
    return dict(topic=TOPIC[day], blocks=dict(ja_kana=kana_items(day), ja_vocab_new=new, ja_vocab_review=review, ja_mc=mc, ja_reorder=reorder, ja_listen=listen, ja_speaking=speak))
