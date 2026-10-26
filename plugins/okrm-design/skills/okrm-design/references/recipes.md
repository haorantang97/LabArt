# 配方

三类产出：版式规范（给人或给排版工具）、HTML/CSS 骨架（可打印、可截图）、图像模型提示词（探索与示意）。
无论哪一类，先完成装置陈述、秩序表、经济决定和序列草图，再进入配方。

## 1. 装置陈述模板

```text
「{既有物} 是 {字面义／性质}，所以 {版面／界面} 做 {具体决定}。」
```

示例（均为虚构项目）：

- 「讲座系列有六个晚上，所以海报就是六行时间表，星期几是最大的字。」
- 「这本目录会进入图书馆，所以它做成图书馆装订的标准目录：布面书脊、索书号标签、无护封。」
- 「这个档案网站的每一条都有编号，所以编号是导航，也是页码。」
- 「这个阅读应用按章推进，所以章节号占满一屏，正文从第二屏开始。」

## 2. 版式规范模板

交付给排版工具或协作者的最小规范：

```text
装置：{装置陈述}
格式：{尺寸 / 折法 / 页数 / 断点}
字体对：{grotesk 家族} + {衬线或等宽家族}
尺度阶梯：caption {x} / body {x} / lead {x} / subhead {x} / display {x} / giant {x}
网格：{派生来源} → {栏数}，边距 {x}，行长 {x} 字符
家具：{至多三种：名称、位置、尺度}
颜色：paper {hex} / ink {hex} / accent {hex}（用途：{一种功能}）
材料：{纸张 / 装订 / 换纸位置} 或 {系统字体栈 / 图像规则}
经济决定：
  - {限制} → {决定}
  - {限制} → {决定}
阅读序列：{页序或滚动段落；重场位置；并置位置}
```

## 3. HTML/CSS 海报骨架

可直接在浏览器打印或截图。尺寸按纸张设置；字号用 `vw` 或 `mm`，不用 px 固定。

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Poster</title>
<style>
  @page { size: 594mm 841mm; margin: 0; }
  html, body { margin: 0; background: #F4F2EC; color: #111; }
  .sheet { width: 594mm; height: 841mm; position: relative; padding: 24mm; box-sizing: border-box;
           font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; display: grid;
           grid-template-rows: auto 1fr auto; }
  .furniture { display: flex; justify-content: space-between; font-size: 14mm; letter-spacing: 0.02em; text-transform: uppercase; }
  .programme { align-self: end; }
  .row { display: grid; grid-template-columns: 1fr 3fr; align-items: baseline; border-top: 1.2mm solid #111; padding: 8mm 0; }
  .row .day { font-size: 120mm; line-height: 0.85; letter-spacing: -0.04em; }
  .row .what { font-size: 22mm; line-height: 1.05; }
  .row .meta { font-family: "Times New Roman", Times, serif; font-size: 14mm; margin-top: 4mm; }
  .colophon { font-family: "Times New Roman", Times, serif; font-size: 11mm; line-height: 1.3; display: grid; grid-template-columns: 1fr 1fr; gap: 12mm; }
  .accent { background: #FFE600; }
</style>
</head>
<body>
  <div class="sheet">
    <header class="furniture"><span>Reading Order</span><span>Six evenings</span></header>
    <main class="programme">
      <div class="row"><div class="day">Mo</div><div><div class="what">What a page number is for</div><div class="meta">19:00, Hall 2</div></div></div>
      <!-- repeat rows; mark the current evening with class="accent" on .day -->
    </main>
    <footer class="colophon"><p>Entry free. Doors 18:30.</p><p>Printed in one colour on uncoated stock.</p></footer>
  </div>
</body>
</html>
```

## 4. 图像模型提示词

用于探索与示意，不用于最终版式（文字会错）。不写任何工作室或设计师的名字；描述装置与秩序。
每次只生成一个方向；在实际尺寸检查；一次只改一个问题。

### 通用前缀

```text
A graphic design artefact, photographed flat or shown as a clean mock-up, following a strict
typographic order. One device drawn from the content drives the whole layout: {device statement}.
Typography is dry, mechanical and systematic: a neutral grotesk sans-serif as the main voice and a
text serif (or monospace) as a second voice for captions and metadata. Extreme scale contrast: one
element is unreasonably large (a page number, an index letter, a single word), body text is small and
calm, captions smaller still. Flush left, ragged right. Furniture (page numbers, numbering, captions)
is large and fixed in position. Paper white and ink black; at most one flat industrial accent colour
({accent}) used for a single function. Dramatic negative space with one dense typographic set-piece.
No gradients, no drop shadows, no textures, no illustration, no decorative icons, no mascots, no
stock-photo lighting.
```

### 海报

```text
{通用前缀}
A {size} poster for {fictional event}. The content list itself is the poster: {n} rows, each with
a giant {day / number} at left and the title plus time at right, separated by hairline rules.
The {current / featured} row carries the accent colour. Header and footer are small uppercase
furniture. Printed in {one / two} colour(s) on uncoated paper. Show the sheet flat on a neutral
surface with a soft, even light.
```

### 视觉识别

```text
{通用前缀}
An identity system for {fictional organisation}. The device is {device}: the name is set as a
complete sentence with its punctuation enlarged / every item carries a number that becomes the
logo / the grid of the building becomes the layout grid. Show the system across four applications
at different scales: a business card, an A4 letter, a street banner, and a website header. The same
rule applies at each scale; only size and material change. No symbol logo unless the device is one.
```

### 书籍与目录

```text
{通用前缀}
An open spread of a {format} book for {fictional subject}. The sequence of reading interleaves
{A} and {B}: left page {full-bleed image / blank}, right page a column of numbered captions in the
second voice, with a large page number as the only furniture. A fold-out or a change of paper
stock marks one event in the sequence. Uncoated paper, honest exposed binding ({sewn / stapled /
rubber band / library cloth}). Show the book from above with the fold visible.
```

### 杂志

```text
{通用前缀}
A spread of a {square / tabloid} journal designed to be folded in half: the fold creates four
columns across the spread. Images and blank pages may cross the fold. Page numbers are unusually
large and are the only regular furniture. Body text is small and set in the grotesk; captions and
footnotes in the serif. Low-gloss uncoated paper, visible crease.
```

### 展览图形

```text
{通用前缀}
Exhibition graphics for {fictional show}. Wall texts are the printed booklet's pages enlarged to
wall scale; every object carries a number that points to a page. Signage is set in the plain system
sans, dry and mechanical, mounted on {bare steel frames / standard boards / existing crates}
whose material carries the mood. One accent colour marks the route. Show a gallery view with one
wall text, two numbered captions and a sign.
```

### 网页与界面

```text
{通用前缀}
A {desktop / mobile} interface for {fictional product}. Navigation is an index ({A–Z / numbered /
table of contents}) set in text, not icons. Lists are tables with hairline rules. Counters,
timestamps and IDs are large furniture in a monospace or serif second voice. The page title can be
a full sentence. The accent colour marks only the current state. System font stack. No cards, no
rounded blobs, no shadows, no illustrations for empty states. Show the screen flat, at actual pixel
density, with the layout grid felt through alignment rather than drawn.
```

## 5. 修正模式

一次只改一个问题；每次修正后在实际尺寸比较。

| 症状 | 修正 |
| --- | --- |
| 像「瑞士复古」cosplay：黑体红色网格，但说不出装置 | 回到第 1 步重找既有物；删掉所有没有理由的元素 |
| 两个概念打架 | 保留与内容来源最直接的一个，另一个降为家具或删除 |
| 一切同尺度 | 挑一个元素放大到不合理；其余缩小一级 |
| 装饰出现（渐变、阴影、纹理、图标） | 全部删除；用尺度和家具替代其功能 |
| 字体太多 | 收到两个家族；第二声部只做题注与元数据 |
| 留白均匀 | 把密度集中到一处重场；其余清空 |
| 看不出序列 | 画页序或滚动段落；加一次尺度跳变或换纸作为重场 |
| 像企业品牌 | 删掉 logo-first 结构；让句子、编号或标点承担识别 |
| 强调色泛滥 | 强调色只给一种功能，其他地方回到墨黑 |
| 家具超过三种 | 合并或删除；保留页码／编号／题注中最承载装置的 |
| 界面像卡片墙 | 改为表格或列表，细线分隔；导航改为文字索引 |
| 动效在表演 | 改为切换或 ≤150 ms 线性过渡；只给装置保留一处表演 |
