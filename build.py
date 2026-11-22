# -*- coding: utf-8 -*-
"""叮叮猫儿Lab · 静态站点生成器 v2（2026-11-21 模板移植）。
以拍板稿（课8 t4-月白 原型 + 网站设计-v1.md）为源整套接管：
月白宽页容器 / 侧抽屉移动导航 / 红猫皮 logo / 课程封面卡流+章节分组 / Tufte 账单边注 / 翻页链。
kind 路由（course/post/gallery），未知 kind 报错拒绝静默。"""
import re, html
from pathlib import Path

ROOT = Path(__file__).parent
ART = ROOT / "articles"
OUT = ROOT / "a"
KINDS = {"course", "post", "gallery"}

NAV = [("index.html", "首页", "home"), ("learn.html", "课程", "learn"),
       ("list.html", "文章", "list"), ("gallery.html", "图文", "gallery"),
       ("about.html", "关于", "about")]

MARK = ('<svg viewBox="0 0 100 100" style="width:26px;height:26px;border-radius:7px">'
        '<rect width="100" height="100" rx="22" fill="#e3c24b"/>'
        '<path d="M18 14 H48 Q82 14 82 50 Q82 86 48 86 H18 Z M40 34 H46 Q62 34 62 50 Q62 66 46 66 H40 Z" fill="#df5a30" fill-rule="evenodd"/>'
        '<path d="M50 40 Q54 45 54 50 Q54 55 50 60 Q46 55 46 50 Q46 45 50 40 Z" fill="#1d4e89"/></svg>')
BRAND = f'<span class="b">{MARK}叮叮猫儿<i class="lab">Lab</i></span>'

STYLE = """
:root{--paper:#f6f6f4;--ink:#141414;--muted:#8a8a86;--ember:#df5a30;--cobalt:#1d4e89;--must:#e3c24b;--line:#e3e3df;--card:#ffffff}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--paper);color:var(--ink);
line-height:1.9;background-image:radial-gradient(rgba(20,20,20,.03) 1px,transparent 1.3px);background-size:26px 26px}
.wrap{max-width:1040px;margin:0 auto;padding:0 26px}
nav{padding:22px 0;display:flex;align-items:center;gap:4px;border-bottom:1.5px solid var(--ink)}
nav .b{display:flex;align-items:center;gap:12px;font-weight:800;font-size:16.5px;margin-right:auto;letter-spacing:.02em}
nav .lab{font-family:Georgia,'Times New Roman',serif;font-style:italic;font-weight:600}
nav .links{display:flex;gap:2px}
nav a.nl{color:var(--muted);text-decoration:none;font-size:14px;padding:7px 14px;border-radius:9px}
nav a.nl:hover{color:var(--ink)}
nav a.nl.on{color:var(--ink);font-weight:800;background:rgba(223,90,48,.10)}
.burger{display:none}
#navcb{display:none}
.drawer{display:none}
@media(max-width:700px){
 nav .links{display:none}
 .burger{display:flex;align-items:center;justify-content:center;width:42px;height:42px;border:1.5px solid var(--ink);border-radius:10px;font-size:17px;font-weight:800;cursor:pointer;background:var(--card)}
 #navcb:checked ~ .drawer{display:flex}
 .drawer{position:fixed;inset:0;z-index:60;background:rgba(20,20,20,.4)}
 .drawer .ovl{flex:1}
 .drawer .panel{width:76%;max-width:320px;background:#fff;height:100%;padding:26px;display:flex;flex-direction:column;box-shadow:24px 0 60px rgba(0,0,0,.25)}
 .drawer a.dl{font-size:25px;font-weight:900;letter-spacing:-.02em;padding:13px 0;border-bottom:1px solid #f0efeb;color:var(--ink);text-decoration:none}
 .drawer a.dl.on{color:var(--ember)}
 .drawer .dfoot{margin-top:auto;font-size:11.5px;color:var(--muted);line-height:2}
}
.head{padding:54px 0 22px}
.kicker{font-family:Consolas,monospace;font-size:11.5px;letter-spacing:4px;color:var(--ember);margin-bottom:14px}
h1{font-size:clamp(28px,5vw,42px);line-height:1.32;font-weight:900;letter-spacing:-.025em}
.meta{margin-top:14px;color:var(--muted);font-size:13.5px;font-family:Consolas,monospace}
article{padding:8px 0 34px}
article p{margin:0 0 20px;font-size:16.5px;color:#2f2c27}
article h2{font-size:22px;margin:36px 0 16px;font-weight:800}
article h3{font-size:18px;margin:28px 0 12px;font-weight:700}
article h4{font-size:16px;margin:20px 0 8px;font-weight:700}
article blockquote{border-left:3px solid var(--ember);background:var(--card);padding:12px 18px;margin:0 0 20px;color:#5a554b;border-radius:0 8px 8px 0}
article ul{margin:0 0 20px 22px}article li{margin:6px 0}
article code{background:#efefec;border:1px solid var(--line);border-radius:4px;padding:1px 6px;font-family:Consolas,monospace;font-size:14px}
article strong{color:var(--ink)}
.lessonpage{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:48px;align-items:start;padding-top:8px}
.marginal{position:sticky;top:22px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;font-size:13.5px;color:#5a554b}
.marginal h2{font-size:11.5px;letter-spacing:3px;color:var(--muted);margin:0 0 12px;font-weight:700}
.marginal p{margin:0 0 10px;font-size:13.5px;color:#5a554b}
.marginal ul{margin:0 0 6px 18px}.marginal li{margin:4px 0}
.narrow{max-width:720px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px;padding:6px 0 30px}
.ccard{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;text-decoration:none;color:var(--ink);transition:.18s;display:flex;flex-direction:column}
.ccard:hover{border-color:var(--ember);transform:translateY(-3px);box-shadow:0 12px 30px rgba(20,20,20,.08)}
.ccard img{width:100%;aspect-ratio:1800/766;object-fit:cover;display:block;border-bottom:1px solid var(--line)}
.ccard .cb{padding:14px 18px 16px}
.ccard .ck{font:700 11px Consolas,monospace;letter-spacing:2px;color:var(--ember)}
.ccard .ct{font-size:15.5px;font-weight:800;margin-top:7px;letter-spacing:-.01em;line-height:1.5}
.ccard .cd{font-size:12px;color:var(--muted);margin-top:6px;font-family:Consolas,monospace}
.chapter-h{display:flex;align-items:baseline;gap:14px;margin:36px 0 4px}
.chapter-h h2{font-size:19px;font-weight:900;letter-spacing:-.01em}
.chapter-h span{font:700 10.5px Consolas,monospace;letter-spacing:2px;color:var(--ember);background:rgba(223,90,48,.1);padding:3px 10px;border-radius:999px}
.search{width:100%;max-width:540px;padding:13px 17px;border:1.5px solid var(--line);border-radius:11px;background:var(--card);font-size:15px;color:var(--ink);outline:none;margin:6px 0}
.search:focus{border-color:var(--ember);box-shadow:0 0 0 3px rgba(223,90,48,.13)}
.hint{font-size:12.5px;color:var(--muted);margin-bottom:6px}
.empty{margin:16px 0 40px;padding:20px;border:1.5px dashed var(--line);border-radius:12px;text-align:center;color:var(--muted);font-size:14px;background:var(--card)}
.empty a,.empty .go-try,.empty .go-clear{color:var(--ember);font-weight:700;cursor:pointer;text-decoration:underline}
.chips{display:flex;gap:10px;margin:16px 0 8px;flex-wrap:wrap}
.chip{padding:8px 16px;border:1px solid var(--line);border-radius:999px;font-size:13.5px;background:var(--card);cursor:pointer;min-height:40px;display:inline-flex;align-items:center;color:var(--ink)}
.chip.on{background:var(--ink);color:#fff;border-color:var(--ink);font-weight:700}
.item{display:flex;gap:16px;padding:14px 0;border-bottom:1px dashed var(--line);text-decoration:none;color:var(--ink);min-height:44px;transition:opacity .18s}
.item:hover .t{color:var(--ember)}
.item .no{font-family:Consolas,monospace;color:var(--ember);font-size:12.5px;flex:none;width:70px;padding-top:4px;letter-spacing:1px}
.item .t{font-size:16px;font-weight:600}
.item .d{margin-left:auto;color:var(--muted);font-size:12px;font-family:Consolas,monospace;flex:none;padding-top:4px}
.dim{opacity:.2}
.cta{display:inline-block;padding:11px 22px;border-radius:11px;font-size:14px;font-weight:700;background:var(--ember);color:#fff;text-decoration:none;margin:14px 10px 0 0}
.cta.g{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.pn{border-top:1.5px solid var(--ink);margin-top:26px;padding-top:18px}
footer{padding:26px 0 56px;border-top:1.5px solid var(--ink);color:var(--muted);font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-top:40px}
footer .no{font-family:Consolas,monospace;color:var(--ember)}
.hide{display:none}
pre{background:#1d1b17;color:#f0ede4;padding:14px 16px;border-radius:10px;overflow-x:auto;font:13.5px/1.7 Consolas,'Courier New',monospace;margin:0 0 20px}
pre code{background:none;border:none;padding:0;color:inherit;font-size:inherit}
table{width:100%;border-collapse:collapse;margin:0 0 20px;font-size:14px}
th,td{border:1px solid var(--line);padding:8px 12px;text-align:left;background:var(--card)}
th{font-weight:700;background:#efefec}
article img{max-width:100%;height:auto;border-radius:10px;border:1px solid var(--line);display:block;margin:0 0 8px}
.imgcap{font-size:12.5px;color:var(--muted);margin:0 0 22px}
@media(max-width:900px){.lessonpage{grid-template-columns:minmax(0,1fr)}.marginal{position:static;order:-1}table{font-size:12.5px}th,td{padding:6px 8px}}
.lessonpage>div,article,pre{min-width:0}
"""

JS = """
function wire(searchId,itemSel,groupSel,emptyId){
 var q=document.getElementById(searchId); if(!q) return;
 var items=[].slice.call(document.querySelectorAll(itemSel));
 var groups=groupSel?[].slice.call(document.querySelectorAll(groupSel)):[];
 var empty=document.getElementById(emptyId);
 function apply(){
   var k=(q.value||'').trim().toLowerCase(),hit=0;
   items.forEach(function(el){
     var on=false;
     if(k){on=el.getAttribute('data-t').split('|').some(function(pp){return pp.indexOf(k)>-1;});
       el.classList.toggle('dim',!on); if(on)hit++;}
     else el.classList.remove('dim');
   });
   if(groups.length)groups.forEach(function(g){
     var vis=[].slice.call(g.querySelectorAll(itemSel)).some(function(l){return !k||!l.classList.contains('dim');});
     g.classList.toggle('hide',!!k&&!vis);
   });
   if(empty){empty.classList.toggle('hide',!(k&&hit===0));
     var e=empty.querySelector('#ekw'); if(e)e.textContent=q.value;}
 }
 q.addEventListener('input',apply);
 document.addEventListener('keydown',function(e){
   if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus();}
   if(e.key==='Escape'&&document.activeElement===q){q.value='';apply();q.blur();}
 });
 document.querySelectorAll('.go-clear,.go-try').forEach(function(g){
   g.addEventListener('click',function(){q.value=g.classList.contains('go-try')?(g.getAttribute('data-k')||''):'';apply();q.focus();});
 });
}
"""

LIST_JS = """
(function(){
 var chips=[].slice.call(document.querySelectorAll('.chip'));
 var rows=[].slice.call(document.querySelectorAll('#rows .item'));
 var cur="";
 function applyF(){
   var hit=0;
   rows.forEach(function(el){
     var okc=!cur||el.getAttribute('data-cat')===cur;
     el.classList.toggle('hide',!okc); if(okc)hit++;
   });
   document.getElementById('empty').classList.toggle('hide',hit!==0);
 }
 chips.forEach(function(c){c.addEventListener('click',function(){
   chips.forEach(function(x){x.classList.remove('on');});c.classList.add('on');cur=c.getAttribute('data-cat');applyF();});});
 var cc=document.getElementById('c-clear');
 if(cc)cc.addEventListener('click',function(){cur='';
   chips.forEach(function(x){x.classList.remove('on');});chips[0].classList.add('on');applyF();});
})();
"""


def parse(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    meta, body = {}, text
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def md(body):
    out, lines = [], body.splitlines()
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("```"):
            lang = ln[3:].strip()
            buf = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1  # 跳过闭合围栏
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            continue
        if ln.startswith("|") and i + 1 < n and re.match(r"^[|\s:-]+$", lines[i+1]):
            rows = []
            while i < n and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not re.match(r"^[|\s:-]+$", lines[i]):
                    rows.append(cells)
                i += 1
            if rows:
                th = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
                out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>")
            continue
        im = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", ln)
        if im:
            alt, src = html.escape(im.group(1)), im.group(2)
            out.append(f'<img src="../assets/{Path(src).name}" alt="{alt}">')
            if alt:
                out.append(f'<div class="imgcap">{alt}</div>')
            i += 1; continue
        hm = re.match(r"^(#{2,6}) (.+)$", ln)
        if hm:
            lvl = len(hm.group(1))
            out.append(f"<h{lvl}>" + inline(hm.group(2)) + f"</h{lvl}>"); i += 1
        elif ln.startswith("> "):
            buf = []
            while i < n and lines[i].startswith("> "):
                buf.append(inline(lines[i][2:])); i += 1
            out.append("<blockquote>" + "<br>".join(buf) + "</blockquote>")
        elif ln.startswith("- "):
            buf = []
            while i < n and lines[i].startswith("- "):
                buf.append("<li>" + inline(lines[i][2:]) + "</li>"); i += 1
            out.append("<ul>" + "".join(buf) + "</ul>")
        else:
            buf, start = [], i
            while i < n and lines[i].strip() and not re.match(r"^(```|#|> |- |\|)", lines[i]):
                buf.append(inline(lines[i])); i += 1
            if i == start:
                buf = [inline(lines[i])]; i += 1
            out.append("<p>" + " ".join(buf) + "</p>")
    return "\n".join(out)


def page(title, content, active, head="", extra_head="", scripts="", base=""):
    links = "".join(f'<a class="nl{" on" if k == active else ""}" href="{base}{h}">{lab}</a>' for h, lab, k in NAV)
    dl = "".join(f'<a class="dl{" on" if k == active else ""}" href="{base}{h}">{lab}</a>' for h, lab, k in NAV)
    return (f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="description" content="叮叮猫儿Lab · 漫游数字世界，实验AI与互联网，同步新鲜动态与实践思考。">
<title>{html.escape(title)} · 叮叮猫儿Lab</title>
<link rel="icon" sizes="16x16" href="{base}favicon-16.png"><link rel="icon" sizes="32x32" href="{base}favicon-32.png">
<style>{STYLE}</style>{extra_head}</head><body>
<input type="checkbox" id="navcb">
<div class="wrap">
<nav>{BRAND}<span class="links">{links}</span><label class="burger" for="navcb">&#9776;</label></nav>
{head}{content}
<footer><span>叮叮猫儿Lab · 漫游数字世界，实验AI与互联网，同步新鲜动态与实践思考。</span><span class="no">est. 2026</span></footer>
</div>
<div class="drawer"><label class="ovl" for="navcb"></label><div class="panel">{dl}<div class="dfoot">本站纯静态 · 零 Cookie 零追踪<br>公众号首发 · 这里永久存档</div></div></div>
<script>{JS}{scripts}</script>
</body></html>""")


def head_block(kicker, h1, meta=""):
    mh = f'<div class="meta">{meta}</div>' if meta else ""
    return f'<div class="head"><div class="kicker">{kicker}</div><h1>{html.escape(h1)}</h1>{mh}</div>'


def main():
    OUT.mkdir(exist_ok=True)
    keep = {f.stem + ".html" for f in ART.glob("*.md")}
    for stale in OUT.glob("*.html"):
        if stale.name not in keep:
            stale.unlink(); print(f"[sweep] 清理孤儿页面 {stale.name}")
    arts = []
    for f in sorted(ART.glob("*.md")):
        meta, body = parse(f.read_text(encoding="utf-8"))
        kind = meta.get("kind", "")
        if kind not in KINDS:
            raise SystemExit(f"[build] 未知 kind: '{kind}'（{f.name}）。允许值：course/post/gallery。拒绝静默。")
        arts.append((kind, meta, body, f.stem))

    course_groups = {}
    for kind, meta, body, slug in arts:
        if kind == "course":
            course_groups.setdefault(meta.get("series", "未分类"), []).append((int(meta.get("number", 0)), meta, slug, body))
    for s in course_groups:
        course_groups[s].sort(key=lambda x: x[0])

    # ---------- 文章页：course 带账单边注 + 翻页；散装窄页 ----------
    for kind, meta, body, slug in arts:
        aside_html = ""
        ms = re.search(r"^## 本课账单\s*$", body, re.M) if kind == "course" else None
        if ms:
            main_body, bill = body[:ms.start()], body[ms.end():]
            aside_html = f'<aside class="marginal"><h2>本课账单</h2>{md(bill)}</aside>'
        else:
            main_body = body
        content = f'<article>{md(main_body)}</article>'
        navrow = ""
        if kind == "course":
            items = course_groups[meta.get("series", "")]
            pos = next(i for i, (n, m, s, b) in enumerate(items) if s == slug)
            cell = []
            if pos > 0:
                cell.append(f'<a class="cta g" href="{items[pos-1][2]}.html">← 上一课：{html.escape(items[pos-1][1].get("title",""))}</a>')
            if pos < len(items) - 1:
                cell.append(f'<a class="cta" href="{items[pos+1][2]}.html">下一课：{html.escape(items[pos+1][1].get("title",""))} →</a>')
            if cell:
                navrow = '<div class="pn">' + "".join(cell) + "</div>"
        ml = (f'{meta.get("series","")} · 第 {meta.get("number","")} 课 · {meta.get("date","")}' if kind == "course"
              else f'{meta.get("series","")} · {meta.get("date","")}')
        if aside_html:
            body_html = f'<div class="lessonpage"><div>{content}{navrow}</div>{aside_html}</div>'
        else:
            body_html = f'<div class="narrow">{content}{navrow}</div>'
        hp = head_block(meta.get("series", "文章"), meta.get("title", slug), ml)
        (OUT / f"{slug}.html").write_text(page(meta.get("title", slug), body_html, "learn" if kind == "course" else "list", head=hp, base="../"), encoding="utf-8")

    # ---------- learn.html：课程馆 = 封面卡流 + 章节分组 + 轻搜索 ----------
    n_course = sum(1 for k, *_ in arts if k == "course")
    blocks = []
    for series, items in sorted(course_groups.items(), key=lambda kv: kv[1][0][1].get("date", "")):
        chapters = {}
        for n, meta, slug, _ in items:
            chapters.setdefault(meta.get("chapter", series), []).append((n, meta, slug))
        inner = ""
        for ch, chitems in chapters.items():
            cards = ""
            for n, m, s in chitems:
                img = f'<img loading="lazy" src="covers/cover-上手课{n:03d}.png">' if (series == "上手课" and (ROOT / "covers" / f"cover-上手课{n:03d}.png").exists()) else ""
                dt = html.escape((m.get("title", "") + f"|课{n}|{n}").lower())
                cards += (f'<a class="ccard" data-t="{dt}" href="a/{s}.html">' + img
                          + f'<div class="cb"><div class="ck">{html.escape(series)} · 第 {n:02d} 课</div>'
                          + f'<div class="ct">{html.escape(m.get("title",""))}</div>'
                          + f'<div class="cd">{m.get("date","")} · 已发布</div></div></a>')
            inner += (f'<div class="chapter-group"><div class="chapter-h"><h2>{html.escape(ch)}</h2>'
                      f'<span>{len(chitems)} 课</span></div><div class="cgrid">{cards}</div></div>')
        blocks.append(inner)
    learn_body = (f'<input class="search" id="q" placeholder="搜课名或课号，比如：后悔药、3（按 / 直达）">'
                  f'<div class="hint">标题与课号即时匹配 · 正文不进索引</div>'
                  + "".join(blocks)
                  + '<div class="empty hide" id="empty">没有匹配「<span id="ekw"></span>」的课。<br><br>'
                  + f'<span class="go-try" data-k="后悔药">试试「后悔药」</span>？或 <span class="go-clear">清空搜索</span> 看全部 {n_course} 课</div>')
    learn_head = head_block("VIBE CODING 上手课 · 全部系列", "跟课学 Vibe Coding",
                            f"共 {n_course} 课 · 纯静态 · 现金成本约一顿饭的零头")
    (ROOT / "learn.html").write_text(page("课程", learn_body, "learn", head=learn_head,
                                          scripts='wire("q",".ccard",".chapter-group","empty");'), encoding="utf-8")

    # ---------- list.html：散装单篇 + 栏目 chips ----------
    posts = [(k, m, s) for k, m, b, s in arts if k == "post"]
    galleries = [(k, m, s) for k, m, b, s in arts if k == "gallery"]
    cats = sorted({m.get("series", "单篇") for _, m, _ in posts})
    chips = '<span class="chip on" data-cat="">全部</span>' + "".join(
        f'<span class="chip" data-cat="{html.escape(c)}">{html.escape(c)}</span>' for c in cats)
    rows = "".join(
        f'<a class="item" data-cat="{html.escape(m.get("series","单篇"))}" data-t="{html.escape(m.get("title","").lower())}" href="a/{s}.html">'
        f'<span class="no">{html.escape(m.get("series",""))}</span><span class="t">{html.escape(m.get("title",s))}</span>'
        f'<span class="d">{m.get("date","")}</span></a>' for _, m, s in posts)
    list_body = (f'<input class="search" id="q" placeholder="搜标题（/ 直达 · Esc 清空）">'
                 f'<div class="hint">只搜标题，正文不进索引 · 共 {len(posts)} 篇</div>'
                 f'<div class="chips">{chips}</div><div id="rows">{rows}</div>'
                 f'<div class="empty hide" id="empty">这个筛选下还没有存货。<br><br>'
                 f'<span class="go-clear" id="c-clear">清空筛选</span> 看全部 {len(posts)} 篇</div>')
    list_head = head_block("ALL WRITING", "文章", "散装单篇 · 课程去「课程」，图进去「图文」")
    (ROOT / "list.html").write_text(page("文章", list_body, "list", head=list_head,
                                         scripts='wire("q","#rows .item",null,"empty");' + LIST_JS), encoding="utf-8")

    # ---------- gallery.html：图文书架（空架兜底） ----------
    if galleries:
        gcards = "".join(f'<a class="ccard" href="a/{s}.html"><div class="cb"><div class="ck">图文</div>'
                         f'<div class="ct">{html.escape(m.get("title",s))}</div><div class="cd">{m.get("date","")}</div></div></a>'
                         for _, m, s in galleries)
        g_body = f'<div class="cgrid">{gcards}</div>'
    else:
        g_body = ('<div class="empty" style="text-align:left;line-height:2">这一架还没搬完——图文（小绿书）正在从公众号归档。'
                  '先去 <a href="learn.html">课程区</a> 或 <a href="list.html">文章区</a> 转转。</div>')
    (ROOT / "gallery.html").write_text(page("图文", g_body, "gallery",
                                            head=head_block("GALLERY", "图文", "图为主，字为辅")), encoding="utf-8")

    # ---------- index.html：Now Page ----------
    latest = course_groups.get("上手课", [None])[-1]
    lc_t = html.escape(latest[1].get("title", "")) if latest else "课程整理中"
    lc_s = f"a/{latest[2]}.html" if latest else "learn.html"
    img = f'<img src="covers/cover-上手课{latest[0]:03d}.png">' if latest and (ROOT / f"covers/cover-上手课{latest[0]:03d}.png").exists() else ""
    hero = (f'<div style="max-width:660px;margin:10px 0 8px"><a class="ccard" href="{lc_s}" style="display:block">'
            + img + f'<div class="cb"><div class="ck">在上的课 · VIBE CODING 上手课 · 最新一期</div>'
            + f'<div class="ct">{lc_t}</div><div class="cd">零基础 / 纯静态 / 现金成本约一顿饭的零头</div></div></a></div>')
    recents = "".join(f'<a class="item" href="a/{s}.html"><span class="no">{html.escape(m.get("series",""))}</span>'
                      f'<span class="t">{html.escape(m.get("title",s))}</span><span class="d">{m.get("date","")}</span></a>'
                      for _, m, s in sorted(posts, key=lambda x: x[1].get("date", ""), reverse=True)[:3])
    idx_body = (f'<div class="meta" style="margin:0 0 22px">已发布 {n_course} 课 · 存档 {len(arts)} 篇 · 更新节奏以公众号为准</div>'
                + hero
                + '<div class="chapter-h"><h2>最新单篇</h2><span>NOTES</span></div>' + (recents or '<div class="hint">第一篇正在路上</div>')
                + '<a class="cta" href="learn.html">从第 1 课开始 →</a><a class="cta g" href="about.html">这是谁建的站</a>')
    idx_head = ('<div class="head" style="padding-bottom:8px"><div class="kicker">DINGDINGCAT LAB · 漫游数字世界</div>'
                '<h1>把新工具、新模型<span style="color:var(--ember)">真的用一遍</span>，<br>写清楚能不能用、卡在哪、值不值。</h1>'
                '<div class="meta">实验AI与互联网，同步新鲜动态与实践思考 · 只写实测的账</div></div>')
    (ROOT / "index.html").write_text(page("首页", idx_body, "home", head=idx_head), encoding="utf-8")

    # ---------- about.html：拍板版（宣言原句 + 这个站 + 二维码直挂） ----------
    about_body = ('<div class="narrow"><article>'
        '<p style="font-size:19px;font-weight:700;border-left:3px solid var(--ember);padding-left:20px;line-height:1.8">「我决定用AI亲手建个人网站，让博客、教程随课程一起生长并留存。」</p>'
        '<p>这个站干的事很简单：<strong>公众号发过的每一篇，这里都在。</strong>课程按编号排好，想系统学就从第 1 课进来；'
        '散装按时间躺着，闲逛随意。文章永久存档，不随平台算法沉底。</p>'
        '<div class="follow"><img src="qrcode.jpg" alt="微信公众号二维码">'
        '<div><strong>连载更新在公众号</strong><br>扫码关注，更新不错过。'
        '<br><span class="acc">微信公众号 · 叮叮猫儿Lab</span></div></div>'
        '<p style="color:var(--muted);font-size:13.5px;line-height:2">找事：公众号后台留言即可。<br>'
        '这个站由它的作者在 Claude Code 里一手盖成——你正在看的页面，本身就是课程的作品。</p>'
        '</article></div>')
    about_css = ('<style>.follow{display:flex;gap:22px;align-items:center;background:var(--card);border:1px solid var(--line);'
        'border-radius:14px;padding:18px 20px;margin:26px 0}.follow img{width:132px;height:132px;border-radius:8px;flex:none;border:1px solid var(--line)}'
        '.follow .acc{display:inline-block;margin-top:8px;font:700 12px Consolas,monospace;border:1px solid var(--ink);border-radius:999px;padding:3px 12px}'
        '@media(max-width:560px){.follow{flex-direction:column;text-align:center}}</style>')
    (ROOT / "about.html").write_text(page("关于", about_body, "about",
                                          head=head_block("ABOUT", "关于叮叮猫儿Lab"), extra_head=about_css), encoding="utf-8")

    print(f"built v2: {len(arts)} arts ({n_course} course/{len(posts)} post/{len(galleries)} gallery) -> index/learn/list/gallery/about + a/")


if __name__ == "__main__":
    main()
