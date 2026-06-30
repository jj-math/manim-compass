__all__ = [
    'DrawArc',
    'MoveNiddleTipTo',
    'RotateCompass',
    'SplitCompass',
    'PutCompass',
    'PutCompassAway'
]
# from manim import *
import numpy as np
from manim.mobject.geometry.arc import Arc
from manim.mobject.geometry.line import Line
from manim.mobject.types.point_cloud_mobject import Point
from manim.animation.composition import AnimationGroup
from manim.animation.transform import ApplyMethod
from manim.animation.rotation import Rotate
from manim.animation.creation import Create
from manim.constants import RIGHT, LEFT, UP, DOWN

from ..compass import Compass
from ..utils.geometry_method import (
    get_vecs_angle,
    get_distance,
    is_counter_clockwise
)

class DrawArc(AnimationGroup):
    def __init__(
        self,
        compass:Compass,
        arc:Arc,
        **kwargs
    ):
        '''
        尺规作图动画类：画圆弧
        注意：该动画之前,需要先移动圆规 compass 的针尖(niddle_tip)到 arc 的圆心,再移动圆规 compass 的笔尖(pen_tip)放到圆弧的起点
        
        Args:
            compass: 圆规
            arc: 圆弧
        '''
        super().__init__(
            Create(arc),
            RotateCompass(compass,arc.angle),
            **kwargs
        )

class SplitCompass(AnimationGroup):
    def __init__(
        self,
        compass:Compass,
        span:float = None,
        **kwargs
    ):
        '''
        尺规作图动画类：将圆规 compass 的两脚, 均匀的向外(内)旋转, 使得张开的距离为 span;
        同时 niddle_tip 不动
        
        Args:
            compass: 圆规
            span: 圆规两脚张开的距离
        '''
        theta_new, theta_old = np.arcsin(span/2/compass.leg_length), compass.theta
        compass.theta = theta_new
        rotate_angle = theta_old - theta_new
        if is_counter_clockwise(
            compass.get_niddle_tip() - compass.c.get_center(),
            compass.get_pen_tip() - compass.c.get_center()
        ):
            rotate_angle = -rotate_angle
        super().__init__(
            Rotate(
                compass.head,
                about_point = compass.c.get_center(),
                angle = rotate_angle
            ),
            Rotate(
                compass.pen_tip,
                about_point = compass.c.get_center(),
                angle = 2*rotate_angle
            ),
            **kwargs
        )

class RotateCompass(Rotate):
    def __init__(
        self,
        compass:Compass,
        angle:float = None,
        **kwargs
    ):
        '''
        尺规作图动画类：将圆规 compass 绕其针尖旋转 angle 度

        Args:
            compass: 圆规
            angle: 旋转角度
        '''
        super().__init__(
            compass,
            about_point = compass.get_niddle_tip(),
            angle = angle,
            **kwargs
        )

class MoveNiddleTipTo(ApplyMethod):
    def __init__(
        self,
        compass:Compass,
        point:Point = None,
        **kwargs
    ):
        '''
        尺规作图动画类：移动圆规 compass 以尖为参考点,整体移到指定 point 点

        Args:
            compass: 圆规
            point: 指定点
        '''
        super().__init__(
            compass.move_niddle_tip_to,
            point,
            **kwargs
        )

class PutCompass(ApplyMethod):
    def __init__(
        self,
        compass:Compass,
        niddle_pos:Point = None,
        pen_pos:Point = None,
        **kwargs
    ):
        '''
        尺规作图动画类：移动圆规 compass 的 niddle_tip 和 pen_tip 放到指定位置

        Args:
            compass: 圆规
            niddle_pos: niddle_tip的放置点
            pen_pos: pen_tip的放置点
        '''
        arc_radius = get_distance(niddle_pos,pen_pos)
        if arc_radius > compass.leg_length*2:
            raise ValueError("超出了圆规的画图范围")
            
        span_angle = compass.get_compass_rotate_angle_with_span(arc_radius)
        rotate_angle = get_vecs_angle(
            compass.get_niddle2pen_vec(),
            Line(niddle_pos,pen_pos).get_unit_vector()
        )
        super().__init__(
            compass.set_compass,
            span_angle/2,
            rotate_angle,
            niddle_pos,
            **kwargs
        )

class PutCompassAway(PutCompass):
    def __init__(
        self,
        compass:Compass,
        point:Point = RIGHT,
        span_buff:float = 0.1,
        **kwargs
    ):
        '''
        尺规作图动画类：将圆规 compass 放置到 point 点, 使得合并两脚的距离为 span_buff

        Args:
            compass: 圆规
            point: 圆规放置点
            span_buff: 合并两脚的距离
        '''
        r = 0.5*compass.leg_length
        vec = r*DOWN if compass.get_compass_rotate_angle_direction() else r*UP
        super().__init__(
            compass,
            niddle_pos = point + span_buff*LEFT + vec,
            pen_pos = point + span_buff*RIGHT + vec,
            **kwargs
        )