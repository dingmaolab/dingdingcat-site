# 网站项目规矩（叮叮猫儿Lab · 个人博客+教程站）

## 这是什么
一个纯静态的个人网站，跟着「Vibe Coding 上手课」一起长。博客放想法，教程放步骤。

## 硬规矩
- 纯静态：访客拿到的永远是 HTML 文件，无后端、无数据库、无运行时 AI 调用。
- AI 只在生产过程帮忙（写代码、生成摘要），产物写死进页面。
- 文章用 Markdown 写在 articles/，顶部 frontmatter 必含 kind/title/series/number/date。
- 门面 chrome（导航/页脚/统计行）零更新承诺词（双周/每周/首发/已发布N 类），正文引用豁免。
- series 字段决定归进哪个书架（在架：上手课；随想等散装用同名 series 自动开架），不要写死系列。
- 风格：温暖克制，纸感底色 + 炉火暖色（#d8551f），不花哨。改样式保持这套变量。

## 结构
- index.html        主页（build 生成，Now Page，手写版已退役）
- articles/*.md     文章源（frontmatter 必含 kind: course|post|gallery）
- build.py          静态生成器：md → html（未知 kind 显式报错拒绝静默）
- learn.html        课程路径页（build 生成：课表流+轻搜索+翻页链）
- list.html         文章区（build 生成：散装单篇+栏目 chips）
- gallery.html      图文区（build 生成：3:4 书架，空架有兜底文案）
- a/*.html          生成的文章页（课程页带上一课/下一课）
- about.html        关于页

## 命令
- 生成全站：python build.py
- 改完文章重新跑 build.py 即可

## 不要做
- 不要引入框架/构建工具链（保持单文件可懂）
- 不要把密钥写进任何前端文件
- 不要加运行时后端
