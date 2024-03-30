import datetime
import random
import numpy as np
from collections import Counter
from pyecharts.charts import Scatter
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pywebio.output import put_html
from pyecharts.charts import Tab
from pyecharts.commons.utils import JsCode
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import WordCloud

df = pd.read_excel("TOP.xlsx")
def getcountrybar(data):
    country_counts = data['国家/地区'].value_counts()
    country_counts = country_counts.sort_values(ascending=True)[-10:]
    c = (
        Bar()
        .add_xaxis(list(country_counts.index))
        .add_yaxis('地区上映数量', country_counts.values.tolist())
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title='地区上映电影数量TOP10'),
            yaxis_opts=opts.AxisOpts(name='国家/地区'),
            xaxis_opts=opts.AxisOpts(name='上映数量'),
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    )
    # 返回 Bar 对象
    return c

def getgenrebar(data):
    # 使用explode()函数将类型分成多个行
    genre_counts = data['类型'].str.split(' / ').explode().value_counts()  # 获取所有电影的类型数量
    genre_counts = genre_counts.groupby(level=0).sum()  # 合并相同类型的电影数量

    # 对类型数量进行排序
    genre_counts = genre_counts.sort_values(ascending=False)

    # 绘制横向滚动的柱状图
    c = (
        Bar()
        .add_xaxis(list(genre_counts.index))
        .add_yaxis('电影类型数量', genre_counts.values.tolist())
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title='高分电影的电影类型数量'),
            yaxis_opts=opts.AxisOpts(name='类型'),
            xaxis_opts=opts.AxisOpts(name='数量'),
            datazoom_opts=opts.DataZoomOpts(orient="vertical"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    )
    # 返回 Bar 对象
    return c



def getzoomline(data):
    year_counts = data['上映年份'].value_counts().sort_index()
    c = (
        Line()
        .add_xaxis([str(year) for year in year_counts.index])
        .add_yaxis(
            "上映数量",
            year_counts.values.tolist(),
            symbol="emptyCircle",
            is_symbol_show=True,
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title='高分电影各年份上映数量'),
            yaxis_opts=opts.AxisOpts(name='上映数量'),
            xaxis_opts=opts.AxisOpts(name='上映年份'),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_='inside')],
        )
    )
    # 返回 Line 对象
    return c


def get_genre_pie(data):
    month_count = data['语言'].value_counts(normalize=True).sort_index()

    # 绘制饼图
    pie_data = [(str(month), count) for month, count in month_count.items()]
    c = (
        Pie()
        .add(
            "",
            pie_data,
            radius=["40%", "75%"],
            label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="高分电影语言占比图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
    )
    return c
def get_genre_pie2(data):
    month_count = data['国家/地区'].value_counts(normalize=True).sort_index()

    # 绘制饼图
    pie_data = [(str(month), count) for month, count in month_count.items()]
    c = (
        Pie()
        .add(
            "",
            pie_data,
            radius=["40%", "75%"],
            label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="高分电影国家/地区分布图"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
        )
    )
    return c


def get_duration_scatter(data):
    duration = data['时长(分钟)']

    # 绘制散点图
    scatter = (
        Scatter()
        .add_xaxis(range(len(duration)))
        .add_yaxis("电影时长", duration, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="电影时长散点图"),
            xaxis_opts=opts.AxisOpts(name="电影排名"),
            yaxis_opts=opts.AxisOpts(name="电影时长（分钟）"),
        )
    )

    return scatter
def film_cloud(df):
    # 生成电影名称的词云图
    title_text = ' '.join(df['片名'].tolist())
    word_counts = Counter(title_text.split())

    title_wordcloud = (
        WordCloud()
        .add(series_name="电影名称", data_pair=list(word_counts.items()), word_size_range=[6, 50])
        .set_global_opts(title_opts=opts.TitleOpts(title="电影名称词云图"))
    )
    return title_wordcloud

def director_cloud(df):
    # 生成导演的词云图
    director_text = ' '.join(df['导演'].tolist())
    # 设置停用词列表
    stop_words = ["/"]
    director_text = ' '.join(word for word in director_text.split() if word not in stop_words)

    word_counts = Counter(director_text.split())
    director_wordcloud = (
        WordCloud()
        .add(series_name="导演", data_pair=word_counts.items(), word_size_range=[6, 66])
        .set_global_opts(title_opts=opts.TitleOpts(title="导演词云图"))
    )
    return director_wordcloud
def writer_cloud(df):
    # 生成编剧的词云图
    writer_text = ' '.join(df['编剧'].tolist())
    # 将编剧文本按空格分割成单独的词
    writer_words = writer_text.split()
    # 设置停用词列表
    stop_words = ["/"]
    # 过滤停用词
    filtered_words = [word for word in writer_words if word not in stop_words]
    # 随机选择指定数量的词
    selected_words = random.sample(filtered_words, 100)
    # 统计每个选中词出现的次数
    word_counts = Counter(selected_words)
    writer_wordcloud = (
        WordCloud()
        .add(series_name="编剧", data_pair=list(word_counts.items()), word_size_range=[10, 60])
        .set_global_opts(title_opts=opts.TitleOpts(title="编剧词云图"))
    )
    return writer_wordcloud

# 调用
c1 = getcountrybar(df)
c2 = getgenrebar(df)
c3 = getzoomline(df)
c4 =get_genre_pie(df)
c5 =get_genre_pie2(df)
c6 =film_cloud(df)
c7 =director_cloud(df)
c8=writer_cloud(df)
c9=get_duration_scatter(df)
tab = (
    Tab(page_title='基于python的豆瓣电影数据可视化分析系统')
    .add(c1, '地区上映电影数量TOP10')
    .add(c2, '高分电影的电影类型数量')
    .add(c3, '高分电影各年份上映数量')
    .add(c4, "高分电影语言占比图")
    .add(c5, "高分电影国家/地区分布图")
    .add(c9, "电影时长散点图")
    .add(c6, "电影名称词云图")
    .add(c7, "导演词云图")
    .add(c8, "编剧词云图")

)



# 将 Tab 对象中的图表显示在 Jupyter Notebook 中的单元格中
put_html(tab.render_notebook())
