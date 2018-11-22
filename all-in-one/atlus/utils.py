# coding: utf-8
"""学習とかで使う汎用的な関数などを定義する
"""

from glob import glob
from logging import getLogger, StreamHandler, FileHandler, Formatter

import numpy as np
import pandas as pd
import seaborn as sns
import MySQLdb

from . import env


def get_connection(**kwargs):
    conn = MySQLdb.connect(user=env.MYSQL_USERNAME,
                           passwd=env.MYSQL_PASSWORD,
                           host=env.MYSQL_HOST,
                           db=env.MYSQL_DB_NAME,
                           charset='utf8',
                           **kwargs)
    return conn


def read_data_from_sql(sql):
    """
    Args:
        sql(str):

    Returns:
        pd.DataFrame
    """
    return pd.read_sql(sql, get_connection())


def set_default_style(style='ticks', font='Noto Sans CJK JP', colors=None):
    """
    matplotlib, seaborn でのグラフ描写スタイルを標準的仕様に設定するメソッド
    このメソッドの呼び出しは破壊的です。

    Args:
        style(str):
        font(str):
        colors(None | list[str]):

    Returns: None

    """
    sns.set(style=style, font=font)
    if colors is None:
        colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
        sns.set_palette(sns.xkcd_palette(colors))
    return



def get_logger(name, log_level="DEBUG", output_file=None, handler_level="INFO"):
    """
    :param str name:
    :param str log_level:
    :param str | None output_file:
    :return: logger
    """
    logger = getLogger(name)

    formatter = Formatter("[%(asctime)s] %(message)s")

    handler = StreamHandler()
    logger.setLevel(log_level)
    handler.setLevel(handler_level)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if output_file:
        file_handler = FileHandler(output_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(handler_level)
        logger.addHandler(file_handler)

    return logger


def get_sample_pos_weight(y):
    """

    Args:
        y(np.ndarray): shape = (n_samples, )

    Returns:
        float
    """
    unique, count = np.unique(y, return_counts=True)
    y_sample_weight = dict(zip(unique, count))
    sample_pos_weight = y_sample_weight[0] / y_sample_weight[1]
    return sample_pos_weight


def read_multiple_csv(glob_path, max_cols=1):
    """
    複数の csv を読み込んで列方向に merge する

    Args:
        glob_path(str): 読み込むファイルへのパスの glob text.
            例えば `"./data/**/*.csv"` など
        max_cols(int): これ以上の column を持つ csv は skip する
            例えば 1 が設定されるとカラムが 2 以上のものを無視する

    Returns:

    """
    path_list = glob(glob_path)
    df = pd.DataFrame()
    for p in path_list:
        _df = pd.read_csv(p)
        if len(_df.columns) > max_cols:
            continue
        df = pd.concat([df, _df], axis=1)
    return df
