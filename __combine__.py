# "put material_and_thinking(简txt) and yingshaoxo_diary and auto_everything and material_and_thinking(complex English) into a txt book, then print 3 books"

simple_material_and_thinking_txt_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Books/《物质与思想》.txt"
diary_txt_path = "/home/yingshaoxo/CS/yingshaoxo_txt_data/all_yingshaoxo_data_2023_11_13.txt" # maybe we should add date into this diary
diary_date_txt_path = "/home/yingshaoxo/CS/yingshaoxo_txt_data/date_for_all_yingshaoxo_data_2023_11_13.txt"

auto_everything_folder_path = "/home/yingshaoxo/CS/auto_everything" # should convert folder file tree into pure text that starts with "# <path>\n\n<content>"
yingshaoxo_file_path = "/home/yingshaoxo/CS/yingshaoxo_txt_data/yingshaoxo/main.py"
yingshaoxo_file_path2 = "/home/yingshaoxo/CS/yingshaoxo_txt_data/yingshaoxo/small_functions.py"

novel_1_path = "/home/yingshaoxo/CS/yingshaoxo_txt_data/books/a_typical_chinese_novel.txt"
novel_2_path = "/home/yingshaoxo/CS/yingshaoxo_txt_data/yingshaoxo/life_simulator.py"

complex_material_and_thinking_markdown_folder = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Books/material-and-thoughts" # should convert markdown tree into a txt file
complex_material_and_thinking_markdown_summary_path = "/home/yingshaoxo/Disk/Sync_Folder/Yingshaoxo_Data/Core/Small_Core/My_Books/material-and-thoughts/SUMMARY.md" # should convert markdown tree into a txt file

from auto_everything.disk import Disk
disk = Disk()

magic_splitor = "\n\n__**__**__yingshaoxo_is_the_top_one__**__**__\n\n"
magic_splitor2 = "\n__**__**__yingshaoxo_is_the_top_one__**__**__\n"

# handle simple theory
with open(simple_material_and_thinking_txt_path, "r", encoding="utf-8") as f:
    simple_theory = f.read()

# handle diary
with open(diary_txt_path, "r", encoding="utf-8") as f:
    diary = f.read()
with open(diary_date_txt_path, "r", encoding="utf-8") as f:
    diary_date = f.read()
diary_piece_list = [one for one in diary.split(magic_splitor)]
date_list = [one for one in diary_date.split("\n")]

new_diary = ""
for index, one in enumerate(date_list):
    new_diary += one.strip() + "\n\n\n" + diary_piece_list[index].strip() + magic_splitor
diary = new_diary

# handle auto_everything_folder_path
files = disk.get_files(auto_everything_folder_path, type_limiter=[".py", ".md"])
new_files = []
for file in files:
    file = file[len(auto_everything_folder_path)+1:]
    if file.startswith("playground/"):
        continue
    if file.startswith("docs/"):
        continue
    if file.startswith("blackhole/"):
        continue
    if file.startswith("dist/"):
        continue
    if file.startswith("tests/"):
        continue
    if file.startswith("service/"):
        continue
    if file.startswith("_auto/"):
        continue
    if "/x11/" in file:
        continue
    if "__pycache__" in file:
        continue
    if "/additional/" in file:
        continue
    if "typed_" in file and ".py" in file:
        continue
    if "super_setup.py" in file:
        continue
    new_files.append(file)
new_files.sort()

auto_everything_txt_data = ""
for file in new_files:
    real_file_path = auto_everything_folder_path + "/" + file
    with open(real_file_path, "r", encoding="utf-8") as f:
        temp_content = f.read()
    auto_everything_txt_data += "# " + file + "\n\n" + temp_content.strip() + magic_splitor

# handle yingshaoxo_file_path
yingshaoxo_thinking_logic = ""
with open(yingshaoxo_file_path, "r", encoding="utf-8") as f:
    yingshaoxo_thinking_logic = f.read()
yingshaoxo_thinking_logic = "# " + "yingshaoxo_main.py\n\n" + yingshaoxo_thinking_logic + magic_splitor

with open(yingshaoxo_file_path2, "r", encoding="utf-8") as f:
    yingshaoxo_thinking_logic2 = f.read()
yingshaoxo_thinking_logic += "# " + "small_functions.py\n\n" + yingshaoxo_thinking_logic2 + magic_splitor


# handle novel_1
novel_1 = ""
with open(novel_1_path, "r", encoding="utf-8") as f:
    novel_1 = f.read()
novel_1 = "# " + "a_typical_chinese_novel.txt\n\n" + novel_1 + magic_splitor


# handle novel_2
novel_2 = ""
with open(novel_2_path, "r", encoding="utf-8") as f:
    novel_2 = f.read()
novel_2 = "# " + "life_simulator.py\n\n" + novel_2 + magic_splitor


# handle complex_material_and_thinking_markdown_path
complex_theory_book_data = ""
summary = ""
with open(complex_material_and_thinking_markdown_summary_path, "r", encoding="utf-8") as f:
    summary = f.read()
complex_theory_book_data += "# 《物质与思想》latest\n\n" + summary + magic_splitor
lines = [one for one in summary.split("\n") if ".md)" in one]
for line in lines:
    link = line.split("](")[1].strip()[:-1]
    real_path = complex_material_and_thinking_markdown_folder + "/" + link
    with open(real_path, "r", encoding="utf-8") as f:
        temp_one = f.read()
    complex_theory_book_data += temp_one + magic_splitor

# combine
all_in_all = ""
all_in_all += simple_theory.strip() + magic_splitor
all_in_all += diary.strip() + magic_splitor
all_in_all += auto_everything_txt_data.strip() + magic_splitor
all_in_all += yingshaoxo_thinking_logic.strip() + magic_splitor
all_in_all += novel_1.strip() + magic_splitor
all_in_all += novel_2.strip() + magic_splitor
all_in_all += complex_theory_book_data.strip()
with open("./test_dict/yingshaoxo_data.txt", "w", encoding="utf-8") as f:
    f.write(all_in_all)
