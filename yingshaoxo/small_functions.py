from auto_everything.ml import Yingshaoxo_Text_Completor
from auto_everything.string_ import String
from auto_everything.disk import Disk
yingshaoxo_string = String()
yingshaoxo_disk = Disk()
yingshaoxo_text_completor = Yingshaoxo_Text_Completor()

def is_it_english(input_text):
    if input_text.isascii():
        return True
    else:
        return False

def is_it_chinese(input_text):
    if is_it_english(input_text):
        return False
    else:
        return True

def get_words_list_from_english(input_text):
    return input_text.split(" ")

def get_words_list_from_chinese(input_text):
    return list(input_text)

def get_words_length(input_text):
    if is_it_english(input_text):
        return len(get_words_list_from_english(input_text))
    elif is_it_chinese(input_text):
        return len(get_words_list_from_chinese(input_text))

def is_it_a_question(input_text):
    if len(input_text) == 0:
        return False
    input_text = input_text.lower()

    if input_text.endswith("?"):
        return True
    elif input_text.startswith("is "):
        return True
    elif input_text.startswith("what "):
        return True
    elif input_text.startswith("where "):
        return True
    elif input_text.startswith("how "):
        return True
    elif input_text.startswith("are "):
        return True
    elif input_text.startswith("should "):
        return True
    elif input_text.startswith("can "):
        return True

    if input_text.endswith("?"):
        return True
    elif input_text.endswith("？"):
        return True
    elif input_text[-1] == "吗":
        return True
    elif input_text.startswith("什么"):
        return True
    elif input_text.startswith("为什么"):
        return True
    elif input_text.startswith("如何"):
        return True
    elif input_text.startswith("怎样"):
        return True
    elif input_text.startswith("是否"):
        return True
    elif input_text.startswith("可否"):
        return True

    return False

def is_it_exists_in_zhihu_question_and_answer_database(input_text):
    return False

def is_it_related_to_me(input_text, id_):
    if len(input_text) == 0:
        return False
    input_text = input_text.lower()

    if input_text.startswith("you "):
        return True
    if input_text.startswith("your "):
        return True
    if " you " in input_text:
        return True
    if " you" in input_text:
        return True
    if " your " in input_text:
        return True
    if "yingshaoxo" in input_text:
        return True
    if "你" in input_text:
        return True
    if "你们" in input_text:
        return True
    if "您" in input_text:
        return True
    if "胡英杰" in input_text:
        return True
    if "英杰" in input_text:
        return True

    return False

def is_it_a_sentence_that_talks_user_itself(input_text, id_):
    if len(input_text) == 0:
        return False
    input_text = input_text.lower()

    if input_text.startswith("i "):
        return True
    if input_text.startswith("we "):
        return True
    if input_text.startswith("my "):
        return True
    if " i " in input_text:
        return True
    if " my " in input_text:
        return True
    if " we " in input_text:
        return True
    if id_ in input_text:
        return True
    if "我" in input_text:
        return True
    if "我们" in input_text:
        return True

    return False

def this_person_is_important_to_me(id_):
    # fake for now
    return True

def is_it_ask_me_to_remember_something(input_text, id_):
    if len(input_text) == 0:
        return False
    input_text = input_text.lower()

    if input_text.startswith("remember "):
        return True
    if " remember " in input_text:
        return True
    if " take a note " in input_text:
        return True
    if input_text.startswith("记住"):
        return True
    if input_text.startswith("记下"):
        return True
    if input_text.startswith("记录"):
        return True
    if "帮" in input_text and "记住" in input_text:
        return True

    return False

def is_it_ask_me_to_do_something(input_text):
    if len(input_text) == 0:
        return False
    input_text = input_text.lower()

    if input_text.startswith("say "):
        return True
    elif input_text.startswith("tell "):
        return True
    elif input_text.startswith("do "):
        return True
    elif input_text.startswith("search "):
        return True
    elif input_text.startswith("play "):
        return True

    return False

def is_it_a_sure_thing_exists_in_this_world(input_text):
    # todo in the future
    return True

def question_sentence_to_normal_sentence(input_text):
    # author yingshaoxo: a very important function for database search

    # for example: "what is desk?" -> "desk is"
    # for example: "what is age your age?" -> "my age is"
    if len(input_text) == 0:
        return False
    input_text = input_text.lower()

    input_text = input_text.replace("样的", "")
    input_text = input_text.replace("的吗", "")
    input_text = input_text.replace("的吧", "")
    input_text = input_text.replace("的呢", "")

    for word in ["知道", "什么", "如何", "怎样", "怎么", "哪儿", "觉得", "认为", "哪些", "哪类", "哪个", " how ", " what ", " where ", " know ", " when ", " feel ", " think "]:
        index = input_text.find(word)
        if index != -1:
            next_2_char = input_text[index+len(word):index+len(word)+2]
            if ("？" not in next_2_char) and ("?" not in next_2_char):
                input_text = input_text[index+len(word):]
    input_text = input_text.strip()

    input_text = input_text.replace("?", "")
    input_text = input_text.replace("？", "")
    input_text = input_text.replace("吗", "")
    input_text = input_text.replace("吧", "")
    input_text = input_text.replace("呢", "")
    input_text = input_text.replace("谁", "")
    input_text = input_text.replace("哪", "")
    input_text = input_text.replace("什么", "")
    input_text = input_text.replace("哪儿", "")

    input_text = input_text.replace("what ", "")
    input_text = input_text.replace("how ", "")
    input_text = input_text.replace("where ", "")
    input_text = input_text.replace("can ", "")
    input_text = input_text.replace("should ", "")
    input_text = input_text.replace("could ", "")
    input_text = input_text.replace("would ", "")
    input_text = input_text.replace("when ", "")
    input_text = input_text.strip()
    input_text = input_text.replace("is ", "")
    input_text = input_text.replace("are ", "")

    input_text = input_text.replace("是怎", "是")

    return input_text

def ask_zhihu_question_and_answer_database(input_text):
    if is_it_exists_in_zhihu_question_and_answer_database(input_text):
        return get_answer_by_looking_for_zhihu_question_and_answer_database(input_text)
    else:
        return "Why you do not know it?\nHave your teacher told you that?\nWhy you can't learn it by doing exploring in real world?"

def is_it_an_agree_sentence(input_text):
    if len(input_text) == 0:
        return False
    input_text = input_text.lower()

    word_list = [
        "yes",
        "right",
        "ok",
        "good",
        "fine",
        "no problem",
        "是的",
        "可以",
        "正确",
        "对的",
        "对了",
        "很好",
        "还行",
        "正解",
        "行了",
        "行吧",
        "没问题",
        "爱你",
        "好啊",
    ]
    ok_inside = False
    for word in word_list:
        if word in input_text:
            ok_inside = True
            break

    word_list = [
        "not",
        "不",
        "非",
        "好看",
    ]
    not_inside = False
    for word in word_list:
        if word in input_text:
            not_inside = True
            break

    if ok_inside == True and not_inside == False:
        return True

    return False

def make_indents_before_every_lines(input_text, indent=4, as_code_block=False):
    if as_code_block == True:
        input_text = "```\n" + input_text + "\n````"
    lines = input_text.split("\n")
    for index in range(len(lines)):
        lines[index] = " "*indent + lines[index]
    return "\n".join(lines)

def replace_your_to_my(input_text):
    input_text = input_text.replace("your", "my")
    input_text = input_text.replace("you", "i")
    input_text = input_text.replace("你", "我")
    return input_text

def switch_you_and_me(input_text):
    you_index_list = []
    me_index_list = []
    for index, char in enumerate(input_text):
        if char == "我":
            me_index_list.append(index)
        if char == "你":
            you_index_list.append(index)
    input_text_list = list(input_text)
    for index in you_index_list:
        if 0 <= (index + 1) < len(input_text_list):
            if input_text_list[index + 1] == "们":
                continue
        input_text_list[index] = "我"
    for index in me_index_list:
        if 0 <= (index + 1) < len(input_text_list):
            if input_text_list[index + 1] == "们":
                continue
        input_text_list[index] = "你"
    input_text = "".join(input_text_list).strip()

    if " " in input_text:
        words = input_text.split(" ")
        if words[0] == "you":
            words[0] = "i"
        elif words[0] == "i":
            words[0] = "you"
        elif words[0] == "my":
            words[0] = "your"
        elif words[0] == "your":
            words[0] = "my"
        new_words = [words[0]]
        for word in words[1:]:
            new_word = ""
            if word == "your":
                new_word = "my"
            elif word == "my":
                new_word = "your"
            elif word == "i":
                new_word = "you"
            elif word == "you":
                new_word = "me"
            elif word == "me":
                new_word = "you"
            elif word == "me.":
                new_word = "you."
            elif word == "me!":
                new_word = "you!"
            else:
                new_word = word
            new_words.append(new_word)
        input_text = " ".join(new_words)
        input_text = input_text.replace("you am ", "you are ")

    return input_text

def get_next_string(source_text, input_text):
    while len(input_text) > 0:
        parts = source_text.split(input_text)
        if len(parts) >= 2:
            return parts[1]
        else:
            input_text = input_text[1:]
    return ""

if __name__ == "__main__":
    print(switch_you_and_me("你是否知道我？"))
    print(switch_you_and_me("i am your dad."))
    print(switch_you_and_me("you dad is me."))
    print(switch_you_and_me("can you give me a story?"))
