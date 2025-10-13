import os

def get_words_length(input_text):
    if is_it_english(input_text):
        return len(get_words_list_from_english(input_text))
    elif is_it_chinese(input_text):
        return len(get_words_list_from_chinese(input_text))

def is_it_a_question(input_text):
    pass

def is_it_related_to_me(input_text, id_):
    pass

def is_it_a_sentence_that_talks_user_itself(input_text, id_):
    pass

def summarize(input_text):
    pass

def remember(input_text, notes, id_):
    pass

def get_memory(notes, id_):
    pass

def is_it_a_true_thing(input_text, id_):
    pass

def get_useful_part_of_text(input_text):
    input_text = input_text.lower()
    patterns = [
        "what xxx? xxx.",
        "xxx is xxx.",
        "xxx can be used for xxx.",
        "xxx can be get from xxx.",
        "xxx is composed by xxx.",
        "you can make xxx by xxx.",
        "the alternative of xxx is xxx.",
        "i think xxx\n",

        "why xxx? because xxx\n",
        "xxx that is why xxx.",
        "the reason of xxx is xxx.",
        "the deep reason of xxx is xxx.",
        "the good part of xxx is xxx.",
        "the bad part of xxx is xxx.",

        "how to do xxx? xxx\n",
        "to xxx, you must xxx.",
        "if you want xxx, you have to xxx\n",
        "xxx requires xxx steps xxx\n",
        "the xxx step for xxx is xxx.",
    ]
    result_list = sentence_pattern_match(patterns, input_text)
    return result_list

def does_it_has_values(input_text):
    result_list = get_useful_part_of_text(input_text)
    if len(result_list) != 0:
        return True
    else:
        return False

def ask_question(input_text):
    if is_it_related_to_me(input_text, id_):
        return ask_me_question(input_text, id_)
    else:
        if get_words_length(input_text) == 1:
            return ask_language_single_word_dict(input_text)
        else:
            if is_it_a_sure_thing_exists_in_this_world(input_text):
                return ask_wiki_cyclopedia(input_text)
            elif is_it_a_virtual_thing_that_has_no_sure_answer(input_text):
                return ask_zhihu_question_and_answer_database(input_text)

def a_normal_sentence(input_text, id_):
    if is_it_related_to_me(input_text, id_):
        summary = summarize(input_text)
        remember(summary, "the feeling that guy talks. it is about me.", id_)
        return "OK, I got your meaning:\n" + summary
    else:
        # it_is_a_sentence_that_talks_others
        if is_it_a_sentence_that_talks_user_itself(input_text, id_):
            if is_it_a_true_thing(input_text, id_):
                summary = summarize(input_text)
                remember(summary, "the feeling that guy talks. it is about itself.", id_)
                return "Got it, you said:\n" + summary
            else:
                return "I think it is not true."
        else:
            # talk other object
            if is_it_a_true_thing(input_text, id_):
                if does_it_has_values(input_text):
                    key_knowledge_list = get_useful_part_of_text(input_text)
                    for one in key_knowledge_list:
                        remember(one, id_)
                    return "The thing you mentioned can be splited into following:\n" + "\n".join(["* "+one for one in key_knowledge_list])
                else:
                    return "I'm not interested in what you said."
            else:
                # it is false
                return "I think it is not right."
            return "OK"

def call_yingshaoxo(input_text, id_="unknown"):
    response = ""
    if is_it_a_question(input_text):
        response = ask_question(input_text, id_)
    else:
        response = a_normal_sentence(input_text, id_)
    return response

os.system("clear")
call_yingshaoxo("say hi to everyone")
print("OK! No syntax error!")
