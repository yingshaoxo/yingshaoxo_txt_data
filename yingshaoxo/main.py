import os

def is_it_a_question(input_text):
    pass

def is_it_related_to_me(input_text, id_):
    pass

def is_it_a_sentence_that_talks_user_itself(input_text, id_):
    pass

def remember(input_text, notes):
    pass

def is_it_a_true_thing(input_text, id_):
    pass

def does_it_has_values(input_text):
    pass

def ask_question(input_text):
    if is_it_related_to_me(input_text, id_):
        return ask_me_question(input_text, id_)
    else:
        if is_it_a_sure_thing_exists_in_this_world(input_text):
            return ask_wiki_cyclopedia(input_text)
        elif is_it_a_virtual_thing_that_has_no_sure_answer(input_text):
            return ask_zhihu_question_and_answer_database(input_text)

def a_normal_sentence(input_text, id_):
    if is_it_related_to_me(input_text, id_):
        remember(input_text, "the feeling that guy talks. it is about me.")
    else:
        # it_is_a_sentence_that_talks_others
        if is_it_a_sentence_that_talks_user_itself(input_text, id_):
            if is_it_a_true_thing(input_text, id_):
                remember(input_text, "the feeling that guy talks. it is about itself.", id_)
            else:
                return "I think it is not true."
        else:
            # talk other object
            if is_it_a_true_thing(input_text, id_):
                if does_it_has_values(input_text):
                    remember_the_sentence(input_text)
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
