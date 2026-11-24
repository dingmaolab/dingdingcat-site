---
title: 第4课｜GitHub：代码头一次离开这台电脑
kind: course
series: 上手课
chapter: 打底
number: 4
date: 2026-11-21
tags: [vibe coding, 教程]
---

上节课你学会了存档。但那些存档全躺在你这台电脑的 `.git` 文件夹里——硬盘坏了，存档跟着作品一起没。这一课把存档托到网上，顺便把 GitHub 一次讲明白：它是什么、怎么用、配好之后你能拿它干什么。

本文按你实际会遇到的顺序走：第①节一句话认清 GitHub；第②节讲隐私开关和一条红线；第③节把 SSH 配好，配没配好有明确信号；第④节四步把代码推上去；第⑤节讲推上去能干什么、什么时候用另一条路。

## 本课目标

- 说清 GitHub 是什么、能干什么、不干什么
- 建好你的头一个远端仓库，把代码推上去
- 拿到一条能发给任何人的代码链接
- 看到 SSH 的成功回音时，知道那是好消息不是坏消息

## 概念卡

- **本地仓库 / 远端仓库**：上节课的 `.git` 是本地仓库，在你机器上；远端仓库是同一个仓库放在 GitHub 服务器上的那份。`git push` 就是把本地新存档传上去。
- **Public / Private**：建仓时的一个开关。Public 全世界可见，Private 只有你邀请的人可见。
- **SSH key**：让你电脑和 GitHub 互相认识的钥匙对。私钥自己留着，公钥交给 GitHub。配好之后推送不用再输密码。

## ① GitHub 是什么

一句话：**GitHub 是托管 git 仓库的网站。** git 管版本，GitHub 管托管——两者不是一个东西，新手最容易在这里搅在一起。

它干三件事：

1、**备份。** 你这份存档在它的服务器上有一份影子，电脑炸了影子还在。
2、**发布。** 朋友、面试官、未来的你，点开一条链接就能看。
3、**协作。** 别人基于你的代码改，双方改动能合回去。

第三件你现在用不到，前两件今天就能拿到。

![课4示意图：左边你这台电脑里的本地仓库，中间 git push 单向搬运，右边 GitHub 服务器上的远端仓库；远端那份可以生成一条链接发给任何人](课4本地远端示意图.png)

## ② 我的代码放上去，会不会谁都能看

看开关。选 Public，确实全世界可见——GitHub 上无数开源项目就是这么公开的，这是它的名声所在。但你不是非公开不可：选 Private，除了你授权的人，谁都进不来。

这门课的仓库，我建议先 Private，等网站要做公开展示再换。

有一条红线不分 Public Private，先立在这里：**密钥永远不进仓库。** 你第 1 课那把 DeepSeek key，在任何情况下都不该出现在被 git 记录的文件里。这一课你还没碰它，后面的课会专门讲怎么防。

## ③ 让 GitHub 认识你这台电脑

两条路：HTTPS 加令牌，或者 SSH 密钥。这门课走 SSH——一次配好长期清净，而且 Windows、Mac 命令一样。

| 步骤 | 命令 / 操作 | 应看到 |
|---|---|---|
| 生成钥匙对 | `ssh-keygen -t ed25519`（PowerShell 或「终端」里跑，一路回车，三个问题都用默认值） | 输出里出现 `Your public key has been saved in ...`，并且多出一个 `.pub` 结尾的文件 |
| 取出公钥内容 | `cat ~/.ssh/id_ed25519.pub`（PowerShell 用 `Get-Content`） | 一整行，以 `ssh-ed25519` 开头，结尾是你的机器名 |
| 交给 GitHub | 网页右上角头像 → Settings → SSH and GPG keys → New SSH key，粘贴那一整行 | 列表里出现你刚加的 key，带着今天日期 |
| 验证 | `ssh -T git@github.com` | `Hi 你的用户名! You've successfully authenticated, but GitHub does not provide shell access.` |

我这台机器收到的回音是（写这课之后的第二天，GitHub 账号改成了新名字，这是改名后重测的现行输出）：

```
Hi dingmaolab! You've successfully authenticated, but GitHub does not provide shell access.
```

新手看到后半句 `does not provide shell access` 容易心里一沉，以为哪里配砸了。恰恰相反——**它认出了你的名字，这就是配对成功**。GitHub 故意不给你命令行入口，只留 git 通道。这句话是好消息，不是坏消息。

（如果你更习惯图形界面：VS Code 装好扩展后也能带你走一遍登录授权，殊途同归。下面继续按终端讲。）

## ④ 把代码推上去

**第一步，在 GitHub 网页建仓库。** 登录后点 New repository，名字起一个（我建的网站仓库就叫 `dingdingcat-site`），选 Private，**下面那几个"初始化"的勾全部不要选**——让仓库是个空盒子，我们再把本地历史整个装进去。

这条不是洁癖。GitHub 在新仓库引导页上给你的那几行命令（`echo` 一个 README、`git init`）是为**全新空项目**准备的剧本；你上节课已经有完整历史了，照着抄会多出一个孤儿提交，后面还得清理。你只需要下面两条。

| 步骤 | 命令 | 应看到 |
|---|---|---|
| 对齐默认分支 | `git branch -M main` | 无输出；`git branch` 那一行前面是 `* main` |
| 告诉本地远端在哪 | `git remote add origin git@github.com:dingmaolab/仓库名.git` | 无输出（没消息就是好消息） |
| 推 | `git push -u origin main` | `* [new branch] main -> main` |
| 复核 | `git ls-remote origin HEAD` | 一串提交号，和 `git log` 最上面那个一致 |

`origin` 是远端的绰号，默认都这么叫；`-u` 的意思是"以后这个分支的默认远端就是它"，下次只打 `git push` 两个词就行。

我这一晚的真实顺序：先跑了 `git push -u origin master`，被 GitHub 顶回来——它新建仓库默认分支叫 `main`，我本地还叫 `master`。改完分支名重推就过了。这条坑已经写进下面的"卡住了"，你多半也会撞上，撞上是正常的。

**最后打开浏览器**刷新仓库页面：文件整整齐齐挂在那里，点 Commits，上节课存的每一版快照都在，`58a3f4b` 那个号原样可见。代码头一次离开这台电脑，就是这么一个刷新的距离。

## ⑤ 什么时候用它，什么时候用另一条路

| 场景 | 走哪条 |
|---|---|
| 自己的机器，长期用 | SSH，一次配好不用再管 |
| 公司电脑 / 装环境受限，动不了密钥 | HTTPS 加令牌 |
| 临时在别人机器上拉一次代码 | HTTPS，用完就走 |
| 要给某个部署系统单独授权（只读、只给这一个仓库） | deploy key——它是 SSH 的窄口子用法，本课不装，知道有这东西就行 |

推上去之后马上能用的三样：把仓库链接发给任何人，对方能看到你的项目和历史；换电脑了，`git clone` 一条命令把全部家当带过去；以及，它给这门课后半段埋好了路——第 14 课我们把网页直接从这个仓库发布成一个真正的网站域名，今天推上去的东西，到时候就是网站的骨架。

## 跟做步骤

1. 跑 ③ 的四步，最后 `ssh -T git@github.com` 收到 `Hi 你的用户名!` 再往下
2. 网页 New repository：起名字、选 Private、初始化勾全选无
3. 按 ④ 的表逐行走，每走一行看一眼"应看到"那列
4. `git push -u origin main` 出现 `[new branch]` 后，浏览器刷新仓库页
5. 对照 `git log` 和网页上的 Commits，提交号能对上

## 及格标准

你手里有一条能打开的仓库链接，里面的提交历史和 `git log` 对得上；并且 `ssh -T` 那句回音，你能说出它是好消息。

## 卡住了

- **push 报 permission denied (publickey)**：公钥没加到 GitHub，或者贴错了文件（只该贴 `.pub` 那个，私钥永远不出机器）
- **remote origin already exists**：之前设过。跑 `git remote set-url origin 新地址` 改掉即可，不用慌
- **push 被拒，说远端有本地没有的东西**：多半是建仓库时勾了初始化（README 之类）。最省事：删掉远端仓库重建，记得不勾；或者 `git pull --rebase` 先合下来
- **提示 master 推不上去**：GitHub 新建仓库默认分支是 main，老 git 默认 master。`git branch -M main` 改名再推，一次解决（我 11-21 当晚撞的就是这条）

## 轮到你了

故意在本地改点东西、提交、push，再刷新 GitHub 页面看那版新快照出现。你在自己电脑上敲的每一版，云上都有一份影子——这个感觉走一遍就够。

下节课开始一个转折：前面四课都是"给 AI 备家伙"，从第 5 课起，轮到 AI 学规矩了。头一个规矩工具，叫 grill-me。

## 深入读

- GitHub 官方 SSH 配置指引：https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- git remote 官方手册：https://git-scm.com/docs/git-remote

## 本课账单

- 时间：SSH 配置加建仓推送，新手预留一小时
- 费用：GitHub 免费额度足够；token 消耗只发生在让 AI 陪你排查的时候，忽略不计
- 图一张为课内自制示意；`ssh -T` 成功回音的终端实拍，留给作者晨间截图补链
