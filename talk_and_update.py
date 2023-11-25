import os
from time import sleep
from auto_everything.ml import Yingshaoxo_Text_Generator
from auto_everything.terminal import Terminal, Terminal_User_Interface
from auto_everything.disk import Disk
terminal = Terminal()
disk = Disk()
terminal_user_interface = Terminal_User_Interface()


the_general_seperator = "\n\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n\n"
output_txt_file = disk.join_paths("./", "dataset.txt")
if not disk.exists(output_txt_file):
    io_.write(output_txt_file, "")

def general_text_wrapper(who_said: str, language: str, content: str):
    text = ""
    text += content
    text += the_general_seperator
    return text

def handle_yingshaoxo_ai_text(text: str):
    text = text.strip()
    if (text == ""):
        return
    with open(output_txt_file, "a", encoding="utf-8", errors="ignore") as f:
        f.write(general_text_wrapper(who_said="yingshaoxo", language="python", content=text))


yingshaoxo_text_generator = Yingshaoxo_Text_Generator(
    input_txt_folder_path="./",
    type_limiter=[".txt"],
    use_machine_learning=False
)

def decode_response(text: str, chat_context: str):
    #print("`"+text+"`")
    splits = text.split("\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n")
    if (len(splits) > 1):
        response = splits[1].strip()
    elif (len(splits) == 1):
        response = splits[0].strip()
    else:
        response = ""
    new_code = f"""
chat_context = '''{chat_context}'''

{response}
"""
    final_response = terminal.run_python_code(code=new_code)
    if final_response.strip() == "":
        final_response = response
    final_response = "\n".join([one for one in final_response.split("\n") if not one.strip().startswith("__**")])
    return final_response

os.system("clear")
all_input_text = ""
while True:
    input_text = input("What you want to say?    ")
    handle_yingshaoxo_ai_text(input_text)

    all_input_text += input_text + "\n"
    real_input = all_input_text[-8000:].strip()
    #response = yingshaoxo_text_generator.search_and_get_following_text_in_a_exact_way(input_text=real_input, quick_mode=False)
    previous_text, response = yingshaoxo_text_generator.next_fuzz_sentence_generation(text_source_data=yingshaoxo_text_generator.text_source_data, input_text=real_input, how_long_the_text_you_want_to_get=800, compare_times=10, also_return_previous_text=True)

    response = decode_response(text=response, chat_context=all_input_text)
    #all_input_text += response

    print("\n\n---------\n\n")
    print(response)
    print("\n\n---------\n\n")

    confirm_text = input("Do you want to edit the response? (y/n)").strip()
    if confirm_text == "y":
        os.system("clear")
        response = terminal_user_interface.edit_box(response, editor="vim -u NONE")
        os.system("clear")
        print("New response is:")
        print(response)
        sleep(5)
    handle_yingshaoxo_ai_text(response)
    os.system("clear")
