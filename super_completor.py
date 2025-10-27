import random
import time
import json


class Yingshaoxo_Text_Completor():
    """
    This method is amazing, but not accurate compared to what human did. If you want human level completor, use 10 years to make a strong AI (child),  so he or she could do primary school stuff.
    """
    def __init__(self):
        pass

    def get_source_text_lines(self, source_text):
        source_text_lines = source_text.split("\n")
        return source_text_lines

    def pattern_looking(self, source_text, input_text):
        # pattern: "xxx mother is xxx."
        from auto_everything.string_ import String
        string = String()
        if "xxx" not in input_text:
            input_text = input_text.replace(" ", "xxx")
            input_text = input_text + "xxx"
        return "\n\n\n\n".join(list(set(string.hard_core_string_pattern_search(source_text, input_text, end_mark="__**__**__yingshaoxo_is_the_top_one__**__**__"))))

    def get_next_text_by_pure_text(self, source_text, input_text, how_many_character_you_want=2000, level=64, complete_how_many_character_for_each_time=None, return_one_word=False, use_background=False, creatively=False):
        """
        This method is ok, if you have big memory.
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

    def find_next_string_in_disk_txt_file(self, file_path, input_text, how_many_characters_you_want=1024, max_input_number=64, max_possibility_number=50, file_encoding="utf-8", splitor="__**__**__yingshaoxo_is_the_top_one__**__**__", get_previous_text=False, start_seek_position=0, end_seek_position=None):
        # quick
        # author: yingshaoxo
        input_text = input_text[-max_input_number:]
        sub_string_list = []
        for i in reversed(list(range(1, max_input_number+1))):
            sub_string = input_text[-i:]
            if len(sub_string) == i:
                sub_string_list.append(sub_string.encode(file_encoding))
        result_dict = {}
        for sub_string_bytes in sub_string_list:
            result_dict[sub_string_bytes] = []

        MB_10_size = 1024 * 1024 * 1
        current_position = start_seek_position
        with open(file_path, "rb") as f:
            f.seek(start_seek_position)
            while True:
                if end_seek_position != None:
                    if current_position >= end_seek_position:
                        # meets end seek position
                        break
                temp_text_bytes = f.read(MB_10_size)
                current_position += MB_10_size
                if len(temp_text_bytes) == 0 or len(temp_text_bytes) == max_input_number:
                    # meets file end
                    break

                for sub_string_bytes in sub_string_list:
                    if len(result_dict[sub_string_bytes]) > max_possibility_number:
                        break

                    start_temp_index = 0
                    while True:
                        index = temp_text_bytes.find(sub_string_bytes, start_temp_index)
                        if index == -1:
                            # not found
                            break
                        else:
                            # found, get next 1024 bytes and save to dict
                            start_temp_index = index + 1
                            sub_bytes = temp_text_bytes[index:index+how_many_characters_you_want]
                            if get_previous_text == True:
                                result_dict[sub_string_bytes].append(sub_bytes)
                            else:
                                result_dict[sub_string_bytes].append(sub_bytes[len(sub_string_bytes):])

                f.seek(-max_input_number, 1) #move back for 64 char

        final_list = []
        for sub_string_bytes in sub_string_list:
            for one in result_dict[sub_string_bytes]:
                if len(one) != 0:
                    one_string = one.decode(file_encoding, errors="ignore")
                    one_string = one_string.split(splitor)[0].rstrip()
                    final_list.append(one_string)
        return final_list

    def search_relative_data_from_disk_txt_file_by_using_keywords(self, file_path, input_text, keyword_list=None, file_encoding="utf-8", return_list=False, start_seek_position=0, end_seek_position=None):
        # quick, this is the best method so far
        if keyword_list == None:
            if " " not in input_text:
                try:
                    import jieba
                    jieba.setLogLevel(20)
                    has_jieba = True
                except Exception as e:
                    has_jieba = False

                if has_jieba:
                    word_list = list(jieba.cut(input_text, cut_all=False))
                else:
                    if " " in input_text:
                        word_list = input_text.split(" ")
                    else:
                        word_list = list(input_text)
            else:
                word_list = input_text.split(" ")
        else:
            word_list = list(keyword_list)

        max_input_number = 512
        word_bytes_list = [one.encode(file_encoding) for one in word_list]

        result_list = []
        result = ""
        #MB_1_size = 1024 * 1024 * 1
        MB_1_size = 1024 * 20 * 1
        current_position = start_seek_position
        with open(file_path, "rb") as f:
            f.seek(start_seek_position)
            while True:
                if end_seek_position != None:
                    if current_position >= end_seek_position:
                        # meets end seek position
                        break
                temp_text_bytes = f.read(MB_1_size)
                current_position += MB_1_size
                if len(temp_text_bytes) == 0 or len(temp_text_bytes) == max_input_number:
                    # meets file end
                    break
                ok = True
                for word_bytes in word_bytes_list:
                    if word_bytes not in temp_text_bytes:
                        ok = False
                        break
                if ok == True:
                    # this chunk matchs
                    result = self.search_long_background_context_by_using_keywords(temp_text_bytes.decode(file_encoding, errors="ignore"), "", keyword_list=list(word_list), words_distance=20)
                    result = result.strip()
                    if result != "":
                        if return_list == False:
                            break
                        else:
                            result_list.append(result)
                f.seek(-max_input_number, 1) #move back for 64 char

        if return_list == False:
            return result
        else:
            return result_list

    def search_long_background_context_by_using_keywords(self, source_text, input_text, keyword_list=None, source_text_splitor=None, accurate_mode=True, words_distance=None):
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
                    index_list = []
                    for key in keywords:
                        found_index = temp_text.find(key)
                        if found_index == -1:
                            # not found
                            ok = False
                            break
                        else:
                            if accurate_mode == True:
                                if len(index_list) > 0:
                                    # make sure the distance between two keyword is less than 20
                                    distance_between_keywords = abs(index_list[-1] - found_index)
                                    if distance_between_keywords == 0:
                                        ok = False
                                        break
                                    center_text = temp_text[min(index_list[-1], found_index): max(index_list[-1], found_index)]
                                    if words_distance == None:
                                        if " " in center_text:
                                            # english
                                            if distance_between_keywords > 64:
                                                ok = False
                                                break
                                        else:
                                            # chinese
                                            if distance_between_keywords > 20:
                                                ok = False
                                                break
                                    else:
                                        if distance_between_keywords > words_distance:
                                            ok = False
                                            break
                                index_list.append(found_index)
                            else:
                                pass
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
                original_length = len(one)
                result = handle_it(one)
                if result != "":
                    if original_length > len(result):
                        return result
                    else:
                        return ""
            return ""
        else:
            original_length = len(source_text)
            result = handle_it(source_text)
            if original_length > len(result):
                return result
            else:
                return ""

    def search_more_relative_data_from_disk_txt_file_by_using_keywords(self, file_path, input_text, keyword_list=None, file_encoding="utf-8", return_list=False, start_seek_position=0, end_seek_position=None, word_distance=20):
        # this is the second best method so far
        # cost is slow. 5 seconds for 200MB txt file.
        # similar to general context search function, but will search more
        def split_string_into_n_char_parts(a_string, n=2):
            a_list = [""]
            for char in a_string:
                if len(a_list[-1]) < n:
                    a_list[-1] += char
                else:
                    a_list.append(char)
            return a_list

        if keyword_list == None:
            if not input_text.isascii():
                word_list = split_string_into_n_char_parts(input_text, 2)
            else:
                word_list = input_text.split(" ")
        else:
            word_list = list(keyword_list)

        wrong_limit = int(len(word_list) * 0.8)
        word_bytes_list = [one.encode(file_encoding) for one in word_list]

        result_list = []
        result = ""
        MB_1_Bytes_Length = 1024 * 1024 * 1
        current_position = start_seek_position
        with open(file_path, "rb") as f:
            f.seek(start_seek_position)
            while True:
                if end_seek_position != None:
                    if current_position >= end_seek_position:
                        # meets end seek position
                        break
                temp_text_bytes = f.read(MB_1_Bytes_Length)
                current_position += MB_1_Bytes_Length
                if len(temp_text_bytes) == 0:
                    # meets file end
                    break
                ok = True
                ok_word_list = []
                wrong_counting = 0
                for word_bytes in word_bytes_list:
                    if word_bytes not in temp_text_bytes:
                        wrong_counting += 1
                        if wrong_counting > wrong_limit:
                            ok = False
                            break
                    else:
                        ok_word_list.append(word_bytes.decode(file_encoding, errors="ignore"))
                if ok == True:
                    # this chunk matchs
                    result = self.search_long_background_context_by_using_keywords(temp_text_bytes.decode(file_encoding, errors="ignore"), "", keyword_list=ok_word_list, words_distance=word_distance)
                    result = result.strip()
                    if result != "":
                        if return_list == False:
                            break
                        else:
                            result_list.append(result)

        if return_list == False:
            return result
        else:
            return result_list

    def search_long_background_context_from_disk_txt_file_by_using_multiprocess(self, file_path, input_text, keyword_list=None, return_text=True, file_encoding="utf-8", get_more=False):
        # super quick
        # recommand for using in dialy tasks
        # get_more=True will give you more data but very slow
        from auto_everything.disk import Disk
        disk = Disk()
        import multiprocessing

        the_100MB_length = 1024 * 1024 * 100
        the_full_length = disk.get_file_size(file_path, level='B')

        part_number = int(the_full_length / the_100MB_length)

        pool = multiprocessing.Pool()
        results = []
        if get_more == False:
            the_function = self.search_relative_data_from_disk_txt_file_by_using_keywords
        else:
            the_function = self.search_more_relative_data_from_disk_txt_file_by_using_keywords
        for part_index in range(0, part_number + 1):
            start_index = part_index * the_100MB_length
            if start_index >= the_full_length:
                break
            end_index = start_index + the_100MB_length
            if end_index > the_full_length:
                end_index = the_full_length - 1

            result = pool.apply_async(
                the_function,
                args=(file_path, input_text, keyword_list, file_encoding, True, start_index, end_index)
            )
            results.append(result)

        pool.close()
        pool.join()

        final_results = []
        for result in results:
            sub_result = result.get()
            if sub_result != None:
                if len(sub_result) != 0:
                    for one in sub_result:
                        one = one.strip()
                        if one != "":
                            final_results.append(one)

        if return_text == False:
            return final_results
        else:
            return "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n".join(final_results)

    def get_simplified_magic_language_tree_dict_from_text_list(self, store_dict, target_dict_folder_path, source_text_list, window_length=11):
        """
        yingshaoxo: super useful one, I recommand this. If you use disk_dict and change window_length into 256. It would be super accurate as deepseek or openai chat gpt3.

        Use jieba word spliting pre_processor would also increase accuracy.


        source_text_list can be [source_text], but you have to set window_length.

        window_length can be None, so the it will use full_length of source_text_list.


        Memory dict has size error, takes too much space. But you can try save 25 chars tree, then search for 24 chars sub_string to complete one char.
        """
        from auto_everything.disk import Disk
        disk = Disk()
        import json
        import os
        import sys
        sys.setrecursionlimit(99999)
        # or you can use {key: "another_dict_id"} to make sure each dict has only 9 depth.
        max_line_length = 512
        ensure_ascii = False

        def load_json_from_file(path):
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    temp_text = f.read()
                return json.loads(temp_text)
            else:
                return {}
        if "character_level_tree_dict" not in store_dict.keys():
            # character_level dict
            target_file_path = os.path.join(target_dict_folder_path, "character_level_tree_dict.json")
            character_level_dict = load_json_from_file(target_file_path)
            store_dict["character_level_tree_dict"] = character_level_dict
        else:
            character_level_dict = store_dict["character_level_tree_dict"]

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

        if window_length == None:
            for a_text in source_text_list:
                add_sub_string_to_dict(character_level_dict, a_text)
        else:
            for a_text in source_text_list:
                if type(a_text) == str:
                    a_text = a_text.strip()
                for char_index in range(0, len(a_text)):
                    char_window_list = a_text[char_index: char_index + window_length]
                    if len(char_window_list) != window_length:
                        continue
                    add_sub_string_to_dict(character_level_dict, char_window_list)

        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(character_level_dict, ensure_ascii=ensure_ascii))
        print("character_level_tree_dict process done")

    def use_simplified_magic_language_tree_dict_to_get_next_text(self, store_dict, target_dict_folder_path, input_text, how_many_character_you_want=1024, window_length=11, no_sleep=False):
        """
        yingshaoxo: super useful one, I recommand this. If you use disk_dict and change window_length into 256. It would be super accurate as deepseek or openai chat gpt3.

        Use jieba word spliting pre_processor would also increase accuracy.

        But normally, we use sqlite to get 1MB data with keywords filter from 2TB text first, then use tree to do the cache and generation.
        """
        import json
        import sys
        import os
        import random
        sys.setrecursionlimit(99999)
        max_line_length = 512

        def load_json_from_file(path):
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    temp_text = f.read()
                return json.loads(temp_text)
            else:
                return {}

        if "character_level_tree_dict" not in store_dict.keys():
            # character_level dict
            target_file_path = os.path.join(target_dict_folder_path, "character_level_tree_dict.json")
            character_level_dict = load_json_from_file(target_file_path)
            store_dict["character_level_tree_dict"] = character_level_dict
        else:
            character_level_dict = store_dict["character_level_tree_dict"]

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

                if the_dict == None:
                    return result_string

                all_child_keys = list(the_dict.keys())
                target_list = all_child_keys
                if len(target_list) == 0:
                    return result_string
                else:
                    one = random.choice(target_list)
                    return result_string + one + get_next_words(the_dict[one])

                return result_text

            def get_next_words_for_list(the_dict):
                result_list = []

                if the_dict == None:
                    return result_list

                all_child_keys = list(the_dict.keys())
                target_list = all_child_keys
                if len(target_list) == 0:
                    return result_list
                else:
                    one = random.choice(target_list)
                    the_value = the_dict.get(one)
                    if the_value != None:
                        return result_list + [one] + get_next_words_for_list(the_dict[one])
                    else:
                        return result_list
                return result_list

            response = None
            segments = input_text[-int(window_length-1):]
            temp_a_dict = trace_words_to_get_sub_dict(character_level_dict, segments)
            while temp_a_dict == None:
                segments = segments[1:] # try less words right half if it is not in tree
                if len(segments) == 0:
                    temp_a_dict = None
                    break
                temp_a_dict = trace_words_to_get_sub_dict(character_level_dict, segments)
            if temp_a_dict == None:
                return None
            else:
                if type(input_text) == str:
                    temp_response = get_next_words(temp_a_dict)
                    if temp_response == "":
                        return None
                elif type(input_text) == list:
                    temp_response = get_next_words_for_list(temp_a_dict)
                if temp_response == None:
                    return None
                response = temp_response
            return response

        if type(input_text) == str:
            print(input_text, end="", flush=True)
            response = ""
            while len(response) < how_many_character_you_want:
                temp_response = real_use_dict_to_get_next(input_text)
                if temp_response == None:
                    break
                if temp_response == "":
                    break
                #temp_response = temp_response.replace(":","")
                print(temp_response, end="", flush=True)
                if no_sleep == False:
                    time.sleep(0.01)
                response += temp_response
                input_text += temp_response
            print("\n\n", end="", flush=True)
        elif type(input_text) == list:
            print(input_text, end="", flush=True)
            response = []
            while len(response) < how_many_character_you_want:
                temp_response = real_use_dict_to_get_next(input_text)
                if temp_response == None:
                    break
                if len(temp_response) == 0:
                    break
                print(temp_response, end="", flush=True)
                if no_sleep == False:
                    time.sleep(0.1)
                response += temp_response
                input_text += temp_response
            print("\n\n", end="", flush=True)

        return response

    def get_magic_language_tree_dict_from_text(self, source_text, char_level=True, window_length=8):
        """
        This will be used for context background information extraction.

        2MB text: window_length == 11
        20KB text: window_length == 32
        """
        """
        tree的目的: 加速和减少干扰概率
        建议: 把数据喂进来之前，先把垃圾数据移除，概率树只处理核心数据
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
                #print("reduce dict size by deleting low frequency words...")
                #delete_low_frequency_words(sub_string_dict, 2)
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
            segments = get_segments(input_text)[-int(window_length-2):] # get right half as input

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
            #time.sleep(0.1)
            response += temp_response
            input_text += temp_response

        #print("\n\n", end="", flush=True)

        return response

    def _is_connector(self, string):
        splits = "the of is and to in that we for an are by be as on with can if from which you it this then at have all not one has or that 的 了 和 是 就 都 而 及 与 着 或 一个 沒有 是否 我們 你們 妳們 他們 她們".split(" ")
        return string in splits

    def _is_punctuation(self, string, more_punctuation="跟讲在有要地的着和便等就让了说想被到是只给几买干从个为以然问没回对先者出也之能上下么儿很会还这"):
        return string in (",.!?;:，。；：!？ \n-=_+()*&^%$#@!`~{}|[]'/<>" + more_punctuation)

    def _get_keywords(self, string, more_punctuation=""):
        # not accurate for chinese, unless you split keyword by using space
        if string.isascii():
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
                keywords = list(jieba.cut(input_text, cut_all=False))
            except Exception as e:
                #print(e)
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

    def one_shoot_next_text_generation_by_using_magic_tree_from_context_string(self, context_text, input_text, frequency_gate=1.0, window_length=8, how_many_character_you_want=128):
        """
        Why don't you use sqlite to search input_text[-32:] result, to get a list of similar text. Then pass that string as context_text to this function.
        """
        context_text = context_text[-50000:]
        the_dict = self.get_magic_language_tree_dict_from_text(context_text, char_level=True, window_length=window_length)
        response = self.use_magic_language_tree_dict_to_generate_next_string(the_dict, input_text, char_level=True, frequency_gate=frequency_gate, window_length=window_length, how_many_character_you_want=how_many_character_you_want)
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
        """
        print("do it yourself")

    def use_repeated_sub_string_dict_to_generate_next_string(self, sub_string_dict, input_text, level=32, how_many_character_you_want=200, creatively=False):
        print("do it yourself")

    def final_goal(self):
        """
        搞个超级聊天数据库txt，从0开始和机器人聊天，让它学习所有长序列，带小女儿，边聊边成长。看得见的成长。
        """
        pass

    def get_disk_simplified_magic_language_tree_dict_from_text_list(self, target_dict_folder_path, source_text_list, window_length=18, no_sliding_window=False):
        """
        You can try save 25 chars tree, then search for 24 chars sub_string to complete one char. In other words, generate dict by using 25 window_length, use dict by using 48 window_length, because 48/2 == 24.

        I think smooth character window tree may not a good idea for very big dataset, because most of the time I will give the start sub string of a sentence. For example: how to xxx
        So if we directly pass data into another program without sliding_window, it will be better in disk size. For example, a class as a 'sentence', a function as a 'sentence'.

        For chat, it can be a simple problem by using two dict, one is for "user_a: xxx\nuser_b:the_first_segment_of_sentence", another is for "the_first_segment_of_sentence -> rest_sentence"
        For question_and_answer, it can be two dict, one is for generating template based on question, another is for generating whole data based on template, template can be: "How to do xxx? -> what is xxx; xxx can be done by xxx; the good part of doing xxx is xxx.". Then use single sentence generation dict to complete the template.
        """
        from auto_everything.io import Disk_Dict
        import sys
        sys.setrecursionlimit(99999)

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

        # character_level dict
        root_disk_dict = Disk_Dict(target_dict_folder_path)
        if no_sliding_window == False:
            for a_text in source_text_list:
                if type(a_text) == str:
                    a_text = a_text.strip()
                for char_index in range(len(a_text)):
                    char_window_list = a_text[char_index: char_index + window_length]
                    if len(char_window_list) != window_length:
                        continue
                    add_sub_string_to_dict(root_disk_dict, char_window_list)
        else:
            for a_text in source_text_list:
                a_text = a_text.strip()
                char_list = list(a_text)
                add_sub_string_to_dict(root_disk_dict, char_list)

        print("character tree process done")

    def use_disk_simplified_magic_language_tree_dict_to_get_next_text(self, target_dict_folder_path, input_text, how_many_character_you_want=512, window_length=18, no_sleep=True):
        from auto_everything.io import Disk_Dict
        import sys
        import random
        sys.setrecursionlimit(99999)
        root_disk_dict = Disk_Dict(target_dict_folder_path)

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

                if the_dict == None:
                    return result_string

                all_child_keys = list(the_dict.keys())
                target_list = all_child_keys
                if len(target_list) == 0:
                    return result_string
                else:
                    one = random.choice(target_list)
                    return result_string + one + get_next_words(the_dict[one])

                return result_text

            def get_next_words_for_list(the_dict):
                result_list = []

                if the_dict == None:
                    return result_list

                all_child_keys = list(the_dict.keys())
                target_list = all_child_keys
                if len(target_list) == 0:
                    return result_list
                else:
                    one = random.choice(target_list)
                    the_value = the_dict.get(one)
                    if the_value != None:
                        return result_list + [one] + get_next_words_for_list(the_dict[one])
                    else:
                        return result_list
                return result_list

            response = None
            segments = input_text[-int(window_length-1):]
            temp_a_dict = trace_words_to_get_sub_dict(root_disk_dict, segments)
            while temp_a_dict == None:
                segments = segments[1:] # try less words right half if it is not in tree
                if len(segments) == 0:
                    temp_a_dict = None
                    break
                temp_a_dict = trace_words_to_get_sub_dict(root_disk_dict, segments)
            if temp_a_dict == None:
                return None
            else:
                if type(input_text) == str:
                    temp_response = get_next_words(temp_a_dict)
                    if temp_response == "":
                        return None
                elif type(input_text) == list:
                    temp_response = get_next_words_for_list(temp_a_dict)
                if temp_response == None:
                    return None
                response = temp_response
            return response

        if type(input_text) == str:
            print(input_text, end="", flush=True)
            response = ""
            while len(response) < how_many_character_you_want:
                temp_response = real_use_dict_to_get_next(input_text)
                if temp_response == None:
                    break
                if temp_response == "":
                    break
                #temp_response = temp_response.replace(":","")
                print(temp_response, end="", flush=True)
                if no_sleep == False:
                    time.sleep(0.01)
                response += temp_response
                input_text += temp_response
            print("\n\n", end="", flush=True)
        elif type(input_text) == list:
            print(input_text, end="", flush=True)
            response = []
            while len(response) < how_many_character_you_want:
                temp_response = real_use_dict_to_get_next(input_text)
                if temp_response == None:
                    break
                if len(temp_response) == 0:
                    break
                print(temp_response, end="", flush=True)
                if no_sleep == False:
                    time.sleep(0.1)
                response += temp_response
                input_text += temp_response
            print("\n\n", end="", flush=True)

        return response

    def get_one_line_based_magic_language_tree_dict(self, source_text_list, target_dict_folder_path, max_length_for_one_line=512):
        # super quick, one sentence un_beatable
        # 294MB的txt数据，用了tree，扩大到780MB，膨胀了3倍。800MB的硬盘tree数据，放到内存，占了21000MB(21GB)，意思就是膨胀了27倍
        from auto_everything.disk import Disk
        disk = Disk()
        import json
        import os
        import sys
        sys.setrecursionlimit(99999)
        ensure_ascii = False

        disk.create_a_folder(target_dict_folder_path)

        root_dict = {}

        target_file_path = os.path.join(target_dict_folder_path, "one_line_dict.json")
        if os.path.exists(target_file_path):
            with open(target_file_path, "r", encoding="utf-8") as f:
                temp_text = f.read()
            root_dict = json.loads(temp_text)

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

        counting = 0
        window_length = 3
        for a_text in source_text_list:
            lines = a_text.split("\n")
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                add_sub_string_to_dict(root_dict, line[:max_length_for_one_line])

            counting += 1
            print(counting)
            if counting >= 99999999:
                counting = 0

        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(root_dict, ensure_ascii=ensure_ascii))
        print("root_dict process done")

    def use_one_line_based_magic_language_tree_dict_to_get_next_text(self, global_dict, target_dict_folder_path, input_text, how_many_character_you_want=256):
        # super quick, one sentence un_beatable
        from auto_everything.disk import Disk
        import os
        import sys
        import random
        sys.setrecursionlimit(99999)

        root_disk_dict = {}

        if global_dict.get("one_line_dict") != None:
            root_disk_dict = global_dict["one_line_dict"]
        else:
            target_file_path = os.path.join(target_dict_folder_path, "one_line_dict.json")
            if os.path.exists(target_file_path):
                with open(target_file_path, "r", encoding="utf-8") as f:
                    temp_text = f.read()
                root_disk_dict = json.loads(temp_text)
            global_dict["one_line_dict"] = root_disk_dict
            print("\ndict loaded!")

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
                the_value = the_dict.get(one)
                if the_value:
                    return result_string + one + get_next_words(the_dict[one])
                else:
                    return result_string

            return result_text

        def directly_use_dict_to_get_next(input_text):
            child_dict = trace_words_to_get_sub_dict(root_disk_dict, input_text)
            if child_dict == None:
                return None
            response = get_next_words(child_dict)
            if response == "":
                return None
            return response

        def reduce_char_to_get_next(input_text):
            input_text = input_text.split("\n")[-1]
            temp_result = directly_use_dict_to_get_next(input_text)
            if temp_result != None:
                return temp_result
            index = 0
            length = len(input_text)
            for i in range(length):
                temp_input = input_text[i:]
                if len(temp_input) == "":
                    return None
                temp_result = directly_use_dict_to_get_next(temp_input)
                if temp_result != None:
                    return temp_result
            return None

        def must_full_fill_length(the_input_text, how_many_character_you_want):
            response = ""
            temp_input = the_input_text
            while True:
                result = reduce_char_to_get_next(temp_input)
                if result != None:
                    response += result + "\n"
                    temp_input += result
                else:
                    return response
                if len(response) >= how_many_character_you_want:
                    return response

        temp_response = must_full_fill_length(input_text, how_many_character_you_want)
        return temp_response

    def get_abstract_dict_from_text_list(self, store_dict, target_dict_folder_path, source_text_list, froze_level_0=True):
        """
        store_dict = {}, in global

        让我们来搞多文件多层抽象dict:
            第一层: 1 char -> 1 char -> number_ID_for_this_path
            第二层: 2 char -> 2 char -> number_ID_for_this_path
            第三层: 4 char -> 4 char -> number_ID_for_this_path
            第四层: 8 char -> 8 char -> number_ID_for_this_path
            第五层: 16 char -> 16 char -> number_ID_for_this_path
            第六层: 32 char -> 32 char -> number_ID_for_this_path
            第七层: 64 char -> 64 char -> number_ID_for_this_path

            number_id is a self made incresing id
            I can give you a minimum example of one layer dict: {"_negative_max_id": "-1", "h": {"i": "0", "h": "1"}}
            Clearly, start from bottom, by tracing the char tree, you can always get number_id.
            We will fill those layer by using sliding_window, I mean input_text[-128:].

            除了第一层的tree node是直接用的char，其它高级层都是用的上一层的number_id。
            当用户来了一个input_text，我首先把它变成第一层的 2字_id，如果有字不在我们的tree里面，就说明它只停留在char第一层，所以我们直接调用第一层的tree去做补全。也就是用最后一个字符，补全下一个字符。
            如果input_text在第一层被完全解析了，那我们会得到[2,5,9,4]，我们照着这个单子查询第二层有没有'"2,5" -> "9,4" -> number_id'，如果有，我们就去到第三层。否则直接用第二层的数据补全下一个词，如"9,4" -> "xxx"，xxx是一个数字，是第一层某两个字符的ID。
            这个东西最终实现的功能，是用极少的存储，保证用很长的一个前序列，补全下一个抽象长序列。比如第6层，如果前面有32个字符存在于第6层，就一下子补全32个字符。但我存储这个长序列，只用了2个数字ID。补全那32个字符，是一层一层调用前面一层的序列。

            这个tree美妙的地方在于，每个节点后面不是一个固定的节点，是一堆可选节点，是可以用随机数选择的。也就是说，每次生成的内容都不一样。
        """
        from auto_everything.disk import Disk
        disk = Disk()
        import json
        import os
        import sys
        sys.setrecursionlimit(99999)
        ensure_ascii = False

        disk.create_a_folder(target_dict_folder_path)

        root_dict = {}
        for i in range(7):
            root_dict[str(i)] = {
                "_negative_max_id": "-1",
            }
            root_dict["-" + str(i)] = {}

        if "super_abstract_dict" in store_dict:
            root_dict = store_dict["super_abstract_dict"]
        else:
            target_file_path = os.path.join(target_dict_folder_path, "super_abstract_dict.json")
            if os.path.exists(target_file_path):
                with open(target_file_path, "r", encoding="utf-8") as f:
                    temp_text = f.read()
                root_dict = json.loads(temp_text)
                store_dict["super_abstract_dict"] = root_dict

        level_0_dict = root_dict[str(0)]
        level_1_dict = root_dict[str(1)]
        level_2_dict = root_dict[str(2)]
        level_3_dict = root_dict[str(3)]
        level_4_dict = root_dict[str(4)]
        level_5_dict = root_dict[str(5)]

        reverse_level_0_dict = root_dict["-"+str(0)]
        reverse_level_1_dict = root_dict["-"+str(1)]
        reverse_level_2_dict = root_dict["-"+str(2)]
        reverse_level_3_dict = root_dict["-"+str(3)]
        reverse_level_4_dict = root_dict["-"+str(4)]
        reverse_level_5_dict = root_dict["-"+str(5)]

        def add_sub_string_to_dict(the_dict, the_list_string):
            if the_list_string in the_dict:
                return None
            current_max_id = int(the_dict["_negative_max_id"])
            current_max_id += 1
            current_max_id = str(current_max_id)
            the_dict["_negative_max_id"] = current_max_id
            the_dict[the_list_string] = current_max_id
            return current_max_id

        def add_id_and_value_pair(level_reverse_dict, id, value):
            level_reverse_dict[id] = value

        def process_sub_string_to_let_it_go_to_level_dict(root_dict, char_window_list):
            # maybe in future training, we can refuse level_0 and level_1 data updating, because if new text does not have a base word coming from level_0 and level_1, we would think it is a random string. We do not remember garbage code.

            #for level 0
            if froze_level_0 == False:
                for i in [4, 3, 2, 1]:
                    small_window_length = i
                    for char_index in range(0, len(char_window_list)):
                        small_char_window_list = char_window_list[char_index: char_index + small_window_length]
                        if len(small_char_window_list) != small_window_length:
                            continue
                        new_id = add_sub_string_to_dict(level_0_dict, small_char_window_list)
                        if new_id != None:
                            add_id_and_value_pair(reverse_level_0_dict, new_id, small_char_window_list)
            return

            if froze_level_0 == False:
                #for level 1
                # we should ignore 1 to 3 short sequence, because we handled it in previous one. even if there has any char not get catched, we can complete it by using our punctuation completion algorithm in the end
                for char_index in range(0, len(char_window_list)):
                    operation_list = [
                        [9, [3,3,3]],
                        [8, [3,3,2]],
                        [7, [3,3,1]],
                        [6, [3,3]],
                        [5, [3,2]],
                        [4, [3,1]],
                    ]
                    string_id_list = []
                    for string_length, part_list in operation_list:
                        small_window_length = string_length
                        small_char_window_list = char_window_list[char_index: char_index + small_window_length]
                        if len(small_char_window_list) != string_length:
                            continue
                        id_list = []
                        for one in part_list:
                            temp_part = small_char_window_list[:one]
                            temp_id = level_0_dict.get(temp_part)
                            if temp_id == None:
                                break
                            id_list.append(temp_id)
                        string_id = "_".join(id_list)
                        string_id_list.append(string_id)

                    for an_id_string in string_id_list:
                        new_id = add_sub_string_to_dict(level_1_dict, an_id_string)
                        if new_id != None:
                            add_id_and_value_pair(reverse_level_1_dict, new_id, an_id_string)

            return

            if froze_level_0 == False:
                #for level 2
                for char_index in range(0, len(char_window_list)):
                    small_window_length = 8
                    small_char_window_list = char_window_list[char_index: char_index + small_window_length]
                    if len(small_char_window_list) != 8:
                        continue

                    part_list = [2, 2, 2, 2]
                    id_list = []
                    for one in part_list:
                        temp_part = small_char_window_list[:one]
                        small_char_window_list = small_char_window_list[one:]
                        temp_id = level_0_dict.get(temp_part)
                        if temp_id == None:
                            break
                        id_list.append(temp_id)
                    if len(id_list) < 4:
                        continue

                    part_list = [id_list[0]+"_"+id_list[1], id_list[2]+"_"+id_list[3]]
                    id_list = []
                    for one in part_list:
                        temp_id = level_1_dict.get(one)
                        if temp_id == None:
                            break
                        id_list.append(temp_id)
                    if len(id_list) < 2:
                        continue

                    string_id_list = "_".join(id_list)
                    new_id = add_sub_string_to_dict(level_2_dict, string_id_list)
                    if new_id != None:
                        add_id_and_value_pair(reverse_level_2_dict, new_id, string_id_list)

        window_length = 64
        for a_text in source_text_list:
            for char_index in range(0, len(a_text)):
                char_window_list = a_text[char_index: char_index + window_length]
                if len(char_window_list) == 0:
                    continue
                process_sub_string_to_let_it_go_to_level_dict(root_dict, char_window_list)

        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(root_dict, ensure_ascii=ensure_ascii))
        print("root_dict process done")

    def use_abstract_dict_to_compress_text(self, store_dict, target_dict_folder_path, input_text):
        from auto_everything.disk import Disk
        disk = Disk()
        import json
        import os
        import sys
        sys.setrecursionlimit(99999)
        ensure_ascii = False

        disk.create_a_folder(target_dict_folder_path)

        root_dict = {}
        for i in range(7):
            root_dict[str(i)] = {
                "_negative_max_id": "-1",
            }
            root_dict["-" + str(i)] = {}

        if "super_abstract_dict" in store_dict:
            root_dict = store_dict["super_abstract_dict"]
        else:
            target_file_path = os.path.join(target_dict_folder_path, "super_abstract_dict.json")
            if os.path.exists(target_file_path):
                with open(target_file_path, "r", encoding="utf-8") as f:
                    temp_text = f.read()
                root_dict = json.loads(temp_text)
                store_dict["super_abstract_dict"] = root_dict

        level_0_dict = root_dict[str(0)]
        level_1_dict = root_dict[str(1)]
        level_2_dict = root_dict[str(2)]
        level_3_dict = root_dict[str(3)]
        level_4_dict = root_dict[str(4)]
        level_5_dict = root_dict[str(5)]

        reverse_level_0_dict = root_dict["-"+str(0)]
        reverse_level_1_dict = root_dict["-"+str(1)]
        reverse_level_2_dict = root_dict["-"+str(2)]
        reverse_level_3_dict = root_dict["-"+str(3)]
        reverse_level_4_dict = root_dict["-"+str(4)]
        reverse_level_5_dict = root_dict["-"+str(5)]

        id_list = []
        index = 0
        while True:
            small_window_length = 4
            sub_string = input_text[index: index + small_window_length]
            temp_id = level_0_dict.get(sub_string)
            if temp_id != None:
                id_list.append(temp_id)
                index += small_window_length
            else:
                small_window_length = 3
                sub_string = input_text[index: index + small_window_length]
                temp_id = level_0_dict.get(sub_string)
                if temp_id != None:
                    id_list.append(temp_id)
                    index += small_window_length
                else:
                    small_window_length = 2
                    sub_string = input_text[index: index + small_window_length]
                    temp_id = level_0_dict.get(sub_string)
                    if temp_id != None:
                        id_list.append(temp_id)
                        index += small_window_length
                    else:
                        small_window_length = 1
                        sub_string = input_text[index: index + small_window_length]
                        temp_id = level_0_dict.get(sub_string)
                        if temp_id != None:
                            id_list.append(temp_id)
                            index += small_window_length
                        else:
                            index += 1
            if index >= len(input_text):
                break

        return "_".join(id_list)

    def use_abstract_dict_to_decompress_text(self, store_dict, target_dict_folder_path, input_text):
        from auto_everything.disk import Disk
        disk = Disk()
        import json
        import os
        import sys
        sys.setrecursionlimit(99999)
        ensure_ascii = False

        disk.create_a_folder(target_dict_folder_path)

        root_dict = {}
        for i in range(7):
            root_dict[str(i)] = {
                "_negative_max_id": "-1",
            }
            root_dict["-" + str(i)] = {}

        if "super_abstract_dict" in store_dict:
            root_dict = store_dict["super_abstract_dict"]
        else:
            target_file_path = os.path.join(target_dict_folder_path, "super_abstract_dict.json")
            if os.path.exists(target_file_path):
                with open(target_file_path, "r", encoding="utf-8") as f:
                    temp_text = f.read()
                root_dict = json.loads(temp_text)
                store_dict["super_abstract_dict"] = root_dict

        level_0_dict = root_dict[str(0)]
        level_1_dict = root_dict[str(1)]
        level_2_dict = root_dict[str(2)]
        level_3_dict = root_dict[str(3)]
        level_4_dict = root_dict[str(4)]
        level_5_dict = root_dict[str(5)]

        reverse_level_0_dict = root_dict["-"+str(0)]
        reverse_level_1_dict = root_dict["-"+str(1)]
        reverse_level_2_dict = root_dict["-"+str(2)]
        reverse_level_3_dict = root_dict["-"+str(3)]
        reverse_level_4_dict = root_dict["-"+str(4)]
        reverse_level_5_dict = root_dict["-"+str(5)]

        small_window_length = 2

        text = ""
        for a_id in input_text.split("_"):
            raw_string = reverse_level_0_dict.get(a_id)
            if raw_string != None:
                text += raw_string

        return text

    def get_feature_based_dict_for_completion(self, source_text_list, max_traning_loop=3):
        # you can feed the final data as "{key}{value}" into the char tree, it would be very accurate
        final_dict = {}
        for i in range(1, 20): # complete value should has length from 1 to 20
            complete_value_length = i
            window_length = complete_value_length
            root_dict = {}
            copy_root_dict = {}
            waiting_for_next_loop_value_set = set()
            while True:
                for text in source_text_list:
                    for char_index in range(len(text)):
                        sub_string = text[char_index:char_index + window_length + complete_value_length]
                        if len(sub_string) == window_length + complete_value_length:
                            previous_string = sub_string[:window_length]
                            next_string = sub_string[window_length:]

                            if next_string in waiting_for_next_loop_value_set:
                                continue

                            if next_string in copy_root_dict.keys():
                                continue

                            if next_string not in root_dict.keys():
                                root_dict[next_string] = previous_string
                            else:
                                if root_dict[next_string] != previous_string:
                                    # why for same next_string, the previous_string is different? 1+1 can only be 2, so in previous text, there must have some feature that we did not catch. So previous_string length should get add by 1.
                                    #print(root_dict[next_string], "|", previous_string, "|", next_string)
                                    waiting_for_next_loop_value_set.add(next_string)
                                    del root_dict[next_string]
                for key,value in root_dict.items():
                    copy_root_dict[key] = value
                window_length += 1
                print("current_window_length: ", window_length)
                waiting_for_next_loop_value_set = set()
                root_dict = {}
                if window_length >= max_traning_loop:
                    break
            final_dict.update({value:key for key,value in copy_root_dict.items()})
        return final_dict

    def use_feature_based_dict_to_get_next_text(self, root_dict, input_text, how_many_character_you_want=64, max_previous_char_number=256):
        def the_real_function(the_input_text, the_level):
            while the_level >= 1:
                right_side_sub_string = the_input_text[-the_level:]
                the_next_value = root_dict.get(right_side_sub_string)
                if the_next_value != None:
                    return the_next_value
                the_level -= 1
            return None

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = the_real_function(input_text, max_previous_char_number)
            if temp_response == None:
                break
            response += temp_response
            input_text += temp_response

        return response

    def get_better_word_dict_by_using_jieba(self, source_text, target_json_file_path):
        # source_text should be a diary or valuable book
        import json
        import jieba
        jieba.setLogLevel(20)

        word_list = list(jieba.cut(source_text, cut_all=False))
        print("jieba word cutting done.")
        word_dict = {}
        for word in word_list:
            if word not in word_dict.keys():
                word_dict[word] = 1
            else:
                word_dict[word] += 1
        word_item_list = [[key,value] for key,value in word_dict.items()]
        word_item_list.sort(key=lambda item: -item[1])

        word_to_id_dict = {}
        id_to_word_dict = {}
        for index, item in enumerate(word_item_list):
            word_to_id_dict[item[0]] = index
            id_to_word_dict[index] = item[0]

        root_dict = {
            "word_to_id_dict": word_to_id_dict,
            "id_to_word_dict": id_to_word_dict,
        }

        print("id dict handle done.")

        with open(target_json_file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(root_dict, ensure_ascii=False))

        print("id dict saving done.")

    def use_word_dict_to_encode_string_to_id_list(self, target_json_file_path, input_text):
        import json
        with open(target_json_file_path, "r", encoding="utf-8") as f:
            temp_text = f.read()
        root_dict = json.loads(temp_text)
        word_to_id_dict = root_dict["word_to_id_dict"]
        #id_to_word_dict = root_dict["id_to_word_dict"]

        copy_text = input_text
        id_list = []
        index = 0
        length = len(copy_text)
        while index < length:
            ok = False
            for i in reversed(list(range(1, 32))):
                sub_string = copy_text[index:index+i]
                if len(sub_string) == 0:
                    continue
                result = word_to_id_dict.get(sub_string)
                if result != None:
                    index += len(sub_string)
                    id_list.append(str(result))
                    ok = True
                    break
            if ok == False:
                index += 1
        return id_list

    def use_word_dict_to_decode_id_list_to_string(self, target_json_file_path, id_list):
        import json
        with open(target_json_file_path, "r", encoding="utf-8") as f:
            temp_text = f.read()
        root_dict = json.loads(temp_text)
        #word_to_id_dict = root_dict["word_to_id_dict"]
        id_to_word_dict = root_dict["id_to_word_dict"]

        result_string = ""
        for a_id in id_list:
            a_id = str(a_id)
            result = id_to_word_dict.get(a_id)
            if result != None:
                result_string += result
        return result_string

    def get_general_word_order_dict(self, source_text_list, order_dict_folder):
        import json
        from auto_everything.disk import Disk
        disk = Disk()
        try:
            import jieba
            jieba.setLogLevel(20)
            has_jieba = True
        except Exception as e:
            has_jieba = False

        word_dict = {}
        word_order_dict = {}
        for part in source_text_list:
            part = part[:1024]
            part = part.strip()
            if has_jieba:
                word_list = list(jieba.cut(part, cut_all=False))
            else:
                word_list = part.split(" ")
            # add word into word_dict
            for word in word_list:
                if word not in word_dict:
                    word_dict[word] = 0
            # add word order into word_order dict
            for index1, word1 in enumerate(word_list):
                for word2 in word_list[index1+1:]:
                    combine = word1 + ">" + word2
                    if combine not in word_order_dict:
                        word_order_dict[combine] = 0
            try:
                memory_use_percent = yingshaoxo_text_completor.get_memory_info()["used_percent"]
                print("memory usage: ", memory_use_percent, "%")
                if memory_use_percent > 50:
                    break
            except Exception as e:
                print(e)

        print("in data saving...")
        disk.create_a_folder(order_dict_folder)
        with open(disk.join_paths(order_dict_folder, "word_dict.json"), "w") as f:
            f.write(json.dumps(word_dict, ensure_ascii=False))
        with open(disk.join_paths(order_dict_folder, "word_order_dict.json"), "w") as f:
            f.write(json.dumps(word_order_dict, ensure_ascii=False))
        print("word order dict generated.")

    def use_general_word_order_dict_to_get_sentence_correct_ratio(self, store_dict, order_dict_folder, input_text):
        try:
            if "jieba" in store_dict:
                jieba = store_dict["jieba"]
            else:
                import jieba
                jieba.setLogLevel(20)
                store_dict["jieba"] = jieba
            has_jieba = True
        except Exception as e:
            has_jieba = False

        if "word_dict" in store_dict:
            word_dict = store_dict["word_dict"]
        else:
            from auto_everything.disk import Disk
            disk = Disk()
            import json
            with open(disk.join_paths(order_dict_folder, "word_dict.json"), "r") as f:
                temp_text = f.read()
            word_dict = json.loads(temp_text)
            store_dict["word_dict"] = word_dict

        if "word_order_dict" in store_dict:
            word_order_dict = store_dict["word_order_dict"]
        else:
            from auto_everything.disk import Disk
            disk = Disk()
            import json
            with open(disk.join_paths(order_dict_folder, "word_order_dict.json"), "r") as f:
                temp_text = f.read()
            word_order_dict = json.loads(temp_text)
            store_dict["word_order_dict"] = word_order_dict

        if len(input_text.strip()) == 0:
            return 0

        all_counting = 0
        correct_counting = 0
        if has_jieba:
            word_list = list(jieba.cut(input_text, cut_all=False))
        else:
            word_list = input_text.split(" ")
        for index1, word1 in enumerate(word_list):
            for index2, word2 in enumerate(word_list[index1+1:]):
                all_counting += 1
                if (word1 in word_dict) and (word2 in word_dict):
                    combine = word1 + ">" + word2
                    if combine in word_order_dict:
                        correct_counting += 1

        if all_counting == 0:
            return 0
        return correct_counting / all_counting

    def get_simple_next_word_dict(self, source_text_list, simple_next_word_dict_folder):
        # this is useless, it is just a tool used to test the sentence checker, see if the checker can get right sentence from random input
        import json
        from auto_everything.disk import Disk
        disk = Disk()
        try:
            import jieba
            jieba.setLogLevel(20)
            has_jieba = True
        except Exception as e:
            has_jieba = False

        simple_next_word_dict = {}
        for part in source_text_list:
            part = part.strip()
            if has_jieba:
                word_list = list(jieba.cut(part, cut_all=False))
            else:
                word_list = part.split(" ")

            # add word into word_dict
            length = len(word_list) - 1
            for index, word in enumerate(word_list):
                if index < length:
                    next_word = word_list[index+1]
                    if word not in simple_next_word_dict:
                        simple_next_word_dict[word] = set([next_word])
                    else:
                        simple_next_word_dict[word].add(next_word)

            try:
                memory_use_percent = yingshaoxo_text_completor.get_memory_info()["used_percent"]
                print("memory usage: ", memory_use_percent, "%")
                if memory_use_percent > 50:
                    break
            except Exception as e:
                print(e)

        for key in simple_next_word_dict.keys():
            simple_next_word_dict[key] = list(simple_next_word_dict[key])

        print("in data saving...")
        disk.create_a_folder(simple_next_word_dict_folder)
        with open(disk.join_paths(simple_next_word_dict_folder, "simple_next_word_dict.json"), "w") as f:
            f.write(json.dumps(simple_next_word_dict, ensure_ascii=False))
        print("simple_next_word_dict generated.")

    def use_simple_next_word_dict_to_get_next_text(self, store_dict, simple_next_word_dict_folder, input_text, how_many_character_you_want=1):
        # this is useless, it is just a tool used to test the sentence checker, see if the checker can get right sentence from random input
        if len(input_text) == 0:
            return ""

        try:
            if "jieba" in store_dict:
                jieba = store_dict["jieba"]
            else:
                import jieba
                jieba.setLogLevel(20)
                store_dict["jieba"] = jieba
            has_jieba = True
        except Exception as e:
            has_jieba = False

        if "simple_next_word_dict" in store_dict:
            simple_next_word_dict = store_dict["simple_next_word_dict"]
        else:
            from auto_everything.disk import Disk
            disk = Disk()
            import json
            with open(disk.join_paths(simple_next_word_dict_folder, "simple_next_word_dict.json"), "r") as f:
                temp_text = f.read()
            simple_next_word_dict = json.loads(temp_text)
            store_dict["simple_next_word_dict"] = simple_next_word_dict

        response = ""
        while len(response) < how_many_character_you_want:
            if has_jieba:
                input_words = list(jieba.cut(input_text[-32:], cut_all=False))
            else:
                input_words = input_text[-32:].split(" ")
            temp_response = simple_next_word_dict.get(input_words[-1])
            if temp_response == None:
                break
            if len(temp_response) == 0:
                break
            temp_response = random.choice(temp_response)
            response += temp_response
            input_text += temp_response

        return response

    def get_memory_info(self):
        mem_info = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    mem_info[key.strip()] = value.strip()

        total = int(mem_info['MemTotal'].split()[0])
        free = int(mem_info['MemFree'].split()[0])
        available = int(mem_info['MemAvailable'].split()[0])

        used = total - free
        usage_percent = (used / total) * 100

        return {
            'total_kb': total,
            'free_kb': free,
            'used_kb': used,
            'used_mb': int(used/1024),
            'used_percent': round(usage_percent, 2)
        }

    def get_core_difference_dict(self, text_list, target_folder):
        # useless

        # what is the core difference for two previous_text -> same next char?
        # they have same chars with same order in previous_text
        # for example: ["mother, morning", "father, morning"] -> "morning!"
        # I did it wrong, I should use this tech to help to filter some previous context
        # previous_6_char -> [["background_common_keyword_in_previous_64_chars", next_1_char], ...]
        import json
        from auto_everything.disk import Disk
        disk = Disk()

        def get_common_char_string(string_1, string_2):
            if len(string_1) < len(string_2):
                string_a = string_1
                string_b = string_2
            else:
                string_a = string_2
                string_b = string_1
            common_char_string = ""
            for char in string_a:
                if char in string_b:
                    common_char_string += char
            if len(common_char_string) == 0:
                return None
            else:
                return common_char_string

        the_dict = {}
        counting = 0
        for text_part in text_list:
            try:
                counting += 1
                print(counting)
                length = len(text_part)
                for temp_level in [1,2,3,4]:
                    index = 0
                    while index+temp_level < length:
                        key_string = text_part[index:index+temp_level]
                        value_string = text_part[index+temp_level:index+temp_level+temp_level]
                        if temp_level == 1:
                            previous_string = text_part[index+temp_level-3:index+temp_level]
                        elif temp_level == 2:
                            previous_string = text_part[index+temp_level-9:index+temp_level]
                        elif temp_level == 3:
                            previous_string = text_part[index+temp_level-18:index+temp_level]
                        elif temp_level == 4:
                            previous_string = text_part[index+temp_level-64:index+temp_level]

                        if key_string not in the_dict:
                            the_dict[key_string] = [[previous_string, value_string]]
                        else:
                            did_changes = False
                            temp_list = the_dict[key_string]
                            for temp_index_1, one_list in enumerate(temp_list):
                                temp_background_common_keywords, next_1_char = one_list
                                if next_1_char == value_string:
                                    temp_result = get_common_char_string(previous_string, temp_background_common_keywords)
                                    if temp_result != None:
                                        the_dict[key_string][temp_index_1][0] = temp_result
                                        did_changes = True
                            if did_changes == False:
                                exists_in_list = False
                                for one_list in temp_list:
                                    _, next_1_char = one_list
                                    if next_1_char == value_string:
                                        exists_in_list = True
                                        break
                                if exists_in_list == False:
                                    the_dict[key_string].append([previous_string, value_string])
                        index += 1
            except KeyboardInterrupt:
                break

        print("in data saving...")
        disk.create_a_folder(target_folder)
        with open(disk.join_paths(target_folder, "core_difference_dict.json"), "w") as f:
            f.write(json.dumps(the_dict, indent=4, ensure_ascii=False))
        print("core_difference_dict generated.")

    def use_core_difference_dict_to_get_next_text(self, store_dict, core_difference_dict_folder, input_text, how_many_character_you_want=256, window_length=64, previous_text_length=2):
        # useless
        if len(input_text) == 0:
            return ""

        if "core_difference_dict" in store_dict:
            core_difference_dict = store_dict["core_difference_dict"]
        else:
            from auto_everything.disk import Disk
            disk = Disk()
            import json
            with open(disk.join_paths(core_difference_dict_folder, "core_difference_dict.json"), "r") as f:
                temp_text = f.read()
            core_difference_dict = json.loads(temp_text)
            store_dict["core_difference_dict"] = core_difference_dict

        def check_if_the_char_order_matchs(need_to_check_string, order_string):
            if len(need_to_check_string) == 0:
                return False
            if len(order_string) == 0:
                return False
            last_index = 0
            for char in order_string:
                index = need_to_check_string.find(char, last_index)
                if index == -1:
                    return False
                if index < last_index:
                    return False
                last_index = index
            return True

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = None

            global_found = False
            for previous_text_length in [4,3,2,1]:
                temp_input = input_text[-previous_text_length:]

                the_current_background_text = ""
                if previous_text_length == 1:
                    the_current_background_text = input_text[-3:]
                elif previous_text_length == 2:
                    the_current_background_text = input_text[-9:]
                elif previous_text_length == 3:
                    the_current_background_text = input_text[-18:]
                elif previous_text_length == 4:
                    the_current_background_text = input_text[-64:]

                if the_current_background_text != "":
                    temp_set_1 = set(list(the_current_background_text))
                else:
                    temp_set_1 = set()

                possibility_list = core_difference_dict.get(temp_input)
                if possibility_list == None:
                    continue

                found = False
                max_score = -1
                random_list = []
                for one_list in possibility_list:
                    temp_background_common_keywords, next_1_char = one_list
                    if temp_background_common_keywords == "":
                        random_list.append(next_1_char)
                        continue
                    temp_set_2 = set(list(temp_background_common_keywords))
                    common_set = temp_set_1.intersection(temp_set_2)
                    if len(common_set) > 0:
                        if list(common_set)[0] != "":
                            if check_if_the_char_order_matchs(the_current_background_text, temp_background_common_keywords):
                                if len(common_set) > max_score:
                                    found = True
                                    temp_response = next_1_char
                                    max_score = len(common_set)
                                    global_found = True
                                    print("not random")
                if found == False and len(random_list) != 0:
                    temp_response = random.choice(random_list)
                    global_found = True
                    print("random")
                if temp_response == None:
                    continue
                if len(temp_response.strip()) == 0:
                    continue

                if global_found == True:
                    break

            if temp_response == None:
                break
            response += temp_response
            input_text += temp_response

        return response

if __name__ == "__main__":
    import jieba
    jieba.setLogLevel(20)

    #train = True
    train = False

    yingshaoxo_text_completor = Yingshaoxo_Text_Completor()
    store_dict = dict()

    def get_source_text_data(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return text
    #source_text = get_source_text_data("/home/yingshaoxo/CS/yingshaoxo_txt_data/all_yingshaoxo_data_2023_11_13.txt")
    #source_text = get_source_text_data("/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Big_Core/General_Book/wiki_encyclopedia/primary_student_article_15000.txt")
    #text_list = source_text.split("__**__**__yingshaoxo_is_the_top_one__**__**__")
    #yingshaoxo_text_completor.get_core_difference_dict(text_list, "./test_dict/4.core_difference_dict")
    #exit()

    #source_text = get_source_text_data("/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Big_Core/General_Book/wiki_encyclopedia/primary_student_article_15000.txt")
    #source_text = get_source_text_data("/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Ebooks/wiki_articles/baidu_wiki_2012.txt")
    #source_text = get_source_text_data("/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Big_Core/General_Book/wiki_encyclopedia/simplified_zh_wiki_2022.txt")

    if train == True:
        #folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Code_Mini"
        #folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Ebooks/Chinese/chinese_sex_novels"
        #folder = "/home/yingshaoxo/Downloads/doing/16.百科词典研究"

        #source_text = yingshaoxo_text_completor.get_all_files_txt_under_a_folder(folder)
        #source_text = source_text.replace("\n", "").replace(" ", "").replace("　","")
        text_list = source_text.split("__**__**__yingshaoxo_is_the_top_one__**__**__")

        yingshaoxo_text_completor.get_general_word_order_dict(text_list, "./test_dict/1.word_order_dict")
        exit()

        text_list = [list(jieba.cut(one, cut_all=False)) for one in text_list]
        yingshaoxo_text_completor.get_simplified_magic_language_tree_dict_from_text_list(store_dict, "./test_dict/2.simple_tree", text_list, window_length=4)

        exit()

    while True:
        try:
            input_text = input("What you want to say: ")
            if input_text == "":
                input_text = "你知道你智力的来源吗？"

            #response = yingshaoxo_text_completor.get_next_text_by_pure_text(source_text, input_text, how_many_character_you_want=300, level=64, complete_how_many_character_for_each_time=None, use_background=False)
            #response = yingshaoxo_text_completor.pattern_looking(source_text, input_text)
            #response = yingshaoxo_text_completor.search_long_background_context_by_using_keywords(source_text, input_text)#, keyword_list=list(jieba.cut(input_text, cut_all=False)))

            #response = yingshaoxo_text_completor.find_next_string_in_disk_txt_file("/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Big_Core/General_Book/wiki_encyclopedia/primary_student_article_15000.txt", input_text, get_previous_text=True)
            #response = yingshaoxo_text_completor.search_relative_data_from_disk_txt_file_by_using_keywords("/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Big_Core/General_Book/wiki_encyclopedia/primary_student_article_15000.txt", input_text, return_list=True)
            #response = "\n\n__________\n\n".join(response[:10])
            #response = yingshaoxo_text_completor.use_simplified_magic_language_tree_dict_to_get_next_text(store_dict, "./test_dict/2.simple_tree", list(input_text_list), how_many_character_you_want=2, no_sleep=True, window_length=4)

            #source_text_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Additional/Ebooks/wiki_articles/baidu_wiki_2012.txt"
            #source_text_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Big_Core/General_Book/wiki_encyclopedia/simplified_zh_wiki_2022.txt"
            #source_text_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Big_Core/General_Book/wiki_encyclopedia/primary_student_article_15000.txt"
            #source_text_path = "/home/yingshaoxo/CS/yingshaoxo_txt_data/all_yingshaoxo_data_2023_11_13.txt"
            source_text_path = "/home/yingshaoxo/CS/yingshaoxo_txt_data/yingshaoxo/temporary_memory.txt"
            response = yingshaoxo_text_completor.search_long_background_context_from_disk_txt_file_by_using_multiprocess(source_text_path, input_text, return_text=True, get_more=True)
            print(response)
            #tree_dict = yingshaoxo_text_completor.get_magic_language_tree_dict_from_text(response[:50000])
            #response = yingshaoxo_text_completor.use_magic_language_tree_dict_to_generate_next_string(tree_dict, input_text, window_length=6)

            if response:
                response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0]
                #print("\n\nComputer: \n" + input_text + response)
                #print("\n\nComputer: \n" + response)
                print("\n\n")
        except KeyboardInterrupt:
            print("\n")
            continue
