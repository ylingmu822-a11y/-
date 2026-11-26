"""Assemble the draft: number notes (規定の順・前掲註), renumber 史料, count characters."""
import re, pathlib

D = pathlib.Path(__file__).parent
K = "〇一二三四五六七八九"
def kd(n):  # digit-wise kanji numerals: 12 -> 一二
    return "".join(K[int(c)] for c in str(n))

BIB = {  # (short name, full citation with {p} for pages)
 "amino":   ("網野", "網野善彦、「異形の王権―後醍醐・文観・兼光―」、『異形の王権』、{p}、平凡社（平凡社ライブラリー）、一九九三年【要確認：版・発行年】"),
 "aminoSake": ("網野", "網野善彦、「造酒司酒麹役の成立について―室町幕府酒屋役の前提―」、竹内理三博士古稀記念会編『続荘園制と武家社会』、{p}、吉川弘文館、一九七八年"),
 "momo":    ("桃崎", "桃崎有一郎、「建武政権論」、『岩波講座日本歴史』第七巻中世二、{p}、岩波書店、二〇一四年"),
 "maruK":   ("丸谷", "丸谷豊、「後醍醐天皇、関白を廃す―建武政権の政治理念―」、『史泉』六八号、{p}、一九八八年"),
 "maruI":   ("丸谷", "丸谷豊、「建武政権と後醍醐天皇綸旨―「一同の法」の意義をめぐって―」、『（誌名・巻号要確認）』、{p}、（発行年要確認）"),
 "mori":    ("森", "森茂暁、「建武政権の法制―内閣文庫本「建武記」を素材として―」、『史淵』一一六輯、{p}、一九七九年"),
 "iikura":  ("飯倉", "飯倉晴武、「建武政権の所領安堵文書の変遷」、『法政史学』三二号、{p}、一九八〇年"),
 "kondo":   ("近藤", "近藤成一、「本領安堵と当知行地安堵」、石井進編『都と鄙の中世史』、{p}、吉川弘文館、一九九二年"),
 "kuroda":  ("黒田", "黒田俊雄、「建武政権の所領安堵政策について―一同の法および徳政令の解釈を中心に―」、『赤松俊秀教授退官記念国史論集』、{p}、京都大学文学部国史研究室、一九七二年【要確認：副題・発行所。のち黒田『日本中世の国家と宗教』岩波書店、一九七五年に収録】"),
 "satoR":   ("佐藤", "佐藤進一、『日本の歴史9　南北朝の動乱』、{p}、中央公論社、一九六五年【要確認：使用した版・発行年】"),
 "satoC":   ("佐藤", "佐藤進一、『日本の中世国家』、{p}、岩波書店（岩波文庫）、二〇二〇年"),
 "inaba":   ("稲葉", "稲葉伸道、「建武政権の寺社政策について」、『名古屋大学文学部研究論集（史学）』六三、{p}、二〇一七年"),
 "sakaL":   ("坂口", "坂口太郎、「後醍醐天皇、討幕への道」、『（掲載誌・巻号要確認）』、{p}、（発行年要確認）"),
 "naga":    ("長又", "長又高夫、「「建武式目」の評価をめぐって」、『國學院雑誌』一二二巻一一号、{p}、二〇二一年"),
 "sakaD":   ("坂口", "坂口太郎、「論文内容の要旨」、京都大学博士（人間・環境学）学位論文『鎌倉後期の王権と真言密教』、{p}、（公表媒体・発行年要確認。審査は二〇一四年）"),
 "hoso":    ("細川", "細川涼一、「三条大宮長福寺尊鏡と唐招提寺慶円―後醍醐天皇と南都律僧―」、『（誌名・巻号要確認）』、{p}、（発行年要確認）"),
 "hori":    ("堀内", "堀内和明、「楠木合戦と摂河泉の在地動向（上）―悪党の系譜をめぐって―」、『（誌名・巻号要確認）』、{p}、（発行年要確認）"),
 "nakai":   ("中井", "中井裕子、「建武新政期の検非違使庁について」、『（誌名・巻号要確認）』、{p}、（発行年要確認）"),
}

def pages(spec):
    spec = spec.strip()
    parts = [x.strip() for x in spec.split(",")]
    out = []
    for x in parts:
        if "–" in x:
            a, b = x.split("–")
            out.append(kd(a) + "〜" + kd(b))
        else:
            out.append(kd(x))
    return "・".join(out) + "頁"

first = {}
notes = []

PDFONLY = {"hoso", "hori", "nakai", "sakaD"}  # print pages unknown

def cite(m, n):
    key, sp = m.group(1), m.group(2)
    short, full = BIB[key]
    pg = pages(sp)
    if key in PDFONLY:
        pg = "PDF" + pg.replace("頁", "頁目") + "【印刷頁要確認】"
    if key not in first:
        first[key] = n
        return full.format(p=pg)
    return f"{short}前掲註（{kd(first[key])}）、{pg}"

def do_note(m):
    n = len(notes) + 1
    body = re.sub(r"\{@(\w+) ([0-9–, ]+)\}", lambda mm: cite(mm, n), m.group(1))
    if not body.endswith("。"):
        body += "。"
    notes.append(body)
    return f"（{kd(n)}）"

text = (D / "src_body1.md").read_text() + "\n" + (D / "src_body2.md").read_text()
text = re.sub(r"⟦(.+?)⟧", do_note, text, flags=re.S)

# 史料 renumbering by first appearance
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
order = []
for m in re.finditer(r"【史料([①-⑳])】", text):
    old = CIRC.index(m.group(1)) + 1
    if old not in order:
        order.append(old)
newnum = {old: i + 1 for i, old in enumerate(order)}
text = re.sub(r"【史料([①-⑳])】", lambda m: f"【史料{CIRC[newnum[CIRC.index(m.group(1)) + 1] - 1]}】", text)

body_only = text
text += "\n## 註\n\n" + "\n".join(f"（{kd(i+1)}）{t}" for i, t in enumerate(notes)) + "\n"
(D / "本文_下書き.md").write_text(text)

# 史料集
src = (D / "src_shiryo.md").read_text()
entries = {}
for blk in re.split(r"^@@", src, flags=re.M)[1:]:
    head, _, rest = blk.partition("\n")
    num, _, title = head.partition(" ")
    entries[int(num)] = (title, rest.strip())
out = ["# 史料集（本文の【史料①】などに対応）", "",
       "本文には史料の本文を入れず、番号だけを示した。返り点は省いた。〈 〉は原注・傍注。",
       "「取った本」は実際に読んだ本と頁で、原典を見ていないものは註に「所引」「による」と記してある。", ""]
for old in order:
    t, r = entries[old]
    out.append(f"## 史料{CIRC[newnum[old]-1]}　{t}\n\n" + r.replace("\n", "  \n") + "\n")
unused = [k for k in entries if k not in order]
(D / "史料集.md").write_text("\n".join(out))

# character count of body (excluding headings, tables, note markers)
cnt = 0
for line in body_only.splitlines():
    if line.startswith("#") or line.startswith("|"):
        continue
    line = re.sub(r"（[〇一二三四五六七八九]+）", "", line)
    line = re.sub(r"【[^】]*】", "", line)
    cnt += len(re.sub(r"\s|[-*]", "", line))
print("notes:", len(notes), "body chars:", cnt, "史料:", len(order), "unused:", unused)
