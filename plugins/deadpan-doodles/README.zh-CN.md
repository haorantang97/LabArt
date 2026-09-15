<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img src="assets/hero-light.svg" alt="Deadpan Doodles · 沙冰 — a little out of proportion" width="900">
</picture>

[English](README.md) | **中文**

# 沙冰 · Deadpan Doodles

比例有点不对，态度一本正经。

用通透的钢笔淡水彩画人物、动物、花草、物件和小场景。保留一处有记忆点的比例反差、松动笔线和透出色层的纸白。不只做头像。

## 开始使用

通过 Codex CLI 从 LabArt 市场安装：

```sh
codex plugin marketplace add haorantang97/LabArt
codex plugin add deadpan-doodles@labart
```

需要宿主具备图像生成能力；本包不内置模型、不配置 API Key，也不锁定某个模型。手动安装时请保留[完整 skill 文件夹](skills/deadpan-doodles)，包括参考文件与图片，不要只复制 SKILL.md。

可以直接说：

> 用 $deadpan-doodles 画一只懒洋洋的猫，旁边有一小枝花。通透水彩，比例有点反常，冷幽默，不要太可爱。

想画有本人辨识度的角色时，附上照片：

> 用 $deadpan-doodles 把这张照片画成冷幽默水彩人物。保留我的外貌特点，但让比例反常搞怪一点。

## 哪些东西保持一致

| 层次 | 负责什么 |
|---|---|
| 材质 | 薄色透纸、局部叠深、露白、松动细笔线 |
| 比例 | 根据主体选一处大小或间距反差；明显，但不是处处夸张 |
| 主体 | 用户要的人、动物、植物、物件或小事件，不是材质样图里的人 |
| 头像模块 | 真人辨识、符号化五官、自然成对的眼睛和角色局部修改 |

猫可以身子稍长、腿短短收着；花可以相对细茎显得有点沉。它们是可能性，不是每次照搬的模板。主体保持平静，让造型自己产生幽默。

这里参考了同仓库 [Antibes Holiday](../antibes-holiday/README.md) 的一个原则：让失衡有用，其他地方安静一些。在沙冰里，它主要作用于**主体内部的比例**，不变成强制构图，也不移植它的黑白线稿材质。

## 自带视觉参考

<table>
  <tr>
    <td width="50%"><img src="skills/deadpan-doodles/assets/style/long-face.png" alt="本项目生成的长脸角色，展示透明水彩层次"></td>
    <td width="50%"><img src="skills/deadpan-doodles/assets/style/high-forehead.png" alt="本项目生成的角色，用于观察薄色洗与开放边缘"></td>
  </tr>
</table>

两张都是本项目生成的人物样本，用于展示材料，不是通用头脸或身体模板。第二张的大额头不是默认要求。包内不包含原作者参考图、真人照片或这些作品的裁切。

[材质索引](skills/deadpan-doodles/references/style-assets.md) 指向完整图片中的局部，不是一套软件画笔，也不是另行生成的笔触板。非人物任务只迁移材料行为，不继承人脸、头发、眼镜、配色或衣服。

## 头像是专用模块，不是整个 skill

[主 skill](skills/deadpan-doodles/SKILL.md) 处理共用的视觉决定。[头像模块](skills/deadpan-doodles/references/portrait.md) 只在真人辨识和人物 IP 任务中读取，保留经过更多测试的人物流程，不把额头高度或固定五官坐标规定给所有主体。

已经选中某张图后，可以这样修改：

> 保留这张图的水彩、头发和小身体。脸缩短一点，但留下反常的轮廓和自然成对的眼睛。

此时选中图就是编辑目标，不承诺其他区域像素级完全不变。

## 边界与验证

这是指令与参考资产包，不是确定性渲染器。人物辨识与风格可能漂移，仅凭固定提示词不能保证每次得到同一个角色。头像经过的迭代更多；扩展题材不代表各类题材已经同样可靠。

新图经过认可才成为正式候选资产；失败测试保留，不偷偷替换，也不直接纳入正向参考库。实际检查和待验证项见[验证记录](VALIDATION.md)。

公开调用名是 `$deadpan-doodles`。早期本地名称 `deadpan-watercolor-ip` 不是第二个公开插件。

## 贡献与许可

反馈时请提供有权分享的需求、实际提示词、输入图角色和首轮结果。不要提交私人照片或第三方参考作品。修改介绍时同步维护两种语言。

包内许可：[PolyForm Noncommercial 1.0.0](LICENSE)。
包的许可不保证输入图或生成结果的权利状态；这些还取决于具体输入和所用生图服务。

[返回 LabArt](../../README.md)
