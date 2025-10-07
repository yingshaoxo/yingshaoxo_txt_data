import random
import time
import json


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

    def _is_connector(self, string):
        splits = "the of is and to in that we for an are by be as on with can if from which you it this then at have all not one has or that 的 了 和 是 就 都 而 及 与 着 或 一个 沒有 是否 我們 你們 妳們 他們 她們".split(" ")
        return string in splits

    def _is_punctuation(self, string, more_punctuation="跟讲在有要地的着和便等就让了说想被到是只给几买干从个为以然问没回对先者出也之能上下么儿很会还这"):
        return string in (",.!?;:，。；：!？ \n-=_+()*&^%$#@!`~{}|[]'/<>" + more_punctuation)

    def _get_keywords(self, string, more_punctuation=""):
        # not accurate for chinese, unless you split keyword by using space
        if " " in string:
            string += " "
            keyword_list = []
            temp_word = ""
            for char in string:
                if self._is_punctuation(char, more_punctuation=more_punctuation):
                    keyword_list.append(temp_word)
                    temp_word = ""
                else:
                    temp_word += char
            return keyword_list
        else:
            try:
                import jieba
                jieba.setLogLevel(20)
                #keywords = list(jieba.cut(input_text, cut_all=False))
                keywords = list(jieba.cut_for_search(input_text))
            except Exception as e:
                print(e)
                keywords = list(input_text)
            return keywords

    def _is_ascii(self, string):
        return string.strip(''' \n1234567890-=_+()*&^%$#@!`~qwertyuiop{}|[]\asdfghjk;':"zxcvbnm,./<>?QWERTYUIOPASDFGHJKLZXCVBNM''') == ""

    def _is_alphabet(self, string):
        return string.strip('''abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM''') == ""

    def _leave_first_sub_string(self, string):
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

    def search_long_background_context_by_using_keywords(self, source_text, input_text, keyword_list=None, source_text_splitor=None):
        # for each 20 lines, if it got all keywords in input_text, we return it
        # but we can scale down to 10 lines to search it again
        # but we can scale down to 5 lines to search it again
        # but we can scale down to 2 lines to search it again
        # but we can scale down to 1 lines to search it again
        """
        This method is going to be super useful in pure_text based robot memory search.
        And it can also be used to char level sub_string search

        It think by using jieba word list, you can get better result.
        Now you should know how they made the context window. You can easily create a 100k long context.

        You can also use this tech in sqlite to get smaller text for AI to read.
        """
        if keyword_list != None:
            keywords = keyword_list
        else:
            keywords = self._get_keywords(input_text, more_punctuation="")

        def handle_it(source_text):
            lines = source_text.split("\n")

            def get_related_text(start_index, end_index, range_length=100):
                if range_length == 0:
                    return "", start_index, end_index

                index = start_index
                while index < end_index:
                    temp_lines = lines[index:index+range_length]
                    temp_text = "\n".join(temp_lines)
                    ok = True
                    for key in keywords:
                        if key not in temp_text:
                            ok = False
                            break
                    if ok == True:
                        new_start_index = index
                        new_end_index = index + range_length

                        if range_length <= 12:
                            new_result, temp_new_start_index, temp_new_end_index = get_related_text(new_start_index, new_end_index, range_length=range_length-1)
                        else:
                            new_result, temp_new_start_index, temp_new_end_index = get_related_text(new_start_index, new_end_index, range_length=int(range_length/2))

                        if new_result != "":
                            return new_result, temp_new_start_index, temp_new_end_index
                        else:
                            return temp_text, new_start_index, new_end_index
                    index += 1

                return "", start_index, end_index

            result, start_index, end_index = get_related_text(0, len(lines))
            if result == "":
                return ""
            else:
                bias = 2
                start_index = start_index - 2
                end_index = end_index + 2
                if start_index < 0:
                    start_index = 0
                return "\n".join(lines[start_index: end_index])

        if source_text_splitor != None:
            source_text_list = source_text.split(source_text_splitor)
            for one in source_text_list:
                result = handle_it(one)
                if result != "":
                    return result
            return ""
        else:
            return handle_it(source_text)

    def get_next_text_by_pure_text(self, source_text, input_text, how_many_character_you_want=2000, level=64, complete_how_many_character_for_each_time=None, return_one_word=False, use_background=False, creatively=False):
        """
        This method is the best so far, if you have big memory.
        It will only return what it got in database. We respect original author content.

        I think those super_AI actually uses database data, then use abstract_language_tree to represent the old data in a new way, similar to language style change.
        """
        if creatively == True:
            print("Why don't you delete this piece of response data from your database? Then it will return a new result.")

        if complete_how_many_character_for_each_time == None:
            complete_how_many_character_for_each_time = level

        if use_background == True:
            source_text = self.search_long_background_context_by_using_keywords(source_text, input_text)

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
            if return_one_word == True:
                return self._leave_first_sub_string(temp_response)
            if len(temp_response) == 0:
                break
            response += temp_response
            input_text += temp_response
            if temp_response.endswith(end_string):
                response = response[:-len(end_string)]
                break

        if use_background == False:
            return response[:how_many_character_you_want]
        else:
            return response[:how_many_character_you_want] + "\n\nFrefrence:\n" + source_text.strip()[:512]

    def get_next_text_creatively(self, source_text, input_text, how_many_character_you_want=200, level=64):
        fake_source_text = str(source_text)

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = self.get_next_text_by_pure_text(fake_source_text, input_text, how_many_character_you_want=int(level/2), level=64, complete_how_many_character_for_each_time=level, use_background=False, creatively=False)
            old_temp_response = temp_response
            temp_response = self._leave_first_sub_string(temp_response)
            print(temp_response, end="", flush=True)
            time.sleep(0.2)
            if len(temp_response) == 0:
                break
            if temp_response.strip() == "":
                break
            old_pattern = old_temp_response[len(temp_response)-1:]
            fake_source_text = fake_source_text.replace(old_pattern, "")
            # need to change a lot of code to use find_string to replace only that place next text
            response += temp_response
            input_text += temp_response

        return response

    def search_long_background_context_by_using_multiprocess(self, source_text, input_text, keyword_list=None, source_text_splitor=None, return_text=True):
        # super quick
        import multiprocessing

        if keyword_list == None:
            keyword_list = self._get_keywords(input_text, more_punctuation="")

        the_100MB_length = 3495253#3
        the_full_length = len(source_text)

        self.source_text_list = []
        part_number = int(the_full_length / the_100MB_length)

        pool = multiprocessing.Pool()
        results = []

        for part_index in range(0, part_number + 1):
            start_index = part_index * the_100MB_length
            if start_index >= the_full_length:
                break
            end_index = start_index + the_100MB_length
            sub_source_text = source_text[start_index: end_index]

            result = pool.apply_async(
                self.get_next_text_by_pure_text,
                args=(sub_source_text, input_text, 512, 64, 512, False, False, False)
            )
            results.append(result)

            #result = pool.apply_async(
            #    self.get_next_text_by_pure_text,
            #    args=(sub_source_text, input_text[:-1], 512, 64, 512, False, False, False)
            #)
            #results.append(result)

        pool.close()
        pool.join()

        final_results = []
        for result in results:
            sub_result = result.get()
            if sub_result != "":
                final_results.append(input_text + sub_result)

        if return_text == False:
            return final_results
        else:
            return "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n".join(final_results)

    def get_magic_language_tree_dict_from_text(self, source_text, char_level=True, window_length=8):
        """
        This will be used for context background information extraction.

        2MB text: window_length == 11
        20KB text: window_length == 32
        """
        """
        tree的目的: 加速和减少干扰概率

        你找重复数据时，可以建几个临时池子，只取频率最高的前50%， 20%， 10%， 5%， 1%。
        """
        from auto_everything.ml import Yingshaoxo_Text_Preprocessor
        yingshaoxo_text_preprocessor = Yingshaoxo_Text_Preprocessor()

        stop_key_list = ['_c_']
        def delete_low_frequency_words(the_dict, gate):
            return # delete will cause the bot can't create new stuff

            all_child_keys = list(the_dict.keys())
            all_child_keys = [one for one in all_child_keys if one not in stop_key_list]
            if len(all_child_keys) == 0:
                    return
            all_child_frequency = [the_dict[key]["_c_"] for key in all_child_keys]
            all_child_items = [[key, all_child_frequency[index]] for index, key in enumerate(all_child_keys)]
            for key, frequency in all_child_items:
                if frequency < gate:
                    del the_dict[key]
                else:
                    delete_low_frequency_words(the_dict[key], gate)

        def add_sub_string_to_dict(the_dict, the_list):
            if len(the_list) == 0:
                return

            element = the_list[0]
            if element not in the_dict:
                the_dict[element] = dict({"_c_": 1})
            else:
                the_dict[element]["_c_"] += 1
            add_sub_string_to_dict(the_dict[element], the_list[1:])

        if char_level == False:
            lines = yingshaoxo_text_preprocessor.split_string_into_list_by_punctuations(source_text)
            lines = [one["text"] for one in lines]
        else:
            #splitor = " "
            lines = list(source_text)

        sub_string_dict = {}
        counting = 0
        for line_index in range(0, len(lines)-window_length):
            temp_segment_list = lines[line_index: line_index + window_length]
            add_sub_string_to_dict(sub_string_dict, temp_segment_list)

            counting += 1
            if counting >= 1000000:
                print("reduce dict size by deleting low frequency words...")
                #current_memory_in_mb = get_current_process_memory()
                #print("current_memory:", current_memory_in_mb, " MB")
                #if current_memory_in_mb >= 2000:
                delete_low_frequency_words(sub_string_dict, 2)
                counting = 0

        delete_low_frequency_words(sub_string_dict, 2)

        return sub_string_dict

    def use_magic_language_tree_dict_to_generate_next_string(self, magic_language_tree_dict, input_text, window_length=8, frequency_gate=1.0, how_many_character_you_want=128, char_level=True):
        """
        You can use word_cloud with background context search to get 100 similar result from database. Then let this function to generate something useful.

        This function similar to gpt2 AI model.
        """
        from auto_everything.ml import Yingshaoxo_Text_Preprocessor
        yingshaoxo_text_preprocessor = Yingshaoxo_Text_Preprocessor()

        def get_segments(input_text):
            if char_level == False:
                segments = yingshaoxo_text_preprocessor.split_string_into_list_by_punctuations(input_text)
                segments = [one["text"] for one in segments]
            else:
                #splitor = " "
                segments = list(input_text)
            return segments

        stop_key_list = ['_c_']

        def trace_words_to_get_sub_dict(the_dict, word_list):
            if len(word_list) == 0:
                return the_dict
            else:
                element = word_list[0]
                if element in the_dict:
                    return trace_words_to_get_sub_dict(the_dict[element], word_list[1:])
                else:
                    return None

        def get_next_words(the_dict):
            result_string = ""

            all_child_keys = list(the_dict.keys())
            all_child_keys = [one for one in all_child_keys if one not in stop_key_list]
            all_child_frequency = [the_dict[key]["_c_"] for key in all_child_keys]
            all_child_items = [[key, all_child_frequency[index]] for index, key in enumerate(all_child_keys)]
            all_child_items.sort(key=lambda item: -item[1])
            all_child_items = all_child_items[:max(int(frequency_gate*len(all_child_items)), 1)]
            target_list = all_child_items
            if len(target_list) == 0:
                return result_string
            else:
                one = random.choice(target_list)
                one = one[0]
                return result_string + one + get_next_words(the_dict[one])

            return result_text

        def error_fix_search(input_text):
            return random.choice(list(input_text))

        #print(input_text, end="", flush=True)
        response = ""
        while len(response) < how_many_character_you_want:
            segments = get_segments(input_text)[-int(window_length/2):] # get right half as input

            temp_a_dict = trace_words_to_get_sub_dict(magic_language_tree_dict, segments)
            while temp_a_dict == None:
                segments = segments[1:] # try less words right half if it is not in tree
                if len(segments) == 0:
                    temp_a_dict = None
                    break
                temp_a_dict = trace_words_to_get_sub_dict(magic_language_tree_dict, segments)
            if temp_a_dict == None:
                break
            else:
                temp_response = get_next_words(temp_a_dict)
                if temp_response == None:
                    break
                if temp_response == "":
                    break

            #print(temp_response, end="", flush=True)
            time.sleep(0.1)
            response += temp_response
            input_text += temp_response

        #print("\n\n", end="", flush=True)

        return response

    def one_shoot_next_text_generation_by_using_magic_tree_from_context_string(self, context_text, input_text, frequency_gate=1.0, window_length=8):
        """
        Why don't you use sqlite to search input_text[-32:] result, to get a list of similar text. Then pass that string as context_text to this function.
        """
        context_text = context_text[-30000:]
        the_dict = self.get_magic_language_tree_dict_from_text(context_text, char_level=True, window_length=window_length)
        response = self.use_magic_language_tree_dict_to_generate_next_string(the_dict, input_text, char_level=True, frequency_gate=frequency_gate, window_length=window_length)
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

    def directly_search_next_string_in_disk_file(self, file_path, input_text):
        # just think the disk file as 1kb_text_bytes + the_input_text + 2kb_text_bytes, you search contextbackground string within 3KB, and other generation method to generate the_input_text.
        pass

    def get_repeated_sub_string_dict_from_text_stream_from_zero(self, source_text, level=32, minimum_frequency=3):
        """
        Another method: generally update sub_string dict, start from the first character, find if it exists in later string, if so, add it to our dict. and looking for that character+next_character sub_string, if that sub_string in the following text, also add it to sub_string dict. For each line, we will cut the first n string that appears in out sub_string dict.
        Genrally speaking, it will add all sub_string that appears 2 times. and it will try to find new longer sub_string based on old sub_string. The heading line character will always be added into our dict if its not exists before.
        This method will require people to define a splitor. (Here it is new line. A not accurate one is 100 long chrarcter context window. in natural world, the splitor is the pause time or stop time)
        看起来，这个我在做的function在实现一个伟大的任务: 从连续的事件中找规律，先从小规律找起，逐渐找到大规律。有了规律，以后查数据库就可以预测未来。

        分词的目的: 得到一堆短序列。然后重复的也有很多，你需要手动搞一个"同义词典"，把可替换的相似的词或者短语，替换为最简单的那个。这样当你得到原始时代的最直白的表述，通常是"你饿吗？"、“你渴吗？”、"你想睡觉吗?"，你就可以通过简单的if-else进行处理。
        """
        global add_new_counting

        sub_string_dict = {}
        add_new_counting = 0
        def add_sub_string_to_dict(sub_string):
            global add_new_counting
            length_string = str(len(sub_string))
            if length_string not in sub_string_dict:
                sub_string_dict[length_string] = dict({sub_string: 1})
            else:
                if sub_string not in sub_string_dict[length_string]:
                    sub_string_dict[length_string][sub_string] = 1
                    add_new_counting += 1
                else:
                    sub_string_dict[length_string][sub_string] += 1
        def delete_some_low_frequency_data(the_frequency_gate=None):
            if the_frequency_gate != None:
                for length_key in list(sub_string_dict.keys()):
                    each_dict = sub_string_dict[length_key]
                    sub_string_key_list = list(each_dict.keys())
                    for sub_string_key in sub_string_key_list:
                        old_frequency = each_dict[sub_string_key]
                        if old_frequency < the_frequency_gate:
                            del each_dict[sub_string_key]
            else:
                # cut half lower frequency sub_string
                for length_key in list(sub_string_dict.keys()):
                    each_dict = sub_string_dict[length_key]
                    key_and_frequency_items = list(each_dict.items())
                    if len(key_and_frequency_items) > 20000:
                        key_and_frequency_items.sort(key=lambda items: -items[1])
                        for key, value in key_and_frequency_items[int(len(key_and_frequency_items)/2):]:
                            del each_dict[key]

        length = len(source_text)
        for current_level in range(2, level):
            index = 0
            temp_line = ""
            while index < length:
                sub_string = source_text[index: index+current_level]
                if len(sub_string) == 0:
                    index += 1
                    continue
                add_sub_string_to_dict(sub_string)
                index += int(len(sub_string)/2)
                if add_new_counting > 10000000:
                    delete_some_low_frequency_data()
                    add_new_counting = 0
                    print("refactor the dict... cut frequency lower than ...")
                index += 1

        delete_some_low_frequency_data(minimum_frequency)

        return sub_string_dict

    def use_repeated_sub_string_dict_to_generate_next_string(self, sub_string_dict, input_text, level=32, how_many_character_you_want=200, creatively=False):
        possible_length = 1
        if creatively == True:
            possible_length = 3

        sub_string_length_keys = [int(one) for one in list(sub_string_dict.keys())]
        sub_string_length_keys.sort(reverse=True)

        def search_string_in_dict(input_text):
            possible_result = []
            for number_length_key in sub_string_length_keys:
                string_length_key = str(number_length_key)
                for key, _ in sub_string_dict[string_length_key].items():
                    if input_text in key:
                        splits = key.split(input_text)
                        if len(splits) >= 2:
                            result = input_text.join(splits[1:])
                            if len(result) != 0:
                                possible_result.append(result)
                                #return result
                    if len(possible_result) >= possible_length:
                        break
                if len(possible_result) >= possible_length:
                    break
            if len(possible_result) >=possible_length:
                return random.choice(possible_result)
            return None

        def get_next_words(input_text):
            for level_index in reversed(list(range(1, min(len(input_text)+1, level)))):
                search_string = input_text[-level_index:]
                result = search_string_in_dict(search_string)
                if result == None:
                    continue
                else:
                    return result
            return None

        print(input_text, end="", flush=True)
        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = get_next_words(input_text)
            if temp_response == None:
                break
            print(temp_response, end="", flush=True)
            time.sleep(0.1)
            response += temp_response
            input_text += temp_response
        print("\n\n", end="", flush=True)

        return response

    def get_high_frequency_sub_string_dict_from_text(self, source_text, level=8, frequency_gate=3):
        """
        We want to have a simple structure. { "7": {7_len_key: [counting, next_7_len_value]} }

        看起来像是我们保存了一个高频词典，方便快速查询。如果有right_sub_string查不到，我们就查原纯文本得到之后的文本。。。

        有句话叫做一级查询，查dict，二期查询，查sentence by loop and find_string

        This function similar to gpt1 AI model. (The original text data is 21 times smaller)

        Suggest test with 2MB diary text. This is a argument change game, different size text need different arguments.
        """
        sub_string_dict = {}

        def delete_low_frequency_words(the_dict, gate):
            for key, value_list in list(the_dict.items()):
                if value_list[0] < gate:
                    del the_dict[key]

        def add_sub_string_to_dict(the_dict, sub_string, next_string):
            if sub_string not in the_dict:
                the_dict[sub_string] = [1, next_string]
            else:
                the_dict[sub_string][0] += 1

        counting = 0
        for level_number in range(1, level+1):
            for char_index in range(0, len(source_text)-level_number):
                sub_string = source_text[char_index: char_index+level_number]
                next_string = source_text[char_index+level_number: char_index+level_number+level_number]

                if len(sub_string) != level_number:
                    continue
                if len(next_string) != level_number:
                    continue

                string_level_index = str(len(sub_string))
                if string_level_index not in sub_string_dict:
                    sub_string_dict[string_level_index] = {}
                add_sub_string_to_dict(sub_string_dict[string_level_index], sub_string, next_string)

                counting += 1
                if counting >= 10000000:
                    print("reduce dict size by deleting low frequency words...")
                    for sub_dict in sub_string_dict.values():
                        delete_low_frequency_words(sub_dict, frequency_gate)
                    counting = 0

        for sub_dict in sub_string_dict.values():
            delete_low_frequency_words(sub_dict, frequency_gate)

        return sub_string_dict

    def use_high_frequency_sub_string_dict_to_generate_next_string(self, high_frequency_sub_string_dict, input_text, level=8, frequency_gate=2, how_many_character_you_want=200):
        # level: longer, more accurate, bascially we are find string in dict database
        # frequency_gate: int
        # If you want to have a creative one, add one random character after input_text.
        def get_next_words(the_dict, input_text):
            for level_index in reversed(list(range(0, level+1))):
                search_string = input_text[-level_index:]
                search_string_length_string = str(len(search_string))
                real_dict = the_dict.get(search_string_length_string)
                if real_dict == None:
                    continue
                result = real_dict.get(search_string)
                if result == None:
                    continue
                if result[0] < frequency_gate:
                    continue
                return result[1]
            return None

        print(input_text, end="", flush=True)
        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = get_next_words(high_frequency_sub_string_dict, input_text)
            if temp_response == None:
                break
            print(temp_response, end="", flush=True)
            time.sleep(0.1)
            response += temp_response
            input_text += temp_response
        print("\n\n", end="", flush=True)

        return response

    def auto_pattern_dict_finding_process(self, source_dict):
        """
        Step 1:
            1. first, it will look for 11 character long sub_sentence that appears 2 times.
            2. then, it will look for 10 character long sub_sentence that appears 2 times.
            3. then, it will look for 9 character long sub_sentence that appears 2 times.
            ...
            n. then, it will look for 1 character long sub_sentence that appears 2 times.
            it adds those sub_string as key_string in a dict

        Step 2:
            1. it will loop all those key_string, to find the next longest common characters. If there has no common character, it will save next 1 character as value. If there has common character, it will save 'next common characters + 1 new character' as value.

        Step 3:
            when you generate things, you randomly choice one from dict, from longest key to shortest key.

        This method needs a lot of storage but easy for people to understand.
        """
        pass

    def get_simplified_magic_language_tree_dict_from_text_list(self, source_text_list, target_dict_folder_path):
        """
        source_text_list can be [source_text]

        1. per two line as a input_string. "a\nb\nc" -> ["a\nb", "b\na"]
        2. every segement sub_sentence that split by punctuation will be input_string. "a: b, c." -> [a, b, c]
        3. every 4 char as input_sub_string.
        4. you can make 4 dict or put them togather.
        5. if you feel complex, try to use "divide by 2" thinking to get many sub_string but not all sub_string to reduce data.

        When you search, search longest string dict first.
        """
        from auto_everything.ml import Yingshaoxo_Text_Preprocessor
        yingshaoxo_text_preprocessor = Yingshaoxo_Text_Preprocessor()
        from auto_everything.disk import Disk
        disk = Disk()
        import json
        import os
        import sys
        sys.setrecursionlimit(99999)
        # or you can use {key: "another_dict_id"} to make sure each dict has only 9 depth.
        max_line_length = 1024
        ensure_ascii = False

        def add_sub_string_to_dict(the_dict, the_list):
            index = 0
            length = len(the_list)
            temp_dict = the_dict
            while index < length:
                element = the_list[index]
                if element not in temp_dict:
                    temp_dict[element] = dict()
                temp_dict = temp_dict[element]
                index += 1

        disk.create_a_folder(target_dict_folder_path)

        # sentence_level dict
        target_file_path = os.path.join(target_dict_folder_path, "1.sentence_level_dict.json")
        sentence_level_dict = {}
        if os.path.exists(target_file_path):
            with open(target_file_path, "r", encoding="utf-8") as f:
                temp_text = f.read()
            sentence_level_dict = json.loads(temp_text)

        for a_text in source_text_list:
            lines = a_text.strip().split("\n")
            lines = [line for line in lines if line.strip() != ""]
            for line_index in range(0, len(lines)-2):
                two_line_text = "\n".join(lines[line_index:line_index+3])
                add_sub_string_to_dict(sentence_level_dict, two_line_text[:max_line_length])

        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(sentence_level_dict, ensure_ascii=ensure_ascii))
        print("sentence_level_dict process done")

        # segment_sentence_level dict
        target_file_path = os.path.join(target_dict_folder_path, "2.segments_level_dict.json")
        segments_level_dict = {}
        if os.path.exists(target_file_path):
            with open(target_file_path, "r", encoding="utf-8") as f:
                temp_text = f.read()
            segments_level_dict = json.loads(temp_text)

        for a_text in source_text_list:
            a_text = a_text.strip()
            segments = yingshaoxo_text_preprocessor.split_string_into_list_by_punctuations(a_text)
            segments = [one["text"] for one in segments]
            for segment in segments:
                add_sub_string_to_dict(segments_level_dict, segment[:max_line_length])

        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(segments_level_dict, ensure_ascii=ensure_ascii))
        print("segments_level_dict process done")

        # character_level dict
        target_file_path = os.path.join(target_dict_folder_path, "3.character_level_dict.json")
        character_level_dict = {}
        if os.path.exists(target_file_path):
            with open(target_file_path, "r", encoding="utf-8") as f:
                temp_text = f.read()
            character_level_dict = json.loads(temp_text)

        window_length = 4
        for a_text in source_text_list:
            a_text = a_text.strip()
            for char_index in range(0, len(a_text)-window_length):
                char_window_list = a_text[char_index: char_index + window_length]
                add_sub_string_to_dict(character_level_dict, char_window_list)

        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(character_level_dict, ensure_ascii=ensure_ascii))
        print("character_level_dict process done")

    #def crazy_get_simplified_magic_language_tree_dict_from_text_list(self, source_text_list, target_dict_folder_path):
    #    from auto_everything.ml import Yingshaoxo_Text_Preprocessor
    #    yingshaoxo_text_preprocessor = Yingshaoxo_Text_Preprocessor()
    #    from auto_everything.disk import Disk
    #    disk = Disk()
    #    import json
    #    import os
    #    import sys
    #    sys.setrecursionlimit(99999)
    #    # or you can use {key: "another_dict_id"} to make sure each dict has only 9 depth.
    #    max_line_length = 1024
    #    ensure_ascii = False

    #    def add_sub_string_to_dict(the_dict, the_list):
    #        index = 0
    #        length = len(the_list)
    #        temp_dict = the_dict
    #        while index < length:
    #            element = the_list[index]
    #            if element not in temp_dict:
    #                temp_dict[element] = dict()
    #            temp_dict = temp_dict[element]
    #            index += 1

    #    disk.create_a_folder(target_dict_folder_path)

    #    # character_level dict
    #    target_file_path = os.path.join(target_dict_folder_path, "1.sentence_level_dict.json")
    #    character_level_dict = {}
    #    if os.path.exists(target_file_path):
    #        with open(target_file_path, "r", encoding="utf-8") as f:
    #            temp_text = f.read()
    #        character_level_dict = json.loads(temp_text)

    #    window_length = 64
    #    for a_text in source_text_list:
    #        a_text = a_text.strip()
    #        lines = a_text.split("\n")
    #        lines = [line for line in lines if line.strip() != ""]
    #        for line in lines:
    #            add_sub_string_to_dict(character_level_dict, line)

    #    with open(target_file_path, "w", encoding="utf-8") as f:
    #        f.write(json.dumps(character_level_dict, ensure_ascii=ensure_ascii))
    #    print("1.sentence_level_dict process done")

    def use_simplified_magic_language_tree_dict_to_get_next_text(self, store_dict, target_dict_folder_path, input_text, how_many_character_you_want=1024):
        import json
        import sys
        import os
        import random
        sys.setrecursionlimit(99999)
        max_line_length = 1024
        window_length = 64

        def load_json_from_file(path):
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    temp_text = f.read()
                return json.loads(temp_text)
            else:
                return {}

        if len(store_dict.keys()) != 3:
            # sentence_level dict
            target_file_path = os.path.join(target_dict_folder_path, "1.sentence_level_dict.json")
            sentence_level_dict = load_json_from_file(target_file_path)
            # segment_sentence_level dict
            target_file_path = os.path.join(target_dict_folder_path, "2.segments_level_dict.json")
            segments_level_dict = load_json_from_file(target_file_path)
            # character_level dict
            target_file_path = os.path.join(target_dict_folder_path, "3.character_level_dict.json")
            character_level_dict = load_json_from_file(target_file_path)
            store_dict["sentence_level_dict"] = sentence_level_dict
            store_dict["segments_level_dict"] = segments_level_dict
            store_dict["character_level_dict"] = character_level_dict
        else:
            sentence_level_dict = store_dict["sentence_level_dict"]
            segments_level_dict = store_dict["segments_level_dict"]
            character_level_dict = store_dict["character_level_dict"]

        def real_use_dict_to_get_next(input_text):
            def trace_words_to_get_sub_dict(the_dict, word_list):
                if len(word_list) == 0:
                    return the_dict
                else:
                    element = word_list[0]
                    if element in the_dict:
                        return trace_words_to_get_sub_dict(the_dict[element], word_list[1:])
                    else:
                        return None

            def get_next_words(the_dict):
                result_string = ""

                all_child_keys = list(the_dict.keys())
                target_list = all_child_keys
                if len(target_list) == 0:
                    return result_string
                else:
                    one = random.choice(target_list)
                    return result_string + one + get_next_words(the_dict[one])

                return result_text

            response = ""
            while len(response) < how_many_character_you_want:
                segments = input_text[-int(window_length/2):] # get right half as input
                segments = list(segments)

                temp_a_dict = trace_words_to_get_sub_dict(sentence_level_dict, segments)
                while temp_a_dict == None:
                    segments = segments[1:] # try less words right half if it is not in tree
                    if len(segments) == 0:
                        temp_a_dict = None
                        break
                    temp_a_dict = trace_words_to_get_sub_dict(sentence_level_dict, segments)
                    if temp_a_dict == None:
                        temp_a_dict = trace_words_to_get_sub_dict(segments_level_dict, segments)
                        if temp_a_dict == None:
                            temp_a_dict = trace_words_to_get_sub_dict(character_level_dict, segments)
                if temp_a_dict == None:
                    break
                else:
                    temp_response = get_next_words(temp_a_dict)
                    if temp_response == None:
                        break
                    if temp_response == "":
                        break

                time.sleep(0.1)
                response += temp_response
                input_text += temp_response

            return response

        print(input_text, end="", flush=True)
        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = real_use_dict_to_get_next(input_text)
            if temp_response == None:
                break
            if temp_response == "":
                break
            print(temp_response, end="", flush=True)
            time.sleep(0.1)
            response += temp_response
            input_text += temp_response
        print("\n\n", end="", flush=True)

        return response

    def final_goal(self):
        """
        搞个超级聊天数据库txt，从0开始和机器人聊天，让它学习所有长序列，带小女儿，边聊边成长。看得见的成长。
        """
        pass

    def pattern_looking(self, source_text, input_text):
        # pattern: "xxx mother is xxx."
        from auto_everything.string_ import String
        string = String()
        return "\n\n\n\n".join(list(set(string.hard_core_string_pattern_search(source_text, input_text))))


if __name__ == "__main__":
    yingshaoxo_text_completor = Yingshaoxo_Text_Completor()

    folder = "/home/yingshaoxo/CS/yingshaoxo_txt_data"
    #folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code_Mini"
    #folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Ebooks/Chinese/chinese_sex_novels"
    #folder = "/home/yingshaoxo/Downloads/doing/16.百科词典研究"

    source_text = yingshaoxo_text_completor.get_all_files_txt_under_a_folder(folder)
    #source_text = source_text.replace("\n", "").replace(" ", "").replace("　","")
    text_list = source_text.split("__**__**__yingshaoxo_is_the_top_one__**__**__")
    #yingshaoxo_text_completor.get_simplified_magic_language_tree_dict_from_text_list(text_list, "test_dict")
    #yingshaoxo_text_completor.crazy_get_simplified_magic_language_tree_dict_from_text_list(text_list, "test_dict")
    #exit()
    store_dict = dict()

    while True:
        try:
            input_text = input("What you want to say: ")
            #response = yingshaoxo_text_completor.get_next_text_by_pure_text(source_text, input_text, how_many_character_you_want=300, level=64, complete_how_many_character_for_each_time=None, use_background=False)

            #background_text = yingshaoxo_text_completor.search_long_background_context_by_using_multiprocess(source_text, input_text)
            #response = yingshaoxo_text_completor.one_shoot_next_text_generation_by_using_magic_tree_from_context_string(background_text, input_text, window_length=11)

            #response = yingshaoxo_text_completor.search_long_background_context_by_using_multiprocess(source_text, input_text, source_text_splitor=None)
            #response = yingshaoxo_text_completor.use_simplified_magic_language_tree_dict_to_get_next_text(store_dict, "test_dict", input_text)
            response = yingshaoxo_text_completor.pattern_looking(source_text, input_text+"xxx")
            if response:
                response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0]
                #print("\n\nComputer: \n" + input_text + response)
                print("\n\nComputer: \n" + response)
                print("\n\n")
        except KeyboardInterrupt:
            print("\n")
            continue
