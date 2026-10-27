[English](README.md) | **中文**

# Lab 平面设计 · Lab Graphic Design

为展览、出版、文化机构和工艺品牌做平面识别，风格安静、精确、有物质感。每样东西都有存在的理由：字形、网格、颜色、印制方式，都能追溯到对象身上一个具体的事实。

## 和一般的风格 skill 有什么不一样

它不是一个模仿视觉效果的 skill，甚至不从任何"样子"出发。

它从选题开始，什么都不预设。先真正去调研这个对象：它的历史、它怎么被做出来、它在什么地方、它以前印过什么东西。列出大量具体的事实，比较好几个可能的切入点，再选定一个。从这里往后，每个决定都有依据可问：为什么是这个字形、这个颜色、这种纸、这个尺寸，答案都指回对象身上真实存在的东西。

所以用它做出来的两个项目看起来完全不同，而且哪一个都没法直接换给另一个客户用。

## 风格

- **字从对象身上长出来。** 一个能指着看的细节，比如一条上过油的纸、搪瓷进炉时挂的那只钩，变成一款定制字形。
- **一条规则管住全部。** 从同一个事实取出一条线或一个比例，海报、墙面、屏幕、书都按它排。
- **颜色取自材料。** 烧过的黏土、普鲁士蓝、钴釉；只有一个强调色，每件只用一次。
- **印制和材料本身就有意义。** 纸张、硫酸纸书衣、冲孔、直接丝印在墙上、按原尺寸复制。
- **第一眼安静，第二眼更多。** 第一眼平静、成立；细看才发现细节和它的来历。层级靠位置和尺度，不靠加粗。

## 效果

两组都是这个 Skill 按书面 brief 做出来的，机构和品牌是虚构的。

<table>
  <tr>
    <td width="50%">
      <img src="../../plugins/lab-graphic-design/assets/examples/sun-prints.jpg" alt="Anna Atkins 展览识别：普鲁士蓝底上的半透明纸条字">
      <br><strong>Anna Atkins: Sun Prints</strong><br>
      她 1843 年那本蓝晒书里的每个字，都先写在上过油的纸上再晒，所以都坐在一张更浅的纸影里。字由这种纸条剪成，两条纸叠在一起的地方就亮一档。
    </td>
    <td width="50%">
      <img src="../../plugins/lab-graphic-design/assets/examples/shenguang-enamel.jpg" alt="上海搪瓷车间识别：申字中竖顶端的挂点">
      <br><strong>申光搪瓷</strong><br>
      每件搪瓷都挂在钩上进炉，杯口内侧留下一个没上面釉的小点。申的中竖就停在这个挂点上，所有版面都从一条挂线往下挂。
    </td>
  </tr>
</table>

第一组的蓝晒原件是 NYPL 的公有领域扫描。第二组的产品和车间照片是 AI 生成替代图，成品里已标明。

## 安装

```bash
gh skill install haorantang97/LabArt plugins/lab-graphic-design/skills/lab-graphic-design@main --agent codex
```

在 Codex 里：

```bash
codex plugin marketplace add haorantang97/LabArt --ref main
codex plugin add lab-graphic-design@labart
```

## 原创性

不要复刻研究和参考里看到的已有识别，也不要把产出说成别的工作室的作品。

## 许可

PolyForm Noncommercial License 1.0.0，见 [LICENSE](../../LICENSE)。
