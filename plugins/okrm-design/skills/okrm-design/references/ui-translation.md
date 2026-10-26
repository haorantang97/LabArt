# 界面翻译

把方法翻译到网页与产品界面。原则不变：装置来自内容，普遍语言，经济即形式，序列阅读。变化的是材料：
系统字体、浏览器默认、断点、状态、交互。

## 1. 证据

- 工作室自身网站：Helvetica/Arial 栈作正文，Times 的小字号版本作第二声部，系统等宽作第三；字号用 vw
  （3.75vw、2.55vw、1.5vw）；黑白；一页式；`(Info)`／`(Information)` 文字开关；作品以 `1 / 31` 计数器
  翻页，每张图配一行题注。
- 艺博会网站：「用户与系统的体验由越来越共同的一套符号、记号与命名定义」→ 页面、按钮、链接与过渡做成**夸张的界面**，
  「隐含的变成显性的」。
- 出版分销商网站：网格式响应布局、清晰导航、照片拍法一致；线上用衬线、印刷用无衬线——「反转惯例」。
- 电子书封面：「无尺度」，要在购物页缩略图和海报上同时成立。

## 2. 从内容找装置

| 内容类型 | 装置 | 字面化 |
| --- | --- | --- |
| 档案、藏品、出版目录 | 索引／编号 | 编号即导航；列表是表格；每条有编号与题注；`0001–0144` 计数器做页眉 |
| 工作室或作品集 | 幻灯片／计数器 | 一页；`1 / N`；`(Info)` 文字开关；每张图一行题注 |
| 期刊、文章 | 页序／折页 | 滚动段落像翻页；断点是对折；期号与「情绪」做固定项与变动项 |
| 工具、仪表盘 | 表格与文件 | 数值与标签用表格线；标签用题注声部；网格显形 |
| 日程、流程 | 清单 | 清单就是界面；完成项划掉；当前项用位置而非颜色 |
| 阅读器 | 打字稿／剧本 | 正文窄列；元数据像舞台指示放在页边 |

装置陈述同样必须写出。

## 3. 隐含变显性

把界面自己的语汇写成文字：

- 按钮是带括号或方括号的文字：`(Info)`、`[Index]`、`(close)`、`add to cart`。
- 状态是文字：`1 / 31`、`Reading · 31%`、`0 items`、`no images loaded`。
- 链接用下划线或括号，不用图标；图标只在它本身是现成物（箭头 `→`、`↗`）时出现。
- 过渡可以被「夸张」：切换时整屏换一个平涂颜色，或显示 `Loading` 字样，而不是淡入淡出。

## 4. 秩序表（token）

先用 `scripts/tokens.py` 生成，再写组件：

```sh
python3 scripts/tokens.py generate --medium web --base 16 \
  --sans "Helvetica Neue, Helvetica, Arial, sans-serif" --serif "Times New Roman, Times, serif" \
  --field "#1F3FBF" --columns 4 --out tokens.css --json tokens.json
python3 scripts/tokens.py check tokens.json
```

token 的含义：

- `--font-sans`、`--font-serif`／`--font-mono`：至多两个声部；
- `--size-caption / body / lead / label / monument`：两极尺度；`label` 是字距放宽的小字，`monument` 是一个词或
  一个数字的尺度（默认正文的 8 倍，网页上建议改用 vw）；
- `--tracking-label`、`--tracking-monument`：字距；
- `--space-*`：由正文行高派生；
- `--grid-columns`、`--grid-gutter`、`--measure`：折法派生的栏数与行长；
- `--border-plate`、`--border-poster`：图版白边（10%）与海报白边（3%）；
- `--paper`、`--ink`、`--field`：纸白、墨黑、一个作为材料的平涂颜色；
- `--rule`：细线，表格与图表只用这一种线。

`check` 拒绝：超过两个家族、纪念碑级不足正文 8 倍、题注不在正文的 0.7–1.0 倍、第二个颜色、对比不足、
默认 12 栏、行长超出 45–75 字符。它不检查装置，装置只能由人验收。

## 5. 组件翻译

| 印刷元素 | 界面组件 | 规则 |
| --- | --- | --- |
| 索引、目录 | 导航 | 文字列表或字母索引；当前项用下划线或位置，不用底色块 |
| 表格 | 列表 | 一行一条，细线分隔，列对齐；不用卡片墙 |
| 页码、编号 | 计数器、ID | 等宽或衬线声部；`1 / N` 固定在页眉或页脚 |
| 题注 | 元数据 | 一行，贴着内容；时间戳、作者、来源都是题注 |
| 书脊上的句子 | 页面标题 | 标题可以是一句话，正文尺度，不放大 |
| 一个词的封面 | 空状态或首屏 | 一个词放到纪念碑尺度，其余为空 |
| 折页 | 展开区 | 展开是一次「折出」，内容尺度可以跳变 |
| 换纸 | 整屏换色 | 用一个平涂颜色切换整屏，不用卡片阴影 |
| 白边图版 | 图像容器 | 白边 10% 或满版；不加圆角与阴影 |
| 标签 | 徽章、标记 | 居中、小型大写、字距放宽、细线框 |

### 按钮与表单

- 主要操作：墨黑底纸白字，无圆角（≤ 2 px）；次要操作：带括号的文字。
- 表单标签用题注声部放在字段上方；字段是一条底线或细线框；错误信息是一行文字，紧贴字段。
- 不用渐变、投影、发光。

### 空状态、加载、错误

- 文字：`No entries.`、`Loading 12 of 144.`、`Could not connect. Retry.` 不用插画。
- 加载指示可以是计数器或一条细线。
- 错误不改变版面结构。

### 动效

- 切换，或 ≤ 150 ms 的线性过渡。
- 不用弹跳、缩放进入、视差。
- 唯一允许的表演是装置本身，且只有一处。
- `prefers-reduced-motion` 下全部关闭。

## 6. 响应式即折法

- 从最大版面开始；每个断点是**对折**：四栏变两栏，两栏变一栏；语义不重排，只换折法。
- 纪念碑级在小屏上仍然纪念碑：用 vw 定义，它可以占满屏幕宽。
- 行长保持 45–75 字符；通过改变列宽，不通过缩小字号。
- 导航在小屏上仍是文字索引：折叠成一行或可展开的清单。

## 7. 经济决定

每个界面项目至少写出：

- 字体：系统字体栈，还是一个自托管家族；理由。
- 图像：是否无图加载；图版规则；题注是否替代缩略图。
- 组件库：用平台组件并覆盖样式，还是从 token 自建。
- 性能：首屏是否纯文本；动效是否可关闭。
- 断点：几次对折；每次折的栏数。

## 8. 无障碍是秩序的一部分

- 文字与纸色对比 ≥ 4.5:1；平涂颜色上的文字也 ≥ 4.5:1，否则该颜色不承载文字。
- 题注声部 ≥ 12 px（网页）或 11 pt（移动）。
- 焦点可见：细线框或下划线。
- 计数器与编号有可读的文本语义。
- 索引可键盘遍历；表格有表头语义。

## 9. HTML/CSS 骨架

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Index</title>
<link rel="stylesheet" href="tokens.css">
<style>
  html { background: var(--paper); color: var(--ink); font-family: var(--font-sans); }
  body { margin: 0; padding: var(--space-2); }
  .furniture { position: sticky; top: 0; display: flex; justify-content: space-between;
               font-family: var(--font-serif); font-size: var(--size-caption); padding-bottom: var(--space-1);
               border-bottom: var(--rule) solid var(--ink); background: var(--paper); }
  .furniture a { color: inherit; text-decoration: none; }
  h1 { font-size: var(--size-body); font-weight: 400; margin: var(--space-3) 0; max-width: var(--measure); }
  .monument { font-size: 18vw; line-height: 0.85; letter-spacing: var(--tracking-monument); font-weight: 500; margin: var(--space-3) 0; }
  nav { display: flex; flex-wrap: wrap; gap: 0 var(--space-1); border-top: var(--rule) solid var(--ink); padding-top: var(--space-1); }
  nav a { color: inherit; text-decoration: none; }
  nav a[aria-current="page"] { text-decoration: underline; }
  table { width: 100%; border-collapse: collapse; margin-top: var(--space-3); }
  th { text-align: left; font-weight: 400; font-family: var(--font-serif); font-size: var(--size-caption); padding: var(--space-1) 0; border-bottom: var(--rule) solid var(--ink); }
  td { padding: var(--space-1) 0; border-bottom: var(--rule) solid var(--ink); vertical-align: top; }
  td.n { font-family: var(--font-serif); width: 6ch; }
  .plate { padding: var(--border-plate); background: var(--paper); }
  .plate img { display: block; width: 100%; }
  .field { background: var(--field); color: var(--paper); padding: var(--space-3) var(--space-2); }
</style>
</head>
<body>
  <header class="furniture"><a href="#">Index</a><span>0001–0144</span><a href="#info">(Info)</a></header>
  <h1>This site is an index. Every entry is numbered, so the number is the navigation.</h1>
  <div class="monument">F</div>
  <nav aria-label="Index"><a href="#a">A</a><a href="#f" aria-current="page">F</a><a href="#z">Z</a></nav>
  <table><thead><tr><th>No.</th><th>Title</th><th>Year</th></tr></thead>
    <tbody><tr><td class="n">0061</td><td>First entry</td><td>2017</td></tr></tbody></table>
</body>
</html>
```

这个骨架只展示秩序如何落到 CSS：标题是一句话，纪念碑是一个字母，导航是文字索引，表格是列表，颜色是整块材料。
内容与装置必须按项目重写；不要把它当成品。
