import time
import threading
import re
from pprint import pprint
import copy
import os, tty, termios, sys, shlex
#from typing import Any, Callable


if sys.version_info[0] == 3 and sys.version_info[1] <= 2:
    import inspect
    def get_arguments(obj):
        if not (inspect.isfunction(obj) or inspect.ismethod(obj)):
            raise TypeError("Input must be a function or method")
        # Get basic argument info
        argspec = inspect.getargspec(obj)
        args = argspec.args
        # Format the signature string
        #result_with_function_name = "{} ({})".format(obj.__name__, ', '.join(args))
        result = "({})".format(', '.join(args))
        return result
else:
    from inspect import signature
    def get_arguments(obj):
        result = str(signature(obj))
        return result


class Python():
    """
    Python model was intended to simplify python development
    """

    def __init__(self):
        from auto_everything.io import IO
        from auto_everything.base import OS
        from auto_everything.terminal import Terminal
        from auto_everything.disk import Disk
        self._io = IO()
        self._os = OS()
        self._t = Terminal()
        self._disk = Disk()

    def check_if_a_variable_is_a_function(self, function):
        #(self, function: Any) -> bool:
        return isinstance(function, Callable)

    def list_python_packages(self):
        """
        Return a list of python packages which installed in your computer
        """
        return self._os.list_python_packages()

    def install_package(self, package_name):
        #(self, package_name: str):
        """
        Parameters
        ----------
        package_name: string
            the python package you want to install
        """
        self._os.install_python_package(package_name)

    def uninstall_package(self, package_name):
        #(self, package_name: str):
        """
        Parameters
        ----------
        package_name: string
            the python package you want to uninstall
        """
        self._os.uninstall_python_package(package_name)

    def create_mini_python(self, variable_dict=None):
        import sys
        import json
        from io import StringIO
        from multiprocessing import Process, Queue

        if variable_dict == None:
            variable_dict = {'__builtins__': __builtins__}
        else:
            if "__builtins__" not in variable_dict:
                variable_dict.update({'__builtins__': __builtins__})

        class Mini_Python():
            def __init__(self, the_variable_dict):
                self.the_variable_dict = the_variable_dict

            def _handle_python_call(self, operation, json_args, eval_only=True):
                try:
                    args = json.loads(json_args)

                    for i, arg in enumerate(args):
                        self.the_variable_dict['data_{0}'.format(i)] = arg

                    if eval_only == True:
                        result = eval(operation, self.the_variable_dict)
                    else:
                        exec(operation, self.the_variable_dict)
                        result = None

                    return json.dumps(result)
                except Exception as e:
                    return json.dumps({'error': str(e)})

            def inject_python(self, code, *args):
                # you can define some global functions and variables here
                try:
                    jsonArgs = json.dumps(args)
                    result = self._handle_python_call(code, jsonArgs, eval_only=False)
                    return json.loads(result)
                except Exception as e:
                    return {"error": str(e)}

            def eval_python(self, code, *args):
                # you can evaluate an expression here
                try:
                    jsonArgs = json.dumps(args)
                    result = self._handle_python_call(code, jsonArgs, eval_only=True)
                    return json.loads(result)
                except Exception as e:
                    return {"error": str(e)}

            def _real_run_code(self, code_str, output_q):
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                try:
                    exec(code_str, self.the_variable_dict)
                    output_q.put(sys.stdout.getvalue())
                except Exception as e:
                    output_q.put("error: " + str(e))
                finally:
                    sys.stdout = old_stdout

            def run_code(self, code, timeout=20):
                output_q = Queue()
                p = Process(target=self._real_run_code, args=(code, output_q))
                p.start()
                p.join(timeout)

                if p.is_alive():
                    p.terminate()
                    return "error: Process timeout"

                return output_q.get()

        return Mini_Python(variable_dict)

    def reactive(self, old_dict):
        #(self, old_dict: dict):
        """
        This function will return a multiprocessing or threads safe dict. You can use it to share pure data structure, like string, int, float, bool, list, dict
        It will not share newly added data unless it is inside the old exists list or dict

        Parameters
        ----------
        old_dict: dict
            a python dict
        """
        from multiprocessing import Manager
        import types
        import inspect

        _manager = Manager()

        def reactive_dict(data):
            for key, value in data.items():
                if isinstance(value, dict):
                    data[key] = reactive_dict(value)
                elif isinstance(value, list):
                    data[key] = reactive_list(value)
                #elif isinstance(value, object) and hasattr(value, "__dict__"):
                #    data[key] = reactive_instance(value)
            return _manager.dict(data)

        def reactive_list(data):
            for i, value in enumerate(data):
                if isinstance(value, dict):
                    data[i] = reactive_dict(value)
                elif isinstance(value, list):
                    data[i] = reactive_list(value)
                #elif isinstance(value, object) and hasattr(value, "__dict__"):
                #    data[i] = reactive_instance(value)
            return _manager.list(data)

        def reactive_instance(instance):
            properties = inspect.getmembers(instance, lambda m: not inspect.isroutine(m))
            properties_dict = {name: value for name, value in properties if not name.startswith("__")}
            properties_dict = reactive_dict(properties_dict)

            # will have a pickle error: can't pickle local class
            class ProxyedClass(type(instance)):
                def __setattr__(self, name, value):
                    super().__setattr__(name, value)
                    self.notify(name, value)

                def notify(self, name, value):
                    properties_dict[name] = value

            proxy_instance = ProxyedClass()
            proxy_instance.__dict__.update(properties_dict)

            return proxy_instance

        return _manager, reactive_dict(old_dict)

    class loop():
        def __init__(self, interval=1, thread=False):
            #(self, interval: int | float=1, thread:bool=False):
            """
            interval: inverval in seconds
            new_thread: do you want to open a new thread? True/False
            """
            self.thread = thread
            self.interval = interval

        def __call__(self, func):
            """
            func: a function which you want to run forever
            """

            def new_function(*args, **kwargs):
                def while_function():
                    while 1:
                        try:
                            func(*args, **kwargs)
                            time.sleep(self.interval)
                        except Exception as e:
                            print(e)

                if self.thread is False:
                    while_function()
                else:
                    threading.Thread(target=while_function).start()

            return new_function

    def help(self, object_):
        """
        get help information about class or function
        """
        if callable(object_):
            arguments = get_arguments(object_)
            print(object_.__name__ + arguments)

            doc = object_.__doc__
            if doc:
                print(doc, '\n')
        else:
            methods = dir(object_)
            private_methods = []
            public_methods = []
            for method in methods:
                if method[:1] == "_":
                    private_methods.append(method)
                else:
                    public_methods.append(method)
            print(private_methods, '\n')
            pprint(public_methods)
            """
            callable_list = inspect.getmembers(object_, predicate=inspect.ismethod) + inspect.getmembers(object_,
                                                                                                         predicate=inspect.isclass)
            callable_list = [(one, one[1].__name__ + str(signature(one[1]))) for one in callable_list]
            not_callable_list = dir(object_)
            for one in callable_list:
                if one[0] in not_callable_list:
                    not_callable_list.remove(one[0])
            not_callable_list = [(one, "") for one in not_callable_list]
            private_methods = []
            public_methods = []
            for one in not_callable_list + callable_list:
                if one[0][:1] == "_":
                    private_methods.append(one[0])
                else:
                    public_methods.append(one)

            print(private_methods, "\n")
            [print(one[0], one[1]) for one in public_methods]
            """

    def fire(self, class_name):
        """
        fire is a function that will turn any Python class into a command line interface
        """
        self.fire2(class_instance=class_name)
        # from fire import Fire #type: ignore
        # Fire(class_name)

    def fire2(self, class_instance, new_arguments=[]):
        #(self, class_instance: Any, new_arguments: list[Any] = []):
        """
        fire2 is a function that come from ying_shao_xo's wild thinking which turn any Python class into a user friendly command line interface
        @yingshaoxo, baby
        """
        type_dict = {
            'int': int,
            'str': str,
            'bool': bool,
            'float': float
        }
        def get_argument_name(text):
            #(text: str):
            if ":" not in text:
                return text.split('=')[0].strip()
            else:
                return text.split(':')[0].strip()
        def get_type_string(text):
            #(text: str):
            if ":" not in text:
                return None
            text = text.split(':')[1].strip().split('=')[0].strip()
            splits = [one.strip() for one in text.split("|") if one.strip() != ""]
            for one in splits:
                if one in type_dict.keys():
                    return one
            return "str"
        def get_type_function(text):
            #(text: str):
            if ":" not in text:
                return None
            text = text.split(':')[1].strip().split('=')[0].strip()
            splits = [one.strip() for one in text.split("|") if one.strip() != ""]
            for one in splits:
                if one in type_dict.keys():
                    return type_dict[one]
            return str

        if not callable(class_instance):
            return

        class_instance2 = class_instance()

        if len(new_arguments) == 0:
            original_command_line_arguments = sys.argv
        else:
            original_command_line_arguments = new_arguments
        command_line_arguments = original_command_line_arguments[1:]
        my_method_and_propertys = {}
        function_string_list = []

        for each_string in vars(class_instance).keys():
            if (not each_string.startswith("_")):
                one = class_instance.__dict__[each_string]
                if callable(one):
                    # it is a sub_function
                    arguments = get_arguments(one)
                    #print(one.__name__, arguments)

                    function_string_list.append(each_string)
                    my_method_and_propertys[each_string] = {
                        'function_name': each_string,
                        'function_instance': getattr(class_instance2, each_string),
                        'arguments': {
                            get_argument_name(one2):
                                {
                                    'type_string': get_type_string(one2),
                                    'type_function': get_type_function(one2),
                                }
                            for one2 in
                            re.sub(
                                r"'(.*?)'", "''",
                                re.sub(r'"(.*?)"', '""',
                                       arguments[1:-1])
                            )
                            .split(', ')[1:]
                        },
                        'arguments_list': [
                            {
                                'argument_name': get_argument_name(one2),
                                'type_string': get_type_string(one2),
                                'type_function': get_type_function(one2),
                            }
                            for one2 in
                            re.sub(
                                r"'(.*?)'", "''",
                                re.sub(r'"(.*?)"', '""',
                                       arguments[1:-1])
                            )
                            .split(', ')[1:]
                        ],
                        'arguments_string': arguments
                    }
        # print(command_line_arguments)
        # print(my_method_and_propertys)

        if len(command_line_arguments) == 0:
            if len(my_method_and_propertys) == 0:
                print("APIs:\n")
                for function_name in function_string_list:
                    argument_part = ', '.join(my_method_and_propertys[function_name]['arguments_string'].split(', ')[1:])
                    if (argument_part.strip() == ""):
                        print((function_name + "\n    " + "()").strip())
                    else:
                        print((function_name + "\n    " + "(" + argument_part).strip())
            else:
                # the user do not know how to use this program, so make a shell for them
                def print_seperate_line():
                    print("\n" + '-'*9 + "\n")
                def print_functions_info(start_with=""):
                    #(start_with: str = ""):
                    start_with = start_with.strip()
                    for function_name in function_string_list:
                        if start_with != "":
                            if (function_name.startswith(start_with)):
                                print(function_name)
                        else:
                            print(function_name)
                def print_argument_info(function_name):
                    #(function_name: str):
                    if (function_name in my_method_and_propertys.keys()):
                        argument_part = ', '.join(my_method_and_propertys[function_name]['arguments_string'].split(', ')[1:])[:-1]
                        print(argument_part)
                    else:
                        print("No such function: {function_name}".format(function_name=function_name))
                def print_chars(text):
                    #(text: str):
                    print(text, end="", flush=True)
                def clear_screen():
                    os.system("clear")
                def get_char_input():
                    #() -> tuple[str, int]:
                    #https://www.physics.udel.edu/~watson/scen103/ascii.html
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(sys.stdin.fileno())
                        char = sys.stdin.read(1)
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    return char, ord(char)
                def get_last_word_of_string(text):
                    #(text:str) -> tuple[str, int]:
                    splits = text.split(" ")
                    splits = [one for one in splits if one.strip() != ""]
                    if (text[-1].strip() == ""):
                        return "", len(splits)
                    if " " not in text:
                        return "", len(splits)
                    return splits[-1], len(splits)
                final_command_line = original_command_line_arguments[0]+" "
                while True:
                    clear_screen()
                    last_word, how_many_words = get_last_word_of_string(final_command_line)

                    if how_many_words == 2 and final_command_line.endswith(" "):
                        current_function_name = final_command_line.split(" ")[1].strip()
                        print_argument_info(current_function_name)
                    elif how_many_words > 2:
                        current_function_name = final_command_line.split(" ")[1].strip()
                        print_argument_info(current_function_name)
                    else:
                        print_functions_info(start_with=last_word)

                    print_seperate_line()
                    print_chars(final_command_line)
                    char, char_id = get_char_input()
                    if (char_id == 27):
                        # esc key
                        clear_screen()
                        break
                    elif char_id in [3]:
                        # ctrl + c key
                        clear_screen()
                        break
                    elif char_id == 127:
                        # delete key
                        final_command_line = final_command_line[:-1]
                    elif char_id == 9:
                        # tab key
                        # do complete
                        if last_word == "":
                            continue
                        new_word = ""
                        if (how_many_words == 0):
                            final_command_line = original_command_line_arguments[0]+" "
                            continue
                        elif (how_many_words == 1):
                            final_command_line = original_command_line_arguments[0]+" "
                            continue
                        elif (how_many_words == 2):
                            # complete function name
                            possible_new_words = []
                            for function_string in function_string_list:
                                if function_string.startswith(last_word):
                                    possible_new_words.append(function_string)
                            if len(possible_new_words) == 1:
                                new_word = possible_new_words[0]
                                # complete a whole word
                                final_command_line = final_command_line[:-len(last_word)]
                                final_command_line += new_word
                            elif len(possible_new_words) == 0:
                                new_word = ""
                                # complete nothing
                            else:
                                # complete common word
                                temp_possible_new_words = [word.lstrip(last_word) for word in possible_new_words]
                                temp_possible_new_words.sort(key=len)
                                the_longest_word = temp_possible_new_words[-1]
                                common_chars = ""
                                end_i = 0
                                while True:
                                    end_i += 1
                                    current_common_chars = the_longest_word[0:end_i]
                                    if all([word.startswith(current_common_chars) for word in temp_possible_new_words]):
                                        common_chars = current_common_chars
                                    if end_i > len(the_longest_word):
                                        break
                                final_command_line += common_chars
                        else:
                            # complete arguments name
                            current_function_name = final_command_line.split(" ")[1].strip()
                            correct_arguments = my_method_and_propertys[current_function_name]["arguments"]
                            for argument_string, value_dict in correct_arguments.items():
                                if argument_string.startswith(last_word):
                                    new_word = argument_string
                                    break
                            if new_word != "":
                                final_command_line = final_command_line[:-len(last_word)]
                                final_command_line += "--{new_word}=".format(new_word=new_word)
                    elif char_id == 10 or char_id == 13:
                        # enter key
                        clear_screen()
                        print(final_command_line)
                        print()
                        self.fire2(class_instance=class_instance, new_arguments=shlex.split(final_command_line.strip()))
                        exit()
                    else:
                        if (final_command_line[-1].strip() == "") and (char.strip() == ""):
                            continue
                        final_command_line += char

            return

        method_name = command_line_arguments[0]
        un_named_arguments = [one for one in command_line_arguments[1:] if not one.startswith('--')]
        named_arguments = [one for one in command_line_arguments[1:] if one.startswith('--')]
        if (method_name in function_string_list):
            one_method = my_method_and_propertys[method_name]
            method_instance = one_method['function_instance']
            right_arguments = one_method['arguments']
            right_arguments_list = one_method['arguments_list']

            custom_arguments = {}

            # for argument that does not have '--name=value', for example "Tools push 'message'""
            for index, one in enumerate(un_named_arguments):
                if index < len(right_arguments_list):
                    argument_name = right_arguments_list[index]['argument_name']
                    argument_value = one.strip()
                    argument_type = right_arguments_list[index]['type_function']

                    if (argument_type != None):
                        custom_arguments[argument_name] = argument_type(argument_value)
                    else:
                        # no type info
                        custom_arguments[argument_name] = str(argument_value)
                        #if str(argument_value).replace('.','',1).isdigit():
                        #    custom_arguments[argument_name] = float(str(argument_value))
                        #else:
                        #    custom_arguments[argument_name] = str(argument_value)

            # for argument that does have '--name=value'
            for one in named_arguments:
                argument_name = one[2:].split("=")[0]
                argument_value = "=".join(one[2:].split("=")[1:])
                argument_type = right_arguments[argument_name]['type_function']
                if (argument_type != None):
                    custom_arguments[argument_name] = argument_type(argument_value)
                else:
                    # no type info
                    custom_arguments[argument_name] = str(argument_value)
                    #if str(argument_value).replace('.','',1).isdigit():
                    #    custom_arguments[argument_name] = float(str(argument_value))
                    #else:
                    #    custom_arguments[argument_name] = str(argument_value)

            #print(f"{method_name} {' '.join(custom_arguments)}")
            method_instance(**custom_arguments)
            return

    def make_it_runnable(self, py_file_path=None):
        #(self, py_file_path: str|None=None):
        """
        make python file runnable

        after use this function, you can run the py_file by: ./your_py_script_name.py
        """
        if py_file_path is None or self._t.exists(py_file_path):
            py_file_path = os.path.join(
                self._t.current_dir, sys.argv[0].strip('./'))
        if os.path.exists(py_file_path):
            codes = self._io.read(py_file_path)
            expected_first_line = '#!/usr/bin/env {}'.format(self._t.py_executable)
            splits = codes.split('\n')
            found = False
            for line in splits:
                if line == expected_first_line:
                    found = True
                    break
            if found == False:
                codes = expected_first_line + '\n' + codes
                self._io.write(py_file_path, codes)
                self._t.run_command('chmod +x {}'.format(py_file_path))

            if not self._disk.executable(py_file_path):
                self._t.run_command('chmod +x {}'.format(py_file_path))

    def make_it_global_runnable(self, py_file_path=None, executable_name=None):
        #(self, py_file_path: str| None=None, executable_name: str | None=None):
        """
        make python file global runnable

        after use this function, you can run the py_file at anywhere by: your_py_script_name.py
        """
        self.make_it_runnable(py_file_path)

        auto_everything_config_folder = "~/.auto_everything"
        bin_folder = os.path.expanduser(os.path.join(auto_everything_config_folder, "bin"))
        if not self._t.exists(bin_folder):
            self._t.run_command("mkdir -p {bin_folder}".format(bin_folder=bin_folder))

        if py_file_path is None or not self._t.exists(py_file_path):
            py_file_path = os.path.join(
                self._t.current_dir, sys.argv[0].strip('./'))

        is_the_first_running = False
        runnable_path = None

        if os.path.exists(py_file_path):
            if executable_name == None:
                _, executable_name = os.path.split(py_file_path)
            runnable_path = os.path.join(bin_folder, executable_name)
            if not os.path.exists(runnable_path):
                is_the_first_running = True

            # remove links that the real file has been moved, or, remove links that match this py_file_path but with a different executable name
            files = os.listdir(bin_folder)
            [self._t.run("cd {bin_folder}; rm {file}".format(bin_folder=bin_folder, file=file)) for file in files if
             not os.path.exists(os.path.join(bin_folder, file))]
            files = self._disk.get_files(bin_folder, recursive=False)
            [self._t.run("rm {file}".format(file=file)) for file in files if
             os.path.realpath(file) == py_file_path and file != runnable_path]

            self._t.run_command("ln -s {py_file_path} {runnable_path}".format(py_file_path=py_file_path, runnable_path=runnable_path))

            bashrc_path = self._t.fix_path("~/.bashrc")
            bashrc_target_line = 'export PATH="$PATH:{bin_folder}"'.format(bin_folder=bin_folder)
            bashrc = self._io.read(bashrc_path)
            if bashrc_target_line not in bashrc.split("\n"):
                bashrc = bashrc + "\n" + bashrc_target_line
                self._t.run_command("touch {bashrc_path}".format(bashrc_path=bashrc_path))
                self._io.write(bashrc_path, bashrc)

        if is_the_first_running and runnable_path:
            print("\n\n------------------\n\nYou could run \n\nsource ~/.bashrc\n\nto get started!")
            print("\n\n------------------\n\nYou could run \n\n{command} -- --completion\n\nto get bash completion scripts".format(command=runnable_path.split('/')[-1]))

    def print(self, data, limit=20):
        #(self, data: Any, limit: int=20):
        """
        print `function help info` or print `dict` with length limit (So you could see the structure easily)
        """
        if callable(data):
            self.help(data)
        else:
            data = copy.deepcopy(data)

            def infinite_loop(the_data):
                the_type = type(the_data)
                if the_type == str:
                    return the_data[:limit] + "..."
                elif the_type == dict:
                    for key, value in the_data.items():
                        the_data[key] = infinite_loop(value)
                    return the_data
                elif the_type == list:
                    return [infinite_loop(element) for element in the_data]
                else:
                    return the_data

            data = infinite_loop(data)
            pprint(data)

    # def _python_code_preprocess(self, python_code: str):
    #     """
    #     { \n } => {}
    #     ( \n ) => ()
    #     \"\"\" \n \"\"\" => add 4 space before every line
    #     \'\'\' \n \'\'\' => add 4 space before every line
    #     > a remind not to touch the comments followed by a function top defination
    #     """
    #     pass

    def generate_documentation_for_a_python_project(self, python_project_folder_path, markdown_file_output_folder_path, only_generate_those_functions_that_has_docstring=False, just_return_string=False):
        #(self, python_project_folder_path: str, markdown_file_output_folder_path: str, only_generate_those_functions_that_has_docstring: bool=False, just_return_string: bool=False):
        all_data_string = ""
        # code_block_match_rule = r"""(?P<code_block>(?:[ \t]*)(?P<code_head>(?:(?:(?:@(?:.*)\s+)*)*(?:(?:class)|(?:(?:async\s+)*def)))[ \t]*(?:\w+)\s*\((?:.*?)\)(?:[ \t]*->[ \t]*(?:(.*)*))?:)(?P<code_body>(?:\n(?:)(?:[ \t]+[^\n]*)|\n)+))"""
        head_information_regex_rule = r"""(?P<class_or_function_top_defination>(?: *@(?:.*?)\n+)* *(?:\s+(?P<is_class>class)|(?P<is_function>def|async +def)) +(?:(?:\n|.)*?):\n+)(?P<documentation>(?:(?:\s+[\"\']{3}(?:(?:\s|.)*?)[\"|\']{3}\n+)?(?:[ \t]*?\#(?:.*?)\n+)*)*)?(?P<class_or_function_propertys>(?(is_class)((?![ \t]+(?:def|class) )(?:(?:.*?): *(?:.*?) *= *(?:.*?)\n)*)|(?:)))?"""
        for file in self._disk.get_files(folder=python_project_folder_path, recursive=True, type_limiter=[".py"], use_gitignore_file=True):
            file_name = self._disk.get_file_name(file)
            if file_name.startswith("_"):
                continue

            raw_content = self._io.read(file)
            result_list = re.findall(pattern=head_information_regex_rule, string=raw_content)
            result_list = [
                {
                    'class_or_function_top_defination': one[0],
                    'is_class': one[1] == 'class',
                    'is_function': one[2] == 'def',
                    'documentation': one[3][0] if len(one[3]) == 1 else one[3],
                    'class_or_function_propertys': one[4]
                }
                for one in result_list
            ]

            text = ""
            for item in result_list:
                class_or_function_top_defination = item["class_or_function_top_defination"]

                # function_name = class_or_function_top_defination.split(" ")[1]
                # if function_name.startswith("_"):
                #     continue

                documentation = item['documentation']
                # documentation = '\n'.join([one[4:] for one in documentation.split('\n')])
                is_class = item["is_class"]
                class_or_function_propertys = item["class_or_function_propertys"]

                heading_space_counting = 0
                for char in class_or_function_top_defination:
                    if char == " ":
                        heading_space_counting += 1
                    else:
                        break

                documentation = documentation.rstrip()
                if only_generate_those_functions_that_has_docstring == True:
                    if len(documentation.strip()) == 0:
                        continue
                class_or_function_propertys = class_or_function_propertys.rstrip() if is_class else ''

                if len(documentation.strip()) != 0 and len(class_or_function_propertys) != 0:
                    text += """
{}
{}
{}
{}pass
                    """.format(
                        class_or_function_top_defination.rstrip(),
                        documentation.rstrip(),
                        class_or_function_propertys,
                        ' ' * heading_space_counting + ' ' * 4
                    )
                elif len(documentation.strip()) != 0 and len(class_or_function_propertys) == 0:
                    text += """
{}
{}
{}pass
                    """.format(
                        class_or_function_top_defination.rstrip(),
                        documentation.rstrip(),
                        ' ' * heading_space_counting + ' ' * 4
                    )
                elif len(documentation.strip()) == 0 and len(class_or_function_propertys) != 0:
                    text += """
{}
{}
{}pass
                    """.format(
                        class_or_function_top_defination.rstrip(),
                        class_or_function_propertys,
                        ' ' * heading_space_counting + ' ' * 4
                    )
                elif len(documentation.strip()) == 0 and len(class_or_function_propertys) == 0:
                    text += """
{}
{}pass
                    """.format(
                        class_or_function_top_defination.rstrip(),
                        ' ' * heading_space_counting + ' ' * 4
                    )

            markdown_template = """
# {file_name}

```python
{text}
```
            """.format(
                file_name=file_name,
                text=text.strip()
            )

            if just_return_string == False:
                output_file_path = self._disk.join_paths(markdown_file_output_folder_path, file_name[:-len(".py")] + ".md")
                self._io.write(file_path=output_file_path, content=markdown_template)

            all_data_string += markdown_template.strip() + "\n\n_______\n\n"

        return all_data_string

if __name__ == "__main__":
    py = Python()
    py.print({
        "hi": "dasssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssshgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggglddlahkdhkashgdkagda",
        "ok": {
            "fuck": "dhaslhdhagkdhaksghdashkgsadsagdsalhgsahd",
            "dhashd": "dsahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhagdagdas",
            "dsadf": [{"sdf": "sadddddddddddddddddddddddddddddddddd"}, "asddddddddddddddddddddddddd"]
        }
    }, limit=25)
