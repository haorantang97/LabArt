---
name: contemporary-zhuo-calligraphy
description: Use when the user asks for 当代拙书、拙味毛笔字、非规整竖排书法, or arbitrary Chinese content in a deliberately awkward contemporary brush hand.
---

# 当代拙书生成

把任意中文一次写成完整作品。核心是可迁移的结构失衡、用笔因果和空间压力，不是复刻一张样图。不要训练模型、搜索字体或逐字拼图。

## 前置资源与边界

以下命令必须从包含 `SKILL.md` 的本 skill 根目录运行。

1. 完整读取 [references/style-grammar.md](references/style-grammar.md)。
2. 完整读取 [references/quality-gate.md](references/quality-gate.md)。
3. `references/runtime-style-kernel.txt` 是提示脚本读取的纯文本风格内核；它不含原作像素、示范字、作者身份或固定构图统计。
4. 使用 `imagegen` 完成整幅生成。

**原始参考只用于离线研究和生成后验收。运行时不得传入任何风格参考图。** 不得为了运行 skill 打开抖音、短链或原帖，也不得把研究档案复制回 skill。若用户另行要求来源或署名取证，将其视为独立任务，取证材料仍不能进入生成主线。

## 工作流

### 0. 锁定内容与实验边界

- 原样记录文字，不擅自改繁简、标点或措辞。
- 默认竖排、从右向左；1–4 字用 1–2 列，5–8 字用 2–3 列，9–18 字用 3–5 列。结合画幅选择列数，不套用固定三列。
- 结果只能按质量门称为失败样例或实验样图；没有陌生文本盲评证据，不宣称 95% 或某位作者亲笔。

### 1. 逐列声明 Unicode 内容

- 在记录中明确每列从上到下的内容与右到左的列序。
- 可拆成常见偏旁的字必须保持为一个完整字符；允许部件错位，不允许偏旁脱离母字成为另一个符号。

### 2. 分离文字身份与无字形关系场

运行：

```bash
python3 scripts/make_semantic_layout_guides.py \
  --text "用户原文" \
  --columns <列数> \
  --width <画幅宽> \
  --height <画幅高> \
  --seed <固定种子> \
  --legend-out <工作目录>/content-legend.png \
  --layout-out <工作目录>/layout-zones.png
```

- `content-legend.png` 用小号中性印刷字和颜色声明 Unicode 身份；字形没有风格或结构权威。
- `layout-zones.png` 是不含任何汉字轮廓的关系场。它用不规则彩色轮廓表达出现次数、大致占幅、弯曲列轴、非等距推进以及字与字的挤压、退让、侵入和悬置。
- 关系场保留阅读顺序，但不建立等宽列、等高行或九宫格；纵向位置必须由不等步长累积产生。
- JSON 清单必须同时写明 `uses_fixed_grid: false`、`uses_source_derived_statistics: false`、`uses_external_style_reference: false` 和 `runtime_image_count: 2`。
- 两张引导图都不是作品，不得交付。不得把大号系统字体轮廓当作字骨蓝图。

### 3. 两图整幅生成

先运行：

```bash
python3 scripts/build_generic_generation_prompt.py \
  <工作目录>/content-legend.json \
  --out <工作目录>/generation-prompt.txt
```

再调用图像生成工具，且只传两张图：

- 图 1 `content-legend.png`：只负责“写什么”。
- 图 2 `layout-zones.png`：只负责“彼此如何占据空间”。

运行时不得传入任何风格参考图、参考作品截图、原字裁片、字体样张或来源统计。提示脚本会载入蒸馏后的文本内核，约束字骨、结体、笔性、章法与反例。

- 一次写完整幅；禁止独立字卡、逐字编辑、裁切回贴或部件拼装。
- 成品必须清除全部颜色和导引轮廓。
- 不加印章、题款、标点、装饰、边框、UI 或水印。

### 4. 硬门验收

先逐字核对。错、漏、重、繁简变化、列序错误或偏旁散架均为硬失败，不做局部修补。

内容正确后，按质量门给字骨、结体、笔性、章法各打 0–100 分，并为每项写一个最具体的失败点。

- 任一项低于 75：保存失败证据并停止该运行，不展示为成品。
- 四项均不低于 75：只能标为实验样图。
- 同一陌生文本最多执行一次预先约定的三样本稳定性测试；三张均未过门即关闭路线，不靠反复抽样碰运气。
- 二次整幅毛边编辑不能冒充字骨迁移，不用它为失败路线续命。

## 输出

- 将选中图、原文、列分配、两张引导图、清单、最终提示和评分记录保存在当前项目。
- 明确区分：离线研究参考、运行引导图、实验生成图和通过图。

## 禁止路径

- 不下载或训练模型权重。
- 不搜索最像字体后做侵蚀、旋转或毛笔化。
- 不建立单字库，不从作品裁字，不按字符拼接。
- 不得把研究目录中的原图、原字、固定坐标或来源统计接回运行主线。
- 不得改用逐字增量编辑、裁切回贴或二次毛边编辑。
- 不得靠反复抽样等待偶然命中。
- 不用 CLIP、SSIM 或像素重叠冒充书法评审。
