# Manim 尺规作图插件

## 简介

作为一个数学内容的创作者（B站博主“**究尽数学**”）,已经使用 Manim 制作了很多期**尺规作图**的动画视频，比如：《正257边形的尺规作图》。其中，用到的圆规和直尺工具，得到了一些粉丝的关注，常有私信要求代码。所以我决定，以 Manim 尺规作图插件的形式，分享一个基于 Manim 的尺规作图工具。

Manim 尺规作图插件包括：自定义的圆规(Compass)、直尺(Ruler)和铅笔(Pencil)三个VMobject类；以及对应的动画类，可以方便地实现圆弧、直线的绘制动画。接下来，我将详细介绍如何使用这个插件。

## 使用方法

### 插件安装

通过 pip 安装：

```shell
pip install manim-compass
```

在 Manim 项目中,导入插件：

```python
from manim_compass import *
```

### 圆规动画

圆规的动画，包括：圆规的张开和闭合、移动、旋转。

#### 移动圆规：MoveNiddleTipTo

代码示例：

```python
compass = Compass().to_edge(LEFT)
self.play(
    MoveNiddleTipTo(compass, ORIGIN),
)
```
移动圆规 compass: 以圆规尖脚尖为参考点,整体移动，使得圆规尖脚尖到指定位置。

#### 旋转圆规：RotateCompass

代码示例：

```python
compass = Compass().to_edge(LEFT)
self.play(
    RotateCompass(compass, PI/2),
)
```
旋转圆规 compass: 以圆规尖脚尖为圆心,整体旋转指定的度数。

#### 张开圆规：SplitCompass

代码示例：

```python
compass = Compass().to_edge(LEFT)
self.play(
    SplitCompass(compass, 2),
)
```
张开圆规 compass: 将圆规 compass 的两脚, 均匀的向外(内)旋转, 使得张开的距离为指定的数值。

#### 放置圆规：PutCompass

代码示例：

```python
compass = Compass().to_edge(LEFT)
self.play(
    PutCompass(compass,niddle_pos = LEFT, pen_pos = RIGHT),
)
```
放置圆规 compass: 将圆规的尖脚尖和笔尖，分别放置到指定的位置。

#### 收起圆规：PutCompassAway

继承自 PutCompass 类，用于收起圆规，代码示例：

```python
self.play(
    PutCompassAway(compass,point = 4*LEFT,span_buff = 0.2),
)
```
收起圆规：将圆规的尖脚尖和笔尖间距设为 span_buff，放置到指定的 point 位置。

#### 画圆弧：DrawArc

代码示例：

```python
self.play(
    DrawArc(compass, arc),
)
```
画圆弧：圆规 compass 尖脚尖已放置到 arc(Arc实例) 圆心，笔尖放到 arc 的起点；旋转圆规和创建圆弧同步，实现圆规画圆弧的动画效果。

DrawArc 的内部实现：收集了圆规的旋转动画 RotateCompass 和圆弧的创建动画 Create。

### 铅笔动画

#### 平移铅笔：MovePencilTipTo

代码示例：

```python
pencil = Pencil().to_edge(LEFT)
self.play(
    MovePencilTipTo(pencil, ORIGIN),
)
```
平移铅笔 pencil: 以铅笔尖为参考点,整体移动，使得铅笔尖到指定位置。

#### 收起铅笔：PutPencilAway

继承自 MovePencilTipTo，用于放置铅笔。代码示例：

```python
pencil = Pencil().to_edge(LEFT)
self.play(
    PutPencilAway(pencil,point = 4*LEFT),
)
```
收起铅笔：其实和 MovePencilTipTo 等效(完全可用替换)，为的是尺规作图动画的制作过程中，增强代码可读性。

#### 按路径移动铅笔：MovePencilAlongPath

代码示例：

```python
pencil = Pencil().to_edge(LEFT)
self.play(
    MovePencilAlongPath(pencil, path),
)
```
按路径移动铅笔 pencil: 以铅笔尖为参考点,整体移动，使得铅笔尖沿着指定的 path(VMobject) 移动。在尺规作图的场景中，path 通常为直线(Line实例)。

#### 画线动画：DrawPath

代码示例：

```python
pencil = Pencil().to_edge(LEFT)
self.play(
    DrawPath(pencil, path),
)
```
画线动画：铅笔 pencil 尖脚尖已放置到 path(VMobject) 的起点，铅笔沿着 path 移动的同时，创建 path；实现铅笔画线的效果。

DrawPath 的内部实现：收集了铅笔的移动动画 MovePencilAlongPath 和 path 的创建动画 Create。

### 直尺动画

#### 放置直尺：PutRuler

代码示例：

```python
ruler = Ruler().to_edge(LEFT)
self.play(
    PutRuler(ruler, start = LEFT, end = UR),
)
```
放置直尺 ruler: 直尺的一边，对齐起点 start 和终点 end。

#### 收起直尺：PutRulerAway

继承自 PutRuler，用于收起直尺。代码示例：

```python
ruler = Ruler().to_edge(LEFT)
self.play(
    PutRulerAway(ruler, point = LEFT, is_flat = False),
)
```
收起直尺：将直尺放置到指定的 point 位置，is_flat 为 True 时，直尺为水平放置；is_flat 为 False 时，直尺为垂直放置。

#### 直尺画直线的动画

需要组合直尺和铅笔的动画，代码示例：

```python
ruler = Ruler().to_edge(LEFT)
pencil = Pencil().to_edge(LEFT)
self.play(
    PutRuler(ruler, start = LEFT, end = UR),
    PutPencil(pencil, point = LEFT),
)
self.play(
    DrawPath(pencil, path),
)
```

收起直尺和铅笔的动画：

```python
self.play(
    PutRulerAway(ruler, point = LEFT),
    PutPencilAway(pencil, point = LEFT),
)
```

### 场景类：CompassScene

要制作尺规作图的动画，除了上面的动画类的组合使用方式，还提供了另外一种使用方法：CompassScene 类。

CompassScene 类，继承自 Scene 类，用于制作尺规作图的场景。场景类包括圆规、直尺和铅笔三个属性，并实现了对应的 draw_arc 和 draw_line 等方法。

具体的使用方法，请参考示例代码：demo/compass_scene_demo.py。