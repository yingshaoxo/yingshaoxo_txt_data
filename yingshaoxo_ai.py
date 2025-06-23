import os
from random import choice
import json

#from yingshaoxo_python import run_python_code
from auto_everything.terminal import Terminal
terminal = Terminal()

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
    return thinking_list, thinking_dataset_text

def get_title_version_of_thinking_list(a_thinking_list):
    new_list = []
    for one in a_thinking_list:
        lines = one.strip().split("\n")
        if len(lines) > 0:
            new_list.append(lines[0])
        else:
            new_list.append("")
    return new_list

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

def get_sub_sentence_list_from_end_to_begin_and_begin_to_end(input_text, no_single_char=True):
    input_text = input_text.strip()
    full_length = len(input_text)
    result_list = []
    for i in range(full_length):
        end_to_begin_sub_string = input_text[i:]
        begin_to_end_sub_string = input_text[:-i]
        if no_single_char == True:
            if len(end_to_begin_sub_string) > 1:
                result_list.append(end_to_begin_sub_string)
            if len(begin_to_end_sub_string) > 1:
                result_list.append(begin_to_end_sub_string)
        else:
            result_list.append(end_to_begin_sub_string)
            result_list.append(begin_to_end_sub_string)
    result_list_2 = []
    for one in result_list:
        if one not in result_list_2:
            result_list_2.append(one)
    return result_list_2

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
    longest_first_sub_sentence_list = get_sub_sentence_list_from_end_to_begin_and_begin_to_end(search_text)
    useful_source_text_list = []
    for sub_sentence in longest_first_sub_sentence_list:
        for index, one in enumerate(source_text_list):
            if sub_sentence in one:
                useful_source_text_list.append(index)
        if len(useful_source_text_list) != 0:
            return useful_source_text_list

    return []

yingshaoxo_diary_path = "./all_yingshaoxo_data_2023_11_13.txt"
memory_dict_path = "./yingshaoxo_memory.json"
thinking_dataset_path = "./yingshaoxo_thinking_dataset.txt"
yingshaoxo_diary_list, _ = read_text_list_from_yingshaoxo_diary(yingshaoxo_diary_path)
yingshaoxo_memory_dict = load_dict_from_json(memory_dict_path)
yingshaoxo_thinking_list, _ = read_yingshaoxo_thinking_list(thinking_dataset_path)
yingshaoxo_thinking_list_for_title = get_title_version_of_thinking_list(yingshaoxo_thinking_list)

def save_yingshaoxo_memory():
    #del yingshaoxo_memory_dict["temporary_memory"]
    save_dict_to_json(yingshaoxo_memory_dict, memory_dict_path)
    #print("yingshaoxo memory dict saved.")

def get_a_random_thinking_from_input(input_text):
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
            one_random_relative_thinking_block = get_a_random_thinking_from_input(calling_content)
            one_line_result = run_a_piece_of_thinking(one_random_relative_thinking_block, no_pre_process=True, no_debug_info=True)
            a_line_indent = a_line[:(len(a_line) - len(a_line.lstrip()))]
            new_piece_of_thinking += a_line_indent + key + " = '''" + one_line_result + "'''" + "\n"
        else:
            new_piece_of_thinking += a_line + "\n"
        line_index += 1
    return new_piece_of_thinking.strip()

def run_a_piece_of_thinking(a_piece_of_thinking, no_pre_process=False, no_debug_info=False):
    global yingshaoxo_memory_dict

    if no_pre_process == False:
        a_piece_of_thinking = pre_process_piece_of_thinking(a_piece_of_thinking)

    mixed_code = ""
    memory_line = "yingshaoxo_memory_dict = {}".format(str(yingshaoxo_memory_dict))
    mixed_code += memory_line + "\n"

    if no_debug_info == False:
        mixed_code += """
print("Question:", yingshaoxo_memory_dict["temporary_memory"]["current_person_say"])
print("Relative_diary_list length ==", len(yingshaoxo_memory_dict["temporary_memory"]["relative_diary_list"]))
print("\\n")
\n
"""

    mixed_code += a_piece_of_thinking
    mixed_code += """
print("\\n\\nTo system, memory updated:")
print(str(yingshaoxo_memory_dict))
"""
    result = terminal.run_python_code(code=mixed_code).strip()

    try:
        # try to save modified memory
        a_list = result.split("\n")
        if len(a_list) >= 2:
            if "To system, memory updated:" in a_list[-2]:
                new_memory_dict = eval(a_list[-1])
                #print(new_memory_dict)
                yingshaoxo_memory_dict = new_memory_dict
                result = "\n".join(a_list[:-2])
    except Exception as e:
        print(e)
        pass

    return result.strip()

def ask_yingshaoxo_ai(input_text):
    relative_diary_list = search_text_in_text_list(input_text, yingshaoxo_diary_list)
    one_random_diary = ""
    if len(relative_diary_list) == 0:
        one_random_diary = ""
    else:
        one_random_diary = choice(relative_diary_list)

    yingshaoxo_memory_dict["temporary_memory"]["current_person_say"] = input_text
    yingshaoxo_memory_dict["temporary_memory"]["relative_diary_list"] = relative_diary_list
    yingshaoxo_memory_dict["temporary_memory"]["one_random_diary"] = one_random_diary

    try:
        one_random_relative_thinking_block = get_a_random_thinking_from_input(input_text)
        result = run_a_piece_of_thinking(one_random_relative_thinking_block)

        if result == None or result == "":
            return one_random_diary

        #save_yingshaoxo_memory()
        return result
    except Exception as e:
        print(e)
        return one_random_diary

def talk_with_yingshaoxo_ai():
    #global yingshaoxo_memory_dict
    #yingshaoxo_memory_dict["temporary_memory"] = {}
    while True:
        print("\n\n\n------------\n\n\n")
        input_text = input("What you want to talk? (你想说什么) ")
        response = ask_yingshaoxo_ai(input_text)
        print(response)
        save_yingshaoxo_memory()

if __name__ == "__main__":
    talk_with_yingshaoxo_ai()
