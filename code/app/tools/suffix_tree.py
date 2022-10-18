#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/16 0:18
@Author     : jzs
@File       : suffix_tree.py
@Software   : PyCharm
@Description:
"""
import ast


class __TreeNode:
    """
    后缀树的结点
    """

    def __init__(self):
        self.g = {}
        self.f = None

    def __str__(self):
        return str(self.g)

    def __repr__(self):
        return str(self.g)

    def to_tree_dict(self):
        """
        将结点转换成字典树，格式{key:(data, 孩子树)}

        :return: 字典树
        """
        return ast.literal_eval(str(self))


INF = 99999999999  # 定义无限


def __update(root, t, s, k, i):
    oldr = root
    (end_point, r) = __test_and_split(t, s, k, i - 1, t[i])
    while not end_point:
        r_prime = __TreeNode()
        r.g[t[i]] = (i, INF, r_prime)
        if oldr != root:
            oldr.f = r
        oldr = r
        (s, k) = __canonize(t, s.f, k, i - 1)
        (end_point, r) = __test_and_split(t, s, k, i - 1, t[i])
    if oldr != root:
        oldr.f = s
    return (s, k)


def __test_and_split(t, s, k, p, char):
    if k <= p:
        k_prime, p_prime, s_prime = s.g[t[k]]
        if char == t[k_prime + p - k + 1]:
            return (True, s)
        else:
            r = __TreeNode()
            k_prime, p_prime, s_prime = s.g.pop(t[k_prime])
            s.g[t[k_prime]] = (k_prime, k_prime + p - k, r)
            r.g[t[k_prime + p - k + 1]] = (k_prime + p - k + 1, p_prime, s_prime)
            return (False, r)
    else:
        k_prime, p_prime, s_prime = s.g.get(char, (None, None, None))
        return (k_prime is not None, s)


def __canonize(t, s, k, p):
    if p < k:
        return (s, k)
    else:
        k_prime, p_prime, s_prime = s.g[t[k]]
        while p_prime - k_prime <= p - k:
            k += p_prime - k_prime + 1
            s = s_prime
            if k <= p:
                k_prime, p_prime, s_prime = s.g[t[k]]
    return (s, k)


def __make_stree(string: str):
    """
    创建后缀树

    :param string:
    :return:
    """
    root = __TreeNode()
    bot = __TreeNode()
    root.f = bot
    for i, v in enumerate(set(string)):
        bot.g[v] = (-i - 1, -i - 1, root)
    s = root
    k = 1
    t = ' ' + string  # python indexes are 0-based, but the algorithm is 1-based
    for i in range(1, len(t)):
        (s, k) = __update(root, t, s, k, i)
        (s, k) = __canonize(t, s, k, i)
    return root


def create_suffix_tree(string: str) -> 'dict':
    """
    创建后缀树(字典树)，返回后缀树的根

    字典树定义:
    树根：  (0, 0, 孩子树)
    孩子树: { key1: (data1, data2, 孩子树),  ... , keyn: (data1, data2, 孩子树)}

    Example use:
        string = '北邮的北邮人'
        root = create_suffix_tree(string)
        print(root)
    Expected output:
        (0, 0, {
            '北': (1, 2, {
                '的': (3, inf, {}),
                '人': (6, inf, {})
            }),
            '邮': (2, 2, {
                '的': (3, inf, {}),
                '人': (6, inf, {})
            }),
            '的': (3, inf, {}),
            '人': (6, inf, {})
        } )

    :param string: 后缀树字符串
    :return: 后缀树的根（字典树）
    """
    child_tree = __make_stree(string).to_tree_dict()
    root = (0, 0, child_tree)
    return root


def print_suffix_tree(string: str) -> None:
    """
    打印后缀树

    Example use:
        string = 'caocao'
        print_suffix_tree(string)
    Expected output:
        0: (1,2) "邮的"
        1:    (3,inf) "北邮人"
        2: (2,2) "的"
        3:    (3,inf) "北邮人"
        5: (3,inf) "北邮人"

    :param string: 后缀树的字符串
    :return:
    """
    result = []

    def impl(self, indent=0):
        for k, p, s in sorted(self.g.values()):
            substring = string[k:len(string) if p == INF else int(p) + 1]
            result.append('%s(%s,%s) "%s" ' % (' ' * 3 * indent, k, p, substring))
            impl(s, indent=indent + 1)

    root = __make_stree(string)
    impl(root)
    ps = '\n'.join('%i: %s' % (i, v) for i, v in enumerate(result))
    print(ps)
