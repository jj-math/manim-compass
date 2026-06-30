__all__ =[
    'Compass',
]
# from manim import *
import numpy as np
from manim.mobject.geometry.line import Line
from manim.mobject.geometry.arc import Circle
from manim.mobject.geometry.polygram import Polygon,Rectangle
from manim.mobject.types.point_cloud_mobject import Point
from manim.mobject.types.vectorized_mobject import VGroup
from manim.utils.color import *
from manim.constants import *

from ..utils.geometry_method import (
    get_distance,
    is_counter_clockwise
)

class Compass(VGroup):
    '''圆规类'''
    def __init__(
        self,
        span = 1.5,
        head_color = WHITE,
        niddle_color = RED,
        pen_color = YELLOW,
        stroke_width = 2,
        leg_length = 3.1,
        leg_width = 0.12,
        r = 0.2,
        **kwargs
    ):
        super().__init__(
            stroke_width = stroke_width,
            **kwargs
        )
        self.head_color = head_color
        self.niddle_color = niddle_color
        self.pen_color = pen_color
        self.span = span
        self.leg_length = leg_length
        self.r = r
        self.leg_width = leg_width
        self._init_compass()

    def _init_compass(self):
        s, l, r, w = self.span, self.leg_length, self.r, self.leg_width
        self.theta = np.arcsin(s/2/l)

        self.c = Circle(
            radius = r,
            color = self.head_color,
            fill_opacity = 1
        )
        c2 = Circle(
            radius = 1.25*r,
            color = self.head_color,
            stroke_width = self.stroke_width
        )

        self.niddle_tip = Polygon(
            ORIGIN, l * RIGHT, (l - w*np.sqrt(3)) * RIGHT + w * DOWN, w * DOWN,
            stroke_width = 0,
            fill_color = self.niddle_color,
            fill_opacity = 0.75
        ).rotate(-PI/2 - self.theta, about_point = self.c.get_center())
        self.pen_tip = Polygon(
            ORIGIN, l * RIGHT, (l - w*np.sqrt(3)) * RIGHT + w * UP, w * UP,
            stroke_width = 0,
            fill_color = self.pen_color,
            fill_opacity = 0.75
        ).rotate(-PI/2 + self.theta, about_point = self.c.get_center())

        h = Rectangle(
            width = 0.5*r,
            height = 1.8*r,
            color = self.head_color,
            fill_opacity = 1
        ).next_to(self.c,UP,buff = 0)
        self.head = VGroup(h, self.c, c2)
        self.add(self.niddle_tip, self.pen_tip, self.head)
        self.move_to(ORIGIN)
        return self

    def get_niddle_tip(self):
        '''获取针尖坐标'''
        return self.niddle_tip.get_vertices()[1]

    def get_pen_tip(self):
        '''获取笔尖坐标'''
        return self.pen_tip.get_vertices()[1]
    
    def get_niddle2pen_vec(self):
        '''获取针尖到笔尖的向量'''
        return Line(
            self.get_niddle_tip(),
            self.get_pen_tip()
        ).get_unit_vector()
    
    def get_span(self):
        '''获取圆规的跨度:笔尖与针尖的距离'''
        return get_distance(
            self.get_pen_tip(),
            self.get_niddle_tip()
        )

    def move_niddle_tip_to(self, pos:Point):
        '''将圆规以针尖为参照,整体移动到指定 pos 位置'''
        self.shift(pos - self.get_niddle_tip())
        return self

    def rotate_about_niddle_tip(self, angle = PI/2):
        self.rotate(
            angle = angle,
            about_point = self.get_niddle_tip()
        )
        return self

    def reverse_tip(self):
        '''镜像翻转针尖和笔尖'''
        self.flip(
            axis = self.head[0].get_end() - self.head[0].get_start(),
            about_point = self.c.get_center()
        )
        return self

    def split_copass_with_gain_angle(self,angle:float):
        '''将圆规的两脚,再张开 angle 角度'''
        self.niddle_tip.rotate(
            angle = -angle,
            about_point = self.c.get_center()
        )
        self.pen_tip.rotate(
            angle = angle,
            about_point = self.c.get_center()
        )
        return self

    def split_compass_with_niddle_tip_fixed(
        self,
        angle:float,
        niddle_tip_pos:Point
    ):
        '''针尖固定,将圆规的两脚,再张开 angle 角度'''
        self.split_copass_with_gain_angle(angle = angle)
        self.move_niddle_tip_to(niddle_tip_pos)
        return self
    
    def get_compass_rotate_angle_direction(self)->bool:
        '''判断圆规两支脚间，是顺时针还是逆时针'''
        return is_counter_clockwise(
            self.get_niddle_tip() - self.c.get_center(),
            self.get_pen_tip() - self.c.get_center()
        )

    def get_compass_rotate_angle_with_span(self,span:float)->float:
        '''将圆规两脚张成 span 时, 返回两脚的夹角'''
        L = self.leg_length
        distance = self.get_span()
        span_start = 2*L if distance > 2*L else distance
        span_res = np.arccos(1 - span_start*span_start/L/L/2) - np.arccos(1 - span*span/L/L/2)
        if self.get_compass_rotate_angle_direction():
            span_res = -span_res
        return span_res

    def set_compass(
        self,
        span_angle:float,
        rotate_angle:float,
        niddle_tip_pos:Point
    ):
        '''设置圆规的跨度、旋转角度和针尖位置'''
        self.split_compass_with_niddle_tip_fixed(span_angle,niddle_tip_pos)
        self.rotate(
            angle = rotate_angle,
            about_point = niddle_tip_pos
        )
        return self