"""
要求pdfminer.six
$ pip install pdfminer.six
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime as dt
import os
import subprocess
from collections.abc import Iterable
from io import StringIO
from os.path import expanduser, join
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
from pandas.api.types import is_number
from pandas.tseries.offsets import BDay, MonthBegin, QuarterBegin, Week
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from cnswd.constants import MARKET_START, ROOT_DIR_NAME


## 日期
def parse_date(x, format='%Y-%m-%d'):
    """以指定日期格式强制转换为日期"""
    if x == '--':
        return pd.NaT
    return pd.to_datetime(x, errors='coerce',
                          infer_datetime_format=True, format=format).date()


def time_for_next_update(last_time, period='D', hour=9):
    """计算下次更新时间
    说明：
        'D'：移动到下一天
        'W'：移动到下周一
        'M'：移动到下月第一天
        'Q'：下一季度的第一天
        将小时调整到指定的hour
    """
    if pd.isnull(last_time):
        return MARKET_START
    period = period.upper()
    if period == 'D':
        d = BDay(normalize=True)
        return d.apply(last_time).replace(hour=hour)
    elif period == 'W':
        w = Week(normalize=True, weekday=0)
        return w.apply(last_time).replace(hour=hour)
    elif period == 'M':
        m = MonthBegin(normalize=True)
        return m.apply(last_time).replace(hour=hour)
    elif period == 'Q':
        q = QuarterBegin(normalize=True)
        return q.apply(last_time).replace(hour=hour)
    else:
        raise TypeError('不能识别的周期类型，仅接受{}'.format(('D', 'W', 'M', 'Q')))


def _sanitize_date(obj, default):
    """转换为日期对象，如果为None则使用默认值。输出datetime.date对象"""
    if isinstance(obj, pd.Timestamp):
        return obj.date()
    # 务必排在dt.date之前
    if isinstance(obj, dt.datetime):
        return obj.date()
    if isinstance(obj, dt.date):
        return obj
    if is_number(obj):
        return dt.date(obj, 1, 1)
    if isinstance(obj, str):
        return pd.to_datetime(obj).date()
    if obj is None:
        return default
    raise ValueError('不能识别的输入日期')


def sanitize_dates(start, end):
    """
    返回日期二元组(date, date)

    当开始日期为None，返回市场开始日期；
    当结束日期为None, 返回当前日期；
    """
    start = _sanitize_date(start, MARKET_START.date())
    end = _sanitize_date(end, dt.datetime.today().date())
    if start > end:
        raise ValueError('开始日期必须小于或等于结束日期')
    return start, end


def loop_period_by(start, end, freq='B',exclude_future=True):
    """按指定频率划循环期间"""
    res = []
    assert freq in ('D', 'B', 'W', 'M', 'Q', 'Y')
    start, end = sanitize_dates(start, end)
    start = pd.Timestamp(start)
    end = pd.Timestamp(end)
    ps = pd.period_range(start, end, freq=freq)
    fmt = r'%Y-%m-%d'
    today = pd.Timestamp('today')
    for p in ps:
        s = pd.Timestamp(p.asfreq('D', 'start').strftime(fmt))
        e = pd.Timestamp(p.asfreq('D', 'end').strftime(fmt))
        # 如果排除未来日期
        if exclude_future:
            if e > today:
                continue
        if s < start:
            s = start
        if e > end:
            e = end
        res.append((s, e))
    return res


## 其他


def get_usable_cpu():
    """返回可用CPU的数量
    
    Returns:
        integer -- 可用cpu数量
    """
    return len(os.sched_getaffinity(0))


def get_server_name(url):
    """获取主机网络地址
    
    Arguments:
        url {string} -- 网址
    
    Returns:
        string -- 返回主机地址
    """
    return urlparse(url)[1]


def ensure_list(x):
    """
    确保输入参数转换为`list`

    Parameters
    ----------
    x : object
        输入

    Returns
    -------
    res : list
        将输入转换为list

    Notes
    -------
		避免无意义的单一字符循环

    Example
    -------
    >>> ensure_list('000001')
    ['000001']
    >>> ensure_list(('000001','000002'))
    ['000001', '000002']
    """
    if isinstance(x, str):
        return [x]
    elif pd.core.dtypes.common.is_number(x):
        return [x]
    elif isinstance(x, Iterable):
        return [v for v in x]
    else:
        raise TypeError('输入参数"x"要么为str对象，要么为可迭代对象。')

## 股票


def loop_codes(input_code, batch_num):
    """分批循环代码"""
    res = []
    codes = ensure_list(input_code)
    total_num = len(codes)
    for start in range(0, total_num, batch_num):
        end = start + batch_num if start + batch_num < total_num else total_num
        res.append(codes[start:end])
    return res


def get_exchange_from_code(stock_code):
    """股票市场分类"""
    f = stock_code[0]
    if f == '2':
        return '深市B'
    elif f == '3':
        return '创业板'
    elif f == '6':
        return '沪市A'
    elif f == '9':
        return '沪市B'
    elif stock_code[:3] == '002':
        return '中小板'
    return '深主板A'


def filter_a(codes):
    """过滤A股代码"""
    codes = ensure_list(codes)
    return [x for x in codes if x[0] in ('0', '3', '6')]


def parse_fields_to_dt(df, columns, dt_fmt='%Y-%m-%d'):
    """将dataframe对象的列解析为Date对象"""
    columns = ensure_list(columns)
    for c in columns:
        df[c] = df[c].apply(pd.to_datetime, errors='coerce', format=dt_fmt)
    return df


def round_price_to_penny(df, ndigits=2):
    """将表中数字类列的小数点调整到指定位数，其余列维持不变"""
    penny_part = df.select_dtypes(include=[np.number], exclude=[np.integer])
    remaining_cols = df.columns.difference(penny_part.columns)
    return pd.concat([df[remaining_cols], penny_part.apply(round, ndigits=ndigits)],
                     axis=1)

## 路径


def data_root(dir_name='data'):
    """在根目录下建立指定名称的子目录"""
    root = expanduser(ROOT_DIR_NAME)
    path = join(root, dir_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def to_plural(word):
    """转换为单词的复数"""
    word = word.lower()
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word + 's'


def to_table_name(class_name):
    """
    将骆峰风格类名称转换为数据库表名称

    Parameters
    ----------
    class_name : string
        骆峰风格类名称

    Returns
    -------
    res : string
        小写字符名称，除首字符外，大写字符以“_”连接
        以"_"连接的尾部名词以复数表示

    Example
    -------
    >>> to_table_name('ClassName')
    class_names

    """
    if not class_name.isidentifier():
        raise ValueError('无效类名称')
    # 如果全部为大写，则返回小写复数形式
    tmp = []
    for i in range(len(class_name)):
        tmp.append(class_name[i].isupper())
    if all(tmp):
        return to_plural(class_name.lower())
    res = class_name[0].lower()
    for i in range(1, len(class_name)):
        if class_name[i].isupper() and not class_name[i].isdigit():
            res += '_' + class_name[i].lower()
        else:
            res += class_name[i].lower()
    parts = res.split('_')
    parts[-1] = to_plural(parts[-1])
    return '_'.join(parts)


def is_connectivity(server):
    """判断网络是否连接"""
    fnull = open(os.devnull, 'w')
    result = subprocess.call('ping ' + server + ' -c 2',
                             shell=True, stdout=fnull, stderr=fnull)
    if result:
        res = False
    else:
        res = True
    fnull.close()
    return res


def most_recent_path(file_dir):
    """获取文件目录下最新的文件路径
    
    Arguments:
        file_dir {str} -- 要寻找的文件目录
    
    Raises:
        FileNotFoundError -- 文件目录下不存在文件
    
    Returns:
        [type] -- [description]
    """
    try:
        iterms = os.scandir(file_dir)
        return sorted(iterms, key=lambda x: x.stat().st_ctime, reverse=True)[0].path
    except:
        raise FileNotFoundError('目录：{} 不存在文件'.format(file_dir))


def get_pdf_text(fname, pages=None):
    """读取pdf文件内容"""
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text
