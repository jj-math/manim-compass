__all__ = [
    'PutRuler',
    'PutRulerAway'
]
# from manim import *
from manim.mobject.types.point_cloud_mobject import Point
from manim.animation.transform import ApplyMethod
from manim.constants import RIGHT, LEFT, UP, DOWN

from ..compass.ruler import Ruler

class PutRuler(ApplyMethod):
    def __init__(
        self,
        ruler:Ruler,
        start:Point = None,
        end:Point = None,
        **kwargs
    ):
        '''
        尺规作图动画类：将直尺 ruler 旋转 angle 度,使其与 start - end 平行

        Args:
            ruler: 直尺
            start: 起始点
            end: 终止点
        '''
        super().__init__(
            ruler.set_ruler,
            start,
            end,
            **kwargs
        )

class PutRulerAway(PutRuler):
    def __init__(
        self,
        ruler:Ruler,
        point:Point = None,
        is_flat:bool = True,
        **kwargs
    ):
        '''
        收起直尺动画类：将直尺 ruler 收起至 point 位置

        Args:
            ruler: 直尺
            point: 放置位置
            is_flat: 水平(竖直)放置
        '''
        if is_flat:
            start = point + LEFT
            end = point + RIGHT
        else:
            start = point + UP
            end = point + DOWN
        super().__init__(
            ruler,
            start,
            end,
            **kwargs
        )