# 网站项目规矩（另起炉录 · 个人博客+教程站）

## 这是什么
一个纯静态的个人网站，跟着「Vibe Coding 上手课」一起长。博客放想法，教程放步骤。

## 硬规矩
- 纯静态：访客拿到的永远是 HTML 文件，无后端、无数据库、无运行时 AI 调用。
- AI 只在生产过程帮忙（写代码、生成摘要），产物写死进页面。
- 文章用 Markdown 写在 articles/，顶部 frontmatter 必含 title/series/number/date。
- series 字段决定归进哪个书架（上手课/讲清/未来系列），不要写死系列。
- 风格：温暖克制，纸感底色 + 炉火暖色（#d8551f），不花哨。改样式保持这套变量。

## 结构
- index.html        主页
- articles/*.md     文章源（frontmatter + 正文）
- build.py          静态生成器：md → html
- a/*.html          生成的文章页
- list.html         栏目页（按 series 归类）
- about.html        关于页

## 命令
- 生成全站：python build.py
- 改完文章重新跑 build.py 即可

## 不要做
- 不要引入框架/构建工具链（保持单文件可懂）
- 不要把密钥写进任何前端文件
- 不要加运行时后端
