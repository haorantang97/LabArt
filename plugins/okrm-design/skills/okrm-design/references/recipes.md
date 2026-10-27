# 配方

任何配方之前先有推导文档（genesis.md 的上游与 form-derivation.md 的推导表）。没有推导表的配方产出一律视为草稿。

三类产出：版式规范、HTML/CSS 骨架（可打印、可截图）、图像资产（有生图工具时，见 5a；提示词见 5）。
无论哪一类，先完成装置陈述、框架段落、秩序表、经济决定、固定项／变动项表和序列草图。

## 1. 装置陈述模板

```text
现成物型：「{内容的某处} 让人想到 {一个现成物／既有文件}，所以整个 {物件／界面} 做成它。」
系统型：  「{项目} 有 {N 个单元／一个流程}，所以 {版面／界面} 就是这个系统本身，并把 {一个组件} 用尺度放大。」
对立型：  「{项目} 同时是 {A} 和 {B}，所以 {A 用某材料或字}，{B 用其对立物}，两者并置。」
```

示例（均为虚构项目）：

- 「这本石头目录会进入图书馆，所以它做成图书馆装订的标准目录：布脊、索书号标签、无护封；每件编号。」
- 「讲座系列有六个晚上，所以海报就是一张六行的通告，星期几放大到不合理。」
- 「这个档案网站的每一条都有编号，所以编号是导航也是页码，界面的每个动作都用括号写出来。」
- 「这本书同时是实验室报告和诗集，所以报告用系统 grotesk 的表格，诗用打字机字，两者交错。」

## 2. 框架段落模板

```text
舞台：{媒介与格式；它的约束：纸张、折法、屏幕、邮寄}
演员：{内容单元及数量}
脚本：{阅读顺序与规则：交错、配对、编号往返、划掉、翻转}
固定项：{格式、标志、家具位置、第一声部}
变动项：{图像、颜色、第二声部、每期的情绪}
```

## 3. 版式规范模板

```text
装置：{装置陈述}
框架：{舞台／演员／脚本}
格式：{尺寸 / 折法 / 页数 / 断点}（由什么决定）
声部：{普遍语言家族} + {找到的字或有来源的字，及来源}，或只用一个家族
尺度：caption {x} / body {x} / label {x，字距 +0.x em} / monument {x}（避开中间）
对齐：{标签居中 / 文件左齐 / 词在角落}
结构：{折法} → {栏数}；细线用于 {图表 / 表格 / 网格}
家具：{至多三种：名称、位置、尺度}
图像：{满版 / 白边 10% / 小图 40% 于材料上}；{双黑 / 彩色分配}
颜色：paper {hex} / ink {hex} / field {hex}（作为材料用于 {封面 / 环衬 / 整屏}）
材料：{纸张 / 装订 / 脊条 / 现成物} 或 {系统字体栈 / 图像规则}
经济决定：
  - {限制} → {决定}
序列：{页序或滚动段落；换挡位置；并置位置}
```

## 4. HTML/CSS 封面骨架（颜色作为材料 ＋ 细线图表 ＋ 角落的词）

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Cover</title>
<style>
  @page { size: 227mm 320mm; margin: 0; }
  html, body { margin: 0; }
  .cover { width: 227mm; height: 320mm; position: relative; background: #1F3FBF; color: #111;
           font-family: Helvetica, Arial, sans-serif; font-size: 4.5mm; letter-spacing: -0.01em; }
  .word { position: absolute; margin: 0; }
  .tl { top: 6%; left: 6%; } .tr { top: 6%; right: 6%; text-align: right; } .bl { bottom: 6%; left: 6%; }
  svg { position: absolute; inset: 0; width: 100%; height: 100%; }
  line { stroke: #111; stroke-width: 0.35mm; }
</style>
</head>
<body>
<div class="cover">
  <p class="word tl">Sorted,</p>
  <p class="word tr">by weight</p>
  <p class="word bl">Index of Stones</p>
  <svg viewBox="0 0 227 320"><!-- the diagram is the content's own structure, drawn in hairlines -->
    <line x1="30" y1="60" x2="200" y2="60"/><line x1="120" y1="40" x2="120" y2="300"/>
  </svg>
</div>
</body>
</html>
```

## 5a. 有生图工具时：资产交给模型，排字留在 HTML

先看当前会话有没有生图能力：一个图像生成工具、一个连到 ChatGPT／Codex 的本地 bridge、或任何能按提示词出图的工具。
有就用它做**资产**；没有就用色块或矢量占位，并在交付里写明「照片为占位」。

分工：图像模型出图像资产；字和版面始终用 HTML/CSS 排（模型会把字写错，也会把尺度两极抹平）。最终画面是两者合成：
生成的图作为 `<img>` 或背景放进 HTML，字、细线、家具在 HTML 里排在上面或旁边，再渲染截图。

### 三类资产

| 类 | 是什么 | 推自 | 用在哪 |
| --- | --- | --- | --- |
| 内容照片 | 项目将来会有的照片的替身（拍摄现场、物件、人、地方） | 推导表「图像」行与第 6 步的拍摄情境 | 页面视图里的图版、满版、网格墙 |
| 材质特写 | 纸的纤维、布面经纬、压印、齿孔、牛皮板、毛毡、钝化钢 | 推导表「材质」行；表里没有的不生成 | 物件视图的表面、页面视图的底纸 |
| 物件视图 | 印好的东西被放在桌上、墙上、架上拍下来 | 第 4 步的物件（格式、装订、容器） | 封面、包装、海报张贴、展陈现场 |

物件视图有两种做法，优先第一种：
1. 生成**空白的物件**（正确的布面、纸色、厚度、装订、放在正确的表面上，封面上没有字），再把 HTML 排好的封面用
   CSS `transform: perspective() rotate…` 或直接平贴叠上去。字是精确的，材质是生成的。
2. 让模型直接出带版面的整张效果图，只作探索；进交付前用第一种重做。

### 提示词规则

- 只描述：现成物、材料、光、取景、比例、情境。不写任何工作室、设计师、品牌或「某某风格」。
- 每条提示词都加：`no text, no letters, no numbers, no logos, no watermark`（字由 HTML 排）。
- 比例与取景来自排列动作：满版出血写明宽高比；网格墙要成套、同光同距；散放的小图要单独生成、背景可去。
- 光：均匀、平常、可信；不要戏剧化布光、不要景深虚化做「高级感」、不要胶片颗粒滤镜，除非推导表写了理由。
- 颜色：推导表写黑白就生成黑白；只有一个平涂颜色时，照片里不要引入第二个强烈的颜色。

```text
内容照片：
{subject from the brief}, photographed {situation: on site / on a table / against a grey card}, {black and white / natural colour},
{aspect ratio}, even daylight, documentary, unretouched, plain and specific, no text, no letters, no numbers, no logos, no watermark.

材质特写：
Close-up of {material from the derivation table: uncoated off-white paper with visible fibres / grey book cloth weave /
blind-embossed board / perforated card edge / kraft board}, flat, evenly lit from above, filling the frame, no objects,
no text, no letters, no logos, no watermark.

空白物件：
A {format: 190 × 240 mm sewn book / 12-inch record sleeve / A1 poster pasted on a tiled wall / paper bag} made of {material},
{binding or finish}, its cover blank, lying on {surface from the brief: a workshop bench / a library table / a concrete floor},
photographed from {straight above / three-quarter}, soft single shadow, no text, no letters, no logos, no watermark.
```

### 记录与诚实

- 每个生成的资产在推导文档里记一行：文件名、提示词、它代替的是什么（「将由摄影师在车库现场拍摄的 120 张之一的替身」）。
- 交付时标明哪些图是生成的。生成的照片是占位，不当作真实的人、地点或作品的记录交给客户或公开。
- 资产放在作品旁的 `assets/` 目录，用相对路径引用；渲染后检查：图像行与材质行里没有的东西，没有出现在画面里。

## 5. 图像模型提示词

用于探索与示意，不用于最终版式（文字会错）。不写任何工作室或设计师的名字；描述装置、现成物与秩序。
每次只生成一个方向；在实际尺寸检查；一次只改一个问题。

### 通用前缀

```text
A designed object photographed flat on a plain surface, in even light, following a strict order.
One device drawn from the content drives everything: {device statement}. The object re-enacts a
readymade: {the readymade: a library-bound catalogue / a postage stamp / an archive envelope / a
notice / a punched card / a typed script}. Typography uses ubiquitous languages only: a Helvetica-class
grotesk and a Times-class serif or a typewriter monospace; at most two voices. Type is either very
small (captions, labels, spine sentences, roughly 1.5% of the object's height) or monumental (one word
or one numeral at 10–40% of the height); nothing in between. Labels are centred and letterspaced;
grotesk words sit in the corners at 6% margins. Hairline rules form diagrams or tables. One flat
colour is used as a material for the whole surface ({field colour}), with type in black or white.
Photographs are black and white, either full bleed or framed by a 10% white border. Materials are
honest and ordinary: cloth spine strip, uncoated paper, kraft board, rubber band, sticker, foil,
blind emboss. No gradients, no drop shadows, no textures added digitally, no illustration, no
decorative icons, no mascots.
```

### 书与目录

```text
{通用前缀}
An open spread of a {format} catalogue for {fictional subject}. The sequence interleaves {A} and {B}:
left page {a full-bleed black-and-white plate / blank}, right page {a column of numbered captions in
the serif voice / a typed poem in monospace}, with a small folio as the only furniture. One change of
paper stock or one fold-out marks a single shift in the sequence. Show the fold.
```

### 封面与物件

```text
{通用前缀}
The cover of a {format} book: a flat {field colour} field; the title set small in the corners; a
hairline diagram derived from the content ({a sorting table / a shelf plan / a timetable}); a cloth
spine strip of about one-tenth of the cover width; a small typed label centred in the upper quarter.
Show the book closed, from above.
```

### 杂志

```text
{通用前缀}
A spread of a square journal folded vertically in half so that the spread reads as four columns.
Dense small body text in the grotesk, charts in hairlines, a photograph crossing the fold. The cover
carries a geometric letter mark derived from historical signage lettering and, against it, a loose
hand-drawn face that changes every issue. Low-gloss thin uncoated paper; a bright orange endpaper.
```

### 海报与节目单

```text
{通用前缀}
A {size} poster that is a notice: {n} rows separated by hairlines, each with a monumental {weekday /
number} at left and the title and time at right in the serif voice. Small uppercase header and footer.
Printed in one colour plus one spot colour on uncoated paper. Flat on a neutral surface.
```

### 识别

```text
{通用前缀}
An identity system for {fictional organisation} built from {a sentence with enlarged punctuation /
a grid that stands for public space / a numbering system}. Shown across a business card, an A4
letter, a street banner and a website header: the same rule at each scale, only size and material
change. No symbol logo unless the device is one.
```

### 展览图形

```text
{通用前缀}
Exhibition graphics for {fictional show}: wall texts are the printed booklet's pages enlarged to wall
scale; every object carries a number that points to a page of a script. Signage is the plain system
grotesk, dry and mechanical, mounted on ordinary materials from other functions ({bent steel frames /
pole protectors / kerb stones / fire-retardant felt}). One flat colour marks the route.
```

### 网页与界面

```text
{通用前缀}
A {desktop / mobile} interface for {fictional product}. The interface makes the implicit explicit:
buttons and states are written as text in brackets — (Info), [Index], 1 / 31. Navigation is an index
set in text; lists are tables with hairline rules; the page title is a sentence at body size; one
letter or numeral is monumental. System font stack. A flat {field colour} fills a whole screen or
panel instead of highlighting buttons. No cards, no rounded blobs, no shadows, no illustrations.
```

## 6. 修正模式

一次只改一个问题；每次修正后在实际尺寸比较。

| 症状 | 修正 |
| --- | --- |
| 像瑞士复古 cosplay：黑体网格齐备，说不出装置 | 回到既有物清单；找一个现成物或既有系统；删掉没有理由的元素 |
| 表达寄托在大标题上 | 把它缩到题注尺度，或放大到纪念碑尺度（≥ 页高 8%） |
| 两个概念打架 | 保留与内容来源最直接的一个，另一个降为家具或删除 |
| 一切同尺度 | 一个元素放大到不合理；其余缩到题注 |
| 装饰出现 | 删除；功能交给尺度、家具与材料 |
| 字体太多或太「有个性」 | 收到普遍语言＋一个有来源的字；展示字体换成 Helvetica/Times 级 |
| 强调色撒在版面里 | 改成一个平涂颜色作为整块材料；版面内回到墨黑 |
| 看不出序列 | 画对页序；加一次换挡（折出、换纸、翻转）；用交错 |
| 像企业品牌 | 删掉 logo-first；让句子、编号、标点或网格承担识别 |
| 图像中等大小 | 改成满版，或带 10% 白边的图版，或 40% 的小图放在材料上 |
| 界面像卡片墙 | 改为表格与索引；动作写成带括号的文字 |
| 动效在表演 | 改为切换；只给装置保留一处表演 |
| 参考图代替了想法 | 删掉情绪板；写框架段落（舞台／演员／脚本） |
