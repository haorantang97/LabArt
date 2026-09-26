# 调用协议

## 标准与实验

标准调用 = 固定配方 + 本次内容 + 经校验的风格参考。默认使用 B 图作为统一风格基准；跨题材迁移材料、形状分配和气质，不复制人物身份。用户指定已有猫图方向时可选 cat。参考路径和校验值由 assets/manifest.json 提供，不凭文件名猜图。

脚本只做本地组装，不生成图、不联网、不安装软件。需要 Python 3，无第三方依赖。首次使用读 STYLES.md 中 core 与相关模式，查看真实参考图。输入图顺序以生成的 references 为准。

标准模式不允许临场重写风格。新风格要求与固定配方冲突时，明确将它作为实验版本处理，不偷改标准配方。用户明确要求不带风格图时，可用 reference_mode=none 加 exception_reason；生成包标为 experimental-no-style-anchor，仍保留固定文字配方。脚本的关键词检查只是防止常见误填，不是完整语义验证。

## 新作输入

用任务目录的 request.json 保存内容，所有内容字段都只写本次画面。以下是花朵示例，不是默认主体：

```json
{
  "mode": "generate",
  "subject_type": "plant",
  "subject": "一枝向下垂着的白花",
  "scene": "放在窗台的一只细玻璃瓶里，窗外有两片云",
  "identity": "五片宽花瓣，浅绿色细茎",
  "allocation": {
    "dominant": "靠左的两片花瓣占去花冠的大半位置",
    "cluster": "小花心与另外三片花瓣挤在右侧",
    "support": "细茎和两片小叶承接偏重的花冠"
  },
  "construction": "花瓣交接处稍挤，瓶肩一边宽一边窄",
  "bleed": "花瓣下沿的淡灰水色、叶尖的浅绿",
  "aspect": "3:4"
}
```

必填：mode、subject_type、subject、allocation（三项）、construction、bleed。scene、identity 默认空；aspect 未指定则省略，不自行锁正方形。text 未指定不加文字；指定时只把原文交给模型，不承诺字形准确。

subject_type 为 portrait、animal、plant、object 或 scene。包含需辨识的固定人物时选 portrait，并读人物模块；它可以是头像或完整场景，不强制半身。内容字段可指定物体固有颜色，不追加第二套线条、色板、纸感或渲染指令。allocation 只描述哪里占得多、哪里挤、哪里偏小，不写一整套新画风；不设统一变形百分比。

可选：
- anchor：canonical（默认 B 图）或 cat（用户指定猫参考方向）。
- subject_references：[{"path": "/绝对路径/照片.png", "role": "identity"}]。role 也可为 selected-shape，表示用户选定的成图形状关系。照片负责身份，selected-shape 负责具体形状与疏密；不要以照片修正常用户选定的夸张。实际文件必须存在。
- reference_mode：standard（默认）或 none；none 必须同时有 exception_reason，说明用户的明确要求。

新作通常一张风格图即可；不要把整组素材和失败试图一起附上。用户要求几版但没给数量时做两张独立图，分别组织内容关系；有数量则遵从，不自动做拼版。

## 生成调用包

在 skill 根目录运行：

```sh
python3 scripts/render_prompt.py --request /绝对路径/request.json --out /绝对路径/call.json
```

输出包含 revision、status、prompt、prompt_sha256、recipe_sha256、request、references、referenced_image_paths。路径按 request 文件所在目录解析，写入调用包时变为绝对路径；移动技能目录后重新运行即可。

调用图像工具时：
1. 原样使用 prompt；不要概括成几句，也不追加另一套美术段落。
2. 按 referenced_image_paths 的实际顺序附图，工具不支持路径时使用其等效图片引用机制，并核对顺序。仅把路径写在文字里不算附图。
3. 标准模式风格图缺失、哈希不符或无法附图时停止标准调用，说明缺了什么；不能悄悄退回文字版。
4. 保存调用包与工具返回的原图。预览可留在宿主生成目录；正式项目资产按宿主要求复制到项目。

脚本执行不可用时，可按相同顺序手工拼接固定区块，但必须逐字核对并记录 manual-assembly；未实际校验资产时标为 unverified-assembly，不声称标准已校验。

## 局部编辑与针对性修正

局部修改只需要：

```json
{
  "mode": "edit",
  "target": "/绝对路径/用户选定图.png",
  "change": "把嘴角放平，其他内容保持原样"
}
```

目标始终是 Image 1；风格图排在后面。使用固定 edit 配方，不附加会要求重画整张的 core/portrait。若用户选中的形状关系与默认风格图不同，目标优先。

只有用户授权迭代，且目视检查发现具体缺项时，才用 correct-material、correct-shape 或 correct-line 替换 mode，change 写清要修改的部位和目标。三个修正模式各自独立，不强制每张都跑完；内容不变的前提下只处理实际缺项。超出已授权编辑范围则报告，不自动扩大修改。

## 交付

按 references/qa.md 记录看得见的通过、未通过或本次不适用项。首轮输出即使失败也保留；不得用隐藏重抽替换首轮证据。用户认可才晋级资产，Agent 检查通过只表示可以给用户审阅。

manifest 固定配方版本与参考文件哈希。更新文件须主动修改 revision 与相应哈希、重新验证；不能让调用时自动重算并接受新参考。相同字节校验不受安装路径影响；重新编码或元数据变化会触发文件不一致，先核验再有意更新 manifest，不把这种报错解释成审美变化。
