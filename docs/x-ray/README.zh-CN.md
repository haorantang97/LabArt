# X-ray

[← LabArt](../../README.md) · [English](README.md)

让外部形态与内部结构同时显现。X-ray 通过层叠密度、材料反差和克制的透视细节，
创作原创放射影像视觉。题材可以是物件、折叠织物、生命体的动作，以及人与机械的互动。

## 示意图

以下四张均为研发中生成的 AI 图像，用来说明视觉方向，不代表物理模拟或解剖验证。

<table>
  <tr>
    <td width="50%"><img src="../../plugins/x-ray/assets/examples/hand-and-ball.png" alt="Hand and ball"><br><strong>手拿球</strong><br>关节、接触关系与浅淡的软组织轮廓。</td>
    <td width="50%"><img src="../../plugins/x-ray/assets/examples/player-and-keys.png" alt="Player and keys"><br><strong>播放器与钥匙</strong><br>致密五金、织物折层与电路的重叠。</td>
  </tr>
  <tr>
    <td width="50%"><img src="../../plugins/x-ray/skills/x-ray/assets/style/folded-shirt.png" alt="Folded shirt"><br><strong>衬衫</strong><br>衣领、袖口、缝线与折叠处形成深浅层次。</td>
    <td width="50%"><img src="../../plugins/x-ray/assets/examples/handbag-front.png" alt="Handbag, front view"><br><strong>正面手提包</strong><br>完整外轮廓中同时显现五金与内含物。</td>
  </tr>
</table>

## 视觉规则

- **用密度建立形态**：薄层浅淡，厚度与重叠增加衰减，致密区域允许遮住后方细节。
- **统一投影与显示**：视角、材料表现与明暗极性在同一画面中保持一致。
- **让动作有接触依据**：检查关节、握持、踏板和工具，不能靠模糊或夸张姿态掩盖结构问题。
- **分清参考图角色**：真实射线影像、生成的外观锚点、主体参考与展示示例具有不同用途。

## 包含内容

- 插件元数据、许可证与四张界面截图。
- 可单独安装的 Skill：入口、Codex 界面配置和独立许可证。
- 成像规则、提示词配方与定性检查标准。
- 两张明确标注为生成图的运行时外观锚点：衬衫和播放器。
- [验证记录](VALIDATION.md)：实际完成的测试与尚未解决的问题。

插件调用环境中可用的生图或编辑工具，本身不包含模型，也不要求 API key 或自动安装研究仓库。
没有图像工具时只提供提示词和检查方法，不会声称已生图。示意图属于合成视觉作品；
解剖、工程准确性与跨题材重复稳定性尚未建立。

## 安装为独立 Skill

GitHub CLI 2.90 或更高版本：

~~~bash
gh skill install haorantang97/LabArt plugins/x-ray/skills/x-ray@main --agent codex
~~~

也可使用开放的 skills 安装器：

~~~bash
npx skills add haorantang97/LabArt --skill x-ray
~~~

## 在 Codex 中安装

~~~bash
codex plugin marketplace add haorantang97/LabArt --ref main
codex plugin add x-ray@labart
~~~

安装后新开聊天以加载 skill。

## 示例请求

- 把折叠夹克做成浅底 X 光影像，让缝线与折层显现。
- 生成手与物件互动的透视画面，检查关节与接触点。
- 保持这张参考图的成像方式，只增加一个致密金属遮挡。
- 生成骑手与自行车的动作场景，再逐项检查人体与机械连接。

## 许可证

沿用仓库的 PolyForm Noncommercial License 1.0.0。
见 [LICENSE](../../LICENSE) 和[包格式检查](../VALIDATION.md)。
