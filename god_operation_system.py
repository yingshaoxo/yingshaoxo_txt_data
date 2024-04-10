print("Welcome to god operation system.\n\n")

choice = input("""
What you want to do today?
0. write diary.
1. write novel.
2. chat with yourself.
3. write code.
""")

if '0' in choice:
    print("You can use an android app called 'freedom' to do it. (it was made by yingshaoxo)")
    exit()
elif '1' in choice:
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
elif '2' in choice:
    import talk_and_update
    exit()
elif '3' in choice:
    print("Just go to a folder called '/home/yingshaoxo/CS'. Then code.")
    exit()
else:
    print("You choose to do nothing")
    exit()
