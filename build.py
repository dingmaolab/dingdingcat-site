# -*- coding: utf-8 -*-
"""另起炉录 · 静态站点生成器。md 文章 → html 页面。无框架，单文件可懂。"""
import re, html, io
from pathlib import Path

ROOT = Path(__file__).parent
ART = ROOT / "articles"
OUT = ROOT / "a"

STYLE = """
:root{--paper:#f7f2ea;--ink:#211a14;--muted:#8a7d6d;--ember:#d8551f;--line:#e4dac9;--card:#fffdf9}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:var(--paper);color:var(--ink);
line-height:1.9;background-image:radial-gradient(rgba(33,26,20,.035) 1px,transparent 1.3px);background-size:26px 26px}
.wrap{max-width:720px;margin:0 auto;padding:0 28px}
nav{padding:34px 0;display:flex;align-items:center;gap:22px;border-bottom:1px solid var(--line)}
nav .b{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:3px;font-size:17px;margin-right:auto}
nav .mark{width:24px;height:24px;border-radius:50%;background:radial-gradient(circle at 50% 62%,#ffd9a0,var(--ember) 58%,#9a3410)}
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
article blockquote{border-left:3px solid var(--ember);background:var(--card);padding:12px 18px;margin:0 0 20px;color:#5a4d3d;border-radius:0 8px 8px 0}
article ul{margin:0 0 20px 22px}article li{margin:6px 0}
article strong{color:var(--ink)}
.list{padding:20px 0 50px}
.series{margin-bottom:36px}
.series h2{font-size:15px;letter-spacing:3px;color:var(--muted);margin-bottom:14px}
.series h2::before{content:"";display:inline-block;width:18px;height:2px;background:var(--ember);vertical-align:4px;margin-right:10px}
.item{display:flex;gap:16px;padding:14px 0;border-bottom:1px dashed var(--line);text-decoration:none;color:var(--ink)}
.item:hover .t{color:var(--ember)}
.item .no{font-family:Consolas,monospace;color:var(--ember);font-size:13px;flex:none;width:40px;padding-top:3px}
.item .t{font-size:16px;font-weight:600}
.item .d{margin-left:auto;color:var(--muted);font-size:12px;font-family:Consolas,monospace;flex:none;padding-top:4px}
footer{padding:34px 0 60px;border-top:1px solid var(--line);color:var(--muted);font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
footer .no{font-family:Consolas,monospace;color:var(--ember)}
@media(max-width:560px){h1{font-size:28px}}
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
        if ln.startswith("### "):
            out.append("<h3>" + inline(ln[4:]) + "</h3>"); i += 1
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
            buf = []
            while i < n and lines[i].strip() and not re.match(r"^(#|> |- )", lines[i]):
                buf.append(inline(lines[i])); i += 1
            out.append("<p>" + " ".join(buf) + "</p>")
    return "\n".join(out)


def page(title, kicker, content, active, h1=None, meta_line=""):
    nav = ""
    for href, label, key in [("index.html", "主页", "home"), ("list.html", "文章", "list"), ("about.html", "关于", "about")]:
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
<title>{html.escape(title)} · 另起炉录</title><style>{STYLE}</style></head><body><div class="wrap">
<nav><span class="b"><span class="mark"></span>另起炉录</span>{nav}</nav>
{head}{content}
<footer><span>另起炉录 · 慢慢探索，沉淀思考与实践</span><span class="no">est. 2026</span></footer>
</div></body></html>"""


def main():
    OUT.mkdir(exist_ok=True)
    arts = []
    for f in sorted(ART.glob("*.md")):
        meta, body = parse(f.read_text(encoding="utf-8"))
        arts.append((meta, body, f.stem))
        slug = f.stem
        content = "<article>" + md(body) + "</article>"
        ml = f'{meta.get("series","")} · 第 {meta.get("number","")} 篇 · {meta.get("date","")}'
        html_out = page(meta.get("title", slug), meta.get("series", "文章"),
                        content, "list", h1=meta.get("title", slug), meta_line=ml)
        (OUT / f"{slug}.html").write_text(html_out, encoding="utf-8")

    # 栏目页：按 series 归类
    groups = {}
    for meta, body, slug in arts:
        groups.setdefault(meta.get("series", "未分类"), []).append((meta, slug))
    blocks = []
    for series, items in groups.items():
        rows = ""
        for meta, slug in sorted(items, key=lambda x: x[0].get("number", "0")):
            rows += (f'<a class="item" href="a/{slug}.html">'
                     f'<span class="no">{meta.get("number","")}</span>'
                     f'<span class="t">{html.escape(meta.get("title",slug))}</span>'
                     f'<span class="d">{meta.get("date","")}</span></a>')
        blocks.append(f'<div class="series"><h2>{html.escape(series)}</h2>{rows}</div>')
    list_html = page("文章", "全部文章", '<div class="list">' + "".join(blocks) + "</div>",
                     "list", h1="文章", meta_line=f"共 {len(arts)} 篇 · 按系列归类")
    (ROOT / "list.html").write_text(list_html, encoding="utf-8")

    # 关于页
    about_body = """<article>
<p>这里是另起炉录。一个在 AI 变革里躬身试新的人。</p>
<p>不追概念，不喊口号。把新工具、新模型真的用一遍，写清楚能不能用、卡在哪、值不值得。</p>
<h2>这个站</h2>
<p>它跟着「Vibe Coding 上手课」一起长。课程做到哪，它就长到哪。博客放想法，教程放步骤，都归在一个域名下。</p>
<p>整站纯静态，用 AI 一行一行写出来。慢一点，但想清楚。</p>
</article>"""
    (ROOT / "about.html").write_text(page("关于", "关于", about_body, "about", h1="关于另起炉录"), encoding="utf-8")

    print(f"built {len(arts)} articles -> a/ ; list.html ; about.html")
    for meta, body, slug in arts:
        print(f"  [{meta.get('series','')}/{meta.get('number','')}] {meta.get('title','')}")


if __name__ == "__main__":
    main()
