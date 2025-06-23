print("Welcome to god operation system.\n\n")

choice = input("""
What you want to do today?
0. write diary.
1. write novel.
2. chat with yourself.
3. write code.
""").strip()

if '0' == choice:
    print("\n\nYou can use an android app called 'freedom' to do it. (it was made by yingshaoxo)")
    exit()
elif '1' == choice:
    print("\n\nEdit './books/a_typical_chinese_novel.txt'")
    print("For example:\nvim ./books/a_typical_chinese_novel.txt")
    exit()

    the_novel_file_path = "./books/a_typical_chinese_novel.txt"
    the_novel_file = open(the_novel_file_path, "a", encoding="utf-8")
    the_novel_file.close()
    try:
        import os
        #the_novel_file.write("hi\n")
        os.system("vim " + the_novel_file_path)
    except Exception as e:
        print(e)
    finally:
        #the_novel_file.close()
        pass
elif '2' == choice:
    print("\n\nModifying 'yingshaoxo_thinking_dataset.txt'")
    print("Then run:\npython3 yingshaoxo_ai.py")
    exit()
elif '3' == choice:
    print("\n\nJust go to a folder called '/home/yingshaoxo/CS'. Then code.")
    exit()
else:
    print("\n\nYou choose to do nothing")
    exit()
