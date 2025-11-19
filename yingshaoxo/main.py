# todo: need to find out why it will stuck at some times
import os
import inspect
import random

from small_functions import *
from ask_other_ai_help import ask_llama

debug = 1
yingshaoxo_diary_file_path = os.path.abspath("../all_yingshaoxo_data_2023_11_13.txt")
magic_splitor = "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n"
temporary_memory_file_path = os.path.abspath("./temporary_memory.txt")
with open(temporary_memory_file_path, "a", encoding="utf-8") as f:
    f.write("")
chat_history_list = []

def get_keywords_list(input_text):
    if input_text.isascii():
        keyword_list = yingshaoxo_string.split_string_into_n_char_parts(input_text, 4)
    else:
        #keyword_list = yingshaoxo_string.split_string_into_n_char_parts(input_text, 2)
        keyword_list = list(input_text)
    return keyword_list

def get_memory_piece_list_from_txt_file(a_txt_path, input_text, accurate=True, wrong_limit_ratio=0.05):
    if accurate == True:
        get_more = False
    else:
        get_more = True

    size = yingshaoxo_disk.get_file_size(a_txt_path, level="MB", bytes_size=None)
    if size > 10:
        memory_list = yingshaoxo_text_completor.search_long_background_context_from_disk_txt_file_by_using_multiprocess(a_txt_path, input_text, return_text=False, get_more=get_more)
    else:
        with open(a_txt_path, "r", encoding="utf-8") as f:
            source_text = f.read()
        text_list = source_text.split(magic_splitor)
        text_list.reverse()

        keyword_list = get_keywords_list(input_text)

        if get_more == False:
            matched_list = []
            for text in text_list:
                if yingshaoxo_string.check_if_string_is_inside_string(text, keyword_list, wrong_limit_ratio=0.5, near_distance=None):
                    if len(yingshaoxo_string.get_relate_sub_string_in_long_string(text, keyword_list, wrong_limit_ratio=wrong_limit_ratio, window_length=None, return_number=1, include_only_one_line=False, include_previous_and_next_one_line=False)) != 0:
                        matched_list.append(text)
        else:
            dynamic_control_number = 2
            matched_list = []
            ratio_kernel = 0.05
            ratio = 0
            steps = int(wrong_limit_ratio/ratio_kernel)
            for _ in range(steps + 1):
                matched_list = []
                for text in text_list:
                    if yingshaoxo_string.check_if_string_is_inside_string(text, keyword_list, wrong_limit_ratio=ratio, near_distance=20):
                        matched_list.append(text)
                if len(matched_list) >= dynamic_control_number:
                    break
                ratio = ratio + ratio_kernel
        memory_list = matched_list

    return memory_list

def get_memory_as_pure_string(input_text, include_diary=False):
    memory_piece_list = get_memory_piece_list_from_txt_file(yingshaoxo_diary_file_path, input_text, accurate=True, wrong_limit_ratio=0.1)
    if len(memory_piece_list) == 0:
        new_input_text = question_sentence_to_normal_sentence(input_text)
        memory_piece_list = get_memory_piece_list_from_txt_file(yingshaoxo_diary_file_path, new_input_text, accurate=True, wrong_limit_ratio=0.1)
    if len(memory_piece_list) > 0:
        one_diary_memory_piece = random.choice(memory_piece_list)
        one_diary_memory_piece = one_diary_memory_piece[:1024]
    else:
        one_diary_memory_piece = 'None'

    memory_piece_list = get_memory_piece_list_from_txt_file(temporary_memory_file_path, input_text, accurate=True, wrong_limit_ratio=0.2)
    if len(memory_piece_list) == 0:
        new_input_text = question_sentence_to_normal_sentence(input_text)
        memory_piece_list = get_memory_piece_list_from_txt_file(temporary_memory_file_path, new_input_text, accurate=True, wrong_limit_ratio=0.5)
    if len(memory_piece_list) > 0:
        one_normal_memory_piece = random.choice(memory_piece_list)
    else:
        one_normal_memory_piece = 'None'

    final_memory = ""

    final_memory += "In recent memory:\n" + make_indents_before_every_lines(one_normal_memory_piece.strip(), 4, as_code_block=True)

    last_message = get_last_chat_message()
    if last_message == "":
        last_message = "None"
    final_memory += "\n\n" + "Last chat message:\n" + make_indents_before_every_lines(last_message, 4, as_code_block=True)

    if include_diary == True:
        final_memory += "\n\n" + "In yingshaoxo diary (yingshaoxo is a teacher, we use it as knowledge base):\n" + make_indents_before_every_lines(one_diary_memory_piece.strip(), 4, as_code_block=True)

    final_memory = final_memory.replace(magic_splitor, "")
    return final_memory

def is_it_in_memory(input_text, id_):
    if input_text == None:
        return False
    if len(input_text) == "":
        return False
    memory_piece_list = get_memory_piece_list_from_txt_file(temporary_memory_file_path, input_text, accurate=True, wrong_limit_ratio=0.5)
    if len(memory_piece_list) == 0:
        return False
    else:
        return True

def get_last_chat_message(id_=None):
    global chat_history_list
    if len(chat_history_list) == 0:
        return ""
    return chat_history_list[-1]

def add_last_chat_message(input_text, id_=None):
    global chat_history_list
    chat_history_list.append(input_text.strip())
    if len(chat_history_list) > 500:
        chat_history_list = chat_history_list[-500:]

def ask_other_ai(input_text):
    input_text = input_text.strip()
    if input_text.startswith("is_it_"):
        input_text += "\n" + "#no other explain needed, just return the 'true' or 'false'"
    else:
        #input_text += "\n" + "#no other explain needed, just return the new data"
        pass
    try:
        response = ask_llama(input_text)
        response = response.split("\n")
        response = response[:6]
        response = "\n".join(response)

        if debug == 1:
            print(make_indents_before_every_lines("Ask other ai:\n" + make_indents_before_every_lines(input_text, 4, as_code_block=True), 4, as_code_block=True))

        return response
    except Exception as e:
        return ask_yingshaoxo_ai(input_text)
        #response = get_memory_as_pure_string(input_text, include_diary=True)
        #return response + "\n\n" + "I don't know."

def what_is_the_task(input_text, id_):
    input_text = input_text.lower()
    all_in_all = str(input_text)
    for input_text in all_in_all.split("\n"):
        input_text = input_text.strip()
        if len(input_text) == 0:
            continue
        if ("你" in input_text) and ("？" in input_text):
            found_index = input_text.find("你")
            found_index2 = input_text.find("？", found_index)
            related_to_me = input_text[found_index:found_index2+1]
            input_text = related_to_me
            input_text = question_sentence_to_normal_sentence(input_text)
            return "get memory", input_text.strip()

        if ("you" in input_text) and ("?" in input_text):
            found_index = input_text.find("you")
            found_index2 = input_text.find("?", found_index)
            related_to_me = input_text[found_index:found_index2+1]
            input_text = related_to_me
            input_text = question_sentence_to_normal_sentence(input_text)
            return "get memory", input_text.strip()

        if ("what " in input_text) and ("?" in input_text):
            found_index = input_text.find("what ")
            found_index2 = input_text.find("?", found_index)
            the_question = input_text[found_index:found_index2+1]
            input_text = question_sentence_to_normal_sentence(input_text)
            return "get memory", input_text.strip()

        if (input_text.endswith("?") or input_text.endswith("？")):
            input_text = question_sentence_to_normal_sentence(input_text)
            return "get memory", input_text.strip()

        if ("你" in input_text) and ("。" in input_text):
            found_index = input_text.find("你")
            found_index2 = input_text.find("。", found_index)
            related_to_me = input_text[found_index:found_index2+1]
            input_text = related_to_me
            return "remember a thing", input_text.strip()

        if (("you " in input_text) or "your " in input_text) and ("." in input_text):
            if "you " in input_text:
                found_index = input_text.find("you ")
                found_index2 = input_text.find(".", found_index)
                related_to_me = input_text[found_index:found_index2+1]
                input_text = related_to_me
                return "remember a thing", input_text.strip()
            if "your " in input_text:
                found_index = input_text.find("your ")
                found_index2 = input_text.find(".", found_index)
                related_to_me = input_text[found_index:found_index2+1]
                input_text = related_to_me
                return "remember a thing", input_text.strip()

    return "unknown", input_text

def finish_a_task(task_name, input_text, id_):
    if len(input_text) == 0:
        return "I don't know."

    if debug == 1:
        print(make_indents_before_every_lines("task name: " + task_name + "\n" + "input_text: " + input_text, 4, as_code_block=True))

    if task_name == "remember a thing":
        old_memory = get_memory_as_pure_string(input_text, include_diary=False)
        if input_text not in old_memory:
            remember(input_text, "just remember.", id_, force=True)
            return "remembered: " + replace_your_to_my(input_text)
        else:
            return "not remembered because I have it in memory: " + replace_your_to_my(input_text)
    elif task_name == "get memory":
        response = get_memory_as_pure_string(input_text, include_diary=True)
        keyword_list = get_keywords_list(input_text)
        relative_line_list = yingshaoxo_string.get_relate_sub_string_in_long_string(response, keyword_list, wrong_limit_ratio=0.4, window_length=int(len(input_text) * 2), return_number=1, include_only_one_line=False, include_previous_and_next_one_line=False, only_return_one_sentence=True)
        if len(relative_line_list) != 0:# and len(relative_line_list[0]) >= len(input_text):
            # find a way to look for before and after 
            one_sentence = relative_line_list[0].strip()
        else:
            one_sentence = yingshaoxo_text_completor.get_next_text_by_pure_text(response, input_text).strip().split("\n")[0].strip()
        return replace_your_to_my(one_sentence)
    elif task_name == "unknown":
        response = "I don't know what you said."
        response += "\n\n" + get_memory_as_pure_string(input_text, include_diary=True)
        return response

def ask_yingshaoxo_ai(input_text, id_="user"):
    if debug == 1:
        print(make_indents_before_every_lines("Ask yingshaoxo ai:\n" + make_indents_before_every_lines(input_text, 4, as_code_block=True), 4, as_code_block=True))

    the_task, input_text = what_is_the_task(input_text, id_=id_)
    result = finish_a_task(the_task, input_text, id_=id_)
    return result

def summarize(input_text):
    input_text = input_text.strip()
    if input_text == "":
        return ""
    if input_text.count("\n") == 0:
        return input_text
    else:
        function_name = inspect.currentframe().f_code.co_name
        response = ask_other_ai(function_name + ":\n" + make_indents_before_every_lines(input_text, 4, as_code_block=True)).lower()
        if response.startswith("error:"):
            return input_text
        else:
            return response

def remember(input_text, notes, id_, force=False):
    if input_text == "":
        return
    #if len(input_text.strip()) < 5:
    #    return

    temporary_memory = magic_splitor + "#" + id_ + ": \n" + input_text

    if force == False:
        if is_it_in_memory(temporary_memory, id_) == True:
            return

    with open(temporary_memory_file_path, "a", encoding="utf-8") as f:
        f.write(temporary_memory)

    if debug == 1:
        print(make_indents_before_every_lines("The new memory:\n" + make_indents_before_every_lines(temporary_memory.replace(magic_splitor, "").strip(), 4, as_code_block=True), 4, as_code_block=True))

def comment(input_text):
    input_text = input_text.strip()
    if input_text == "":
        return ""

    core_request = "Please make a comment on user newest message" + ":\n" + make_indents_before_every_lines(input_text, 4, as_code_block=True)

    request = ""
    request += core_request + "\n\n"

    temp_memory = get_memory_as_pure_string(input_text, include_diary=True)
    request += """memory:\n{}""".format(make_indents_before_every_lines(temp_memory, 4, as_code_block=True)).strip() + "\n\n"

    request += core_request

    response = ask_other_ai(request).lower()
    if response.startswith("error:"):
        return ""
    else:
        sentence_and_comment = "user: " + input_text + "\n\n" + "bot: " + response.strip()
        add_last_chat_message(sentence_and_comment)
        return response

def get_memory(input_text, id_, should_it_inject_old_diary_memory=False):
    with open(temporary_memory_file_path, "r", encoding="utf-8") as f:
        temporary_memory = f.read()
    recent_temporary_memory = temporary_memory[-500:].strip()

    if should_it_inject_old_diary_memory == True:
        temp_memory = get_memory_as_pure_string(input_text, include_diary=True)
    else:
        temp_memory = get_memory_as_pure_string(input_text, include_diary=False)

    core_request = "Please make a answer on user newest question:\n" + make_indents_before_every_lines(input_text, 4, as_code_block=True)

    task_description = ""
    task_description += core_request + "\n\n"
    task_description += """memory:\n{}""".format(make_indents_before_every_lines(temp_memory, 4, as_code_block=True)).strip() + "\n\n"
    task_description += core_request

    response = ask_other_ai(task_description).lower()
    question_and_answer_string = "user: " + input_text + "\n\n" + "bot: " + response.strip()
    add_last_chat_message(question_and_answer_string)

    return response

def answer_anything_that_related_to_me(input_text, id_, use_diary_data=True):
    if use_diary_data == True:
        should_it_inject_old_diary_memory = True
    else:
        should_it_inject_old_diary_memory = False
    return get_memory(input_text, id_, should_it_inject_old_diary_memory=should_it_inject_old_diary_memory)

def ask_me_question(input_text, id_):
    if this_person_is_important_to_me(id_):
        return answer_anything_that_related_to_me(input_text, id_, use_diary_data=True)
    else:
        return answer_anything_that_related_to_me(input_text, id_, use_diary_data=False)

def is_it_a_true_thing(input_text, id_):
    # this is a very important function
    return True
    #function_name = inspect.currentframe().f_code.co_name
    #response = ask_other_ai(function_name + ":\n" + "```" + input_text + "```").lower()
    #return response

def sentence_pattern_match(pattens, input_text):
    from auto_everything.string_ import String
    string = String()

    data_list = []
    for rule in pattens:
        data_list += list(set(string.hard_core_string_pattern_search(input_text, rule)))
    return data_list

def get_useful_part_of_text(input_text):
    input_text = input_text.lower()
    patterns = [
        "my xxx.",
        "you xxx.",
        "what xxx? xxx.",
        "xxx is xxx.",
        "xxx can be used for xxx.",
        "xxx can be get from xxx.",
        "xxx is composed by xxx.",
        "you can make xxx by xxx.",
        "the alternative of xxx is xxx.",
        "i think xxx",

        "why xxx? because xxx",
        "xxx that is why xxx.",
        "the reason of xxx is xxx.",
        "the deep reason of xxx is xxx.",
        "the good part of xxx is xxx.",
        "the bad part of xxx is xxx.",

        "how to do xxx? xxx",
        "to xxx, you must xxx.",
        "if you want xxx, you have to xxx",
        "xxx requires xxx steps xxx",
        "the xxx step for xxx is xxx.",
        "to success in xxx you have to xxx",

        "我xxx",
        "你xxx",
        "xxx是xxx",
        "xxx有xxx",
        "因为xxx所以xxx",
        "如果xxx就会xxx",
        "如果xxx就能xxx",
        "如果xxx就可以xxx",
        "如果xxx就应该xxx",
        "xxx能够xxx",
        "xxx能帮xxx",
        "xxx能做xxx",
        "xxx能干xxx",
        "xxx能得xxx",
        "xxx能取xxx",
        "为什么xxx？xxx",
        "如何xxx？xxx",
        "知道xxx吗？xxx",
        "我xxx想到xxx",
        "我xxx发现xxx",
        "看起来xxx",
        "xxx想出了xxx",
        "xxx发明了xxx",
        "xxx创造了xxx",
        "xxx得到了xxx",
        "xxx的方法是xxx",
        "xxx的算法是xxx",
        "xxx的途径是xxx",
        "xxx的好处是xxx",
        "xxx的坏处是xxx",
        "要想xxx，你xxx",
        "没有xxx你就xxx",
        "xxx制作方法xxx",
        "理论上xxx",
        "实际上xxx",
        "xxx个秘密xxx",
    ]
    result_list = sentence_pattern_match(patterns, input_text)
    result_list = [one for one in result_list if not one.endswith("?")]
    result_list = [one for one in result_list if not one.endswith("？")]
    return result_list

def does_it_has_values(input_text):
    result_list = get_useful_part_of_text(input_text)
    if len(result_list) != 0:
        return True
    else:
        return False

def ask_question(input_text, id_):
    if is_it_related_to_me(input_text, id_):
        if is_it_ask_me_to_remember_something(input_text, id_):
            remember(input_text, "just remember.", id_)
        else:
            return ask_me_question(input_text, id_)
    else:
        return ask_me_question(input_text, id_)
        if get_words_length(input_text) == 1:
            return ask_language_single_word_dict(input_text)
        else:
            if is_it_a_sure_thing_exists_in_this_world(input_text):
                return ask_wiki_cyclopedia(input_text)
            elif is_it_a_virtual_thing_that_has_no_sure_answer(input_text):
                return ask_zhihu_question_and_answer_database(input_text)

def a_normal_sentence(input_text, id_):
    if is_it_an_agree_sentence(input_text):
        last_chat_message = get_last_chat_message(id_)
        if is_it_in_memory(last_chat_message, id_) == False:
            remember(last_chat_message, "save my last chat message as knowledge because the user think it is right", id_=id_)

    if is_it_related_to_me(input_text, id_):
        summary = summarize(input_text)

        if does_it_has_values(summary):
            remember(summary, "the feeling that guy talks. it is about me.", id_)

        a_comment = comment(summary)
        return "OK, I got your meaning:\n" + replace_your_to_my(summary) + "\n\n" + a_comment
    else:
        # it_is_a_sentence_that_talks_others
        if is_it_a_sentence_that_talks_user_itself(input_text, id_):
            if is_it_a_true_thing(input_text, id_):
                summary = summarize(input_text)
                if does_it_has_values(summary):
                    remember(summary, "the feeling that guy talks. it is about itself.", id_)
                a_comment = comment(summary)
                return "Got it, you said:\n" + replace_your_to_my(summary) + "\n\n" + a_comment
            else:
                return "I think it is not true."
        else:
            # talk other object
            if is_it_a_true_thing(input_text, id_):
                if does_it_has_values(input_text):
                    key_knowledge_list = get_useful_part_of_text(input_text)
                    for one in key_knowledge_list:
                        #remember(one, "knowledge.", id_) # not working for unknown reason
                        old_memory = get_memory_as_pure_string(one, include_diary=False)
                        if one not in old_memory:
                            remember(one, "just remember.", id_, force=True)
                    return "The thing you mentioned can be splited into following:\n" + "\n".join(["* "+one for one in key_knowledge_list])
                else:
                    a_comment = comment(input_text)
                    return "I'm not interested in what you said." + "\n\n" + a_comment
            else:
                # it is false
                return "I think it is not right."

def call_yingshaoxo(input_text, id_="user"):
    response = ""
    if is_it_a_question(input_text):
        response = ask_question(input_text, id_)
    else:
        response = a_normal_sentence(input_text, id_)
    return response

os.system("clear")
#print(call_yingshaoxo("say hi to everyone"))
print("OK! No syntax error!\n\n")

while True:
    try:
        input_text = input("What you want to say: ")
        response = call_yingshaoxo(input_text)
        if response:
            response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0]
            print("\n\nComputer: \n" + response)
            print("\n\n")
    except KeyboardInterrupt:
        print("\n")
        continue

# todo: add "search it again"
