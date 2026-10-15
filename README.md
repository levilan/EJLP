# 英日雙語練習包（Phase 0）

手機優先的英文 A1 + 日文 N5 自學練習頁。單一 HTML 檔，題庫已內建，不需要伺服器或安裝。

**直接使用**：手機打開 **https://levilan.github.io/EJLP/** ，加入主畫面即可。也可以直接開 `index.html`。

## 功能

**每日練習（Day 1–14）**
- 英文每天 11 個區塊、約 240 題：新字、單字複習、選擇、填空、中譯英、改錯、重組、閱讀、聽寫、口說、寫作
- 日文每天 7 個區塊、約 130 題：假名、新字、單字複習、文法選擇、中譯日拼句、聽力、口說
- 英日文法同日對應（be 動詞 ↔ 〜は〜です、所有格 ↔ の、have/has ↔ あります／います）
- 檢測：入門診斷、週檢測（≥80% 進下一週），交卷後依文法點顯示弱項

**分級閱讀**
- 英文 A1：*The House of Usher*、*The Gift*；日文 N5：《桃太郎》《鶴の恩返し》（皆為公有領域原著的原創改寫）
- 閱讀／收聽（逐句朗讀＋高亮）／翻譯三種模式，譯文可切中、英、日
- 點單字：音標、發音、中文與日文（英文書）或假名、羅馬拼音、中文與英文（日文書）
- 生字本依間隔重複排程（1、2、4、7、15、30 天），每日 10 分鐘閱讀目標

**介面**
- 一題一畫面、操作在拇指區、隨時中斷續做
- 日文可切換：漢字注音／只用假名／加羅馬拼音、詞間空格
- 語音使用瀏覽器內建 `speechSynthesis`；日文需先在系統安裝日文語音（iOS：設定 → 輔助使用 → 朗讀內容 → 聲音 → 日文）

## 目錄

```
index.html                     英日雙語版（題庫內建，主要入口）
data/
  phase0-days1-14.json         英文題庫
  phase0-days1-14-enja.json    英日完整題庫（含書庫、詞彙表）
generators/                    題庫產生器（Python）
docs/mobile-design-spec.md     手機版設計規格
legacy/                        早期版本（純英文原型、Day 1–14 英文版）
```

## 重新產生題庫

```bash
pip install -r requirements.txt
python generators/gen_days1-14.py   # → data/phase0-days1-14.json
python generators/assemble.py       # → data/phase0-days1-14-enja.json
```

產生器使用固定亂數種子，重跑結果與 repo 內的 JSON 相同。要更新 `index.html` 內建的題庫，把 `window.PRACTICE_DATA=` 後面的 JSON 換成新的 `phase0-days1-14-enja.json`；或在頁面「設定 → 匯入題庫」載入。

## 已知限制

- 進度存在瀏覽器 `localStorage`，換裝置請用「設定 → 匯出進度」
- 聽力是瀏覽器 TTS，不是真人語音
- 目前內容只到英文 Day 14、日文 N5；書架上 A2 以上與 N4 以上顯示「製作中」
