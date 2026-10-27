[English](README.md) | **中文**

# APFEL 式研究驱动识别

一套做研究驱动视觉识别的六步方法，蒸馏自伦敦设计工作室 A Practice for Everyday Life（APFEL）的工作方法，而不是它的作品外观。APFEL 说过不想要签名风格，它的项目彼此看起来都不一样，相同的是一条路径。

这条路径是：研究对象，选一个能指着看的事实，写一句话论点，从这个事实里画出定制字形和一条主导网格规则，每件只留一处可追溯的张力，把规则带到各种媒介上，最后打分再交付。

## 效果

两组都是这个 Skill 按书面 brief 做出来的，研究用的是真实网络资料。机构和品牌是虚构的测试题目。

<table>
  <tr>
    <td width="50%">
      <img src="../../plugins/apfel-research-led-identity/assets/examples/sun-prints.jpg" alt="Anna Atkins 展览识别：普鲁士蓝底上的半透明纸条字">
      <br><strong>Anna Atkins: Sun Prints</strong><br>
      种子：她 1843 年那本蓝晒书里的每个字，都先写在上过油的纸上再晒，所以都坐在一张更浅的纸影里。字由这种纸条剪成，两条纸叠在一起的地方就亮一档。
    </td>
    <td width="50%">
      <img src="../../plugins/apfel-research-led-identity/assets/examples/shenguang-enamel.jpg" alt="上海搪瓷车间识别：申字中竖顶端的挂点">
      <br><strong>申光搪瓷</strong><br>
      种子：每件搪瓷都挂在钩上进炉，杯口内侧留下一个没上面釉的小点。申的中竖就停在这个挂点上，所有版面都从一条挂线往下挂。
    </td>
  </tr>
</table>

第一组的蓝晒原件是 NYPL 的公有领域扫描。第二组的产品和车间照片是 AI 生成替代图，成品里已标明。

## 六步

1. **立论点**：从场所、物件、材料与工艺、档案四类来源各列 3–5 个具体事实，选一个种子，写"X 是 Y，所以所有元素都 Z"。
2. **字体层级**：L0 是从种子长出来的定制字形；L1 展示；L2 一款安静的现成正文字；L3 可选的第二声音。
3. **网格**：一条从种子推出、有固定比例或物理尺寸的主导规则，加普通的 4–6 栏。
4. **受控张力**：每件只有一处张力，而且能追溯到研究。
5. **跨媒介测试**：识别总图、海报、导视、网站首屏、书封。
6. **原创性与一致性评估**：8 项各打 0–2 分，低于 12/16 回到第 1 步换种子。

## 安装

```bash
gh skill install haorantang97/LabArt plugins/apfel-research-led-identity/skills/apfel-research-led-identity@main --agent codex
```

在 Codex 里：

```bash
codex plugin marketplace add haorantang97/LabArt --ref main
codex plugin add apfel-research-led-identity@labart
```

## 原创性

复用的是 APFEL"取形 → 成字 → 成规则"的路径，不是它的字形或版面。不要复刻它的已有项目（Hepworth 的斜角、威尼斯的眼睛、CAM 的 A），也不要把产出说成 APFEL 的作品。

## 许可

PolyForm Noncommercial License 1.0.0，见 [LICENSE](../../LICENSE)。测试记录见 [VALIDATION.md](VALIDATION.md)。
