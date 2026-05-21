"""
TBPU（Text Block Processing Unit）排版解析器。

移植自 Umi-OCR 的 GapTree 间隙树排序算法，含：
  - 行预处理（旋转矫正 + bbox 标准化）
  - GapTree 多列阅读顺序排序
  - 段落分析（预测行末分隔符：空格 / 连字符 / 换行）
"""

from __future__ import annotations

from math import atan2, cos, sin, sqrt, pi, radians
from statistics import median
from typing import Callable
import unicodedata


# ============================================================
# 行预处理
# ============================================================

_ANGLE_THRESHOLD = 3
_ANGLE_THRESHOLD_RAD = radians(_ANGLE_THRESHOLD)


def _distance(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def _calculate_angle(box):
    width = _distance(box[0], box[1])
    height = _distance(box[1], box[2])
    if width < height:
        angle_rad = atan2(box[2][1] - box[1][1], box[2][0] - box[1][0])
    else:
        angle_rad = atan2(box[1][1] - box[0][1], box[1][0] - box[0][0])
    if angle_rad < -pi / 2 + _ANGLE_THRESHOLD_RAD:
        angle_rad += pi
    elif angle_rad >= pi / 2 + _ANGLE_THRESHOLD_RAD:
        angle_rad -= pi
    return angle_rad


def _get_bboxes(text_blocks, rotation_rad):
    if abs(rotation_rad) <= _ANGLE_THRESHOLD_RAD:
        return [
            (
                min(x for x, y in tb["box"]),
                min(y for x, y in tb["box"]),
                max(x for x, y in tb["box"]),
                max(y for x, y in tb["box"]),
            )
            for tb in text_blocks
        ]
    cos_a = cos(-rotation_rad)
    sin_a = sin(-rotation_rad)
    bboxes = []
    min_x, min_y = float("inf"), float("inf")
    for tb in text_blocks:
        rotated = [(cos_a * x - sin_a * y, sin_a * x + cos_a * y) for x, y in tb["box"]]
        xs, ys = zip(*rotated)
        bbox = (min(xs), min(ys), max(xs), max(ys))
        bboxes.append(bbox)
        min_x, min_y = min(min_x, bbox[0]), min(min_y, bbox[1])
    if min_x < 0 or min_y < 0:
        bboxes = [(x - min_x, y - min_y, x2 - min_x, y2 - min_y) for x, y, x2, y2 in bboxes]
    return bboxes


def line_preprocessing(text_blocks: list) -> list:
    """行预处理：过滤空文本块，计算旋转角度，生成归一化 bbox，按 Y 排序。

    Args:
        text_blocks: OCR 文本块列表（含 box 和 text 字段）。

    Returns:
        预处理后的文本块列表。
    """
    text_blocks = [tb for tb in text_blocks if tb.get("text")]
    if not text_blocks:
        return text_blocks
    angles = (_calculate_angle(tb["box"]) for tb in text_blocks)
    rotation_rad = median(angles)
    bboxes = _get_bboxes(text_blocks, rotation_rad)
    for i, tb in enumerate(text_blocks):
        tb["normalized_bbox"] = bboxes[i]
    text_blocks.sort(key=lambda tb: tb["normalized_bbox"][1])
    return text_blocks


# ============================================================
# GapTree 间隙树排序
# ============================================================

class GapTree:
    """
    GapTree 排序算法 — 按人类阅读顺序重排页面文本块。
    Author: hiroi-sora (https://github.com/hiroi-sora/GapTree_Sort_Algorithm)
    """

    def __init__(self, get_bbox: Callable):
        self.get_bbox = get_bbox
        self.current_rows = []
        self.current_cuts = []
        self.current_nodes = []

    def sort(self, text_blocks: list) -> list:
        """按人类阅读顺序排序文本块。

        Args:
            text_blocks: 预处理后的文本块列表。

        Returns:
            重排后的文本块列表。
        """
        units, page_l, page_r = self._get_units(text_blocks, self.get_bbox)
        cuts, rows = self._get_cuts_rows(units, page_l, page_r)
        root = self._get_layout_tree(cuts, rows)
        nodes = self._preorder_traversal(root)
        new_text_blocks = self._get_text_blocks(nodes)
        self.current_rows = rows
        self.current_cuts = cuts
        self.current_nodes = nodes
        return new_text_blocks

    def get_nodes_text_blocks(self) -> list:
        """获取最近一次排序结果中各节点的文本块分组。

        Returns:
            二维列表，每项为一个节点内的文本块列表。
        """
        result = []
        for node in self.current_nodes:
            if node["units"]:
                result.append([unit[1] for unit in node["units"]])
        return result

    def _get_units(self, text_blocks, get_bbox):
        units = []
        page_l, page_r = float("inf"), -1
        for tb in text_blocks:
            x0, y0, x2, y2 = get_bbox(tb)
            units.append(((x0, y0, x2, y2), tb))
            page_l = min(page_l, x0)
            page_r = max(page_r, x2)
        units.sort(key=lambda a: a[0][1])
        return units, page_l, page_r

    def _get_cuts_rows(self, units, page_l, page_r):
        def update_gaps(gaps1, gaps2):
            flags1 = [True] * len(gaps1)
            flags2 = [True] * len(gaps2)
            new_gaps1 = []
            for i1, g1 in enumerate(gaps1):
                l1, r1, _ = g1
                for i2, g2 in enumerate(gaps2):
                    l2, r2, _ = g2
                    inter_l = max(l1, l2)
                    inter_r = min(r1, r2)
                    if inter_l <= inter_r:
                        new_gaps1.append((inter_l, inter_r, g1[2]))
                        flags1[i1] = False
                        flags2[i2] = False
            for i2, f2 in enumerate(flags2):
                if f2:
                    new_gaps1.append(gaps2[i2])
            del_gaps1 = [gaps1[i1] for i1, f1 in enumerate(flags1) if f1]
            return new_gaps1, del_gaps1

        page_l -= 1
        page_r += 1
        rows = []
        completed_cuts = []
        gaps = []
        row_index = 0
        unit_index = 0
        l_units = len(units)

        while unit_index < l_units:
            unit = units[unit_index]
            u_bottom = unit[0][3]
            row = [unit]
            for i in range(unit_index + 1, len(units)):
                next_u = units[i]
                if next_u[0][1] > u_bottom:
                    break
                row.append(next_u)
                unit_index = i
            row.sort(key=lambda x: (x[0][0], x[0][2]))

            row_gaps = []
            search_start = page_l
            for u in row:
                l = u[0][0]
                r = u[0][2]
                if l > search_start:
                    row_gaps.append((search_start, l, row_index))
                if r > search_start:
                    search_start = r
            row_gaps.append((search_start, page_r, row_index))

            gaps, del_gaps = update_gaps(gaps, row_gaps)
            row_max = row_index - 1
            for dg in del_gaps:
                completed_cuts.append((*dg, row_max))
            rows.append(row)
            unit_index += 1
            row_index += 1

        row_max = len(rows) - 1
        for g in gaps:
            completed_cuts.append((*g, row_max))
        completed_cuts.sort(key=lambda c: c[0])
        return completed_cuts, rows

    def _get_layout_tree(self, cuts, rows):
        rows_gaps = [[] for _ in rows]
        for cut in cuts:
            for r_i in range(cut[2], cut[3] + 1):
                rows_gaps[r_i].append((cut[0], cut[1]))

        root = {
            "x_left": cuts[0][0] - 1,
            "x_right": cuts[-1][1] + 1,
            "r_top": -1,
            "r_bottom": -1,
            "units": [],
            "children": [],
        }
        completed_nodes = [root]
        now_nodes = []

        def complete(node):
            node_r = node["x_right"] - 2
            max_nodes = []
            max_r = -2
            for com_node in completed_nodes:
                if node_r < com_node["x_left"] or node_r > com_node["x_right"] + 0.0001:
                    continue
                if com_node["r_bottom"] >= node["r_top"]:
                    continue
                if com_node["r_bottom"] > max_r:
                    max_r = com_node["r_bottom"]
                    max_nodes = [com_node]
                elif com_node["r_bottom"] == max_r:
                    max_nodes.append(com_node)
            max_node = max(max_nodes, key=lambda n: n["x_right"])
            max_node["children"].append(node)
            completed_nodes.append(node)

        for r_i, row in enumerate(rows):
            row_gaps = rows_gaps[r_i]
            u_i = g_i = 0
            new_nodes = []

            for node in now_nodes:
                l_flag = r_flag = False
                completed_flag = False
                x_left = node["x_left"]
                x_right = node["x_right"]
                for gap in row_gaps:
                    if gap[1] == x_left:
                        l_flag = True
                    if gap[0] == x_right:
                        r_flag = True
                    if x_left < gap[0] < x_right or x_left < gap[1] < x_right:
                        completed_flag = True
                        break
                if not l_flag or not r_flag:
                    completed_flag = True
                if completed_flag:
                    complete(node)
                else:
                    node["r_bottom"] = r_i
                    new_nodes.append(node)
            now_nodes = new_nodes

            while u_i < len(row):
                unit = row[u_i]
                x_l = row_gaps[g_i][1]
                x_r = row_gaps[g_i + 1][0]
                if unit[0][0] + 0.0001 > x_r:
                    g_i += 1
                    continue
                flag = False
                for node in now_nodes:
                    if node["x_left"] == x_l and node["x_right"] == x_r:
                        node["units"].append(unit)
                        flag = True
                        break
                if flag:
                    u_i += 1
                    continue
                now_nodes.append({
                    "x_left": x_l,
                    "x_right": x_r,
                    "r_top": r_i,
                    "r_bottom": r_i,
                    "units": [unit],
                    "children": [],
                })
                u_i += 1

        for node in now_nodes:
            complete(node)
        for node in completed_nodes:
            node["children"].sort(key=lambda n: n["x_left"])
            node["units"].sort(key=lambda u: u[0][1])
        return root

    def _preorder_traversal(self, root):
        if not root:
            return []
        stack = [root]
        result = []
        while stack:
            node = stack.pop()
            result.append(node)
            stack += reversed(node["children"])
        return result

    def _get_text_blocks(self, nodes):
        result = []
        for node in nodes:
            for unit in node["units"]:
                result.append(unit[1])
        return result


# ============================================================
# 段落分析
# ============================================================

_TH = 1.2


def _word_separator(letter1: str, letter2: str) -> str:
    def is_cjk(ch):
        """判断字符是否属于 CJK 字符集。

        Args:
            ch: 单个字符。

        Returns:
            True 如果是 CJK 字符。
        """
        cjk_ranges = [
            (0x4E00, 0x9FFF), (0x3040, 0x30FF), (0x1100, 0x11FF),
            (0x3130, 0x318F), (0xAC00, 0xD7AF),
            (0x3000, 0x303F), (0xFE30, 0xFE4F), (0xFF00, 0xFFEF),
        ]
        return any(s <= ord(ch) <= e for s, e in cjk_ranges)

    if is_cjk(letter1) and is_cjk(letter2):
        return ""
    if letter1 == "-":
        return ""
    if unicodedata.category(letter2).startswith("P"):
        return ""
    return " "


class ParagraphParse:
    """段落分析器 — 预测行间分隔符（空格/换行）。"""
    def __init__(self, get_info: Callable, set_end: Callable):
        self.get_info = get_info
        self.set_end = set_end

    def run(self, text_blocks: list) -> list:
        """对文本块列表执行段落分析，设置行末分隔符。

        Args:
            text_blocks: 带 bbox 和 text 的文本块列表。

        Returns:
            处理后的文本块列表。
        """
        units = self._get_units(text_blocks)
        self._parse(units)
        return text_blocks

    def _get_units(self, text_blocks):
        units = []
        for tb in text_blocks:
            bbox, text = self.get_info(tb)
            units.append((bbox, (text[0], text[-1]), tb))
        return units

    def _parse(self, units):
        units.sort(key=lambda a: a[0][1])
        para_l, para_top, para_r, para_bottom = units[0][0]
        para_line_h = para_bottom - para_top
        para_line_s = None
        now_para = [units[0]]
        paras = []
        paras_line_space = []

        for i in range(1, len(units)):
            l, top, r, bottom = units[i][0]
            h = bottom - top
            ls = top - para_bottom
            if (
                abs(para_l - l) <= para_line_h * _TH
                and abs(para_r - r) <= para_line_h * _TH
                and (para_line_s is None or ls < para_line_s + para_line_h * 0.5)
            ):
                para_l = (para_l + l) / 2
                para_r = (para_r + r) / 2
                para_line_h = (para_line_h + h) / 2
                para_line_s = ls if para_line_s is None else (para_line_s + ls) / 2
                now_para.append(units[i])
            else:
                paras.append(now_para)
                paras_line_space.append(para_line_s)
                now_para = [units[i]]
                para_l, para_r, para_line_h = l, r, bottom - top
                para_line_s = None
            para_bottom = bottom

        paras.append(now_para)
        paras_line_space.append(para_line_s)

        # 合并孤行
        for i1 in reversed(range(len(paras))):
            para = paras[i1]
            if len(para) == 1:
                l, top, r, bottom = para[0][0]
                up_flag = down_flag = False
                if i1 > 0:
                    up_l, up_top, up_r, up_bottom = paras[i1 - 1][-1][0]
                    up_h = up_bottom - up_top
                    up_flag = abs(up_l - l) <= up_h * _TH and r <= up_r + up_h * _TH
                    if (
                        paras_line_space[i1 - 1] is not None
                        and top - up_bottom > paras_line_space[i1 - 1] + up_h * 0.5
                    ):
                        up_flag = False
                if i1 < len(paras) - 1:
                    down_l, down_top, down_r, down_bottom = paras[i1 + 1][0][0]
                    down_h = down_bottom - down_top
                    if down_l - down_h * _TH <= l <= down_l + down_h * (1 + _TH):
                        if len(paras[i1 + 1]) > 1:
                            down_flag = abs(down_r - r) <= down_h * _TH
                        else:
                            down_flag = down_r - down_h * _TH < r
                    if (
                        paras_line_space[i1 + 1] is not None
                        and down_top - bottom > paras_line_space[i1 + 1] + down_h * 0.5
                    ):
                        down_flag = False

                if up_flag and down_flag:
                    if top - paras[i1 - 1][-1][0][3] < paras[i1 + 1][0][0][1] - bottom:
                        paras[i1 - 1].append(para[0])
                    else:
                        paras[i1 + 1].insert(0, para[0])
                elif up_flag:
                    paras[i1 - 1].append(para[0])
                elif down_flag:
                    paras[i1 + 1].insert(0, para[0])
                if up_flag or down_flag:
                    del paras[i1]
                    del paras_line_space[i1]

        for para in paras:
            for i1 in range(len(para) - 1):
                sep = _word_separator(para[i1][1][1], para[i1 + 1][1][0])
                self.set_end(para[i1][2], sep)
            self.set_end(para[-1][2], "\n")


# ============================================================
# 公开接口
# ============================================================


def run_tbpu(text_blocks: list) -> list:
    """
    对一页 OCR 文本块执行完整排版解析。

    每次调用创建独立的 GapTree / ParagraphParse 实例，确保线程安全。

    Returns:
        排序后的文本块列表，每个块增加 "end" 键（行末分隔符）。
    """
    if not text_blocks:
        return text_blocks
    text_blocks = line_preprocessing(text_blocks)
    if not text_blocks:
        return text_blocks

    gtree = GapTree(lambda tb: tb["normalized_bbox"])
    pp = ParagraphParse(
        get_info=lambda tb: (tb["normalized_bbox"], tb["text"]),
        set_end=lambda tb, end: tb.__setitem__("end", end),
    )

    text_blocks = gtree.sort(text_blocks)
    nodes = gtree.get_nodes_text_blocks()
    for tbs in nodes:
        pp.run(tbs)
        for tb in tbs:
            tb.pop("normalized_bbox", None)
    return text_blocks
