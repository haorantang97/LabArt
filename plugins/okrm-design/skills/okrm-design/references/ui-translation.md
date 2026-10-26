# 界面翻译

把印刷的秩序翻译到网页与产品界面。原则不变：装置来自内容，排印是骨干，经济即形式，阅读是序列。
变化的是材料：系统字体、浏览器默认、断点、状态、交互。

## 1. 从内容找装置

界面的既有物比印刷更多：内容类型（档案、目录、期刊、工具）、用户要完成的序列、数据本身的结构
（时间、编号、字母、层级）、平台约束（系统字体、组件库、性能预算）。

常见装置：

| 内容类型 | 装置 | 字面化 |
| --- | --- | --- |
| 档案、藏品、出版物目录 | 索引 | A–Z 或编号导航；列表是表格；每条有编号与题注 |
| 期刊、文章 | 页序 | 滚动段落像翻页；大页码或章节号做家具；断点是对折 |
| 工具、仪表盘 | 表格与计数 | 数值做大；标签用题注声部；网格显形 |
| 日程、流程 | 时间表 | 时间列是版面；当前时刻用强调色；步骤编号是家具 |
| 阅读器 | 边注 | 元数据贴在页边；正文窄列；题注与正文两个声部 |

装置陈述同样必须写出：「这个产品是 Y，所以界面做 Z。」

## 2. 秩序表（token）

先用 `scripts/tokens.py` 生成，再写组件：

```sh
python3 scripts/tokens.py generate --medium web --base 16 --sans "Helvetica Neue, Helvetica, Arial, sans-serif" \
  --serif "Times New Roman, Times, serif" --accent "#FFE600" --columns 4 --out tokens.css --json tokens.json
python3 scripts/tokens.py check tokens.json
```

生成的 token 包含：

- `--font-sans`、`--font-serif`（或 `--font-mono`）：最多两个家族；
- `--size-caption / body / lead / subhead / display / giant`：至少跨三个量级；
- `--space-*`：由正文行高派生的间距阶梯；
- `--grid-columns`、`--grid-gutter`、`--measure`：由折法派生的栏数与行长；
- `--ink`、`--paper`、`--accent`：纸白墨黑加一个强调色；
- `--rule`：细线粗细，表格与分隔只用这一种线。

`check` 会拒绝：超过两个字体家族、尺度阶梯不足三个量级、超过一个强调色、强调色与纸色对比不足。

## 3. 组件翻译

| 印刷元素 | 界面组件 | 规则 |
| --- | --- | --- |
| 目录、索引 | 导航 | 文字列表或字母索引；不用图标栏；当前项用强调色或下划线，不用底色块 |
| 表格 | 列表 | 一行一条，细线分隔，列对齐；不用卡片墙；可排序列在表头用题注声部标出 |
| 页码、编号 | 计数器、步骤号、ID | 做大，固定位置；等宽字体对齐数字 |
| 题注 | 元数据 | 小号等宽或衬线，贴着内容；时间戳、作者、来源都是题注 |
| 标题句 | 页面标题 | 可以是一个完整句子；标点保留；标题可以是页面最大的元素 |
| 折页 | 展开区、抽屉 | 展开是一次「折出」，内容尺度可以跳变 |
| 换纸 | 分区背景 | 用纸色的细微变化或一条细线分区，不用卡片阴影 |
| 装订 | 页面边缘 | 固定的页眉页脚是装订：同位、同字、只变数值 |
| 强调色 | 状态 | 强调色只给当前、选中、进行中；错误用文字说明而非红色泛滥 |

### 按钮与表单

- 按钮是文字加细线框或下划线；主要操作用墨黑底纸白字，次要操作只用文字。
- 表单标签用题注声部放在字段上方；字段是一条底线或细线框；错误信息是一行文字，紧贴字段。
- 不用圆角泡泡、渐变、投影、发光。圆角半径为 0 或极小（≤ 2 px）。

### 空状态、加载、错误

- 干的文字说明：「尚无条目。」「正在读取 12 条。」「无法连接，重试。」不用插画。
- 加载指示可以是一个计数器或一条细线进度，与家具同一声部。
- 错误不改变版面结构；只增加一行题注声部的文字。

### 动效

- 切换，而非缓动表演：状态变化用即时切换或 ≤ 150 ms 的线性过渡。
- 不用弹跳、缩放进入、视差。滚动就是翻页，不加装饰。
- 唯一允许的「表演」是装置本身：如果装置是霓虹切换或翻页，动效服务于它，并且只有一处。

## 4. 响应式即折法

- 从最大版面开始：桌面是一张展开的版面。
- 每个断点是**对折**：四栏变两栏，两栏变一栏；元素不重排语义，只换折法。
- 巨型尺度在小屏上仍然巨型：它可以占满整屏宽度，这是装置的延续，不是错误。
- 行长在所有断点保持 45–75 字符；通过改变列宽，不通过缩小字号。
- 导航在小屏上仍是文字索引：折叠成一行或一个可展开的清单，不换成汉堡图标加抽屉卡片。

## 5. 经济决定

每个界面项目至少写出以下「限制 → 决定」：

- 字体：系统字体栈，还是一个自托管家族；为什么。
- 图像：是否无图加载；图像尺寸规则；题注是否替代缩略图。
- 组件库：用平台组件并覆盖样式，还是从 token 自建。
- 性能：首屏是否纯文本；动效是否可被 `prefers-reduced-motion` 关闭。
- 断点：几次对折；每次折的栏数。

## 6. 无障碍是秩序的一部分

- 文字与纸色对比 ≥ 4.5:1；强调色上的文字 ≥ 4.5:1，否则强调色只做线或块，不承载文字。
- 题注声部不小于 12 px（网页）或 11 pt（移动）；
- 焦点状态可见：细线框或下划线，与当前状态区分；
- 所有家具（计数器、时间戳）有可读的文本语义，不只是视觉；
- 索引导航可键盘遍历；表格有表头语义。

## 7. HTML/CSS 骨架

```html
<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Index</title>
<link rel="stylesheet" href="tokens.css">
<style>
  html { background: var(--paper); color: var(--ink); font-family: var(--font-sans); }
  body { margin: 0; padding: var(--space-3) var(--space-2); }
  .furniture { position: sticky; top: 0; display: flex; justify-content: space-between;
               font-size: var(--size-caption); font-family: var(--font-serif); padding-bottom: var(--space-1);
               border-bottom: var(--rule) solid var(--ink); background: var(--paper); }
  h1 { font-size: var(--size-display); line-height: 0.95; letter-spacing: -0.02em; font-weight: 500; margin: var(--space-4) 0; max-width: 12ch; }
  .index { display: grid; grid-template-columns: repeat(var(--grid-columns), 1fr); gap: 0 var(--grid-gutter); }
  .index a { grid-column: span 1; padding: var(--space-1) 0; border-top: var(--rule) solid var(--ink); text-decoration: none; color: inherit; }
  .index a[aria-current="page"] { background: var(--accent); }
  table { width: 100%; border-collapse: collapse; font-size: var(--size-body); }
  th { text-align: left; font-weight: 400; font-family: var(--font-serif); font-size: var(--size-caption); padding: var(--space-1) 0; border-bottom: var(--rule) solid var(--ink); }
  td { padding: var(--space-1) 0; border-bottom: var(--rule) solid var(--ink); vertical-align: top; }
  td.n { font-family: var(--font-serif); font-size: var(--size-subhead); width: 4ch; }
  @media (max-width: 720px) { .index { grid-template-columns: repeat(2, 1fr); } }
</style>
</head>
<body>
  <header class="furniture"><span>Index</span><span>0001–0144</span></header>
  <h1>Every entry is numbered, so the number is the navigation.</h1>
  <nav class="index" aria-label="Index"><a href="#a" aria-current="page">A</a><a href="#b">B</a><!-- … --></nav>
  <table>
    <thead><tr><th>No.</th><th>Title</th><th>Year</th></tr></thead>
    <tbody><tr><td class="n">0001</td><td>First entry</td><td>2026</td></tr></tbody>
  </table>
</body>
</html>
```

这个骨架只展示秩序如何落到 CSS：家具固定、标题巨型、索引是导航、表格是列表、强调色只给当前项。
内容与装置必须按项目重写；不要把这个骨架当成品。
