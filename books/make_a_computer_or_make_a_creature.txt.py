level_1 = """
# make_a_computer_or_make_a_creature

author: yingshaoxo
writing technique 1: ascii_keyboard + old_ubuntu + ext2 + terminator + vim + lowercase_english + simplified_chinese
writing technique 2: step by step, physical workable is more important than talking and understanding. experiment driving knowledge base. fully re_produceable if no one breaks the dependencies, for example, remove an material from the world, remove a language from the world.
_______

day 1:
created a book called "make_a_computer_or_make_a_creature", so that we will not lose memory after day 9999.
defined a new way to write experiment notes. video is expensive, text is cheap. if we can control the note language, start from basic words and concept and ideas, it can be easy for people to understand. but the main purpose is to keep memory safe. you can't share a valuable knowledge to those deeply controlled slaves in this world. those low level people can't control what kind of information they receive.

我听说电线是电脑的基础元件之一。电线是一根线，这根线是导电金属制作的。测量方法是用万用电表，切换到"测电阻模式"的最小档位，如果得到电阻值为0，那么就是可导电金属。
> but what if there has no "electronic meter", how to know if a line is electronic line? (a tip: when you connect positive and negtive 3V line for 0.1 second, there will have "electronic flowers")
_______

day 2:
put 2 green vegetable with root into soil. maybe it will grow.
我把植物带根放进室内泥土杯子，没有太阳，不知道会不会正常生长。已经过了2天，在冬天，植物好像没那么容易死亡。
_______

day 5:
green vegetable is still alive. and some warm start to show, I killed them all for now, because I want to study green plant first.
i heared plastic material will not allow electricity to flow inside of them, so plastic material can be a good material for making box case for electricity device, such as mobile phone, computer.
_______

day 6:
try to find some knowledge on internet about how to make a storage, but no answer, they are all users. no one knows how to make a disk by themselves. i basically think the computing part is secondary, the storage part is first. because without memory, people are low level animal.
"""

def 我靠_function_可以支持中文():
    print("牛逼牛逼" + ", 真自然语言编程！")

def 三极管实验():
    print("""
好像没有毛用。三极管这个滑动变阻器发烫严重，一点都不省电。只是拿来当个反向逻辑生成器，就烫得不得了，浪费电。还不如用NMOS。NMOS类似于arduino的range_map function，但可以操控现实世界的电压。
    """)

def _什么垃圾玩意儿():
    print("什么垃圾玩意儿, 好像没有毛用。")

def 麦克风咪头测试():
    _什么垃圾玩意儿()
    print("""
我买的这个麦克风咪头据说是电容的，可以在说话时改变电压。它有两个pin，我直接把一个接入了analog pin，另一个接入了地。发现在吹气时，会有明显上升值。但是说话无法识别。我也试过给它1.5V的电，但它也只在吹气时有反应。说明市面上根本没有合格的产品。别人的麦克风可以拿来录音，我买的麦克风只能拿来监测音高。
也许我线接反了，它的两个引脚中，接外壳的是负极(好像有3根线)，不接外壳的是正极。
    """)

def 蚯蚓实验():
    print("""
我在一个小杯子里装满土，养了一根半透明幼年蚯蚓。我没喂食什么东西，一个月后那蚯蚓还活着。
    """)

def 三极管音频放大实验():
    print("""
因为原始的单片机引脚的电压比较小，直接驱动喇叭感觉声音不大。所以搞了一个三极管。

连接方式：
    电阻：1kΩ (不加电阻会让单片机重启)
    三极管：1=Emitter(ground)，2=Collector(positive)，3=Base(signal)

    Pico Pin5 (音频信号，0~3V的wav数据map) -> 1kΩ 电阻 -> 三极管B基极
    Pico 3.3V -> 喇叭正极
    喇叭负极 -> 三极管C集电极
    三极管E发射极 -> Ground

感觉声音一下子就大了起来。

三极管只是个可调电阻，负载反着接也行。比如：
    Pico Pin5 -> 1kΩ 电阻 -> 三极管B基极
    Pico 3.3V -> 三极管E发射极
    三极管C集电极 -> 喇叭正极
    喇叭负极 -> Ground
    """)

def 电容能提升喇叭音质():
    print("""
我用的是CBB_474J_630V电容，据说有0.47uf。这种电容不区分正负极，我就是因为懒才买的它。我完全不知道电容的用法。但据说它能提升喇叭声音的音质。
直接接到放大三极管的'地'与‘信号输入’之间，感觉瞬间音质就变好了，杂音就减少了。副作用是，声音好像也小了一点。
    """)

def 电容麦克风声音放大到喇叭的实验():
    print("""
实际上碳粒麦克风要简单点，能直接串联5v电池，输出2到4v的电压，直接驱动喇叭，都不需要放大。但市面上没有，被人为删除了。

1.麦克风负极接地。2.麦克风正极串联一个10k电阻到3v。3.麦克风正极串联一个0.5uf到1uf左右的电容，电容的另一端接上“音频功率放大器(一般是用的lm386芯片), 功率放大器是用的3v”。

用手去感受喇叭的震动要比用耳朵听更灵敏。

这个方法，时好时怀，感觉lm386等芯片是不稳定的不确定性元器件，不好用，没准儿自带后门也说不定。
    """)

def 直接用三极管放大麦克风并输出到喇叭的实验():
    print("""
麦克风:
    1.麦克风负极接地。2.麦克风正极串联一个10k电阻到5v。3.麦克风正极串联一个1uf或者100uf的电容，电容的另一端为音频信号输入pin。
三极管放大器:
    1.喇叭负极接C。喇叭正极接5V。E接地。电容麦克风的信号接B。(相当于信号B在控制三极管这个可调电阻。)

这个实验会失败，因为最终的声音很小。
    """)
    print("现代麦克风太垃圾了。基本上要和匹配的电容、电阻、电压、三极管一起使用，才能正常工作。稍微生产商一做手脚，改改参数，你整个构架都得大调整。浪费钱、浪费时间与生命、浪费存储、浪费仓库！")

def _元器件描述(a_list):
    device_dict = {}
    for one in a_list:
        splits = one.split("_")
        device_name = splits[0]
        if device_name not in device_dict:
            device_dict.update({splits[0]: [{"pin_name": splits[1], "pin_number": splits[2]}]})
        else:
            device_dict[device_name].append({"pin_name": splits[1], "pin_number": splits[2]})
    print("\n基本元器件有:")
    for device_name, info in device_dict.items():
        print((" " * 4) + device_name)
        print((" " * 8) + str(info))
    print()

def _连接(point_a, point_b):
    print("用电线连接: '" + point_a + "' 和 '" + point_b + "'。")

def 用python来画电路板也是一样的():
    # 名字是名字(可带数字)，引脚是末尾数字，中间用下划线连接。
    print("让我们用python画个电路板，来点个灯。")

    device_list = ["小灯_正极_1", "小灯_负极_2", "电源3v_正极_1", "电源3v_负极_2"]
    #通过解析，能知道有2个设备: "小灯" 与 "电源3v"。还能知道对应设备的pin脚名字与编号，如"正极"与"1"。

    _元器件描述(device_list)
    _连接("电源3v_正极_1", "小灯_正极_1")
    _连接("小灯_负极_2", "电源3v_负极_2")
    # 这种方法搞出来的电路板设计图，存储起来是最简单的。程序与机械臂解析起来也简单。

def 动圈麦克风声音放大到喇叭的实验():
    print("""
动圈麦克风很高级，圆磁铁外直接用塑料薄膜悬浮套了一圈铜线圈，当你讲话，那薄膜会直接电磁感应生成电压。虽然小，但单片机可以直接采集到。比如pi pico micropython的模拟pin能采集到0到6万的数值，而动圈麦克风可以在2000到1万浮动。
我直接读取的动圈麦克风的正极，然后软件上放大10倍，接着输出信号到大功率三极管直接驱动喇叭。发现能用。当我用手把麦克风与嘴紧密连接起来时，我讲话，喇叭是会同步震动的，有质量比较低的人声输出。
我觉得这是可调的，有些几十年前的老式的动圈麦克风，灵敏度特别高，录音质量也应该比较高。另外，你自制的大动圈麦克风，和手掌差不多大，估计输出电压也不会小，单片机处理起来应该是毫无压力。(极柱体电容麦克风就应该被淘汰，搞得过于复杂。)
实在不行，徒手搞个碳粒麦克风，直接接上5v就能用，就不需要折腾别人的垃圾电子元件了。
    """)

def 电容的作用():
    print("""
电容的作用，网上都没人讲明白，并联时，它只有一个作用: 高压吸收、低压补偿，削弱峰值，平滑波形，减少信号的噪音。属于快冲快放的高速电池。
举几个例子:
    小信号小电压的麦克风降噪: 0.1uf或者1uf的电容适合并联到麦克风的输入引脚，可以减少一部分噪音。如果你用大电容，会把小信号给吃掉。
    喇叭降噪: 100uf的电容适合并联到喇叭的输出引脚，可以减少一部分噪音。如果你用小电容，反而会增加噪音。
    pwm稳压: 如果你直接用单片机生成一个0到3v的模拟电压，那是很抖的，它是高频开关，电压不稳定。所以你要在 pwm信号与地之间 并联一个100uf的电容，它可以让电压更稳定。也适用于nmos继电器。
> 市面上的电容碰到220v高电压直接就爆炸了。实际上可以做出，高于xx电压就舍弃多余电压，低于xx电压就多充会儿电再释放的电容。有这种超级电容，就不需要电源适配器了，直接在不稳定电压后接一个超级电容，就能得到稳定的电压了。可惜市面上没人做这个。
    """)

def 阳光的作用():
    print("我的叶片植物，如果不照射阳光，会逐渐枯萎。说明阳光里是有能量的。这也侧面证明了太阳能充电板的合理性。但我不知道叶子与太阳能充电板之间的具体原理是否相同。")







all_function_list = dir()
all_function_list = [one for one in all_function_list if (not one.startswith("_"))]

try:
    from auto_everything.string_ import String
    string = String()
    def search_text_in_list(search_text, a_list):
        keywords = string.get_keywords_list(search_text)
        for one in a_list:
            if search_text == one:
                return one
            if string.check_if_string_is_inside_string(one, keywords, wrong_limit_ratio=0.3):
                return one
        return ""
except Exception as e:
    print(e)
    def search_text_in_list(search_text, a_list):
        for one in a_list:
            if search_text == one:
                return one
        keyword_length = 5
        while keyword_length >= 2:
            sub_string_list = []
            a_index = 0
            while a_index < len(search_text):
                temp_string = search_text[a_index:a_index + keyword_length]
                if len(temp_string) == keyword_length:
                    sub_string_list.append(temp_string)
                a_index += 1
            for one in a_list:
                for sub_string in sub_string_list:
                    if sub_string in one:
                        return one
            keyword_length -= 1
        return ""

while True:
    input_text = input("哎呀呀，你想知道啥？我帮你看看yingshaoxo的实验日志里有没有: ").strip()
    print("\n")
    function_name = search_text_in_list(input_text, all_function_list)
    if function_name != "":
        instance = globals()[function_name]
        if type(instance) == str:
            print(instance)
        else:
            result = instance()
            if result != None:
                print(result)
    print("\n")
