import random


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
            response += temp_response
            input_text += temp_response
            if temp_response.endswith(end_string):
                response = response[:-len(end_string)]
                break

        return response

    def get_next_text_by_pure_text(self, source_text, input_text, how_many_character_you_want=2000, level=64):
        """
        This method is the best so far, if you have big memory.
        """
        end_string = "[*|end|*]"

        def down_side_complete(the_input_text):
            for right_side_index in range(0, level):
                right_side_sub_string = the_input_text[right_side_index:]

                the_splits = source_text.split(right_side_sub_string)
                the_length_of_splits = len(the_splits)
                if the_length_of_splits >= 2:
                    index = random.randint(1, the_length_of_splits-1)
                    target_text = the_splits[index][:level]
                    return target_text
                else:
                    pass
            return " " + end_string

        response = ""
        while len(response) < how_many_character_you_want:
            temp_response = down_side_complete(input_text)
            response += temp_response
            input_text += temp_response
            if temp_response.endswith(end_string):
                response = response[:-len(end_string)]
                break

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
            response += temp_response
            input_text += temp_response

        return response

    def update_source_text_dict_for_sqlite(self, source_text, sqlite_path, level=7):
        pass

    def get_next_text_by_using_sqlite_dict(self, sqlite_path, input_text, level=7, how_many_character_you_want=100):
        pass


if __name__ == "__main__":
    source_text = get_source_text_data()
    yingshaoxo_text_completor = Yingshaoxo_Text_Completor()

    lines = yingshaoxo_text_completor.get_source_text_lines(source_text)
    lines = source_text.split("__**__**__yingshaoxo_is_the_top_one__**__**__")

    while True:
        input_text = input("What you want to say: ")
        response = yingshaoxo_text_completor.get_next_text_by_pure_text(source_text, input_text, how_many_character_you_want=2000, level=64)
        if response:
            response = response.split("__**__**__yingshaoxo_is_the_top_one__**__**__")[0]
            print("Computer: " + response)
            print("\n\n")
