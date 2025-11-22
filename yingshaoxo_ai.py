# -*- coding: utf-8 -*-
"""
yingshaoxo after one month of development: In my thinking, in all current task, it will only last for 5 or 10 history chat message. I mean I should use last 10 chat history to determine if now is in making_love mode or other mode. Sometimes it can be other mode, for example, feel_sad mode. This is just a big picture. Sometimes a variable in temporary_memory will also effects the response, for example, if memory["is_girlfriend"]==True, it will say something differently.
"""
"""
Just think about this:

example: hi, mom! -> hi, kid!
actually it is: [*greeting*], [*to_name*]! -> [*greeting*], [*from_name*]!

You could in the end do coding like: input_text.human_format(greeting=random.choice(language.greeting), from_name="you")
"""

import os
import sys
from random import choice
import json

#from yingshaoxo_python import run_python_code
if os.path.exists("./yingshaoxo_txt_data"):
    sys.path.insert(1, "./yingshaoxo_txt_data")
try:
    from auto_everything.disk import Store
    from auto_everything.python import Python
    local_storage = Store("yingshaoxo_ai")
    python = Python()
    global_mini_python_variable_dict = {
        "local_storage": local_storage
    }
    mini_python = python.create_mini_python(global_mini_python_variable_dict)

    from auto_everything.string_ import String
    yingshaoxo_string = String()
except Exception as e:
    print(e)
    print("clone a folder to current folder: https://github.com/yingshaoxo/auto_everything/tree/dev/auto_everything")
    print("It is a folder inside of that repository.")
    print("""
auto_everything/
├── all.py
├── http_.py
├── ...
├── terminal.py
""")
    exit()

from yingshaoxo.main import ask_yingshaoxo_ai as have_memory_version_of_ask_yingshaoxo_ai


def read_text_list_and_text_from_folder(the_folder_path):
    def read_text_files(folder_path):
        new_text = ""
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.txt', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            new_text += f.read() + "\n\n\n\n"
                    except UnicodeDecodeError:
                        try:
                            with open(file_path, 'r', encoding='latin-1') as f:
                                new_text += f.read() + "\n\n\n\n"
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
        return new_text

    new_text = read_text_files(the_folder_path)
    the_text_list = [one.strip() for one in new_text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n") if one.strip() != ""]
    new_text_list = []
    for one in the_text_list:
        temp_list1 = one.split("\n# ")
        temp_list2 = []
        for sub_one in temp_list1:
            if "\n第" in sub_one and "章 " in sub_one:
                temp_list2 += sub_one.split("\n\n\n")
            else:
                temp_list2 += [sub_one]
        new_text_list += temp_list2
    the_text_list = new_text_list
    new_text = "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n".join(the_text_list)
    return the_text_list, new_text

def read_text_list_from_yingshaoxo_diary(diary_path):
    with open(diary_path, "r", encoding="utf-8") as f:
        text = f.read()
    the_text_list = [one.strip() for one in text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n") if one.strip() != ""]
    return the_text_list, text

def read_yingshaoxo_thinking_list(thinking_dataset_path):
    with open(thinking_dataset_path, "r", encoding="utf-8") as f:
        thinking_dataset_text = f.read()
    thinking_list = [one.strip() for one in thinking_dataset_text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n") if one.strip() != ""]
    # to make sure it uses older thinking before young thinking
    thinking_list.reverse()
    return thinking_list, thinking_dataset_text

def get_title_version_of_thinking_list(a_thinking_list):
    simple_list = []
    for one in a_thinking_list:
        if not (one.strip().startswith('"""')):
            lines = one.strip().split("\n")
            if len(lines) > 0:
                a_line = lines[0]
                if a_line.startswith("#"):
                    a_line = a_line[1:]
                simple_list.append(a_line)
            else:
                simple_list.append("")
        else:
            simple_list.append("")

    complex_list = []
    for one in a_thinking_list:
        if (one.strip().startswith('"""')) and (one.count('"""') >= 2):
            # read code inside """ """ as python code filter, or regex_similar python code, if that code return True, means it matchs this thinking piece.
            the_filter_code = one.split('"""')[1]
            if 'input_text = ""' in the_filter_code:
                complex_list.append(the_filter_code)
            else:
                complex_list.append("")
        else:
            complex_list.append("")

    return simple_list, complex_list

def save_dict_to_json(a_dict, filename="yingshaoxo_memory.json"):
    text = json.dumps(a_dict, indent=4)
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(text)

def load_dict_from_json(filename="yingshaoxo_memory.json"):
    if not os.path.exists(filename):
        save_dict_to_json({}, filename=filename)
        return load_dict_from_json(filename=filename)
    with open(filename, 'r', encoding="utf-8") as f:
        text = f.read()
    json_dict = json.loads(text)
    return json_dict

def get_sub_sentence_list_from_end_to_begin_and_begin_to_end(input_text, no_single_char=True, char_limit=True):
    input_text = input_text.strip()
    full_length = len(input_text)
    if char_limit == True:
        char_limit_number = int(full_length / 2)
    else:
        char_limit_number = 1
    result_list = []
    for i in range(full_length):
        end_to_begin_sub_string = input_text[i:]
        begin_to_end_sub_string = input_text[:-i]
        if no_single_char == True:
            if len(end_to_begin_sub_string) > char_limit_number:
                result_list.append(end_to_begin_sub_string)
            if len(begin_to_end_sub_string) > char_limit_number:
                result_list.append(begin_to_end_sub_string)
        else:
            result_list.append(end_to_begin_sub_string)
            result_list.append(begin_to_end_sub_string)
    result_list_2 = []
    for one in result_list:
        if one not in result_list_2:
            result_list_2.append(one)
    return result_list_2

def is_ascii(input_text):
    if not isinstance(input_text, str):
        return False
    try:
        input_text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def should_we_use_hard_search_method(input_text):
    keyword_list = input_text.split(" ")
    has_non_english_inside = False
    for keyword in keyword_list:
        if not is_ascii(keyword):
            has_non_english_inside = True
            break
    if has_non_english_inside == True:
        return True
    else:
        return False

def split_string_by_characters(input_text, splitors):
    result_list = [input_text]
    for splitor in list(splitors):
        new_result_list = []
        for one in result_list:
            new_result_list += one.split(splitor)
        result_list = new_result_list
    return result_list

def hard_search_text_in_text_list(keyword_string_that_should_be_split_by_space, source_text_list):
    keyword_string_that_should_be_split_by_space = keyword_string_that_should_be_split_by_space.strip()

    if "|" in keyword_string_that_should_be_split_by_space:
        keyword_list = keyword_string_that_should_be_split_by_space.split("|")
    else:
        if should_we_use_hard_search_method(keyword_string_that_should_be_split_by_space):
            # chinese, we split by space
            keyword_list = split_string_by_characters(keyword_string_that_should_be_split_by_space, " ,.?!;:，。？！\n")
        else:
            # english, we use all string
            keyword_list = split_string_by_characters(keyword_string_that_should_be_split_by_space, ",.?!;:，。？！\n")

    keyword_list = [one.strip() for one in keyword_list if one.strip() != ""]

    result_list = []
    for one in source_text_list:
        ok = True
        for keyword in keyword_list:
            if keyword not in one:
                ok = False
                break
        if ok == True:
            result_list.append(one)
    return result_list

def search_text_in_text_list(search_text, source_text_list):
    longest_first_sub_sentence_list = get_sub_sentence_list_from_end_to_begin_and_begin_to_end(search_text)
    useful_source_text_list = []
    for sub_sentence in longest_first_sub_sentence_list:
        for one in source_text_list:
            if sub_sentence in one:
                useful_source_text_list.append(one)
        if len(useful_source_text_list) != 0:
            return useful_source_text_list

    return []

def search_text_in_text_list_to_get_their_index_list(search_text, source_text_list):
    keywords = yingshaoxo_string.get_keywords_list(search_text)
    matched_list = []
    for index, text in enumerate(source_text_list):
        if yingshaoxo_string.check_if_string_is_inside_string(text, keywords, wrong_limit_ratio=0.2, near_distance=20):
            matched_list.append(index)
    return matched_list


resource_basic_folder_path = os.path.dirname(os.path.abspath(__file__))
yingshaoxo_diary_path = os.path.join(resource_basic_folder_path, "./all_yingshaoxo_data_2023_11_13.txt")
thinking_dataset_path = os.path.join(resource_basic_folder_path, "./yingshaoxo_thinking_dataset.txt")

yingshaoxo_diary_list, _ = read_text_list_from_yingshaoxo_diary(yingshaoxo_diary_path)
yingshaoxo_thinking_list, _ = read_yingshaoxo_thinking_list(thinking_dataset_path)
yingshaoxo_thinking_list_for_title, yingshaoxo_complex_thinking_list_for_title = get_title_version_of_thinking_list(yingshaoxo_thinking_list)

def inject_yingshaoxo_memory_into_code(some_code):
    global yingshaoxo_memory_dict

    mixed_code = ""
    mixed_code += """
# -*- coding: utf-8 -*-

try:
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except Exception as e:
    #print(e)
    pass

"""
    mixed_code += some_code
    return mixed_code

def get_complex_thinking_from_input(input_text):
    def get_index_list_from_complex_thinking_title(a_input_text, the_python_code_list):
        the_index_list = []
        for index, python_code in enumerate(the_python_code_list):
            if python_code.strip() == "":
                continue
            else:
                lines = python_code.split("\n")
                new_lines = []
                for line in lines:
                    if 'input_text = ""' in line:
                        new_lines.append('input_text = ' + json.dumps(a_input_text))
                    else:
                        new_lines.append(line)
                new_python_code = "\n".join(new_lines)
                new_python_code = inject_yingshaoxo_memory_into_code(new_python_code)
                result = mini_python.run_code(code=new_python_code).strip()
                if "True" in result and "error" not in result.lower():
                    the_index_list.append(index)
        return the_index_list

    sub_list_of_thinking_list_index = get_index_list_from_complex_thinking_title(input_text, yingshaoxo_complex_thinking_list_for_title)
    if len(sub_list_of_thinking_list_index) == 0:
        return None

    sub_list_of_thinking_list = []
    for index in sub_list_of_thinking_list_index:
        sub_list_of_thinking_list.append(yingshaoxo_thinking_list[index])
    one_random_thinking_block = choice(sub_list_of_thinking_list)
    return one_random_thinking_block.strip()

def get_a_thinking_based_on_input(input_text):
    the_thinking = get_complex_thinking_from_input(input_text)
    if the_thinking != None:
        return the_thinking

    sub_list_of_thinking_list_index = search_text_in_text_list_to_get_their_index_list(input_text, yingshaoxo_thinking_list_for_title)
    sub_list_of_thinking_list = []
    for index in sub_list_of_thinking_list_index:
        sub_list_of_thinking_list.append(yingshaoxo_thinking_list[index])

    if len(sub_list_of_thinking_list) == 0:
        return None
    one_random_thinking_block = choice(sub_list_of_thinking_list)
    return one_random_thinking_block.strip()

def pre_process_piece_of_thinking(a_piece_of_thinking):
    lines = a_piece_of_thinking.split("\n")
    new_piece_of_thinking = ""
    line_index = 0
    while line_index < len(lines):
        a_line = lines[line_index]
        a_line_pure = a_line.strip()
        if (" = " in a_line_pure) and ('call_yingshaoxo("' in a_line_pure) and (a_line_pure.endswith('")')):
            key, value = a_line_pure.split(" = ")
            key, value = key.strip(), value.strip()
            calling_content = value[len('call_yingshaoxo("'):-2]
            one_relative_thinking_block = get_a_thinking_based_on_input(calling_content)
            one_line_result = run_a_piece_of_thinking(one_relative_thinking_block, no_pre_process=True, no_debug_info=True, input_text=calling_content)
            a_line_indent = a_line[:(len(a_line) - len(a_line.lstrip()))]
            new_piece_of_thinking += a_line_indent + key + " = '''" + one_line_result + "'''" + "\n"
        elif (" = " in a_line_pure) and ('search_yingshaoxo_diary(' in a_line_pure) and (a_line_pure.endswith(')')):
            # this method still has problem, it should get running in runtime than pre_process
            key, value = a_line_pure.split(" = ")
            key, value = key.strip(), value.strip()
            search_content = value[len('search_yingshaoxo_diary('):-1]
            search_content = eval(search_content)
            result_content = "I don't know."
            for one_diary in yingshaoxo_diary_list:
                temp_result_list = yingshaoxo_string.hard_core_string_pattern_search(one_diary, search_content, end_mark="__**__**__")
                if len(temp_result_list) != 0:
                    result_content = temp_result_list[0]
                    break
            a_line_indent = a_line[:(len(a_line) - len(a_line.lstrip()))]
            new_piece_of_thinking += a_line_indent + key + " = '''" + result_content + "'''" + "\n"
        else:
            new_piece_of_thinking += a_line + "\n"
        line_index += 1
    return new_piece_of_thinking.strip()

def run_a_piece_of_thinking(a_piece_of_thinking, no_pre_process=False, no_debug_info=False, input_text=None):
    global yingshaoxo_memory_dict

    result = ""
    if a_piece_of_thinking == None:
        return result

    if no_pre_process == False:
        a_piece_of_thinking = pre_process_piece_of_thinking(a_piece_of_thinking)

    mixed_code = ""
    mixed_code = inject_yingshaoxo_memory_into_code(mixed_code)
    if input_text != None:
        mixed_code += "\n" + "input_text='''{}'''".format(input_text)

    if no_debug_info == False:
        mixed_code += """
print("Question:", local_storage.get("input_text", ""))
print("\\n")
\n
""".format(input_text=local_storage.get("input_text", ""))
    else:
        mixed_code += """
\n
"""

    mixed_code += a_piece_of_thinking

    result = mini_python.run_code(code=mixed_code).strip()

    return result.strip()

def mixed_result(input_text, *response_list):
    response_list = list(response_list)

    hard_search_result_list = hard_search_text_in_text_list(input_text, yingshaoxo_diary_list)
    if len(hard_search_result_list) != 0:
        hard_search_result = choice(hard_search_result_list)
    else:
        hard_search_result = None

    if (hard_search_result):
        response_list = [hard_search_result] + response_list

    new_response_list = []
    for one in response_list:
        one = one.strip()
        if one not in new_response_list:
            new_response_list.append(one)

    return "\n\n\n-------\n\n\n".join(new_response_list)

def ask_yingshaoxo_ai(input_text, no_debug_info=True):
    input_text = input_text.lower().strip()

    local_storage.set("input_text", input_text)
    local_storage.set("chat_history", input_text)

    simple_input_text = yingshaoxo_string.question_sentence_to_normal_sentence(input_text)
    relative_diary_list = search_text_in_text_list(simple_input_text, yingshaoxo_diary_list)
    one_relative_random_diary = ""
    if len(relative_diary_list) == 0:
        one_relative_random_diary = ""
    else:
        one_relative_random_diary = choice(relative_diary_list)

    try:
        one_relative_thinking_block = get_a_thinking_based_on_input(input_text)
        result = run_a_piece_of_thinking(one_relative_thinking_block, no_debug_info=no_debug_info, input_text=input_text)

        chat_history = local_storage.get("chat_history", "")
        chat_history += "\n-*-\n" + input_text
        chat_history = chat_history[-2048:]
        local_storage.set("chat_history", chat_history)

        if result == "":
            return mixed_result(input_text, one_relative_random_diary)

        return mixed_result(input_text, result)
    except Exception as e:
        print("Error when run 'ask_yingshaoxo_ai'", e)
        return mixed_result(input_text, one_relative_random_diary)

def talk_with_yingshaoxo_ai():
    while True:
        print("\n\n\n------------\n\n\n")
        input_text = input("What you want to talk? ")
        response = ask_yingshaoxo_ai(input_text, no_debug_info=True)
        response2 = have_memory_version_of_ask_yingshaoxo_ai(input_text)
        if response.strip() == "":
            response = response2
        print("\n\n")
        print(response)

if __name__ == "__main__":
    talk_with_yingshaoxo_ai()
