---
title: 第4课｜GitHub：代码头一次离开这台电脑
kind: course
series: 上手课
chapter: 打底
number: 4
date: 2026-11-21
tags: [vibe coding, 教程]
---

上一课你学会了存档。但那些存档全躺在你这台电脑的 `.git` 文件夹里。硬盘坏了，存档跟着作品一起没。这一课把存档托到网上去，顺便把 GitHub 这个东西一次讲明白。

形式换成问答。五个问题，是新手对 GitHub 最常有的五个疑问。每个我都用真跑过的操作回答。

## 本课目标

- 说清 GitHub 是什么、能干什么、不干什么
- 建好你的头一个远端仓库，把代码推上去
- 拿到一条能发给任何人的代码链接

## 概念卡

- **本地仓库 / 远端仓库**：上一课的 `.git` 是本地仓库，在你机器上。远端仓库是同一个仓库放在 GitHub 服务器上的那份。`git push` 就是把本地的新存档传上去。
- **Public / Private**：建仓时的一个开关。Public 全世界可见，Private 只有你邀请的人可见。
- **SSH key**：让你电脑和 GitHub 互相认识的钥匙对。一把自己留着（私钥），一把交给 GitHub（公钥）。配好之后，推送不用再输密码。

## 问答正文

### Q1：GitHub 到底是个什么东西？

一句话：**GitHub 是托管 git 仓库的网站。** 上一课说过，git 管版本，GitHub 管托管。

打个完整点的比方：git 是游戏的存档功能，GitHub 是那个云存档服务器，顺便还是个广场。它干三件事：给你备份（电脑炸了存档还在）；给你发布（朋友、面试官、未来的你，点开链接就能看）；给你协作（别人基于你的代码改，双方改动能合回去）。

你现在用不到第三件，但前两件，今天就能拿到。

### Q2：我的代码放上去，会不会谁都能看？

看开关。建仓库时选 Public，确实全世界可见——GitHub 上无数开源项目就是这么公开的，这是它的名声所在。但你不是非公开不可：选 Private，除了你授权的人，谁都进不来。

这门课的仓库，我建议先 Private，等网站要做公开展示再换。

有一条红线不分 Public Private，先立在这里：**密钥永远不进仓库。** 你第 1 课那把 DeepSeek key，在任何情况下都不该出现在被 git 记录的文件里。这一课你还没碰它，后面的课会专门讲怎么防。

### Q3：怎么让 GitHub 认识我这台电脑？

两条路：HTTPS 加令牌，或者 SSH 密钥。我用 SSH，一次配好长期清净。

过程两步。你电脑上生成一对钥匙（PowerShell 跑 `ssh-keygen -t ed25519`，一路回车）；然后把公钥的内容复制到 GitHub 网页 Settings → SSH keys 里。

配好之后验证，跑：

```powershell
ssh -T git@github.com
```

我这台机器收到的回音是：

```
Hi qiluluai! You've successfully authenticated, but GitHub does not provide shell access.
```

新手看到 `does not provide shell access` 容易心里一沉，以为哪里配砸了。恰恰相反——**它认出了你的名字，这就是配对成功**。GitHub 故意不给你命令行入口，只留 git 通道。这句话是好消息，不是坏消息。

（如果你更习惯图形界面：VS Code 装好扩展后也能带你走一遍登录授权，殊途同归。下面继续按终端讲。）

### Q4：怎么把代码真正推上去？

四步，我在自己电脑上走通的全过程：

**第一步，在 GitHub 网页建仓库。** 登录后点 New repository，名字起一个（我建的网站仓库就叫 `dingdingcat-site`），选 Private，**下面那几个"初始化"的勾全部不要选**——让仓库是个空盒子，我们再把本地历史整个装进去。

**第二步，告诉本地仓库远端在哪。** 在你的项目文件夹里：

```
git remote add origin git@github.com:你的用户名/dingdingcat-site.git
```

`origin` 是远端的绰号，默认都这么叫。

**第三步，推。**

```
git push -u origin master
```

`-u` 的意思是"以后这个分支的默认远端就是它"，下次只打 `git push` 两个词就行。

**第四步，打开浏览器。** 刷新仓库页面，你的文件整整齐齐挂在那里；点 Commits，上一课存的每一版快照都在，`58a3f4b` 那个号原样可见。代码头一次离开这台电脑，就是这么一个刷新的距离。

### Q5：推上去之后，我能拿它干什么？

三样马上能用的：把仓库链接发给任何人，对方能看到你的项目和历史；换电脑了，`git clone` 一条命令把全部家当带过去；以及，它给这门课后半段埋好了路——第 14 课我们把网页直接从这个仓库发布成一个真正的网站域名，今天推上去的东西，到时候就是网站的骨架。

## 跟做步骤

1. 注册/登录 GitHub，生成 SSH key 并在网页添加，`ssh -T git@github.com` 收到 Hi 你的用户名 即通
2. 网页 New repository：起名字、选 Private、初始化勾全选无
3. 在项目文件夹 `git remote add origin git@github.com:用户名/仓库名.git`
4. `git push -u origin master`
5. 浏览器刷新仓库，确认文件和提交历史都在

## 及格标准

你手里有一条能打开的仓库链接，里面的提交历史和 `git log` 对得上；而且 `ssh -T` 那句回音，你能说出它是好消息。

## 卡住了

- **push 报 permission denied (publickey)**：公钥没加到 GitHub，或者加的是私钥（只贴 `xxx.pub` 那个文件的内容）。重看 Q3 第二步。
- **remote origin already exists**：之前设过。跑 `git remote set-url origin 新地址` 改掉即可，不用慌。
- **push 被拒，说远端有本地没有的东西**：多半是建仓库时勾了初始化（README 之类）。最省事：删掉远端仓库重建，记得不勾；或者用 `git pull --rebase` 先合下来。
- **master 推不上去，提示 main**：GitHub 新建默认分支叫 main，老 git 默认 master。跑 `git branch -M main` 改名再推，一次解决。

## 轮到你了

故意在本地改点东西、提交、push，再刷新 GitHub 页面看那版新快照出现。存档上云的感觉走一遍：你在自己电脑上敲的每一版，云上都有一份影子。

下一课开始一个转折：前面四课都是"给 AI 备家伙"，从第 5 课起，轮到 AI 学规矩了。头一个规矩工具，叫 grill-me。

## 深入读

- GitHub 官方 SSH 配置指引：https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- git remote 官方手册：https://git-scm.com/docs/git-remote

## 本课账单

- 时间：SSH 配置加建仓推送，新手预留一小时
- 费用：GitHub 免费额度足够；token 消耗只发生在让 AI 陪你排查的时候，忽略不计
