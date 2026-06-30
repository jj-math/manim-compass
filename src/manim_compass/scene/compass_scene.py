__all__ = [
    'CompassScene'
]
# from manim import *
from typing import List

from manim.mobject.geometry.line import Line
from manim.mobject.geometry.arc import Arc
from manim.mobject.types.point_cloud_mobject import Point
from manim.animation.animation import Animation
from manim.animation.composition import AnimationGroup
from manim.animation.rotation import Rotate
from manim.animation.creation import Create
from manim.scene.moving_camera_scene import MovingCameraScene
from manim.utils.rate_functions import linear
from manim.utils.color.manim_colors import YELLOW
from manim.constants import *

from ..compass import Compass,Ruler,Pencil
from ..animations import *
from ..utils.geometry_method import (
    get_distance,
    get_vecs_angle
)

class CompassScene(MovingCameraScene):
    '''
    带有圆规、直尺、铅笔的场景类,主要实现：圆规的放置、画圆弧等操作；直尺和铅笔的动画
    '''
    def setup(self):
        self.compass = Compass(span = 0.5).to_edge(LEFT)
        self.ruler = Ruler().to_edge(DOWN)
        self.pencil = Pencil().to_corner(UR)

    def compass_move_niddle_tip_to(self,pos = ORIGIN,run_time = 1):
        '''将圆规的niddle_tip移动到pos'''
        self.play(
            self.compass.animate.move_niddle_tip_to(pos),
            # MoveNiddleTipTo(self.compass,pos),
            run_time = run_time
        )

    def rotate_compass_about_niddle_tip(
        self,
        angle_or_arc:float | Arc,
        arc:Arc = None,
        added_anims:List[Animation] = None,
        **kwargs
    ):
        '''
        以圆规的针脚niddle_tip为圆心, 旋转angle
        '''
        anims = [
            Rotate(
                self.compass,
                about_point = self.compass.get_niddle_tip(),
                angle = angle_or_arc.angle if isinstance(angle_or_arc,Arc) else angle_or_arc
            ),
            # RotateCompass(self.compass,angle = angle_or_arc.angle if isinstance(angle_or_arc,Arc) else angle_or_arc)
        ]
        if added_anims is not None:
            anims.extend(added_anims)
        if isinstance(angle_or_arc,Arc):
            anims.append(Create(angle_or_arc))
        self.play(*anims, **kwargs)

    def compass_split_span(self,span = 3,run_time = 1):
        '''将圆规的两脚, 均匀的向外、向内旋转, 使得张开的距离为span'''
        self.play(
            SplitCompass(self.compass,span = span),
            run_time = run_time,
            rate_func = linear
        )

    def split_cmpass_span(self,span = 1,run_time = 1):
        '''
        固定niddle_tip后, 在niddle_tip和pen_tip的连线上, 移动pen_tip,达到指定的宽度
        '''
        angle = self.compass.get_compass_rotate_angle_with_span(span)
        self.play(
            self.compass.animate.split_compass_with_niddle_tip_fixed(
                angle/2,
                self.compass.get_niddle_tip()
            ),
            run_time = run_time
        )

    def set_compass(
        self,
        niddle_pos:Point = None,
        pen_pos:Point = None,
        run_time:float = 1.0
    ):
        '''
        将圆规放到指定的位置上: niddle_tip 移到 niddle_pos,pen_tip 移到 pen_pos

        args
            niddle_pos: 圆规的支脚尖(niddle_tip)指向的位置
            pen_pos: 圆规的笔头(pen_tip)指向的位置
        '''
        self.play(
            PutCompass(
                self.compass,
                niddle_pos = niddle_pos,
                pen_pos = pen_pos,
            ),
            run_time = run_time
        )

    def draw_arc(
        self,
        niddle_point = ORIGIN,
        pen_point = RIGHT,
        angle = PI/3,
        move_time = 1.0,
        wait_time = 1.0,
        run_time = 1.0,
        arc_color = None,
        **kwargs
    )-> Arc:
        '''
        使用圆规画圆弧: 通过 niddle_point 和 pen_point 计算圆弧半径

        args
            niddle_point : 圆弧的圆心
            pen_point : 圆弧的起始点
            angle : 圆弧的圆心角
            move_time : 移动圆规的时间
            run_time : 画圆弧的时间
            wait_time : 两个动画之间的等待时间
            arc_color : 圆弧的颜色
            kwargs : 圆弧的其他关键词参数
        return
            返回所画的圆弧
        '''
        self.set_compass(
            niddle_point,
            pen_point,
            run_time = move_time
        )
        if wait_time > 0:
            self.wait(wait_time)
        arc_radius = get_distance(niddle_point,pen_point)
        arc = Arc(
            arc_center = niddle_point,
            radius = arc_radius,
            start_angle = get_vecs_angle(RIGHT,self.compass.get_niddle2pen_vec()),
            angle = angle,
            color = self.compass.pen_tip.get_color() if arc_color is None else arc_color,
            **kwargs
        )
        self.play(
            DrawArc(
                self.compass,
                arc,
            ),
            run_time = run_time
        )
        return arc
    
    def flip_compass(self,run_time = 1):
        '''翻转圆规'''
        self.play(
            self.compass.animate.reverse_tip(),
            run_time = run_time
        )

    def put_compass_aside(
        self,
        aside_pos:Point = RIGHT,
        span_buff:float = 0.1,
        run_time:float = 1.0
    ):
        '''
        将圆规放置于一边

        args
            aside_pos:圆规放置的位置
            span_buff:放置圆规时,圆规的两脚距离
            run_time:放置需要的时间
        '''
        r = 0.5*self.compass.leg_length
        vec = r*DOWN if self.compass.get_compass_rotate_angle_direction() else r*UP
        self.set_compass(
            niddle_pos = aside_pos + span_buff*LEFT + vec ,
            pen_pos = aside_pos + span_buff*RIGHT + vec,
            run_time = run_time
        )
    
    def set_ruler(
        self,
        start:Point = None,
        end:Point = None,
        lag_ratio:float = 0.5,
        run_time:float = 1.0,
        with_pencil:bool = True
    ):
        '''
        放置直尺,使直尺的一边对齐start和end两点

        args
            start:直尺放置的起始点
            end:直尺放置的终点
            lag_ratio:直尺和铅笔的放置动画的延迟比例
            run_time:放置直尺的时间
            with_pencil:是否同时放置铅笔
        '''
        if with_pencil:
            self.play(
                AnimationGroup(
                    PutRuler(self.ruler,start = start,end = end),
                    MovePencilTipTo(self.pencil,start),
                    lag_ratio = lag_ratio
                ),
                run_time = run_time
            )
        else:
            self.play(
                PutRuler(self.ruler,start = start,end = end),
                run_time = run_time
            )

    def set_pencil(self,pos,run_time = 1.0):
        self.play(
            self.pencil.animate.move_nid_to(pos),
            # MovePencilTipTo(self.pencil,pos),
            run_time = run_time
        )

    def draw_line(
        self,
        start:Point = None,
        end:Point = None,
        run_time:float = 1.0,
        with_pencil:bool = True,
        color = YELLOW,
        **kwargs
    )-> Line:
        '''用直尺画直线'''
        self.set_ruler(start = start,end = end,run_time = 0.5*run_time,with_pencil = with_pencil)
        line = Line(start,end,color = color,**kwargs)
        if with_pencil:
            self.play(
                DrawPath(self.pencil,line),
                run_time = 0.5*run_time
            )
        else:
            self.play(
                Create(line),
                run_time = 0.5*run_time
            )
        return line
    
    def put_pencil_away(self,pos = 3*DOWN,run_time = 1):
        curr_pos = self.pencil.get_center()
        self.play(
            self.pencil.animate.shift(pos - curr_pos),
            run_time = run_time
        )

    def put_ruler_aside(
        self,
        aside_pos:Point = 3*DOWN,
        horizontal_or_vertical:bool = True,
        run_time:float = 1.0
    ):
        '''
        将直尺放置到aside_pos

        args
            aside_pos:直尺将要放置的位置
            horizontal_or_vertical:是否水平放置
            run_time:放置所需时间
        '''
        vec_w = self.ruler.get_direction_vector_of_ruler()
        vec = RIGHT if horizontal_or_vertical else DOWN
        self.play(
            Rotate(
                self.ruler,
                about_point = self.ruler.get_center(),
                angle = get_vecs_angle(vec_w,vec)
            ),
            run_time = 0.35*run_time
        )
        self.play(
            self.ruler.animate.move_to(aside_pos),
            run_time = 0.65*run_time
        )