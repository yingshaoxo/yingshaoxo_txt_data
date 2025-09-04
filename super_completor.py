import random
import time
from pprint import pprint


def get_source_text_data():
    with open("all_yingshaoxo_data_2023_11_13.txt", "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return text


class Yingshaoxo_Text_Completor():
    """
    This method is amazing, but not accurate compared to what human did. If you want human level completor, use 10 years to make a strong AI (child),  so he or she could do primary school stuff.
    """
    def __init__(self):
        pass

    def get_source_text_lines(self, source_text):
        source_text_lines = source_text.split("\n")
        return source_text_lines

    def get_next_text_by_first_data_first(self, source_text_lines_list, input_text, how_many_lines_you_want=300):
        # Could make a micro_controller version by handle line pointer in file reader. So it would work for small memory devices
        length = len(source_text_lines_list)

        for right_side_index in range(len(input_text)):
            right_side_sub_string = input_text[right_side_index:]

            index = 0
            while index < length:
                line1 = source_text_lines_list[index]
                line2 = source_text_lines_list[index+1]
                current_text = line1 + "\n" + line2

                if (right_side_sub_string != "") and (right_side_sub_string in current_text):
                    target_text = right_side_sub_string.join(current_text.split(right_side_sub_string)[1:])
                    target_text += "\n".join(source_text_lines_list[index+2:index+2+how_many_lines_you_want])
                    return target_text

                index += 1
                if (index + 1) >= length:
                    break
        return ""

    def get_next_text_by_using_a_simple_list(self, source_text_lines_list, input_text, how_many_character_you_want=2000, level=64):
        """
        This method will not return content after new line. Except you pass text pieces that has new line inside.
        """
        length = len(source_text_lines_list)
        end_string = "[|end|]"

        def down_side_complete(the_input_text):
            for right_side_index in range(0, level):
                right_side_sub_string = the_input_text[right_side_index:]

                #index = 0
                index = random.randint(0, length)
                while index < length:
                    current_text = source_text_lines_list[index]

                    if (right_side_sub_string != "") and (right_side_sub_string in current_text):
                        target_text = right_side_sub_string.join(current_text.split(right_side_sub_string)[1:])
                        if len(target_text) >= 1:
                            return target_text[:int(level/2)]
                            #return target_text + "\n"
                            #return target_text[0]
                        else:
                            return "\n"

                    index += 1
            return " " + end_string

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = down_side_complete(input_text)
            if len(temp_response) == 0:
                break
            response += temp_response
            input_text += temp_response
            if temp_response.endswith(end_string):
                response = response[:-len(end_string)]
                break

        return response

    def _is_punctuation(self, string, more_punctuation="跟讲在有要地的着和便等就让了说想被到是只给几买干从个为以然问没回对先者出也之能上下么儿很会"):
        return string in (",.!?;:，。；：!？ \n-=_+()*&^%$#@!`~{}|[]'/<>" + more_punctuation)

    def _is_ascii(self, string):
        return string.strip(''' \n1234567890-=_+()*&^%$#@!`~qwertyuiop{}|[]\asdfghjk;':"zxcvbnm,./<>?QWERTYUIOPASDFGHJKLZXCVBNM''') == ""

    def _is_alphabet(self, string):
        return string.strip('''abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM''') == ""

    def _leave_first_sub_string(self, string):
        # abandand: english until not_alphabet, chinese next character
        # it should complete until [,.!?;:，。；：!？space \n]
        if len(string) > 1:
            first_char = string[0]
            if self._is_punctuation(first_char):
                return first_char
            else:
                temp_string = first_char
                for char in string[1:]:
                    if self._is_punctuation(char):
                        return temp_string + char
                    else:
                        temp_string += char
                return temp_string
        return string

    def get_next_text_by_pure_text(self, source_text, input_text, how_many_character_you_want=2000, level=64, complete_how_many_character_for_each_time=None):
        """
        This method is the best so far, if you have big memory.
        It will only return what it got in database. We respect original author content.
        """
        if complete_how_many_character_for_each_time == None:
            complete_how_many_character_for_each_time = level

        end_string = "[*|end|*]"

        def down_side_complete(the_input_text):
            for right_side_index in range(0, level):
                right_side_sub_string = the_input_text[right_side_index:]

                if len(right_side_sub_string) == 0:
                    return " " + end_string

                the_splits = source_text.split(right_side_sub_string)
                the_length_of_splits = len(the_splits)
                if the_length_of_splits >= 2:
                    index = random.randint(1, the_length_of_splits-1)
                    target_text = the_splits[index][:complete_how_many_character_for_each_time]
                    return target_text
                else:
                    pass
            return " " + end_string

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = down_side_complete(input_text)
            if len(temp_response) == 0:
                break
            response += temp_response
            input_text += temp_response
            if temp_response.endswith(end_string):
                response = response[:-len(end_string)]
                break

        return response

    def get_next_most_frequent_text_by_pure_text(self, source_text, input_text, how_many_character_you_want=2000, level=64, complete_how_many_character_for_each_time=None, debug_stream_print=False, get_only_one_word=False):
        """
        This will only return the one from two most frequent result.
        """
        if complete_how_many_character_for_each_time == None:
            complete_how_many_character_for_each_time = level

        end_string = "[*|end|*]"

        def down_side_complete(the_input_text):
            for right_side_index in range(0, level):
                right_side_sub_string = the_input_text[right_side_index:]

                if len(right_side_sub_string) == 0:
                    return " " + end_string

                the_splits = source_text.split(right_side_sub_string)
                the_length_of_splits = len(the_splits)
                if the_length_of_splits >= 3:
                    next_word_dict = {}
                    for index in range(1, the_length_of_splits-1):
                        next_string = the_splits[index][:complete_how_many_character_for_each_time]
                        next_word = self._leave_first_sub_string(next_string)
                        if next_word not in next_word_dict.keys():
                            next_word_dict[next_word] = 1
                        else:
                            next_word_dict[next_word] += 1
                    next_word_items = list(next_word_dict.items())
                    next_word_items.sort(key=lambda item: -item[1])
                    if len(next_word_items) > 0:
                        return random.choice(next_word_items[:2])[0]
                    else:
                        return self._leave_first_sub_string(the_splits[1])
                else:
                    pass
            return " " + end_string

        if debug_stream_print == True:
            print(input_text, end="", flush=True)

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = down_side_complete(input_text)
            if get_only_one_word == True:
                return temp_response
            if debug_stream_print == True:
                print(temp_response, end="", flush=True)
                time.sleep(0.1)
            if len(temp_response) == 0:
                break
            response += temp_response
            input_text += temp_response
            if temp_response.endswith(end_string):
                response = response[:-len(end_string)]
                break

        if debug_stream_print == True:
            print("\n\n", end="", flush=True)

        return response

    def get_source_text_dict(self, source_text, level=7):
        # level is a number, the bigger, the accurate but slow
        source_dict = {}

        for temp_level in range(1, level + 1):
            index = 0
            length = len(source_text)
            while index+temp_level < length:
                key_string = source_text[index:index+temp_level]
                value_string = source_text[index+temp_level]

                if key_string in source_dict:
                    pass
                else:
                    source_dict[key_string] = set()
                source_dict[key_string].add(value_string)

                index += 1

        for key, value in source_dict.items():
            source_dict[key] = list(value)

        return source_dict

    def get_next_text_by_using_dict(self, source_text_dict, input_text, level=7, how_many_character_you_want=100):
        # level is a number, the bigger, the accurate but slow
        """
        # created by yingshaoxo
        Algorithem:

        [
            I love you,
            I like you,
            I hate you,
        ]

        data:
            next_word:
                [I] -> love
                [I] -> like
                [I] -> hate

                [I,love] -> you
                [I,like] -> you
                [I,hate] -> you

                [I,love,you] -> .
                [I,like,you] -> .
                [I,hate,you] -> .

        > As you can see, the original data is small, but after this 'to dict process', it got bigger. why we want to do this? because we want to get as much as data as possible from original data, so the text generation will go on and on infinately.... It is just like what human do when they are in thinking, the new data always pollute the base data to generate new ideas. we keep thinking or talking in our mind.

        > It seems like you just need a best data, that data is in our mind. If you could save the thinking text in your brain, you can use that data as source, to let new machine to keep generate new text based on the old thinking text, which will make a copy of you. (Think like you)

        > If you can't read mind, you can talk to yourself without end, write it down as pure text, doing this for 1 week, everyday 8 hours, then you can collect enough data.

        > The good part about this tech is: it will do brain copy in the exact way, 1 to 1, no other dirty data. The bad part is, it can not do self upgrade unless it has permission to change its old data, I mean, it should have "thinking to action" bindings, so that it can modify the old text it generated. All in all, if you have less data you can't make a self_upgraded_able thinking machine.

        > Above is just minimum example of 'self inner brain thinking text data'.

        > But if you just want to create digital person, this method will only copy yourself. You have to be a teacher, and teach your students. So that they could have sex gender. Just simplifying yourself to child level, then teach them from basics.
        """
        # todo: maybe I should do some improvement to let it save those most frequent two values for each key sub_string.
        def the_real_function(the_input_text, the_level):
            while the_level >= 1:
                right_side_sub_string = the_input_text[-the_level:]

                the_target_list = source_text_dict.get(right_side_sub_string)
                if the_target_list != None:
                    # should use random module, but for no dependencie reason, we use mod operator
                    #the_target_index = len(the_input_text) % len(the_target_list)
                    the_target_index = random.randint(0, len(the_target_list)-1)
                    the_target = the_target_list[the_target_index]
                    #print(right_side_sub_string, the_target, the_target_list)
                    return the_target

                the_level -= 1
            return " "

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = the_real_function(input_text, level)
            if len(temp_response) == 0:
                break
            response += temp_response
            input_text += temp_response

        return response

    def update_source_text_dict_for_sqlite(self, source_text, sqlite_path, level=7):
        pass

    def get_next_text_by_using_sqlite_dict(self, sqlite_path, input_text, level=7, how_many_character_you_want=100):
        pass

    def _split_string_into_word_list(self, string):
        words = string.replace("\n", " ").split(" ")
        new_words = []
        for word in words:
            if self._is_alphabet(word):
                # english
                new_words.append(word)
            else:
                # chinese
                new_words += list(word)
        return new_words

    def _get_background_string_similarity(self, string_1, string_2):
        # return similarity, from `0.0` to `1.0`, 1 means equal, 0 means no relate.
        # Actually, this function should shoose the better one, it has to know if which string is better.
        char_set_1 = set(self._split_string_into_word_list(string_1))
        char_set_2 = set(self._split_string_into_word_list(string_2))
        common_char_set = char_set_1 & char_set_2
        all_char_set = char_set_1 | char_set_2
        later_part = len(all_char_set)
        if later_part != 0:
            similarity = len(common_char_set) / later_part
        else:
            similarity = 0
        return similarity

    def get_next_text_creatively_by_pure_text(self, source_text, input_text, how_many_character_you_want=2000, level=64, use_background_context_window=False, complete_how_many_character_for_each_time=None, debug_stream_print=False, get_only_one_word=False):
        """
        A slow method. But more creative, it return something that is not in the database.

        This method will force to choice from two result for each next_word_completion, by default, it will choose randomly.
        It may do the choise based on content background.
        Creativety is not easy to get. It has to have a lot of text data, larger than 100MB.

        The background context match method is:
            1. __________---next_text
            2. "__________" represent the background text, if 1000 words has 500 words match sequently, then the background matchs. Or you could use other fuzz match method.
            3. "---" mens the end small part of input_text, it must full match by using "==". So the complete words will be a continus thing.
            4. The length of the background is normally a paramater called "context_window_length".

        This method can be quick if you use web_search_engine pure_text result, it will jump 10 top website to re_mix a fine text that well answered your question.
        """
        # maybe background context is not important, you can simply let the chat history in top of database.
        end_string = "[*|end|*]"
        if use_background_context_window == True:
            if len(input_text) > level:
                background_text = input_text[:-level]
                background_context_window_length = len(background_text)
            else:
                use_background_context_window = False

        def down_side_complete(the_input_text):
            for right_side_index in range(0, level):
                right_side_sub_string = the_input_text[right_side_index:]

                if len(right_side_sub_string) == 0:
                    return " " + end_string

                the_splits = source_text.split(right_side_sub_string)
                the_length_of_splits = len(the_splits)
                if the_length_of_splits >= 3:
                    if use_background_context_window == False:
                        index = random.randint(1, the_length_of_splits-1)
                        if complete_how_many_character_for_each_time != None:
                            target_text = the_splits[index][:complete_how_many_character_for_each_time]
                        else:
                            target_text = the_splits[index][:level]
                            target_text = self._leave_first_sub_string(target_text)
                        return target_text
                    else:
                        a_check_list = []
                        for background_index in range(0, the_length_of_splits-1): #[from_a, to_b_minus_1)
                            temp_background_string = the_splits[background_index][-background_context_window_length:]
                            similarity = self._get_background_string_similarity(temp_background_string, background_text)
                            a_check_list.append([similarity, background_index+1])
                        a_check_list.sort(key=lambda item: -item[0])
                        if complete_how_many_character_for_each_time != None:
                            target_text = the_splits[a_check_list[0][1]][:complete_how_many_character_for_each_time]
                        else:
                            target_text = the_splits[a_check_list[0][1]][:level]
                            target_text = self._leave_first_sub_string(target_text)
                        return target_text
                else:
                    pass
            return " " + end_string

        if debug_stream_print == True:
            print(input_text, end="", flush=True)

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = down_side_complete(input_text)
            if get_only_one_word == True:
                return temp_response
            if debug_stream_print == True:
                print(temp_response, end="", flush=True)
                time.sleep(0.1)
            if len(temp_response) == 0:
                break
            response += temp_response
            input_text += temp_response
            if temp_response.endswith(end_string):
                response = response[:-len(end_string)]
                break

        if debug_stream_print == True:
            print("\n\n", end="", flush=True)

        return response

    def get_all_files_txt_under_a_folder(self, directory_name, type_limiter=[".py", ".txt", ".md"]):
        from auto_everything.disk import Disk
        disk = Disk()
        files = disk.get_files(directory_name, True, type_limiter=type_limiter)
        source_text = ""
        for file_path in files:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                source_text += text + "\n\n\n\n"
        return source_text

    def load_super_big_txt_string(self, source_text):
        # Actually what we want to do here is simply split 1TB file into 10000 x 100MB files.
        # First use 'get_next_text_by_pure_text()' to get 10000 x 1KB string
        # Then use 'get_next_text_creatively_by_pure_text()' to get final result from 10MB string. 
        the_100MB_length = 3495253#3
        the_full_length = len(source_text)

        self.source_text_list = []
        part_number = int(the_full_length/the_100MB_length)
        #print(part_number)
        for part_index in range(0, part_number+1):
            start_index = part_index * the_100MB_length
            if start_index >= the_full_length:
                break
            end_index = start_index + the_100MB_length
            sub_source_text = source_text[start_index: end_index]
            self.source_text_list.append(sub_source_text)

    def get_next_text_from_big_txt_string(self, the_input_text, level=64, how_many_character_you_want=64, debug_stream_print=False, creatively=False):
        end_string = "[*|end|*]"

        new_source_text = ""
        for source_text in self.source_text_list:
            temp_result = self.get_next_text_by_pure_text(source_text, the_input_text, how_many_character_you_want=how_many_character_you_want*30, level=level, complete_how_many_character_for_each_time=how_many_character_you_want*30)
            temp_result = the_input_text + temp_result
            new_source_text += temp_result + "\n\n\n\n" + end_string
            #print("************")
            #print(temp_result)
            #print("************")

        if creatively == False:
            response = self.get_next_most_frequent_text_by_pure_text(new_source_text, the_input_text, how_many_character_you_want=how_many_character_you_want, level=level, complete_how_many_character_for_each_time=None, debug_stream_print=debug_stream_print)
        else:
            response = self.get_next_text_creatively_by_pure_text(new_source_text, the_input_text, how_many_character_you_want=how_many_character_you_want, level=level, use_background_context_window=False, complete_how_many_character_for_each_time=None, debug_stream_print=debug_stream_print)

        response = response.split(end_string)[0]
        return response

    def get_deep_abstract_language_thinking_tree_dict_and_converted_text_and_complete_function(self, source_text, level=5, min_repeated_times=2):
        """
        yingshaoxo 的奇思妙想之暴力文本抽象大法:


        主要还是讲一个暴力规律提取大法：

        从sub_string level 1 到 16

        只保留重复次数达2次及以上的key，且value为word


        这个是一层套一层，类似converlutional layer

        第一次提取两个字的词，把纯文本转为id

        第二次寻找4个字的抽象重复词， 但实际表现为两个前后连续的id

        第三次寻找8个字的抽象重复词， 但实际表现为仍为下层两个前后连续的id

        最终结果是一串很短的序列，是在查数据库，类似于hidden layer tensor

        你通过查数据库得到短序列，解析高层短序列输出结果时，你要倒过来一层一层解码到原纯文本

        据说这也是抽象的一种方法。你不搞数字id，直接弄字符串缩句词典也是可以的。


        抽象到什么方面呢？我指的什么呢？是这样的，最顶层看起来就是一个id，但实际上有两个更底层value_id都可以代替它，所以到下一层变成了2个id, 二选一。到再下面一层，每个id又有两个更下层的id，于是可能性变成了4个，如果有32层，那么就有几亿中可能性，很接近人对语言的抽象能力了。举个例子，最顶层就是”写个故事“，经过32层抽象补全，变成了一篇几百万字的故事书。

        让我们给这个理论方案取个名字，应该叫做 abstract_language_thinking_tree_dict_based_text_completion


        这让我不禁意间想到7z，没准它也是把数据对折7次，实现了压缩。比如2bit变成1.1bit。original_data*repeated_time。但7z和我们的算法还是有点儿区别的。我们这个是有损压缩，顶层"今天心情好"有无数种底层表达。而7z是无损压缩。


        我们来定义一下这个function应该返回怎样的dict:
            {
                1: {
                    "你好": "您好",
                    "hello": "您好",
                    "检查数据库": "查数据库",
                    "check database": "查数据库",
                    "在家里": "在家",
                    "In house": "在家",
                    "玩游戏": "玩",
                },
                2: {
                    "您好，查数据库": "警察查房",
                    "在家玩": "闲",
                },
                3: {
                    "闲，警察查房": "抄家"
                }
            }

            这个dict神奇的地方在于，把如下一段话变成了很短的话:
                original_text = "在家里玩游戏，‘你好, 检查数据库。'"
                level_1 = "在家玩，'警察查房'"
                level_2 = "抄家"

            从最终的抽象文本，又可以衍生出无穷的实际句子:
                original_text = "抄家"
                level_1 = "在家玩，'警察查房'"
                level_2 = "在家玩，'您好，查数据库'"
                level_3 = "In house 玩游戏，'hello，check database!'"

            dict里的level1总是有非常多的表述方法，但在最顶层的抽象思考逻辑，就一个东西: 被抄家了！因为自己的数据与算法做得太好了！

            其实抄家与强拆是一个东西，都是弱势个体留不住有价值的东西的一种外在表现。

            当然这个只是初级抽象，人比较牛逼，搞的是代码抽象，比如 抄家(actor=警察)、抄家(actor=皇帝)、抄家(actor=old_strong_AI)


        所以这个function一共要返回3个东西。一个是dict, 一个是经过dict抽象后的文本，另一个则是a_function(source_dict, input_text)->raw_text


        # abstract_tree, final_text, completion_func = abstractor.get_deep_abstract_language_thinking_tree_dict_and_converted_text_and_complete_function(source_text)
        # completed_text = completion_func(abstract_tree, "这里应该是普通底层文本，应该是你的程序根据字典树将它转成高层形式，然后再反向生成，看能不能生成新的底层文本，类似于文本风格迁移")


        所以人脑的秘密就是: 一方面，信息进入会有个抽象化的过程，你看见其他生物，不是几十万像素，而是某动物的名字。另一方面，生物存储信息也是用的abstract_information_tree，目的是极限压缩与快速查询。最终人为了生存，搞了个“趋利弊害”的规则，动态的更新数据库。生物就是在这个loop里存活了几亿年。
        """
        # You need to help to complete this greate function that mimic human brain with just cpu. No other third party library, just pure python without pip.
        pass


if __name__ == "__main__":
    yingshaoxo_text_completor = Yingshaoxo_Text_Completor()

    #folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code_Mini"
    folder = "/home/yingshaoxo/CS/yingshaoxo_txt_data"
    #folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Ebooks/Chinese/chinese_sex_novels"
    source_text = yingshaoxo_text_completor.get_all_files_txt_under_a_folder(folder)
    #source_text = source_text.replace("\n", "").replace(" ", "").replace("　","")

    #yingshaoxo_text_completor.load_super_big_txt_string(source_text)

    abstraction_dict, converted_text, complete_function = yingshaoxo_text_completor.get_deep_abstract_language_thinking_tree_dict_and_converted_text_and_complete_function_1(source_text[:30000])
    pprint(abstraction_dict)
    print(converted_text[:500])
    while True:
        try:
            input_text = input("What you want to say: ")
            response = complete_function(abstraction_dict, input_text)
            if response:
                print("\n\nComputer: \n" + input_text + response)
                print("\n\n")
        except KeyboardInterrupt:
            print("\n")
            continue
    exit()

    while True:
        try:
            input_text = input("What you want to say: ")
            #response = yingshaoxo_text_completor.get_next_text_by_pure_text(source_text, input_text, how_many_character_you_want=300, level=64, complete_how_many_character_for_each_time=None)
            #response = yingshaoxo_text_completor.get_next_most_frequent_text_by_pure_text(source_text, input_text, how_many_character_you_want=300, level=64, complete_how_many_character_for_each_time=None, debug_stream_print=True)
            #response = yingshaoxo_text_completor.get_next_text_creatively_by_pure_text(source_text, input_text, how_many_character_you_want=300, level=64, use_background_context_window=False, complete_how_many_character_for_each_time=None, debug_stream_print=True)
            #response = yingshaoxo_text_completor.get_next_text_from_big_txt_string(input_text, how_many_character_you_want=256, level=64, debug_stream_print=True, creatively=True)
            #response = yingshaoxo_text_completor.get_next_text_by_using_dict(source_text_dict, input_text, how_many_character_you_want=300)
            if response:
                response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0]
                print("\n\nComputer: \n" + input_text + response)
                print("\n\n")
        except KeyboardInterrupt:
            print("\n")
            continue
