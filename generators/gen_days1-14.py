# -*- coding: utf-8 -*-
"""Phase 0 Days 1–14 題庫產生器（be 動詞 / 家人與所有格 + have-has）"""
import json, random, itertools
rnd = random.Random(20260830)

# ---------------------------------------------------------------- 字彙（每日 25）
V = {}
V[1] = [('teacher','n.','老師','I am a teacher.'),('student','n.','學生','You are a student.'),('doctor','n.','醫生','I am a doctor.'),
 ('nurse','n.','護理師','You are a nurse.'),('engineer','n.','工程師','I am an engineer.'),('cook','n.','廚師','You are a cook.'),
 ('driver','n.','司機','I am a driver.'),('farmer','n.','農夫','You are a farmer.'),('singer','n.','歌手','I am a singer.'),
 ('worker','n.','工人','You are a worker.'),('boy','n.','男孩','I am a boy.'),('girl','n.','女孩','You are a girl.'),
 ('man','n.','男人','I am a man.'),('woman','n.','女人','You are a woman.'),('friend','n.','朋友','You are my friend.'),
 ('name','n.','名字','My name is Ken.'),('hello','int.','你好','Hello, I am Amy.'),('hi','int.','嗨','Hi! I am Tom.'),
 ('nice','adj.','好的；愉快的','Nice to meet you.'),('meet','v.','見面','Nice to meet you.'),('yes','adv.','是','Yes, I am.'),
 ('no','adv.','不','No, I am not.'),('thank you','phr.','謝謝','Thank you.'),('please','adv.','請','Sit down, please.'),
 ('goodbye','int.','再見','Goodbye, Amy.')]
V[2] = [('happy','adj.','開心的','She is happy.'),('sad','adj.','難過的','He is sad.'),('tired','adj.','累的','My father is tired.'),
 ('busy','adj.','忙碌的','My mother is busy.'),('hungry','adj.','餓的','The cat is hungry.'),('thirsty','adj.','渴的','He is thirsty.'),
 ('hot','adj.','熱的','It is hot today.'),('cold','adj.','冷的','It is cold.'),('tall','adj.','高的','Tom is tall.'),
 ('short','adj.','矮的；短的','Amy is short.'),('old','adj.','老的；舊的','My grandfather is old.'),('young','adj.','年輕的','She is young.'),
 ('late','adj.','遲到的','He is late.'),('early','adj.','早的','She is early.'),('ready','adj.','準備好的','It is ready.'),
 ('sick','adj.','生病的','My brother is sick.'),('angry','adj.','生氣的','The teacher is angry.'),('rich','adj.','有錢的','He is rich.'),
 ('beautiful','adj.','漂亮的','She is beautiful.'),('strong','adj.','強壯的','My father is strong.'),('kind','adj.','親切的','Our teacher is kind.'),
 ('funny','adj.','有趣的','Tom is funny.'),('quiet','adj.','安靜的','The room is quiet.'),('clean','adj.','乾淨的','The kitchen is clean.'),
 ('big','adj.','大的','The house is big.')]
V[3] = [('Taiwan','n.','台灣','I am from Taiwan.'),('Taiwanese','adj./n.','台灣的；台灣人','We are Taiwanese.'),('Japan','n.','日本','She is from Japan.'),
 ('Japanese','adj./n.','日本的；日本人','They are Japanese.'),('Korea','n.','韓國','He is from Korea.'),('Korean','adj./n.','韓國的；韓國人','My friend is Korean.'),
 ('China','n.','中國','They are from China.'),('Chinese','adj./n.','中國的；中國人','He is Chinese.'),('America','n.','美國','Tom is from America.'),
 ('American','adj./n.','美國的；美國人','Tom is American.'),('England','n.','英國','Emma is from England.'),('English','adj./n.','英國的；英語','Emma is English.'),
 ('France','n.','法國','We are from France.'),('French','adj./n.','法國的；法國人','They are French.'),('Australia','n.','澳洲','Jack is from Australia.'),
 ('Australian','adj./n.','澳洲的；澳洲人','Jack is Australian.'),('Canada','n.','加拿大','Lisa is from Canada.'),('Canadian','adj./n.','加拿大的；加拿大人','Lisa is Canadian.'),
 ('Germany','n.','德國','Anna is from Germany.'),('German','adj./n.','德國的；德國人','Anna is German.'),('country','n.','國家','Taiwan is a small country.'),
 ('city','n.','城市','Taipei is a big city.'),('people','n.','人們','They are kind people.'),('children','n.','孩子們','The children are happy.'),
 ('from','prep.','來自','Where are you from?')]
V[4] = [('home','n.','家','I am at home.'),('school','n.','學校','We are at school.'),('office','n.','辦公室','My father is at the office.'),
 ('hospital','n.','醫院','The doctor is in the hospital.'),('park','n.','公園','The children are in the park.'),('shop','n.','商店','She is in the shop.'),
 ('restaurant','n.','餐廳','They are in the restaurant.'),('bank','n.','銀行','He is at the bank.'),('station','n.','車站','We are at the station.'),
 ('library','n.','圖書館','Amy is in the library.'),('room','n.','房間','The room is clean.'),('kitchen','n.','廚房','My mother is in the kitchen.'),
 ('bathroom','n.','浴室','Tom is in the bathroom.'),('garden','n.','花園','The garden is beautiful.'),('car','n.','汽車','The car is new.'),
 ('bus','n.','公車','We are on the bus.'),('train','n.','火車','They are on the train.'),('bike','n.','腳踏車','My bike is old.'),
 ('phone','n.','手機','My phone is new.'),('computer','n.','電腦','The computer is old.'),('book','n.','書','This book is good.'),
 ('bag','n.','包包','My bag is big.'),('pen','n.','筆','The pen is red.'),('desk','n.','書桌','The desk is clean.'),('chair','n.','椅子','The chair is small.')]
V[5] = [('cat','n.','貓','Is the cat hungry?'),('dog','n.','狗','The dog is big.'),('bird','n.','鳥','Is it a bird?'),('fish','n.','魚','The fish is small.'),
 ('rabbit','n.','兔子','The rabbit is white.'),('today','adv.','今天','Are you busy today?'),('now','adv.','現在','Is he at home now?'),
 ('tomorrow','adv.','明天','Is tomorrow Monday?'),('morning','n.','早上','Good morning!'),('afternoon','n.','下午','Good afternoon!'),
 ('evening','n.','晚上','Good evening!'),('night','n.','夜晚','Good night!'),('Monday','n.','星期一','Today is Monday.'),('Tuesday','n.','星期二','Tomorrow is Tuesday.'),
 ('Wednesday','n.','星期三','Is today Wednesday?'),('Thursday','n.','星期四','Today is Thursday.'),('Friday','n.','星期五','Is it Friday?'),
 ('Saturday','n.','星期六','Saturday is my favorite day.'),('Sunday','n.','星期日','Is tomorrow Sunday?'),('week','n.','星期；週','A week is seven days.'),
 ('day','n.','天；日子','It is a good day.'),('birthday','n.','生日','Is today your birthday?'),('party','n.','派對','Is the party tomorrow?'),
 ('weekend','n.','週末','Are you free on the weekend?'),('fine','adj.','好的；不錯的','I am fine, thank you.')]
V[6] = [('what','pron.','什麼','What is your name?'),('where','adv.','哪裡','Where are you?'),('who','pron.','誰','Who is he?'),('how','adv.','如何；多麼','How old are you?'),
 ('age','n.','年齡','What is your age?'),('year','n.','年','I am ten years old.'),('one','num.','一','I have one brother.'),('two','num.','二','Two students are late.'),
 ('three','num.','三','She is three years old.'),('four','num.','四','Four people are here.'),('five','num.','五','It is five now.'),('six','num.','六','He is six years old.'),
 ('seven','num.','七','A week is seven days.'),('eight','num.','八','My sister is eight.'),('nine','num.','九','I am nine years old.'),('ten','num.','十','Ten children are in the park.'),
 ('eleven','num.','十一','Tom is eleven.'),('twelve','num.','十二','Amy is twelve years old.'),('fifteen','num.','十五','He is fifteen.'),('eighteen','num.','十八','She is eighteen.'),
 ('twenty','num.','二十','I am twenty years old.'),('question','n.','問題','It is a good question.'),('answer','n.','答案','What is the answer?'),
 ('class','n.','班級；課','Who is in your class?'),('job','n.','工作','What is your job?')]
V[8] = [('father','n.','爸爸','My father is a driver.'),('mother','n.','媽媽','My mother is a nurse.'),('dad','n.','爸爸（口語）','My dad is tall.'),
 ('mom','n.','媽媽（口語）','My mom is kind.'),('brother','n.','兄弟','My brother is ten.'),('sister','n.','姊妹','Your sister is beautiful.'),
 ('grandfather','n.','祖父','My grandfather is old.'),('grandmother','n.','祖母','My grandmother is kind.'),('aunt','n.','阿姨；姑姑','My aunt is a teacher.'),
 ('uncle','n.','叔叔；舅舅','My uncle is a cook.'),('cousin','n.','表／堂兄弟姊妹','My cousin is twelve.'),('son','n.','兒子','Your son is funny.'),
 ('daughter','n.','女兒','My daughter is a student.'),('parents','n.','父母','My parents are teachers.'),('grandparents','n.','祖父母','My grandparents are old.'),
 ('family','n.','家人；家庭','My family is big.'),('husband','n.','丈夫','My husband is an engineer.'),('wife','n.','太太','Your wife is kind.'),
 ('baby','n.','寶寶','The baby is small.'),('kid','n.','小孩','My kid is five.'),('twins','n.','雙胞胎','My sisters are twins.'),
 ('older','adj.','年長的','My older brother is tall.'),('younger','adj.','年幼的','My younger sister is nine.'),('photo','n.','照片','This is my family photo.'),
 ('house','n.','房子','My house is small.')]
V[9] = [('key','n.','鑰匙','This is his key.'),('wallet','n.','錢包','That is her wallet.'),('watch','n.','手錶','His watch is new.'),
 ('hat','n.','帽子','Her hat is red.'),('shirt','n.','襯衫','His shirt is blue.'),('shoes','n.','鞋子','Their shoes are clean.'),
 ('umbrella','n.','雨傘','This is our umbrella.'),('cup','n.','杯子','Her cup is big.'),('bottle','n.','瓶子','This is its bottle.'),
 ('box','n.','盒子','Their box is small.'),('ball','n.','球','This is our ball.'),('toy','n.','玩具','This is his toy.'),
 ('camera','n.','相機','Her camera is old.'),('glasses','n.','眼鏡','His glasses are new.'),('ring','n.','戒指','Her ring is beautiful.'),
 ('jacket','n.','外套','This is my jacket.'),('bed','n.','床','Our bed is big.'),('clock','n.','時鐘','Their clock is old.'),
 ('lamp','n.','檯燈','This is her lamp.'),('picture','n.','圖片','This is our picture.'),('this','pron.','這','This is my key.'),
 ('that','pron.','那','That is her bag.'),('its','det.','它的','The dog is hungry. Its bowl is empty.'),('our','det.','我們的','Our house is big.'),
 ('their','det.','他們的','Their car is new.')]
V[10] = [('red','adj.','紅色的','I have a red bag.'),('blue','adj.','藍色的','She has blue eyes.'),('green','adj.','綠色的','He has a green hat.'),
 ('yellow','adj.','黃色的','We have a yellow car.'),('black','adj.','黑色的','My cat has black eyes.'),('white','adj.','白色的','I have a white shirt.'),
 ('pink','adj.','粉紅色的','My sister has a pink phone.'),('brown','adj.','棕色的','She has brown hair.'),('orange','adj.','橘色的','He has an orange ball.'),
 ('purple','adj.','紫色的','Amy has a purple umbrella.'),('hair','n.','頭髮','She has long hair.'),('eyes','n.','眼睛','He has big eyes.'),
 ('face','n.','臉','The baby has a small face.'),('nose','n.','鼻子','He has a big nose.'),('mouth','n.','嘴巴','She has a small mouth.'),
 ('hand','n.','手','I have two hands.'),('leg','n.','腿','A dog has four legs.'),('arm','n.','手臂','He has strong arms.'),
 ('head','n.','頭','The cat has a small head.'),('foot','n.','腳','I have two feet.'),('long','adj.','長的','My mother has long hair.'),
 ('curly','adj.','捲的','Tom has curly hair.'),('straight','adj.','直的','Amy has straight hair.'),('dark','adj.','深色的','We have dark hair.'),
 ('pretty','adj.','漂亮的','She has pretty eyes.')]
V[11] = [('money','n.','錢','I don\'t have money.'),('time','n.','時間','She doesn\'t have time.'),('ticket','n.','票','He doesn\'t have a ticket.'),
 ('pet','n.','寵物','We don\'t have a pet.'),('motorbike','n.','機車','My brother doesn\'t have a motorbike.'),('laptop','n.','筆電','I don\'t have a laptop.'),
 ('tablet','n.','平板','They don\'t have a tablet.'),('headphones','n.','耳機','He doesn\'t have headphones.'),('notebook','n.','筆記本','I don\'t have a notebook.'),
 ('pencil','n.','鉛筆','She doesn\'t have a pencil.'),('eraser','n.','橡皮擦','Tom doesn\'t have an eraser.'),('ruler','n.','尺','We don\'t have a ruler.'),
 ('map','n.','地圖','They don\'t have a map.'),('dictionary','n.','字典','I don\'t have a dictionary.'),('letter','n.','信','She doesn\'t have a letter.'),
 ('card','n.','卡片','He doesn\'t have a card.'),('gift','n.','禮物','I don\'t have a gift.'),('plan','n.','計畫','We don\'t have a plan.'),
 ('idea','n.','想法','I don\'t have an idea.'),('problem','n.','問題（麻煩）','She doesn\'t have a problem.'),('homework','n.','功課','We don\'t have homework today.'),
 ('lunch','n.','午餐','He doesn\'t have lunch.'),('breakfast','n.','早餐','I don\'t have breakfast.'),('dinner','n.','晚餐','They don\'t have dinner at home.'),
 ('any','det.','任何','I don\'t have any money.')]
V[12] = [('water','n.','水','Do you have water?'),('tea','n.','茶','Does she have tea?'),('coffee','n.','咖啡','Do you have coffee?'),
 ('milk','n.','牛奶','Does he have milk?'),('juice','n.','果汁','Do they have juice?'),('bread','n.','麵包','Do we have bread?'),
 ('rice','n.','飯','Does she have rice?'),('egg','n.','蛋','Do you have eggs?'),('apple','n.','蘋果','Does Tom have an apple?'),
 ('banana','n.','香蕉','Do you have a banana?'),('cake','n.','蛋糕','Does Amy have a cake?'),('cookie','n.','餅乾','Do you have cookies?'),
 ('pizza','n.','披薩','Do they have pizza?'),('hamburger','n.','漢堡','Does he have a hamburger?'),('noodles','n.','麵','Do you have noodles?'),
 ('chicken','n.','雞肉','Does she have chicken?'),('meat','n.','肉','Do we have meat?'),('soup','n.','湯','Do you have soup?'),
 ('salad','n.','沙拉','Does he have salad?'),('sugar','n.','糖','Do you have sugar?'),('salt','n.','鹽','Do we have salt?'),
 ('fruit','n.','水果','Does she have fruit?'),('vegetable','n.','蔬菜','Do they have vegetables?'),('food','n.','食物','Do you have food?'),
 ('drink','n.','飲料','Does he have a drink?')]
V[13] = [('neighbor','n.','鄰居','This is my neighbor\'s dog.'),('boss','n.','老闆','That is my boss\'s car.'),('classmate','n.','同學','This is my classmate\'s pen.'),
 ('roommate','n.','室友','That is my roommate\'s bike.'),('girlfriend','n.','女朋友','This is Tom\'s girlfriend.'),('boyfriend','n.','男朋友','That is Amy\'s boyfriend.'),
 ('whose','pron.','誰的','Whose bag is this?'),('mine','pron.','我的（東西）','This bag is mine.'),('yours','pron.','你的（東西）','Is this pen yours?'),
 ('hers','pron.','她的（東西）','The hat is hers.'),('ours','pron.','我們的（東西）','The house is ours.'),('theirs','pron.','他們的（東西）','The car is theirs.'),
 ('horse','n.','馬','This is my uncle\'s horse.'),('cow','n.','牛','That is the farmer\'s cow.'),('pig','n.','豬','The pig is big.'),
 ('sheep','n.','羊','The sheep is white.'),('duck','n.','鴨子','This is Ken\'s duck.'),('mouse','n.','老鼠','The mouse is small.'),
 ('elephant','n.','大象','The elephant is big.'),('lion','n.','獅子','The lion is strong.'),('tiger','n.','老虎','The tiger is beautiful.'),
 ('monkey','n.','猴子','The monkey is funny.'),('owner','n.','主人','Who is the owner?'),('thing','n.','東西','Whose thing is this?'),
 ('bowl','n.','碗','This is the cat\'s bowl.')]

# ---------------------------------------------------------------- 主詞
def S(en, zh, p, pron, pzh, poss, posszh):
    be = {'1s':'am','2':'are','3s':'is','1p':'are','3p':'are'}[p]
    neg = {'1s':['am','not'],'2':["aren't"],'3s':["isn't"],'1p':["aren't"],'3p':["aren't"]}[p]
    return dict(en=en, zh=zh, p=p, be=be, beq=be.capitalize(), neg=neg, pron=pron, pzh=pzh,
                have='has' if p=='3s' else 'have', do='does' if p=='3s' else 'do', dont="doesn't" if p=='3s' else "don't",
                poss=poss, posszh=posszh)
SUBJ = {
 'I': S('I','我','1s','I','我','my','我的'), 'You': S('You','你','2','you','你','your','你的'),
 'He': S('He','他','3s','he','他','his','他的'), 'She': S('She','她','3s','she','她','her','她的'), 'It': S('It','它','3s','it','它','its','它的'),
 'We': S('We','我們','1p','we','我們','our','我們的'), 'They': S('They','他們','3p','they','他們','their','他們的'),
}
NAMES_M = ['Tom','Ken','Leo','Ben','Jack','Mark','Kai']; NAMES_F = ['Amy','Mei','Anna','Emma','Lisa','Yu','Lin']
for n in NAMES_M: SUBJ[n] = S(n, n, '3s','he','他','his','他的')
for n in NAMES_F: SUBJ[n] = S(n, n, '3s','she','她','her','她的')
NOUN_SG = [('My father','我爸爸','he'),('My mother','我媽媽','she'),('My brother','我哥哥','he'),('My sister','我姊姊','she'),('My friend','我的朋友','he'),
           ('My teacher','我的老師','she'),('The cat','這隻貓','it'),('The dog','這隻狗','it'),('My grandfather','我爺爺','he'),('My aunt','我阿姨','she')]
for en,zh,pr in NOUN_SG:
    SUBJ[en] = S(en, zh, '3s', pr, {'he':'他','she':'她','it':'它'}[pr], {'he':'his','she':'her','it':'its'}[pr], {'he':'他的','she':'她的','it':'它的'}[pr])
NOUN_PL = [('My parents','我的父母'),('My friends','我的朋友們'),('The children','孩子們'),('Tom and Amy','Tom 和 Amy'),('My sisters','我的姊妹們'),('The students','學生們')]
for en,zh in NOUN_PL: SUBJ[en] = S(en, zh, '3p','they','他們','their','他們的')

def mid(s):
    en=s['en']
    if en=='I': return 'I'
    if en.split(' ')[0] in ('You','He','She','It','We','They','My','The'): return en[0].lower()+en[1:]
    return en
def ntok(s): return len(s['en'].split(' '))
def zj(a,b):
    return a+(' ' if a and a[-1].isascii() and a[-1].isalpha() else '')+b
AGES_ADULT = [('thirty years old','三十歲'),('forty years old','四十歲'),('forty-five years old','四十五歲')]
AGES_ELDER = [('sixty years old','六十歲'),('seventy years old','七十歲'),('eighty years old','八十歲')]
def ages_for(en):
    e=en.lower()
    if any(k in e for k in ('grand',)): return AGES_ELDER
    if any(k in e for k in ('father','mother','aunt','uncle','husband','wife','teacher','parents')): return AGES_ADULT
    return AGES
def jobs_for(en):
    e=en.lower()
    if any(k in e for k in ('brother','sister','cousin','son','daughter','kid','children','students')): return [JOBS[1]]
    if 'baby' in e: return []
    if 'grand' in e: return [j for j in JOBS if j[0] in ('a farmer','a teacher','a cook','a doctor')]
    return [j for j in JOBS if j[0]!='a student'] if any(k in e for k in ('father','mother','aunt','uncle','husband','wife','parents')) else JOBS
# ---------------------------------------------------------------- 補語（be）
JOBS = [('a teacher','teachers','老師'),('a student','students','學生'),('a doctor','doctors','醫生'),('a nurse','nurses','護理師'),('an engineer','engineers','工程師'),
        ('a cook','cooks','廚師'),('a driver','drivers','司機'),('a farmer','farmers','農夫'),('a singer','singers','歌手'),('a worker','workers','工人')]
ROLES = [('a boy','boys','男孩'),('a girl','girls','女孩'),('a man','men','男人'),('a woman','women','女人'),('my friend','my friends','我的朋友')]
NATS = [('Taiwanese','台灣人'),('Japanese','日本人'),('Korean','韓國人'),('Chinese','中國人'),('American','美國人'),('English','英國人'),('French','法國人'),('Australian','澳洲人'),('Canadian','加拿大人'),('German','德國人')]
FROM = [('Taiwan','台灣'),('Japan','日本'),('Korea','韓國'),('China','中國'),('America','美國'),('England','英國'),('France','法國'),('Australia','澳洲'),('Canada','加拿大'),('Germany','德國')]
ADJ = [('happy','很開心','不開心','開心'),('sad','很難過','不難過','難過'),('tired','很累','不累','累'),('busy','很忙','不忙','忙'),('hungry','餓了','不餓','餓'),
       ('thirsty','渴了','不渴','渴'),('tall','很高','不高','高'),('short','很矮','不矮','矮'),('old','很老','不老','老'),('young','很年輕','不年輕','年輕'),
       ('late','遲到了','沒有遲到','遲到了'),('early','很早','不早','早'),('ready','準備好了','還沒準備好','準備好了'),('sick','生病了','沒有生病','生病了'),
       ('angry','很生氣','不生氣','生氣'),('rich','很有錢','不有錢','有錢'),('beautiful','很漂亮','不漂亮','漂亮'),('strong','很強壯','不強壯','強壯'),
       ('kind','很親切','不親切','親切'),('funny','很有趣','不有趣','有趣'),('quiet','很安靜','不安靜','安靜'),('free','有空','沒空','有空'),('fine','很好','不太好','好')]
THING_ADJ = [('big','很大','不大','大'),('small','很小','不小','小'),('new','是新的','不是新的','是新的'),('old','很舊','不舊','舊'),('clean','很乾淨','不乾淨','乾淨'),('beautiful','很漂亮','不漂亮','漂亮')]
MOOD_ADJ = [a for a in ADJ if a[0] in ('happy','sad','tired','busy','hungry','thirsty','sick','angry','fine')]
TRAIT_ADJ = [a for a in ADJ if a[0] in ('kind','funny','quiet','tall','strong','rich','young','old','beautiful')]
PLACES = [('at home','在家'),('at school','在學校'),('at the office','在辦公室'),('in the hospital','在醫院'),('in the park','在公園'),('in the shop','在商店'),
          ('in the restaurant','在餐廳'),('at the bank','在銀行'),('at the station','在車站'),('in the library','在圖書館'),('in the room','在房間'),
          ('in the kitchen','在廚房'),('in the bathroom','在浴室'),('in the garden','在花園'),('in the car','在車上'),('on the bus','在公車上'),('on the train','在火車上')]
AGES = [('eight years old','八歲'),('ten years old','十歲'),('twelve years old','十二歲'),('fifteen years old','十五歲'),('eighteen years old','十八歲'),('twenty years old','二十歲')]
THINGS = [('My phone','我的手機'),('The car','這台車'),('The room','這個房間'),('My bag','我的包包'),('The kitchen','廚房'),('The book','這本書'),('The bus','公車'),('My bike','我的腳踏車'),('The garden','花園'),('The computer','電腦')]
for en,zh in THINGS: SUBJ[en] = S(en, zh, '3s','it','它','its','它的')

def comp(kind, item, plural):
    """回傳 (en, aff_zh, neg_zh, q_zh)；zh 皆為「主詞之後」的謂語。"""
    if kind=='job':
        en = item[1] if plural else item[0]; z=item[2]; return en, f'是{z}', f'不是{z}', f'是{z}嗎'
    if kind=='nat': return item[0], f'是{item[1]}', f'不是{item[1]}', f'是{item[1]}嗎'
    if kind=='from': return 'from '+item[0], f'來自{item[1]}', f'不是來自{item[1]}', f'來自{item[1]}嗎'
    if kind=='adj': return item[0], item[1], item[2], item[3]+'嗎'
    if kind=='place': return item[0], item[1], '不'+item[1], item[1]+'嗎'
    if kind=='age': return item[0], item[1], '不是'+item[1], item[1]+'嗎'
    if kind=='name': return item, f'是 {item}', f'不是 {item}', f'是 {item} 嗎'

PERSON_WHY = {'1s':'I 搭配 am。','2':'you 搭配 are。','3s':'第三人稱單數（he / she / it 或單數名詞）用 is。','1p':'we 搭配 are。','3p':'複數主詞用 are。'}

def opts_for(cat, correct):
    pools = {
      'be':['am','is','are','be'], 'beq':['Am','Is','Are','Do'], 'neg':["isn't","aren't","don't","not"],
      'have':['have','has','is','are'], 'dont':["don't","doesn't","isn't","aren't"], 'doq':['Do','Does','Is','Are'],
      'sa_be':['am','is','are','do'], 'sa_do':['do','does','have','has'], 'sa_neg':["isn't","aren't","doesn't","don't"],
      'wh':['What','Where','Who','How'],
    }
    if cat in pools:
        p=[o for o in pools[cat] if o!=correct]; rnd.shuffle(p); o=p[:3]+[correct]; rnd.shuffle(o); return o
    if cat=='poss':
        pool=['my','your','his','her','its','our','their','me','him','he','she','they']
        base=[x for x in ['my','your','his','her','its','our','their'] if x!=correct.lower()]
        extra=[x for x in ['me','him','he','she','them','I'] if x!=correct.lower()]
        o=rnd.sample(base,2)+[rnd.choice(extra)]
        if correct[0].isupper(): o=[x.capitalize() for x in o]
        o.append(correct); rnd.shuffle(o); return o
    if cat=='pos_s':
        base=correct[:-2]; o=[base, base+'s', base+' is', correct]; rnd.shuffle(o); return o
    if cat=='whose':
        o=['Whose','Who','What','Where']; return o

def blank(sentence, idx):
    t=sentence.split(' '); core=t[idx].rstrip('.,?!'); punct=t[idx][len(core):]
    return ' '.join(t[:idx]+['___'+punct]+t[idx+1:]), core, punct

def err(sentence, idx, wrong):
    t=sentence.split(' '); core=t[idx].rstrip('.,?!'); punct=t[idx][len(core):]
    t2=t[:]; t2[idx]=wrong+punct; return ' '.join(t2), core

# ---------------------------------------------------------------- 句子產生器：每個句子 = dict(en, zh, idx, cat, correct, gp, why, wrongs)
def be_aff(s, kind, item, prefix=''):
    plural = s['p'] in ('1p','3p')
    en_c, az, nz, qz = comp(kind, item, plural)
    if prefix:
        en = f"{prefix}{mid(s)} {s['be']} {en_c}."; zh = '你好，'+zj(s['zh'],az)+'。'; idx = 1+ntok(s)
    else:
        en = f"{s['en']} {s['be']} {en_c}."; zh = zj(s['zh'],az)+'。'; idx = ntok(s)
    return dict(en=en, zh=zh, idx=idx, cat='be', correct=s['be'], gp='be 動詞', why=PERSON_WHY[s['p']],
                wrongs=[x for x in ['am','is','are'] if x!=s['be']])
def be_neg(s, kind, item):
    plural = s['p'] in ('1p','3p'); en_c, az, nz, qz = comp(kind, item, plural)
    en = f"{s['en']} {' '.join(s['neg'])} {en_c}."
    if s['p']=='1s':
        return dict(en=en, zh=zj(s['zh'],nz)+'。', idx=1, cat='be', correct='am', gp='be 動詞', why='I 的否定是 am not，沒有縮寫 amn\'t。', wrongs=['is','are'])
    return dict(en=en, zh=zj(s['zh'],nz)+'。', idx=ntok(s), cat='neg', correct=s['neg'][0], gp='be 動詞', why=PERSON_WHY[s['p']].replace('用 is','用 isn\'t').replace('搭配 are','搭配 aren\'t').replace('用 are','用 aren\'t'),
                wrongs=[x for x in ["isn't","aren't"] if x!=s['neg'][0]]+["not"])
def be_q(s, kind, item):
    plural = s['p'] in ('1p','3p'); en_c, az, nz, qz = comp(kind, item, plural)
    en = f"{s['beq']} {mid(s)} {en_c}?"
    return dict(en=en, zh=zj(s['zh'],qz)+'？', idx=0, cat='beq', correct=s['beq'], gp='be 動詞', why='be 動詞問句把 '+s['be']+' 放到句首。', wrongs=[x for x in ['Am','Is','Are'] if x!=s['beq']]+['Do'])
def be_sa(s, kind, item, yes):
    q = be_q(s, kind, item)
    a_s = SUBJ['I'] if s['en']=='You' else s
    pron, pzh = a_s['pron'], a_s['pzh']
    if s['en']=='You': pron, pzh = 'I', '我'
    be = {'I':'am','you':'are','he':'is','she':'is','it':'is','we':'are','they':'are'}[pron]
    if yes:
        en = f"{q['en']} Yes, {pron} {be}."; zh = f"{q['zh']} 是的，{pzh}是。"
        idx = len(q['en'].split(' '))+2
        return dict(en=en, zh=zh, idx=idx, cat='sa_be', correct=be, gp='be 動詞', why=f'簡答用 {pron} + {be}。', wrongs=[x for x in ['am','is','are'] if x!=be])
    neg = "am not" if pron=='I' else ("isn't" if be=='is' else "aren't")
    en = f"{q['en']} No, {pron} {neg}."; zh = f"{q['zh']} 不，{pzh}不是。"
    idx = len(q['en'].split(' '))+2
    if pron=='I': return dict(en=en, zh=zh, idx=idx, cat='sa_be', correct='am', gp='be 動詞', why='簡答用 I am not。', wrongs=['is','are'])
    return dict(en=en, zh=zh, idx=idx, cat='sa_neg', correct=neg, gp='be 動詞', why=f'否定簡答用 {pron} {neg}。', wrongs=[x for x in ["isn't","aren't"] if x!=neg]+["not"])
def wh_where(s):
    en = f"Where {s['be']} {mid(s)}?"
    return dict(en=en, zh=zj(s['zh'],'在哪裡？'), idx=0, cat='wh', correct='Where', gp='be 動詞', why='問地點用 Where。', wrongs=['What','Who'])
def wh_from(s):
    en = f"Where {s['be']} {mid(s)} from?"
    return dict(en=en, zh=zj(s['zh'],'來自哪裡？'), idx=1, cat='be', correct=s['be'], gp='be 動詞', why=PERSON_WHY[s['p']], wrongs=[x for x in ['am','is','are'] if x!=s['be']])
def wh_age(s):
    en = f"How old {s['be']} {mid(s)}?"
    return dict(en=en, zh=zj(s['zh'],'幾歲？'), idx=0, cat='wh', correct='How', gp='be 動詞', why='問年齡用 How old。', wrongs=['What','Where'])
def wh_who(s):
    en = f"Who {s['be']} {mid(s)}?"
    return dict(en=en, zh=zj(s['zh'],'是誰？'), idx=0, cat='wh', correct='Who', gp='be 動詞', why='問人用 Who。', wrongs=['What','Where'])
def wh_name(s):
    en = f"What is {s['poss']} name?"
    return dict(en=en, zh=f"{s['posszh']}名字是什麼？", idx=0, cat='wh', correct='What', gp='be 動詞', why='問名字用 What。', wrongs=['Who','Where'])
def wh_name_be(s):
    en = f"What is {s['poss']} name?"
    return dict(en=en, zh=f"{s['posszh']}名字是什麼？", idx=1, cat='be', correct='is', gp='be 動詞', why='name 是單數名詞，用 is。', wrongs=['am','are'])

FAM_SG = [('father','爸爸','he'),('mother','媽媽','she'),('brother','哥哥','he'),('sister','姊姊','she'),('grandfather','爺爺','he'),('grandmother','奶奶','she'),
          ('aunt','阿姨','she'),('uncle','叔叔','he'),('cousin','表哥','he'),('son','兒子','he'),('daughter','女兒','she'),('husband','丈夫','he'),('wife','太太','she'),('baby','寶寶','it')]
FAM_PL = [('parents','父母'),('grandparents','祖父母'),('brothers','兄弟'),('sisters','姊妹'),('children','孩子')]
OBJ = [('key','鑰匙'),('wallet','錢包'),('watch','手錶'),('hat','帽子'),('shirt','襯衫'),('umbrella','雨傘'),('cup','杯子'),('bottle','瓶子'),('box','盒子'),('ball','球'),
       ('toy','玩具'),('camera','相機'),('ring','戒指'),('jacket','外套'),('bed','床'),('clock','時鐘'),('lamp','檯燈'),('picture','圖片'),('house','房子'),('photo','照片'),
       ('phone','手機'),('bag','包包'),('book','書'),('pen','筆'),('car','車'),('bike','腳踏車'),('dog','狗'),('cat','貓')]
POSS_LIST = [('my','我的'),('your','你的'),('his','他的'),('her','她的'),('its','它的'),('our','我們的'),('their','他們的')]

def poss_fam_be(poss, fam, kind, item):
    """My father is a doctor. / Your sisters are tall."""
    pen,pzh = poss
    if len(fam)==3:
        fen,fzh,pr = fam; s=S(f"{pen.capitalize()} {fen}", f"{pzh}{fzh}", '3s', pr, '', '', '')
    else:
        fen,fzh = fam; s=S(f"{pen.capitalize()} {fen}", f"{pzh}{fzh}", '3p','they','','','')
    d = be_aff(s, kind, item)
    return d
def poss_fam_blank(poss, fam, kind, item):
    d = poss_fam_be(poss, fam, kind, item)
    d.update(idx=0, cat='poss', correct=poss[0].capitalize(), gp='所有格', why=f'「{poss[1]}」的所有格是 {poss[0]}，放在名詞前。',
             wrongs=[x for x in ['My','Your','His','Her','Our','Their'] if x!=poss[0].capitalize()][:2]+[{'my':'I','your':'you','his':'he','her':'she','its':'it','our':'we','their':'they'}[poss[0]].capitalize()])
    return d
def this_is_poss(poss, obj, this='This'):
    pen,pzh = poss; oen,ozh = obj
    en = f"{this} is {pen} {oen}."; zh = f"{'這' if this=='This' else '那'}是{pzh}{ozh}。"
    return dict(en=en, zh=zh, idx=2, cat='poss', correct=pen, gp='所有格', why=f'「{pzh}」的所有格是 {pen}，放在名詞前。',
                wrongs=[x for x in ['my','your','his','her','our','their'] if x!=pen][:2]+[{'my':'me','your':'you','his':'him','her':'she','its':'it','our':'us','their':'them'}[pen]])
def poss_obj_adj(poss, obj, adj):
    pen,pzh = poss; oen,ozh = obj
    plural = oen in ('shoes','glasses')
    be = 'are' if plural else 'is'
    en = f"{pen.capitalize()} {oen} {be} {adj[0]}."; zh = f"{pzh}{ozh}{adj[1]}。"
    return dict(en=en, zh=zh, idx=0, cat='poss', correct=pen.capitalize(), gp='所有格', why=f'「{pzh}」的所有格是 {pen}。',
                wrongs=[x for x in ['My','Your','His','Her','Our','Their'] if x!=pen.capitalize()][:2]+[{'my':'I','your':'You','his':'He','her':'She','its':'It','our':'We','their':'They'}[pen]])

HAVE_OBJ = [('a car','一台車'),('a bike','一台腳踏車'),('a phone','一支手機'),('a computer','一台電腦'),('a book','一本書'),('a bag','一個包包'),('a pen','一支筆'),
            ('a dog','一隻狗'),('a cat','一隻貓'),('two cats','兩隻貓'),('three books','三本書'),('a big house','一間大房子'),('a small car','一台小車'),
            ('a new phone','一支新手機'),('two brothers','兩個哥哥'),('a sister','一個姊姊'),('a red bag','一個紅色的包包'),('long hair','長頭髮'),('blue eyes','藍色的眼睛'),
            ('a key','一把鑰匙'),('a watch','一支手錶'),('an umbrella','一把雨傘'),('a camera','一台相機'),('money','錢'),('time','時間'),('a job','工作'),
            ('a ticket','一張票'),('a pet','寵物'),('a laptop','一台筆電'),('homework','功課'),('a map','一張地圖'),('a gift','一份禮物'),('water','水'),
            ('coffee','咖啡'),('an apple','一顆蘋果'),('bread','麵包'),('milk','牛奶'),('a cake','一個蛋糕'),('rice','飯'),('eggs','蛋'),('a big family','一個大家庭'),
            ('curly hair','捲髮'),('a green hat','一頂綠色的帽子'),('a black cat','一隻黑貓'),('two children','兩個孩子'),('a baby','一個寶寶'),('a motorbike','一台機車'),
            ('a dictionary','一本字典'),('a plan','一個計畫'),('a question','一個問題'),('tea','茶'),('juice','果汁'),('a banana','一根香蕉'),('cookies','餅乾'),('pizza','披薩')]
HAVE_WHY = {'3s':'第三人稱單數（he / she / it 或單數名詞）用 has。'}
def have_aff(s, obj):
    en = f"{s['en']} {s['have']} {obj[0]}."; zh = zj(s['zh'],f"有{obj[1]}。")
    return dict(en=en, zh=zh, idx=ntok(s), cat='have', correct=s['have'], gp='have-has', why=HAVE_WHY.get(s['p'], f"{s['pron']} 搭配 have。"), wrongs=['has' if s['have']=='have' else 'have', s['be']])
def have_neg(s, obj):
    en = f"{s['en']} {s['dont']} have {obj[0]}."; zh = zj(s['zh'],f"沒有{obj[1]}。")
    return dict(en=en, zh=zh, idx=ntok(s), cat='dont', correct=s['dont'], gp='have-has', why=("第三人稱單數否定用 doesn't have（have 用原形）。" if s['p']=='3s' else f"{s['pron']} 的否定用 don't have。"),
                wrongs=["doesn't" if s['dont']=="don't" else "don't", "isn't" if s['p']=='3s' else "aren't"])
def have_neg_bare(s, obj):
    d = have_neg(s, obj); d.update(idx=ntok(s)+1, cat='have', correct='have', why="don't / doesn't 後面的動詞用原形 have。", wrongs=['has','had']); return d
def have_q(s, obj):
    en = f"{s['do'].capitalize()} {mid(s)} have {obj[0]}?"; zh = zj(s['zh'],f"有{obj[1]}嗎？")
    return dict(en=en, zh=zh, idx=0, cat='doq', correct=s['do'].capitalize(), gp='have-has', why=("第三人稱單數問句用 Does，動詞用原形 have。" if s['p']=='3s' else f"{s['pron']} 的問句用 Do。"),
                wrongs=['Does' if s['do']=='do' else 'Do', s['beq']])
def have_sa(s, obj, yes):
    q = have_q(s, obj)
    pron, pzh = ('I','我') if s['en']=='You' else (s['pron'], s['pzh'])
    do = 'does' if pron in ('he','she','it') else 'do'
    idx = len(q['en'].split(' '))+2
    if yes:
        return dict(en=f"{q['en']} Yes, {pron} {do}.", zh=f"{q['zh']} 是的，{pzh}有。", idx=idx, cat='sa_do', correct=do, gp='have-has', why=f'簡答用 {pron} {do}，不用 have/has。', wrongs=['has' if do=='does' else 'have', 'do' if do=='does' else 'does'])
    dont = "doesn't" if do=='does' else "don't"
    return dict(en=f"{q['en']} No, {pron} {dont}.", zh=f"{q['zh']} 不，{pzh}沒有。", idx=idx, cat='sa_neg', correct=dont, gp='have-has', why=f'否定簡答用 {pron} {dont}。', wrongs=["don't" if dont=="doesn't" else "doesn't", "isn't"])

OWNERS = [('Tom','Tom'),('Amy','Amy'),('Ken','Ken'),('Mei','Mei'),('Lisa','Lisa'),('Jack','Jack'),('my father','我爸爸'),('my mother','我媽媽'),('my sister','我姊姊'),
          ('my brother','我哥哥'),('my uncle','我叔叔'),('my aunt','我阿姨'),('my neighbor','我鄰居'),('my boss','我老闆'),('my classmate','我同學'),('my roommate','我室友'),('the teacher','老師'),('the farmer','農夫')]
def pos_s_this(owner, obj, this='This'):
    oen,ozh = owner; ten,tzh = obj
    en = f"{this} is {oen}'s {ten}."; zh = f"{'這' if this=='This' else '那'}是"+zj(ozh,f"的{tzh}。")
    idx = 2 if ' ' not in oen else 3
    return dict(en=en, zh=zh, idx=idx, cat='pos_s', correct=oen.split(' ')[-1]+"'s", gp='所有格', why='名詞＋’s 表示「…的」。', wrongs=[oen.split(' ')[-1], oen.split(' ')[-1]+'s'])
def pos_s_be(owner, obj, adj):
    oen,ozh = owner; ten,tzh = obj
    plural = ten in ('shoes','glasses'); be='are' if plural else 'is'
    en = f"{oen[0].upper()+oen[1:]}'s {ten} {be} {adj[0]}."; zh = zj(ozh,f"的{tzh}{adj[1]}。")
    idx = 0 if ' ' not in oen else 1
    return dict(en=en, zh=zh, idx=idx, cat='pos_s', correct=en.split(' ')[idx], gp='所有格', why='名詞＋’s 表示「…的」。', wrongs=[en.split(' ')[idx][:-2], en.split(' ')[idx][:-2]+'s'])
def whose(owner, obj):
    oen,ozh = owner; ten,tzh = obj
    en = f"Whose {ten} is this? It's {oen}'s."; zh = f"這是誰的{tzh}？是"+zj(ozh,'的。')
    return dict(en=en, zh=zh, idx=0, cat='whose', correct='Whose', gp='所有格', why='問「誰的」用 Whose。', wrongs=['Who','What'])

# ---------------------------------------------------------------- 每日結構配置
def pick(lst, n): return rnd.sample(lst, min(n, len(lst)))
def subj(*names): return [SUBJ[n] for n in names]
Q_SUBJ = ['You','He','She','Tom','Amy','Ken','Mei','My father','My mother','My friend','The cat','They','My parents','The children','Tom and Amy','My friends']
ALL_SUBJ = ['I','You','He','She','It','We','They','Tom','Amy','Ken','Mei','Leo','Anna','My father','My mother','My brother','My sister','My friend','My teacher','The cat','The dog','My parents','My friends','The children','Tom and Amy','My sisters','The students']

def gen_day_sentences(day):
    P = []  # 候選句
    if day==1:
        for sn in ['I','You']:
            s=SUBJ[sn]
            for j in JOBS: P.append(be_aff(s,'job',j)); P.append(be_aff(s,'job',j,'Hello, '))
            for r in ROLES: P.append(be_aff(s,'job',r))
            for a in [x for x in ADJ if x[0] in ('happy','tired','hungry','busy','fine','ready','late')]: P.append(be_aff(s,'adj',a))
            for n in NAMES_M+NAMES_F: P.append(be_aff(s,'name',n))
        for n in NAMES_M+NAMES_F:
            P.append(dict(en=f"My name is {n}.", zh=f"我的名字是 {n}。", idx=2, cat='be', correct='is', gp='be 動詞', why='name 是單數名詞，用 is。', wrongs=['am','are']))
    elif day==2:
        for sn in ['He','She','It','Tom','Amy','Ken','Mei','My father','My mother','My brother','My sister','My teacher','The cat','The dog']:
            s=SUBJ[sn]
            for a in ADJ: 
                if sn in ('It','The cat','The dog') and a[0] in ('rich','kind','funny','late','early','ready','free','fine','sad','busy'): continue
                P.append(be_aff(s,'adj',a))
            if sn not in ('It','The cat','The dog'):
                for j in jobs_for(sn): P.append(be_aff(s,'job',j))
        for tn,tz in THINGS:
            for a in THING_ADJ+[('hot','很熱','不熱','熱'),('cold','很冷','不冷','冷')]: P.append(be_aff(SUBJ[tn],'adj',a))
    elif day==3:
        for sn in ['We','They','My parents','My friends','The children','Tom and Amy','My sisters','The students']:
            s=SUBJ[sn]
            for j in jobs_for(sn): P.append(be_aff(s,'job',j))
            for n in NATS: P.append(be_aff(s,'nat',n))
            for f in FROM: P.append(be_aff(s,'from',f))
            for a in pick(ADJ,10): P.append(be_aff(s,'adj',a))
        for sn in ['I','You','He','She','Tom','Amy','My father','My friend']:
            s=SUBJ[sn]
            for n in NATS: P.append(be_aff(s,'nat',n))
            for f in FROM: P.append(be_aff(s,'from',f))
    elif day==4:
        for sn in ALL_SUBJ:
            s=SUBJ[sn]; thing = sn in ('It','The cat','The dog')
            kinds = [('place',p) for p in PLACES] if not sn.startswith('My teacher') else []
            if not thing:
                kinds += [('job',j) for j in pick(jobs_for(sn),4)] + [('adj',a) for a in pick(ADJ,6)] + [('from',f) for f in pick(FROM,3)]
            else:
                kinds += [('adj',a) for a in pick(THING_ADJ,5)]
            for k,i in kinds: P.append(be_neg(s,k,i)); 
            for k,i in pick(kinds,6): P.append(be_aff(s,k,i))
        for tn,tz in THINGS:
            for a in THING_ADJ: P.append(be_neg(SUBJ[tn],'adj',a))
    elif day==5:
        for sn in Q_SUBJ:
            s=SUBJ[sn]; thing = sn in ('The cat',)
            kinds = [('place',p) for p in pick(PLACES,6)] + ([] if thing else [('job',j) for j in pick(jobs_for(sn),4)] + [('adj',a) for a in pick(ADJ,6)] + [('from',f) for f in pick(FROM,3)])
            for k,i in kinds:
                P.append(be_q(s,k,i)); P.append(be_sa(s,k,i, rnd.random()<0.5))
        for tn,tz in THINGS:
            for a in pick(THING_ADJ,4): P.append(be_q(SUBJ[tn],'adj',a)); P.append(be_sa(SUBJ[tn],'adj',a, rnd.random()<0.5))
    elif day==6:
        for sn in Q_SUBJ+['It','My brother','My sister','Leo','Anna']:
            s=SUBJ[sn]
            P.append(wh_where(s)); P.append(wh_from(s)); P.append(wh_age(s))
            if s['p']=='3s' and sn not in ('The cat','It'): P.append(wh_who(s))
            if sn in ('You','He','She','They','Tom','Amy'): P.append(wh_name(s)); P.append(wh_name_be(s))
        for sn in ['You','He','She','Tom','Amy','They','My father','My sister']:
            s=SUBJ[sn]
            for a in pick(ages_for(sn),3): P.append(be_aff(s,'age',a)); P.append(be_q(s,'age',a))
            for p in pick(PLACES,4):
                d=be_aff(s,'place',p); d['en']=f"Where {s['be']} {mid(s)}? {s['pron'].capitalize() if s['en']!='You' else 'I'} {'am' if s['en']=='You' else s['be']} {p[0]}."
                d['zh']=zj(s['zh'],f"在哪裡？{'我' if s['en']=='You' else s['pzh']}{p[1]}。"); d['idx']=1; P.append(d)
    elif day==7:
        for d in (1,2,3,4,5,6): P += pick(gen_day_sentences(d), 45)
    elif day==8:
        for pen,pzh in POSS_LIST[:2]:
            for fam in FAM_SG:
                adjs = MOOD_ADJ if fam[0]=='baby' else ADJ
                kinds = [('job',j) for j in pick(jobs_for(fam[0]),3)]+[('adj',a) for a in pick(adjs,4)]+([] if fam[0]=='baby' else [('age',a) for a in pick(ages_for(fam[0]),2)])
                for k,i in kinds:
                    P.append(poss_fam_be((pen,pzh),fam,k,i)); P.append(poss_fam_blank((pen,pzh),fam,k,i))
            for fam in FAM_PL:
                for k,i in [('job',j) for j in pick(jobs_for(fam[0]),2)]+[('adj',a) for a in pick(ADJ,3)]:
                    P.append(poss_fam_be((pen,pzh),fam,k,i)); P.append(poss_fam_blank((pen,pzh),fam,k,i))
            for fam in FAM_SG: P.append(this_is_poss((pen,pzh),(fam[0],fam[1]), rnd.choice(['This','That'])))
    elif day==9:
        for pen,pzh in POSS_LIST[2:]:
            for obj in OBJ:
                P.append(this_is_poss((pen,pzh),obj, rnd.choice(['This','That'])))
                P.append(poss_obj_adj((pen,pzh),obj, rnd.choice(THING_ADJ)))
            if pen!='its':
                for fam in pick([f for f in FAM_SG if f[0]!='baby'],6):
                    for k,i in [('job',rnd.choice(jobs_for(fam[0]))),('adj',rnd.choice(ADJ))]:
                        P.append(poss_fam_blank((pen,pzh),fam,k,i))
    elif day==10:
        for sn in ALL_SUBJ:
            for obj in pick(HAVE_OBJ,10): P.append(have_aff(SUBJ[sn],obj))
    elif day==11:
        for sn in ALL_SUBJ:
            for obj in pick(HAVE_OBJ,8): P.append(have_neg(SUBJ[sn],obj)); P.append(have_neg_bare(SUBJ[sn],obj))
            for obj in pick(HAVE_OBJ,3): P.append(have_aff(SUBJ[sn],obj))
    elif day==12:
        for sn in Q_SUBJ:
            for obj in pick(HAVE_OBJ,8): P.append(have_q(SUBJ[sn],obj)); P.append(have_sa(SUBJ[sn],obj, rnd.random()<0.5))
    elif day==13:
        for own in OWNERS:
            for obj in pick(OBJ,5): P.append(pos_s_this(own,obj, rnd.choice(['This','That']))); P.append(pos_s_be(own,obj, rnd.choice(THING_ADJ)))
            for obj in pick(OBJ,2): P.append(whose(own,obj))
    elif day==14:
        for d in (8,9,10,11,12,13): P += pick(gen_day_sentences(d), 45)
        for d in (2,4,5): P += pick(gen_day_sentences(d), 12)
    # 去重
    seen=set(); out=[]
    for d in P:
        if d['en'] in seen: continue
        seen.add(d['en']); out.append(d)
    rnd.shuffle(out); return out

# ---------------------------------------------------------------- 閱讀短文
CITIES = [('Taipei','台北'),('Tokyo','東京'),('Seoul','首爾'),('London','倫敦'),('Sydney','雪梨'),('New York','紐約'),('Paris','巴黎'),('Berlin','柏林'),('Taichung','台中'),('Toronto','多倫多')]
def reading_week1(i):
    n = rnd.choice(NAMES_M+NAMES_F); he = 'He' if n in NAMES_M else 'She'
    f = rnd.choice([x for x in NAMES_M+NAMES_F if x!=n]); fhe = 'He' if f in NAMES_M else 'She'
    job = rnd.choice(JOBS); age = rnd.choice(AGES if job[0]=='a student' else AGES_ADULT); country = rnd.choice(FROM); adj = rnd.choice(MOOD_ADJ)
    fjob = rnd.choice([j for j in JOBS if j!=job]); fadj = rnd.choice(TRAIT_ADJ); city = rnd.choice(CITIES)
    place = rnd.choice([('in the park','在公園'),('at school','在學校'),('in a restaurant','在餐廳'),('at home','在家'),('in the library','在圖書館')])
    text = (f"Hello! My name is {n}. I am {age[0]}. I am from {country[0]}. I am {job[0]}. I am {adj[0]} today. "
            f"My friend is {f}. {fhe} is {fjob[0]}. {fhe} is {fadj[0]}. {fhe} is not from {country[0]}. We are in {city[0]} now. We are {place[0]}.")
    def mc(q, correct, pool, fmt=lambda x:x):
        opts=[fmt(correct)]+[fmt(x) for x in pick([p for p in pool if p!=correct],3)]; rnd.shuffle(opts); return dict(q=q, opts=opts, a=opts.index(fmt(correct)))
    qs = [mc(f"How old is {n}?", age, AGES, lambda x:x[0].replace(' years old','')),
          mc(f"Where is {n} from?", country, FROM, lambda x:x[0]),
          mc(f"What is {n}'s job?", job, JOBS, lambda x:x[0][2:] if x[0].startswith('a ') else x[0][3:]),
          mc(f"Who is {f}?", f"{n}'s friend", [f"{n}'s friend", f"{n}'s brother", f"{n}'s sister", f"{n}'s teacher", f"{n}'s father"]),
          mc(f"Where are {n} and {f} now?", city, CITIES, lambda x:x[0]),
          mc(f"How is {n} today?", adj, MOOD_ADJ, lambda x:x[0]),
          mc(f"Is {f} from {country[0]}?", 'No', ['No','Yes','We don\'t know','Maybe'])]
    rnd.shuffle(qs); return dict(title=f"{n} and {f}", text=text, qs=qs[:5])
def reading_week2(i):
    fn = rnd.choice(NAMES_M); mn = rnd.choice(NAMES_F); bn = rnd.choice([x for x in NAMES_M if x!=fn]); sn = rnd.choice([x for x in NAMES_F if x!=mn])
    AJ=[x for x in JOBS if x[0]!='a student']; fjob = rnd.choice(AJ); mjob = rnd.choice([x for x in AJ if x!=fjob]); k = rnd.choice([1,2,3]); j = rnd.choice([1,2])
    bage = rnd.choice(AGES); pet = rnd.choice([('dog','狗'),('cat','貓'),('rabbit','兔子'),('bird','鳥')]); pn = rnd.choice(['Coco','Momo','Bobo','Lucky','Mimi','Max'])
    city = rnd.choice(CITIES); adj = rnd.choice(THING_ADJ); color = rnd.choice(['red','blue','green','white','black','yellow'])
    text = (f"This is my family. My father is {fjob[0]}. His name is {fn}. My mother is {mjob[0]}. Her name is {mn}. "
            f"I have {['one','two','three'][k-1]} brother{'s' if k>1 else ''} and {['one','two'][j-1]} sister{'s' if j>1 else ''}. My older brother's name is {bn}. He is {bage[0]}. "
            f"My sister {sn} has long hair. We have a {pet[0]}. Its name is {pn}. It has {color} eyes. Our house is in {city[0]}. It is {adj[0]}. I don't have a car, but my father has one.")
    def mc(q, correct, pool, fmt=lambda x:x):
        opts=[fmt(correct)]+[fmt(x) for x in pick([p for p in pool if p!=correct],3)]; rnd.shuffle(opts); return dict(q=q, opts=opts, a=opts.index(fmt(correct)))
    qs = [mc("What is the father's job?", fjob, JOBS, lambda x:x[0][2:] if x[0].startswith('a ') else x[0][3:]),
          mc("What is the mother's name?", mn, NAMES_F),
          mc("How many sisters does the writer have?", j, [1,2,3,4], lambda x:str(x)),
          mc(f"How old is {bn}?", bage, AGES, lambda x:x[0].replace(' years old','')),
          mc(f"What is the {pet[0]}'s name?", pn, ['Coco','Momo','Bobo','Lucky','Mimi','Max']),
          mc("Where is their house?", city, CITIES, lambda x:x[0]),
          mc("Who has a car?", 'The father', ['The father','The writer','The mother','The brother']),
          mc(f"What color are the {pet[0]}'s eyes?", color, ['red','blue','green','white','black','yellow'])]
    rnd.shuffle(qs); return dict(title=f"{fn}'s family", text=text, qs=qs[:5])

# ---------------------------------------------------------------- 口說 & 寫作（每日手寫）
SPEAK = {
 1:[("Say hello and your name.","Hello! My name is Alex."),("Say: I am a student.","I am a student."),("Tell me your job.","I am an engineer."),("Say: Nice to meet you.","Nice to meet you."),
    ("Say goodbye to Amy.","Goodbye, Amy."),("Say: You are my friend.","You are my friend."),("Say: I am a man. You are a woman.","I am a man. You are a woman."),("Say thank you.","Thank you very much.")],
 2:[("How is your mother today?","My mother is busy today."),("Describe your father.","My father is tall and strong."),("Say: He is tired.","He is tired."),("Is your room clean? Say it.","My room is clean."),
    ("Describe your friend.","My friend is funny and kind."),("Say: It is hot today.","It is hot today."),("Say: She is a doctor. She is busy.","She is a doctor. She is busy."),("Describe the cat.","The cat is small and hungry.")],
 3:[("Where are you from?","I am from Taiwan."),("Say: We are Taiwanese.","We are Taiwanese."),("Talk about two friends.","Tom and Amy are my friends. They are students."),("Say: They are from Japan.","They are from Japan."),
    ("Say: My parents are teachers.","My parents are teachers."),("Say: The children are happy.","The children are happy."),("Talk about a country.","Japan is a beautiful country."),("Say: We are in a big city.","We are in a big city.")],
 4:[("Where are you now?","I am at home now."),("Say: I am not tired.","I am not tired."),("Say: My phone is not new.","My phone is not new."),("Say: They aren't at school.","They aren't at school."),
    ("Talk about your mother.","My mother is in the kitchen. She isn't busy."),("Say: The car is not clean.","The car is not clean."),("Say: We are on the bus.","We are on the bus."),("Say: He isn't a doctor. He is a nurse.","He isn't a doctor. He is a nurse.")],
 5:[("Ask: Are you a student?","Are you a student?"),("Answer: Yes, I am.","Yes, I am."),("Ask: Is Tom at home?","Is Tom at home?"),("Answer: No, he isn't.","No, he isn't."),
    ("Ask if the cat is hungry.","Is the cat hungry?"),("Ask if they are from Korea.","Are they from Korea?"),("Say: Today is Monday.","Today is Monday."),("Ask: Is today your birthday?","Is today your birthday?")],
 6:[("Ask: What is your name?","What is your name?"),("Ask: How old are you?","How old are you?"),("Answer: I am twenty years old.","I am twenty years old."),("Ask: Where is she?","Where is she?"),
    ("Ask: Who is he?","Who is he?"),("Answer: He is my teacher.","He is my teacher."),("Ask: Where are you from?","Where are you from?"),("Ask: What is her job?","What is her job?")],
 7:[("Introduce yourself in three sentences.","Hi, my name is Alex. I am from Taiwan. I am an engineer."),("Describe your family in two sentences.","My father is a driver. My mother is a nurse."),
    ("Ask a friend three questions.","Where are you from? How old are you? Are you a student?"),("Say: I am not a teacher. I am a student.","I am not a teacher. I am a student."),
    ("Say where you are now.","I am at home now."),("Describe the weather.","It is hot today."),("Say: My friends are kind.","My friends are kind."),("Answer: Yes, they are.","Yes, they are.")],
 8:[("Talk about your father.","My father is a driver. He is tall."),("Talk about your mother.","My mother is a teacher. She is kind."),("Say: My family is big.","My family is big."),("Say: This is my sister.","This is my sister."),
    ("Say: My parents are busy.","My parents are busy."),("Say: Your brother is funny.","Your brother is funny."),("Say: My grandmother is old.","My grandmother is old."),("Say: This is my family photo.","This is my family photo.")],
 9:[("Say: This is his key.","This is his key."),("Say: Her hat is red.","Her hat is red."),("Say: Our house is big.","Our house is big."),("Say: Their car is new.","Their car is new."),
    ("Say: That is her bag.","That is her bag."),("Talk about a friend's thing.","This is Tom's phone. His phone is new."),("Say: Its name is Coco.","Its name is Coco."),("Say: Our teacher is kind.","Our teacher is kind.")],
 10:[("Say: I have a phone.","I have a phone."),("Say: She has long hair.","She has long hair."),("Talk about your family.","I have one brother and one sister."),("Say: My father has a car.","My father has a car."),
     ("Describe your eyes and hair.","I have black hair and brown eyes."),("Say: We have a dog.","We have a dog."),("Say: They have two cats.","They have two cats."),("Say: He has a big house.","He has a big house.")],
 11:[("Say: I don't have a car.","I don't have a car."),("Say: She doesn't have time.","She doesn't have time."),("Say: We don't have a pet.","We don't have a pet."),("Say: He doesn't have a ticket.","He doesn't have a ticket."),
     ("Talk about something you don't have.","I don't have a laptop."),("Say: They don't have homework today.","They don't have homework today."),("Say: My brother doesn't have a bike.","My brother doesn't have a bike."),("Say: I don't have any money.","I don't have any money.")],
 12:[("Ask: Do you have a pen?","Do you have a pen?"),("Answer: Yes, I do.","Yes, I do."),("Ask: Does she have a cat?","Does she have a cat?"),("Answer: No, she doesn't.","No, she doesn't."),
     ("Ask if Tom has an apple.","Does Tom have an apple?"),("Ask if they have water.","Do they have water?"),("Ask: Do you have coffee?","Do you have coffee?"),("Answer: No, I don't. I have tea.","No, I don't. I have tea.")],
 13:[("Say: This is Tom's bag.","This is Tom's bag."),("Ask: Whose car is this?","Whose car is this?"),("Answer: It's my father's.","It's my father's."),("Say: Amy's brother is a doctor.","Amy's brother is a doctor."),
     ("Say: This bag is mine.","This bag is mine."),("Ask: Is this pen yours?","Is this pen yours?"),("Say: The house is theirs.","The house is theirs."),("Say: This is my neighbor's dog.","This is my neighbor's dog.")],
 14:[("Introduce your family in four sentences.","I have a small family. My father is an engineer. My mother is a teacher. We have a dog."),("Say what you have and don't have.","I have a phone, but I don't have a car."),
     ("Ask a friend two questions with have.","Do you have a pet? Does your sister have a bike?"),("Say: This is my brother's room.","This is my brother's room."),("Say: Her hair is long and black.","Her hair is long and black."),
     ("Answer: Yes, he does.","Yes, he does."),("Say: Our house isn't big.","Our house isn't big."),("Ask: Whose phone is this?","Whose phone is this?")],
}
WRITE = {
 1:[("用兩句話介紹自己（名字、職業）。例：I am ... / I am a ...",8,"Hello! My name is Alex. I am an engineer."),("寫兩句話介紹你的朋友（用 You are ...）。",8,"You are Amy. You are my friend."),("寫一段打招呼的對話（Hello / Nice to meet you / Goodbye）。",8,"Hello, I am Ken. Nice to meet you. Goodbye!"),("寫出三種職業，每個用一句「I am a ...」。",9,"I am a teacher. I am a cook. I am a driver.")],
 2:[("用三句話描述你的爸爸或媽媽（用 He/She is + 形容詞）。",12,"My mother is a nurse. She is busy. She is kind."),("描述今天的天氣和你的心情（用 It is ... / I am ...）。",8,"It is hot today. I am tired."),("描述一隻動物（用 It is ...）。",9,"It is a cat. It is small. It is hungry."),("用三個形容詞寫三句話描述你的朋友。",12,"Tom is my friend. He is tall. He is funny.")],
 3:[("寫三句話：你來自哪裡、你是哪國人、你住的城市。",12,"I am from Taiwan. I am Taiwanese. Taipei is a big city."),("寫兩句話描述兩個朋友（用 They are ...）。",10,"Tom and Amy are my friends. They are students."),("寫一段介紹你的家人（用 We are ...）。",10,"We are a big family. We are from Taichung."),("寫三個國家和他們的人（用 ... are from ...）。",12,"Ken is from Japan. Emma and Jack are from England. They are English.")],
 4:[("寫三句否定句描述自己（I am not ...）。",12,"I am not a teacher. I am not tired. I am not at school."),("描述你現在在哪裡、家人在哪裡（用 at / in / on）。",12,"I am at home. My father is at the office. My mother is in the kitchen."),("用兩句話描述你的手機或腳踏車（用 is / isn't）。",10,"My phone is old. It isn't new."),("寫三句話：某人「不是」什麼（用 isn't / aren't）。",12,"Tom isn't a doctor. My friends aren't at home. The car isn't clean.")],
 5:[("寫三個 Yes/No 問句問朋友，並寫出簡答。",18,"Are you a student? Yes, I am. Is your father a doctor? No, he isn't. Are you busy today? Yes, I am."),("寫出今天是星期幾、明天是星期幾，並問一個問題。",12,"Today is Monday. Tomorrow is Tuesday. Is it your birthday tomorrow?"),("寫一段小對話（問一個問題、回答、再問一個）。",15,"Is the cat hungry? Yes, it is. Is it your cat? No, it isn't."),("問三個關於動物的問題（Is it ...?）。",12,"Is it a dog? Is it big? Is it hungry?")],
 6:[("用 What / Where / How old 寫三個問題並回答。",20,"What is your name? My name is Alex. Where are you from? I am from Taiwan. How old are you? I am twenty."),("寫一段自我介紹，包含年齡（I am ... years old）。",12,"My name is Alex. I am twenty years old. I am from Taipei."),("問你朋友的姓名、年齡和來自哪裡。",12,"What is your name? How old are you? Where are you from?"),("寫出你班上三個人的名字和他們是誰（Who is ...?）。",15,"Who is Tom? He is my friend. Who is Amy? She is my teacher.")],
 7:[("總複習：用六句話介紹自己（名字、年齡、國家、職業、心情、地點）。",25,"My name is Alex. I am twenty years old. I am from Taiwan. I am an engineer. I am happy today. I am at home now."),("寫一段對話：兩個人第一次見面（至少三個問句）。",25,"Hello! What is your name? My name is Amy. Where are you from? I am from Japan. Are you a student? Yes, I am."),("用五句話描述你的家人（用 is / are / isn't / aren't）。",20,"My father is a driver. My mother is a nurse. They are busy. My brother isn't tall. My sisters are students."),("寫三句話：今天、明天、週末。",12,"Today is Saturday. Tomorrow is Sunday. I am free on the weekend.")],
 8:[("用 my 寫四句話介紹家人（My father is ...）。",16,"My father is a cook. My mother is a teacher. My brother is ten. My sister is a student."),("寫三句話用 your 問或描述朋友的家人。",12,"Your mother is kind. Your brother is funny. Your family is big."),("寫一段「這是我的家庭照」的介紹（This is my ...）。",15,"This is my family photo. This is my father. This is my mother. This is my little sister."),("描述你的祖父母（My grandfather / grandmother ...）。",12,"My grandfather is old. My grandmother is kind. They are at home.")],
 9:[("用 his / her 各寫兩句話描述朋友的東西。",16,"This is Tom's hat. His hat is red. This is Amy's bag. Her bag is big."),("用 our / their 寫三句話（房子、老師、車）。",12,"Our house is small. Our teacher is kind. Their car is new."),("描述一隻寵物和它的東西（用 its）。",12,"This is my dog. Its name is Coco. Its ball is yellow."),("寫四句話：This is ... / That is ... + 所有格。",16,"This is my key. That is his wallet. This is her watch. That is their umbrella.")],
 10:[("用 have / has 寫四句話介紹你的家人有什麼。",16,"I have a phone. My father has a car. My mother has long hair. We have two cats."),("描述你自己的外表（hair / eyes）。",12,"I have short black hair. I have brown eyes. I have a small nose."),("描述一位朋友的外表和他的東西。",15,"Amy has long curly hair. She has blue eyes. She has a red bag."),("寫三句話用顏色描述東西（have + 顏色 + 名詞）。",12,"I have a blue shirt. He has a green hat. They have a white car.")],
 11:[("寫三句話說你「沒有」什麼（I don't have ...）。",12,"I don't have a car. I don't have a pet. I don't have time today."),("用 doesn't have 寫三句話描述家人。",15,"My brother doesn't have a bike. My mother doesn't have a laptop. My father doesn't have time."),("寫兩句有、兩句沒有（have / don't have）。",16,"I have a phone, but I don't have a tablet. We have a dog, but we don't have a cat."),("描述今天沒有的東西（homework / money / plan ...）。",12,"I don't have homework today. I don't have a plan. I don't have any money.")],
 12:[("寫三個 Do / Does 問句並回答。",18,"Do you have a pen? Yes, I do. Does she have a cat? No, she doesn't. Do they have water? Yes, they do."),("寫一段在餐廳的對話（Do you have ...?）。",15,"Do you have coffee? Yes, we do. Do you have cake? No, we don't. We have cookies."),("問三個關於食物的問題（Do / Does）。",12,"Do you have bread? Does he have rice? Do they have juice?"),("寫一段對話問朋友有沒有寵物。",15,"Do you have a pet? Yes, I do. I have a dog. Does your sister have a pet? No, she doesn't.")],
 13:[("用 's 寫四句話（Tom's / my father's ...）。",16,"This is Tom's bag. That is my father's car. Amy's brother is a doctor. My sister's hair is long."),("寫兩個 Whose 問句並回答。",12,"Whose phone is this? It's mine. Whose hat is that? It's Amy's."),("用 mine / yours / hers / theirs 各寫一句。",16,"This pen is mine. Is this book yours? The hat is hers. The house is theirs."),("描述鄰居或同學的東西（my neighbor's ...）。",12,"This is my neighbor's dog. Its name is Max. My classmate's bike is new.")],
 14:[("總複習：用六句話介紹你的家人（用 have/has、所有格、's）。",30,"I have a small family. My father is a driver. His car is old. My mother has long hair. Her name is Mei. This is my brother's room."),("寫一段對話問朋友的家人（Do / Does / Whose）。",25,"Do you have a brother? Yes, I do. Does he have a car? No, he doesn't. Whose bike is this? It's my sister's."),("描述你有和沒有的東西，各三句。",24,"I have a phone. I have a laptop. I have a dog. I don't have a car. I don't have a tablet. I don't have a cat."),("用 our / their / its 寫五句話描述你家和寵物。",20,"Our house is in Taipei. It is small. We have a cat. Its name is Momo. Its eyes are green. Their house is big.")],
}
TOPIC = {1:'be 動詞：I am / You are',2:'be 動詞：He / She / It is',3:'be 動詞：We / They are',4:'be 動詞否定句',5:'be 動詞問句與簡答',6:'Wh- 問句',7:'第 1 週總複習',
         8:'家人與 my / your',9:'his / her / its / our / their',10:'have / has',11:"don't / doesn't have",12:'Do / Does … have?',13:"名詞 ’s 與 Whose",14:'第 2 週總複習'}

# ---------------------------------------------------------------- 組裝每天
def vocab_new_for(day):
    if day in (7,14):
        pool=[]; 
        for d in range(day-6, day): pool += V[d]
        return [dict(w=w,pos=p,zh=z,ex=e,review=True) for w,p,z,e in pick(pool,25)]
    return [dict(w=w,pos=p,zh=z,ex=e) for w,p,z,e in V[day]]
def vocab_review_for(day):
    pool=[]
    for d in range(max(1,day-10), day+1 if day<=3 else day):
        if d in V: pool += V[d]
    items=[]
    for w,p,z,e in pick(pool, 60):
        others=[x for x in pool if x[0]!=w and x[2]!=z]
        if rnd.random()<0.5:
            opts=[w]+[x[0] for x in pick(others,3)]; rnd.shuffle(opts); items.append(dict(q=z,a=w,opts=opts,dir='zh2en'))
        else:
            opts=[z]+[x[2] for x in pick(others,3)]; rnd.shuffle(opts); items.append(dict(q=w,a=z,opts=opts,dir='en2zh'))
    return items

def build_day(day, used_mc, used_fill):
    P = gen_day_sentences(day)
    mc=[]; fill=[]; errs=[]; trans=[]; reorder=[]; dict_=[]
    # MC：優先用本週還沒用過的句子
    fresh=[d for d in P if d['en'] not in used_mc]
    for d in fresh[:50]:
        q,core,punct = blank(d['en'], d['idx']); opts=opts_for(d['cat'], d['correct'])
        if core not in opts: opts[-1]=core
        mc.append(dict(q=q, opts=opts, a=opts.index(core), gp=d['gp'], why=d['why'])); used_mc.add(d['en'])
    fresh=[d for d in P if d['en'] not in used_fill]
    rnd.shuffle(fresh)
    for d in fresh[:50]:
        q,core,punct = blank(d['en'], d['idx'])
        hint = {'be':'am / is / are','beq':'Am / Is / Are','neg':"isn't / aren't",'have':'have / has','dont':"don't / doesn't",'doq':'Do / Does','sa_be':'am / is / are','sa_do':'do / does','sa_neg':"isn't / aren't / don't / doesn't",'wh':'What / Where / Who / How','poss':'my / your / his / her / its / our / their','pos_s':"名詞＋'s",'whose':'Whose'}[d['cat']]
        fill.append(dict(q=q, a=[core], hint=hint, gp=d['gp'], why=d['why'])); used_fill.add(d['en'])
    for d in pick(P, 15):
        w = rnd.choice(d['wrongs']); s,core = err(d['en'], d['idx'], w)
        errs.append(dict(s=s, wrong=d['idx'], fix=core, gp=d['gp'], why=d['why']))
    for d in pick(P, 20): trans.append(dict(zh=d['zh'], a=[d['en']], gp=d['gp']))
    short=[d for d in P if 3<=len(d['en'].split(' '))<=6 and '?' not in d['en'][:-1]]
    for d in pick(short, 15):
        words=d['en'].split(' '); sh=words[:]
        for _ in range(10):
            rnd.shuffle(sh)
            if sh!=words: break
        reorder.append(dict(words=sh, a=d['en']))
    mid=[d for d in P if 4<=len(d['en'].split(' '))<=8 and ' Yes,' not in d['en'] and ' No,' not in d['en']]
    for d in pick(mid, 10): dict_.append(dict(s=d['en']))
    week = 1 if day<=7 else 2
    reading=[(reading_week1 if week==1 else reading_week2)(i) for i in range(4)]
    speaking=[dict(prompt=p, model=m) for p,m in SPEAK[day]] + [dict(prompt='Read aloud: '+d['en'], model=d['en']) for d in pick(mid,12)]
    writing=[dict(prompt=p, minWords=n, sample=s) for p,n,s in WRITE[day]]
    return dict(week=week, dayOfWeek=((day-1)%7)+1, topic=TOPIC[day], review=day in (7,14),
                blocks=dict(vocab_new=vocab_new_for(day), vocab_review=vocab_review_for(day), mc=mc, fill=fill, translate=trans, error=errs, reorder=reorder,
                            reading=reading, dictation=dict_, speaking=speaking, writing=writing))

# ---------------------------------------------------------------- 檢測題庫
def test_items(days, n):
    P=[]
    for d in days: P += gen_day_sentences(d)
    seen=set(); out=[]
    for d in P:
        if d['en'] in seen: continue
        seen.add(d['en']); out.append(d)
    rnd.shuffle(out); items=[]
    for d in out[:n]:
        q,core,punct = blank(d['en'], d['idx']); opts=opts_for(d['cat'], d['correct'])
        if core not in opts: opts[-1]=core
        items.append(dict(type='mc', q=q, opts=opts, a=opts.index(core), gp=d['gp']))
    return items

DATA = dict(meta=dict(day1='2026-08-30', days=56, version='days1-14 v1'), days={}, tests={})
used_mc=set(); used_fill=set()
for day in range(1,15):
    if day in (1,8): used_mc=set(); used_fill=set()
    DATA['days'][str(day)] = build_day(day, used_mc, used_fill)
DATA['tests'] = dict(
    diagnostic=dict(items=test_items([1,2,3,4,5,6], 35)),
    weekly={'1':dict(items=test_items([1,2,3,4,5,6], 25)), '2':dict(items=test_items([8,9,10,11,12,13], 25))},
    final=dict(items=[]), retention=dict(pool=[dict(w=w,zh=z,learnedDay=d) for d in V for w,p,z,e in V[d]]),
    cefr=dict(a1=['能用簡單句自我介紹（名字、年齡、國家、職業）','能描述家人與朋友','能問答 Yes/No 問題','能用 Wh- 問句問基本資訊','能說出自己有／沒有的東西','能聽懂慢速的簡單句子','能讀懂 5–8 句的短文','能寫 3–5 句的簡短自我介紹','能用所有格描述物品歸屬','能用正確的 be 動詞與 have/has'], a2=[])
)
import re
def fixzh(o):
    if isinstance(o,dict): return {k:(fixzh(v) if k!='en' else v) for k,v in o.items()}
    if isinstance(o,list): return [fixzh(v) for v in o]
    if isinstance(o,str) and re.search(r'[\u4e00-\u9fff]',o):
        o=re.sub(r'([\u4e00-\u9fff，。？！、（）])([A-Za-z])', r'\1 \2', o); o=re.sub(r'([A-Za-z])([\u4e00-\u9fff])', r'\1 \2', o)
        o=re.sub(r'([A-Za-z]) ([，。？！、])', r'\1\2', o)
        return o
    return o
for d in DATA['days'].values():
    for k in ('translate','vocab_review','vocab_new','writing','speaking','mc','fill','error'):
        d['blocks'][k]=fixzh(d['blocks'][k])
json.dump(DATA, open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','data','phase0-days1-14.json'),'w',encoding='utf-8'), ensure_ascii=False)

# 統計
for day in range(1,15):
    b=DATA['days'][str(day)]['blocks']
    print(day, {k:len(v) for k,v in b.items()})
print('total mc', sum(len(DATA['days'][str(d)]['blocks']['mc']) for d in range(1,15)))
