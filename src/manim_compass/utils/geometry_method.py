__all__ =[
    "get_arc",
]
import numpy as np
from manim.mobject.geometry.arc import Arc
from manim.constants import RIGHT
from manim.utils.color.manim_colors import YELLOW

def get_arc(
    niddle_pos:np.ndarray,
    pen_pos:np.ndarray,
    angle:float,
    color = YELLOW,
    **kwargs
)-> Arc:
    arc_radius = get_distance(niddle_pos,pen_pos)
    vec_s = pen_pos - niddle_pos
    return Arc(
        arc_center = niddle_pos,
        radius = arc_radius,
        start_angle = get_vecs_angle(RIGHT,vec_s),
        angle = angle,
        color = color,
        **kwargs
    )

def get_distance(
    point_start:np.ndarray,
    point_end:np.ndarray
)-> float:
    """计算两点距离"""
    return np.linalg.norm(point_start - point_end)

def is_counter_clockwise(
    vector_start:np.ndarray,
    vector_end:np.ndarray
)-> bool:
    """判断向量 vector_end 是否在 vector_start 的逆时针方向"""
    return np.cross(vector_start,vector_end)[-1] > 0

def get_vecs_angle(
    vec_s:np.ndarray,
    vec_e:np.ndarray
)-> float:
    """
    计算向量 vec_s = (x1,y1) 到 vec_e = (x2,y2) 的夹角:

    区分顺、逆时针(sign = x1*y2 - x2*y1):
        sign > 0, vec_e 在 vec_s 的逆时针方向;
        sign < 0,为顺时针方向;
        sign = 0,共线
    """
    angle = np.arccos(
        np.true_divide(
            np.dot(vec_s,vec_e),
            np.linalg.norm(vec_s) * np.linalg.norm(vec_e)
        )
    )
    return angle if is_counter_clockwise(vec_s,vec_e) else -angle