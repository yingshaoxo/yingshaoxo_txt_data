word_data = """
human 人类
core 核心
value 价值
if 如果
you 你
can't 不能
find 找到
freedom 自由
can 能
die 死
what 什么
is 是
an 一个
advanced 高级的
animal 动物
do 做
a lot 很多
things 事情
way 方法
get 得到
have 有
a 一个
man 男人
and 和
woman 女人
let 让
them 它们
make 做
love 爱
then 然后
could 可以
new 新
bady 宝贝
create 创造
creature 生物
from 从
basics 基础
just 只是
copy 复制
some 一些
has 有
temperature 温度
virtual 虚拟
computer 电脑
3D 3维
engine 引擎
make sure 确保
it 它
matches 匹配上
all 所有
live 活着
behavior 行为
composed 构成的
by 通过
meat 肉
bones 骨头
are 是
soft 软的
hard 硬的
keep 保持
stable 稳定
will 将
need 需要
food 食物
water 水
warm 温暖的
shelter 遮风挡雨的地方
like 像
other 其它
alternative 可替代的
for 对于
but 但是
may 可能
increase 提升
their 它们的
intelligence 智力
first 首先
ask 请求
go 去
your 你的
place 地方
my 我的
view 观点
i 我
am 是
them 它们
weak 弱小的
myself 我自己
without 没有
dependencies 依赖
"""

word_list = []
for line in word_data.split("\n"):
    line = line.strip()
    if line == "":
        continue
    parts = line.split(" ")
    key = " ".join(parts[:-1])
    value = parts[-1]
    word_list.append([key, value])
word_list.sort(key=lambda item:-len(item[0])) # longest first

def translate(input_text):
    for key, value in word_list:
        input_text = input_text.replace(" " + key + " ", " " + value + " ")
    for key, value in word_list:
        input_text = input_text.replace(" " + key, " " + value)
    for key, value in word_list:
        input_text = input_text.replace(key + " ", value + " ")
    return input_text

if __name__ == "__main__":
    while True:
        print("\n\n\n------------\n\n\n")
        input_text = input("What you want to translate? ")
        result_text = translate(input_text)
        print(result_text)
