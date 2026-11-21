# -*- coding: utf-8 -*-
"""叮叮猫儿Lab · 静态站点生成器。md 文章 → html 页面。无框架，单文件可懂。
P1/P2 施工版（2026-11-21）：kind 路由（course/post/gallery）；course 归 learn.html 课程路径，
散装（post/gallery）归 list.html；课程页带上一课/下一课；未知 kind 报错停下，不静默。"""
import re, html
from pathlib import Path

ROOT = Path(__file__).parent
ART = ROOT / "articles"
OUT = ROOT / "a"
KINDS = {"course", "post", "gallery"}

STYLE = """
:root{--paper:#f7f2ea;--ink:#211a14;--muted:#8a7d6d;--ember:#d8551f;--line:#e4dac9;--card:#fffdf9}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:var(--paper);color:var(--ink);
line-height:1.9;background-image:radial-gradient(rgba(33,26,20,.035) 1px,transparent 1.3px);background-size:26px 26px}
.wrap{max-width:720px;margin:0 auto;padding:0 28px}
nav{padding:34px 0;display:flex;align-items:center;gap:22px;border-bottom:1px solid var(--line)}
nav .b{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:3px;font-size:17px;margin-right:auto}
nav .mark{width:24px;height:21px;position:relative;background:radial-gradient(circle at 35% 58%,#2a1608 1.6px,transparent 2.2px),radial-gradient(circle at 65% 58%,#2a1608 1.6px,transparent 2.2px),radial-gradient(circle at 50% 68%,#ffd9a0,var(--ember) 58%,#9a3410);border-radius:50% 50% 46% 46%}
nav .mark::before,nav .mark::after{content:"";position:absolute;top:-5px;width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid var(--ember)}
nav .mark::before{left:1px;transform:rotate(-18deg)}
nav .mark::after{right:1px;transform:rotate(18deg)}
nav a{color:var(--muted);text-decoration:none;font-size:14px}
nav a.on,nav a:hover{color:var(--ember)}
.head{padding:54px 0 30px}
.kicker{font-family:Consolas,monospace;font-size:12px;letter-spacing:2px;color:var(--ember);margin-bottom:16px}
h1{font-size:36px;line-height:1.3;font-weight:800}
.meta{margin-top:16px;color:var(--muted);font-size:13px;font-family:Consolas,monospace}
article{padding:10px 0 50px}
article p{margin:0 0 20px;font-size:16.5px;color:#3a3128}
article h2{font-size:22px;margin:36px 0 16px;font-weight:800}
article h3{font-size:18px;margin:28px 0 12px;font-weight:700}
article h4{font-size:16px;margin:20px 0 8px;font-weight:700}
article blockquote{border-left:3px solid var(--ember);background:var(--card);padding:12px 18px;margin:0 0 20px;color:#5a4d3d;border-radius:0 8px 8px 0}
article ul{margin:0 0 20px 22px}article li{margin:6px 0}
article strong{color:var(--ink)}
.pn{display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--line);padding:22px 0 6px;font-size:14px}
.pn a{text-decoration:none;color:var(--ink);max-width:48%}
.pn .lab{font-family:Consolas,monospace;font-size:11px;letter-spacing:2px;color:var(--muted);display:block}
.pn .t{color:var(--ember);font-weight:700}
.list{padding:20px 0 50px}
.series{margin-bottom:36px}
.series h2{font-size:15px;letter-spacing:3px;color:var(--muted);margin-bottom:14px}
.series h2::before{content:"";display:inline-block;width:18px;height:2px;background:var(--ember);vertical-align:4px;margin-right:10px}
.item{display:flex;gap:16px;padding:14px 0;border-bottom:1px dashed var(--line);text-decoration:none;color:var(--ink);min-height:44px}
.item:hover .t{color:var(--ember)}
.item .no{font-family:Consolas,monospace;color:var(--ember);font-size:13px;flex:none;width:40px;padding-top:3px}
.item .t{font-size:16px;font-weight:600}
.item .d{margin-left:auto;color:var(--muted);font-size:12px;font-family:Consolas,monospace;flex:none;padding-top:4px}
.search{width:100%;padding:13px 16px;border:1px solid var(--line);border-radius:10px;background:var(--card);font:15px/1.5 inherit;color:var(--ink);outline:none;margin:6px 0 4px}
.search:focus{border-color:var(--ember);box-shadow:0 0 0 3px rgba(216,85,31,.14)}
.hint{font-size:12px;color:var(--muted);margin-bottom:20px}
.dim{opacity:.25}
.empty{margin-top:20px;padding:18px 20px;border:1.5px dashed var(--line);border-radius:10px;text-align:center;color:var(--muted);font-size:14px}
.empty .go{color:var(--ember);font-weight:700;cursor:pointer;text-decoration:underline}
footer{padding:34px 0 60px;border-top:1px solid var(--line);color:var(--muted);font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
footer .no{font-family:Consolas,monospace;color:var(--ember)}
@media(max-width:560px){h1{font-size:28px}}
"""

SEARCH_JS = """
(function(){
 var q=document.getElementById('q'),box=document.getElementById('courses'),
     empty=document.getElementById('empty'),ekw=document.getElementById('ekw'),
     items=[].slice.call(document.querySelectorAll('.item[data-t]')),
     groups=[].slice.call(document.querySelectorAll('.series[data-series]'));
 function apply(){
   var k=q.value.trim().toLowerCase(),hit=0;
   items.forEach(function(el){
     var on=false;
     if(k){
       on=el.getAttribute('data-t').split('|').some(function(p){return p.indexOf(k)>-1;});
       el.classList.toggle('dim',!on); if(on)hit++;
     } else el.classList.remove('dim');
   });
   groups.forEach(function(g){
     var vis=[].slice.call(g.querySelectorAll('.item[data-t]')).some(function(l){return !k||!l.classList.contains('dim');});
     g.classList.toggle('empty-hide',!!k&&!vis);
   });
   ekw.textContent=q.value;
   empty.classList.toggle('hide',!(k&&hit===0));
   box.classList.toggle('hide',k&&hit===0);
 }
 q.addEventListener('input',apply);
 document.addEventListener('keydown',function(e){
   if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus();}
   if(e.key==='Escape'&&document.activeElement===q){q.value='';apply();q.blur();}
 });
 [].slice.call(document.querySelectorAll('.go')).forEach(function(g){
   g.addEventListener('click',function(){q.value=(g.id==='c1')?'后悔药':'';apply();q.focus();});
 });
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
        hm = re.match(r"^(#{2,6}) (.+)$", ln)
        if hm:
            lvl = len(hm.group(1))
            out.append(f"<h{lvl}>" + inline(hm.group(2)) + f"</h{lvl}>"); i += 1
        elif ln.startswith("## "):
            out.append("<h2>" + inline(ln[3:]) + "</h2>"); i += 1
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
            while i < n and lines[i].strip() and not re.match(r"^(#|> |- )", lines[i]):
                buf.append(inline(lines[i])); i += 1
            if i == start:  # 未识别行兜底：吞一行并前进，绝不原地打转
                buf = [inline(lines[i])]; i += 1
            out.append("<p>" + " ".join(buf) + "</p>")
    return "\n".join(out)


def page(title, kicker, content, active, h1=None, meta_line="", extra_style=""):
    nav = ""
    for href, label, key in [("index.html", "主页", "home"), ("list.html", "文章", "list"),
                             ("learn.html", "课程", "learn"), ("about.html", "关于", "about")]:
        cls = ' class="on"' if key == active else ""
        nav += f'<a href="{href}"{cls}>{label}</a>'
    head = ""
    if h1:
        head = f'<div class="head"><div class="kicker">{kicker}</div><h1>{html.escape(h1)}</h1>'
        if meta_line:
            head += f'<div class="meta">{meta_line}</div>'
        head += "</div>"
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{html.escape(title)} · 叮叮猫儿Lab</title><style>{STYLE}{extra_style}</style></head><body><div class="wrap">
<nav><span class="b"><span class="mark"></span>叮叮猫儿Lab</span>{nav}</nav>
{head}{content}
<footer><span>叮叮猫儿Lab · 慢慢探索，沉淀思考与实践</span><span class="no">est. 2026</span></footer>
</div></body></html>"""


def main():
    OUT.mkdir(exist_ok=True)
    arts = []
    for f in sorted(ART.glob("*.md")):
        meta, body = parse(f.read_text(encoding="utf-8"))
        kind = meta.get("kind", "")
        if kind not in KINDS:
            raise SystemExit(f"[build] 未知 kind: '{kind}'（{f.name}）。允许值：course/post/gallery。拒绝静默。")
        arts.append((kind, meta, body, f.stem))

    # 课程序列：按系列分组、系列内 number 升序（翻页链数据）
    course_groups = {}
    for kind, meta, body, slug in arts:
        if kind == "course":
            course_groups.setdefault(meta.get("series", "未分类"), []).append((int(meta.get("number", 0)), meta, slug))
    for s in course_groups:
        course_groups[s].sort(key=lambda x: x[0])

    # 文章页
    for kind, meta, body, slug in arts:
        content = "<article>" + md(body) + "</article>"
        if kind == "course":
            series = meta.get("series", "")
            items = course_groups[series]
            pos = next(i for i, (n, m, s) in enumerate(items) if s == slug)
            ml = f'{series} · 第 {meta.get("number","")} 课 · {meta.get("date","")}'
            links = []
            if pos > 0:
                pm = items[pos-1][1]
                links.append(f'<a href="{items[pos-1][2]}.html"><span class="lab">← 上一课</span>'
                             f'<span class="t">{html.escape(pm.get("title",""))}</span></a>')
            if pos < len(items) - 1:
                nm = items[pos+1][1]
                links.append(f'<a href="{items[pos+1][2]}.html" style="text-align:right"><span class="lab">下一课 →</span>'
                             f'<span class="t">{html.escape(nm.get("title",""))}</span></a>')
            if links:
                content += '<div class="pn">' + "".join(links) + "</div>"
        else:
            ml = f'{meta.get("series","")} · 第 {meta.get("number","")} 篇 · {meta.get("date","")}'
        html_out = page(meta.get("title", slug), meta.get("series", "文章"),
                        content, "list", h1=meta.get("title", slug), meta_line=ml)
        (OUT / f"{slug}.html").write_text(html_out, encoding="utf-8")

    # 文章页(list)：仅散装（post/gallery），课程不混排
    loose = [(k, m, s) for k, m, b, s in arts if k != "course"]
    lg = {}
    for k, meta, slug in loose:
        lg.setdefault(meta.get("series", "单篇"), []).append((int(meta.get("number", 0)), meta, slug))
    blocks = []
    for series, items in sorted(lg.items(), key=lambda kv: min(m.get("date","") for _, m, _ in kv[1])):
        rows = "".join(
            f'<a class="item" href="a/{slug}.html"><span class="no">{meta.get("number","")}</span>'
            f'<span class="t">{html.escape(meta.get("title",slug))}</span>'
            f'<span class="d">{meta.get("date","")}</span></a>'
            for _, meta, slug in sorted(items))
        blocks.append(f'<div class="series"><h2>{html.escape(series)}</h2>{rows}</div>')
    list_html = page("文章", "全部文章", '<div class="list">' + "".join(blocks) + "</div>",
                     "list", h1="文章", meta_line=f"共 {len(loose)} 篇 · 按栏目归类")
    (ROOT / "list.html").write_text(list_html, encoding="utf-8")

    # 课程路径页 learn.html（P2）：课表流 + 轻搜索 + 空结果逃生口
    n_course = sum(1 for k, *_ in arts if k == "course")
    ordered = sorted(course_groups.items(),
                     key=lambda kv: min(m.get("date", "") for _, m, _ in kv[1]))
    blocks = []
    for series, items in ordered:
        rows = "".join(
            f'<a class="item" data-t="{html.escape((meta.get("title","")+"|"+series+"|"+str(meta.get("number",""))+"|课"+str(meta.get("number",""))).lower())}"'
            f' href="a/{slug}.html"><span class="no">{int(meta.get("number",0)):02d}</span>'
            f'<span class="t">{html.escape(meta.get("title",slug))}</span>'
            f'<span class="d">{meta.get("date","")}</span></a>'
            for _, meta, slug in items)
        blocks.append(f'<div class="series" data-series><h2>{html.escape(series)}</h2>{rows}</div>')
    learn_body = (
        f'<input class="search" id="q" placeholder="搜课名或课号，比如：后悔药、3（按 / 直达）">'
        f'<div class="hint">标题与课号即时匹配，正文不参与搜索</div>'
        f'<div id="courses">{"".join(blocks)}</div>'
        f'<div class="empty hide" id="empty">没有匹配「<span id="ekw"></span>」的课。<br><br>'
        f'试试 <span class="go" id="c1">后悔药</span>？或者 <span class="go" id="c2">清空搜索</span> 看全部 {n_course} 课</div>'
    )
    extra = ".empty.hide,.hide{display:none}"
    learn_html = page("课程", "VIBE CODING 上手课", learn_body, "learn",
                      h1="跟课学 Vibe Coding", meta_line=f"共 {n_course} 课",
                      extra_style=extra) + ""
    learn_html = learn_html.replace("</body>", f"<script>{SEARCH_JS}</script></body>")
    (ROOT / "learn.html").write_text(learn_html, encoding="utf-8")

    # 关于页
    about_body = """<article>
<p>这里是叮叮猫儿Lab。漫游数字世界，实验 AI 与互联网。</p>
<p>不追概念，不喊口号。把新工具、新模型真的用一遍，同步新鲜动态与实践思考。</p>
<h2>这个站</h2>
<p>它跟着「Vibe Coding 上手课」一起长。课程做到哪，它就长到哪。博客放想法，教程放步骤，都归在一个域名下。</p>
<p>整站纯静态，用 AI 一行一行写出来。慢一点，但想清楚。</p>
</article>"""
    (ROOT / "about.html").write_text(page("关于", "关于", about_body, "about", h1="关于叮叮猫儿Lab"), encoding="utf-8")

    print(f"built {len(arts)} articles ({n_course} course) -> a/ ; list.html ; learn.html ; about.html")
    for s, items in ordered:
        print(f"  [{s}] {len(items)} 课: " + ", ".join(str(n) for n, _, _ in items))


if __name__ == "__main__":
    main()
