__all__ = [
    'MovePencilAlongPath',
    'MovePencilTipTo',
    'DrawPath',
    'PutPencilAway'
]
from typing import Union
from manim.mobject.types.vectorized_mobject import VMobject
from manim.mobject.types.point_cloud_mobject import Point
from manim.animation.movement import MoveAlongPath
from manim.animation.composition import AnimationGroup
from manim.animation.creation import Create
from manim.animation.transform import ApplyMethod

from ..compass.pencil import Pencil

class MovePencilAlongPath(MoveAlongPath):
    '''铅笔笔头沿着指定路径移动的动画效果'''
    def __init__(
        self,
        mobject: Pencil,
        path: VMobject = None,
        suspend_mobject_updating: Union[bool, None] = False,
        **kwargs
    ) -> None:
        start = path.get_start()
        path = path.copy().shift(mobject.get_center() - start)
        super().__init__(mobject, path, suspend_mobject_updating, **kwargs)

class MovePencilTipTo(ApplyMethod):
    def __init__(
        self,
        pencil: Pencil,
        point:Point = None,
        **kwargs
    ):
        '''
        移动铅笔 pencil 以笔尖为参考点,整体移到指定 point 点

        Args:
            pencil: 铅笔
            point: 指定点
        '''
        super().__init__(
            pencil.move_nid_to,
            point,
            **kwargs
        )

class DrawPath(AnimationGroup):
    def __init__(
        self,
        pencil:Pencil,
        path: VMobject = None,
        **kwargs
    ):
        '''
        铅笔笔头沿着指定路径移动,同时绘制路径的动画效果
        
        Args:
            pencil: 铅笔
            path:路径
        '''
        super().__init__(
            Create(path),
            MovePencilAlongPath(pencil,path),
            **kwargs
        )

class PutPencilAway(MovePencilTipTo):
    def __init__(
        self,
        pencil:Pencil,
        point:Point = None,
        **kwargs
    ):
        '''
        收起铅笔动画类：将铅笔 pencil 收起至 point 位置

        Args:
            pencil: 铅笔
            point: 放置位置
        '''
        super().__init__(pencil,point,**kwargs)