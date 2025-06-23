import json
import os


class IO():
    """
    This is for normal IO processing
    """

    def __init__(self):
        self.current_dir = os.getcwd()
        self.__log_path = os.path.join(self.current_dir, '.log')

    def make_sure_sudo_permission(self):
        """
        exit if you don't have sudo permission
        """
        if os.getuid() != 0:
            print("\n I only got my super power if you run me with sudo!")
            exit()

    def read(self, file_path, auto_detect_encoding=False, encoding="utf-8"):
        """
        read text from txt file

        Parameters
        ----------
        file_path
            txt file path
        encoding
            utf-8 or ascii, ascii would be smaller for text storage
        """
        if (auto_detect_encoding == True):
            import chardet
            rawdata = open(file_path, "rb").read()
            result = chardet.detect(rawdata)
            if (result != None):
                encoding = result['encoding']

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding=encoding, errors="ignore") as f:
                result = f.read()
            return result
        else:
            print("File '" + file_path + "' does not exists.")
            return ""

    def write(self, file_path, content, encoding="utf-8"):
        """
        write text into txt file

        Parameters
        ----------
        file_path
            target txt file path
        content
            text string
        encoding
            utf-8 or ascii, ascii would be smaller for text storage
        """
        with open(file_path, 'w', encoding=encoding, errors="ignore") as f:
            f.write(content)

    def append(self, file_path, content):
        """
        append text at the end of a txt file

        Parameters
        ----------
        file_path
            target txt file path
        content
            text string
        """
        with open(file_path, 'a', encoding="utf-8", errors="ignore") as f:
            f.write(content)

    def string_to_hex(self, utf_8_string):
        """
        Don't use hex, it adds complexity
        """
        return utf_8_string.encode("utf-8", errors="ignore").hex()

    def hex_to_string(self, hex_string):
        """
        Don't use hex, it adds complexity
        """
        return bytes.fromhex(hex_string).decode("utf-8", errors="ignore")

    def bytes_list_to_int_list(self, bytes_data):
        """
        a byte can be represented as a integer between 0 and 255.
        actually, if you loop python bytes object, you'll get a list of integer.
        > a number between 0 and 255 can be a chracter in ASCII table. I recommand use ASCII to save text data, because it is easy to read from bytes data from disk storage.
        """
        list_ = [None] * len(bytes_data)
        if type(bytes_data) == bytes or type(bytes_data) == bytearray:
            for index, int_byte in enumerate(bytes_data):
                list_[index] = int_byte
        else:
            for index, byte in enumerate(bytes_data):
                zero_and_one_string_for_one_byte = bin(byte)[2:]
                leading_zeros = ((8-len(zero_and_one_string_for_one_byte)) * '0')
                zero_and_one_string_for_one_byte = leading_zeros + zero_and_one_string_for_one_byte
                list_[index] = int(zero_and_one_string_for_one_byte, 2)
        return list_

    def int_list_to_bytes_list(self, int_list, big_or_little="little"):
        """
        a byte can be represented as a integer between 0 and 255
        to make it simple, you can think a byte as an integer in range of [0, 255]. actually, if you loop python bytes object, you'll get a list of integer.
        > a number between 0 and 255 can be a chracter in ASCII table

        The return bytearray object can get converted to bytes by using 'bytes(a_bytearray)'

        Why ask you to choose big or little?
        Let's assume you have a byte: 00000001, it is normal in your computer, it is 'little'
        But after you send it from right to left to another device, it becomes 10000000, it is 'big'. But if the other side do a reverse to let it become original data 00000001, they can still use 'little' to do the right parse.

        I think for those old generation of people, they are stupid. If they could use 'little' all the time by doing a list[::-1] at the other side in a communication, why they use 'big'?
        """
        use_little = True
        if big_or_little != "little":
            use_little = False

        a_bytearray = bytearray(range(len(int_list)))
        for index, int_between_0_and_255 in enumerate(int_list):
            if use_little:
                a_bytearray[index] = int_between_0_and_255
            else:
                a_bytearray[index] = int_between_0_and_255.to_bytes(2, big_or_little)[0]
        return a_bytearray

    def bytes_to_binary_zero_and_one(self, bytes_data):
        """
        Yes, a byte can be a integer in range of [0, 255], but if you want to send data over electrical line, you have to send 0 and 1 signal, which is 0v and 5v voltage.
        So you have to convert [0,255] number into a 8 length of string that only has 0 and 1.

        The return value is a list of zero and one string, similar to [00000001, 00000010, 00000011]

        Why for a byte, it has 8 number of zero or one? Because 2^8 == 256, you have to use 8 length of 0 and 1 to represent a number between 0 and 255 (a byte can represent a integer in range of [0,255])
        That's also why in C language, you use char or int to represent a byte. a byte is nothing but a integer between 0 and 255.

        > By the way, if you want to use 0 and 1 to represent a bigger number, for example 65536, you have to use 16 length of 0 and 1 number, because 2^16==65536.
        """
        list_ = [None] * len(bytes_data)
        for index, byte in enumerate(bytes_data):
            zero_and_one_string_for_one_byte = bin(byte)[2:]
            leading_zeros = ((8-len(zero_and_one_string_for_one_byte)) * '0')
            zero_and_one_string_for_one_byte = leading_zeros + zero_and_one_string_for_one_byte
            list_[index] = zero_and_one_string_for_one_byte
        return list_

    def binary_zero_and_one_to_bytes(self, zero_and_one_string_list):
        a_bytearray = bytearray(range(len(zero_and_one_string_list)))
        for index, binary_string in enumerate(zero_and_one_string_list):
            a_bytearray[index] = int(binary_string, 2)#.to_bytes(2, big_or_little)[0]
        return bytes(a_bytearray)

    def int_byte_to_binary_string(self, a_number):
        """
        For a byte or ascii number in range of [0,255], the binary_string should have 8 chracters, similar to 01100100
        """
        try:
            return format(a_number, "b")
        except Exception as e:
            # yingshaoxo method of Hexadecimal conversion
            half_number_list = [[0,128], [0,64], [0,32], [0,16], [0,8], [0,4], [0,2], [0,1]]
            binary_string = ""
            for _, one in half_number_list:
                if a_number >= one:
                    binary_string += "1"
                    a_number -= one
                else:
                    binary_string += "0"
            return binary_string

    def string_binary_to_int_byte(self, binary_string):
        """
        For a byte or ascii number in range of [0,255], the binary_string should have 8 chracters, similar to 01100100
        Which means a byte has 8 characters. The binary_string length you gave to me should be 8.
        """
        try:
            return int(binary_string, 2)
        except Exception as e:
            half_number_list = [[0,128], [0,64], [0,32], [0,16], [0,8], [0,4], [0,2], [0,1]]
            the_number = 0
            index = 0
            for _, one in half_number_list:
                if binary_string[index] == "1":
                    the_number += one
                index += 1
            return the_number

    def __make_sure_txt_exist(self, path):
        if not os.path.exists(path):
            self.write(path, "")

    def read_settings(self, key, defult):
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            data = json.loads(text)
            return data[key]
        except Exception as e:
            print(e)
            return defult

    def write_settings(self, key, value):
        try:
            settings_path = os.path.join(self.current_dir, 'settings.ini')
            self.__make_sure_txt_exist(settings_path)
            text = self.read(settings_path)
            try:
                data = json.loads(text)
            except Exception as e:
                print(e)
                data = dict()
            data.update({key: value})
            text = json.dumps(data)
            self.write(settings_path, text)
            return True
        except Exception as e:
            print(e)
            return False

    def empty_settings(self):
        settings_path = os.path.join(self.current_dir, 'settings.ini')
        try:
            self.write(settings_path, "")
            os.remove(settings_path)
        except Exception as e:
            print(e)

    def log(self, text):
        import time
        text = str(text)
        now = time.asctime(time.localtime(time.time()))
        text = '\n' * 2 + text + '   ' + '({})'.format(now)
        self.append(self.__log_path, text)

    def get_logs(self):
        return self.read(self.__log_path)


class File_IO:
    def __init__(self, filename, mode=None):
        # 'wb' for write bytes but will clear the whole file first, 'w' for write string
        # 'rb+' for reading bytes and write bytes at any position
        # 'ab' for appending data at the end
        self.filename = filename

        if mode == None:
            if self.exists():
                mode = "rb+"
            else:
                mode = "wb+"
        self.mode = mode

        print(mode)
        self.file = open(filename, mode)

    def read(self, size=-1):
        return self.file.read(size)

    def write(self, data):
        if 'w' in self.mode or 'a' in self.mode or '+' in self.mode:
            self.file.write(data)

    def seek(self, offset, whence=None):
        # where to start: os.SEEK_END, start from end; os.SEEK_SET, start from beginning
        if whence == None:
            self.file.seek(offset)
        else:
            self.file.seek(offset, whence)

    def seek_from_end(self, negative_offset=0):
        # only support binary mode
        self.file.seek(negative_offset, os.SEEK_END)

    def tell(self):
        # get current file pointer that was set by seek
        return self.file.tell()

    def close(self):
        self.file.close()

    def get_size(self):
        try:
            return os.path.getsize(self.filename)
        except Exception as e:
            info = os.stat(self.filename)
            filesize = info[6]
            return filesize

    def exists(self):
        try:
            os.stat(self.filename)
            return True
        except Exception as e:
            return False

    def flush(self):
        self.file.flush()


class Yingshaoxo_List():
    def __init__(self):
        self.memory_slots_number = 16
        # create a list with 16 memory slots
        self.items = [None] * self.memory_slots_number
        self.length = 0

        self.iteration_not_done = False
        self._current_iterate_index = 0

    def _copy_old_items_to_new_items_based_on_memory_slots_number(self):
        new_items = [None] * self.memory_slots_number
        for i in range(self.length):
            new_items[i] = self.items[i]
        self.items = new_items

    def _double_the_memory_slots_number(self):
        self.memory_slots_number = self.memory_slots_number * 2
        self._copy_old_items_to_new_items_based_on_memory_slots_number()

    def _cut_half_the_memory_slots_number(self):
        new_slots_number = max(8, int(self.memory_slots_number / 2))
        if new_slots_number >= self.length:  # Ensure no data loss
            self.memory_slots_number = new_slots_number
            self._copy_old_items_to_new_items_based_on_memory_slots_number()

    def print(self):
        print("[", end="")
        for i in range(self.length):
            print(self.items[i], end="")
            if i != self.length - 1:
                print(", ", end="")
        print("]\n", end="")

    def append(self, an_element):
        if self.length >= self.memory_slots_number:
            # need to create a new list with self.memory_slots_number * 2 slots
            self._double_the_memory_slots_number()

        self.items[self.length] = an_element
        self.length += 1

    def index(self, an_element):
        for i in range(self.length):
            if self.items[i] == an_element:
                return i
        return None

    def delete(self, index):
        if index >= 0 and index < self.length:
            #del self.items[index]
            new_items = [None] * self.memory_slots_number
            new_index = 0
            for i in range(self.length):
                if i != index:
                    new_items[new_index] = self.items[i]
                    new_index += 1
            self.items = new_items
            self.length -= 1

        if self.length < int(self.memory_slots_number / 2):
            # need to create a new list with self.memory_slots_number / 2 slots
            self._cut_half_the_memory_slots_number()

    def set(self, index, an_element):
        if index < 0 or index >= self.length:
            return False
        else:
            self.items[index] = an_element
            return True

    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        return self.items[index]

    def insert(self, index, an_element):
        if index < 0 or index >= self.length:
            return

        if self.length >= self.memory_slots_number:
            # need to create a new list with self.memory_slots_number * 2 slots
            self._double_the_memory_slots_number()

        new_items = [None] * self.memory_slots_number
        new_index = 0
        for i in range(self.length):
            if i == index:
                new_items[new_index] = an_element
                new_index += 1
            new_items[new_index] = self.items[i]
            new_index += 1
        self.items = new_items
        self.length += 1

    def sublist(self, start_index, end_index):
        sub_list = Yingshaoxo_List()
        if start_index >= 0 and end_index <= self.length and start_index < end_index:
            for i in range(start_index, end_index):
                sub_list.append(self.items[i])
                # better do a copy for those values
        return sub_list

    def start_iteration(self):
        # most of the time, it is True
        self.iteration_not_done = self.length > 0
        self._current_iterate_index = 0

    def get_next_one(self):
        if not self.iteration_not_done or self._current_iterate_index >= self.length:
            self.iteration_not_done = False
            return None

        an_element = self.items[self._current_iterate_index]
        self._current_iterate_index += 1

        if self._current_iterate_index >= self.length:
            self.iteration_not_done = False

        return an_element


class Yingshaoxo_Dict():
    """
    This dict is based on yingshaoxo hash table algorithm.
    """
    def __init__(self, second_level=False):
        self.key_and_value_distribution_list = [None] * 255
        self.second_level = second_level
        if second_level == True:
            for i in range(255):
                # for each branch, it has [key_list, value_list]
                self.key_and_value_distribution_list[i] = [
                    [], []
                ]
        else:
            for i in range(255):
                self.key_and_value_distribution_list[i] = Yingshaoxo_Dict(second_level=True)

    def _get_yingshaoxo_hash_id_of_a_string_for_the_first_level(self, key):
        """
        It returns a index between [0, 254]
        """
        key = str(key)
        return (ord(key[0]) + ord(key[-1])) % 255

    def _get_yingshaoxo_hash_id_of_a_string(self, key):
        """
        It returns a index between [0, 254]
        """
        key = str(key)
        #return ord(key[int(len(key)/2)]) % 255
        hash_id = 0
        sign = True
        for byte in key[::3].encode("utf-8"):
            if sign == True:
                hash_id += byte
            else:
                hash_id -= byte
            sign = not sign
        hash_id = hash_id % 255
        return hash_id

    def set(self, key, value):
        if self.second_level == True:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string(key)
            # python pass list as pointer, so we will change original list
            keys, values = self.key_and_value_distribution_list[hash_id]
            for index, old_key in enumerate(keys):
                if old_key == key:
                    values[index] = value
                    return
            keys.append(key)
            values.append(value)
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            a_dict.set(key, value)

    def get(self, key):
        """
        If not exists, we return None
        """
        if self.second_level == True:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string(key)
            keys, values = self.key_and_value_distribution_list[hash_id]
            for index, old_key in enumerate(keys):
                if old_key == key:
                    return values[index]
            return None
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            return a_dict.get(key)

    def delete(self, key):
        if self.second_level == True:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string(key)
            keys, values = self.key_and_value_distribution_list[hash_id]
            target_index = None
            for index, old_key in enumerate(keys):
                if old_key == key:
                    target_index = index
                    break
            if target_index != None:
                del keys[target_index]
                del values[target_index]
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            a_dict.delete(key)

    def has_key(self, key):
        if self.second_level == True:
            if self.get(key) == None:
                return False
            else:
                return True
        else:
            hash_id = self._get_yingshaoxo_hash_id_of_a_string_for_the_first_level(key)
            a_dict = self.key_and_value_distribution_list[hash_id]
            return a_dict.has_key(key)


class MyIO():
    def __init__(self):
        import io
        import hashlib
        import base64
        self.io = io
        self.hashlib = hashlib
        self.base64 = base64

    def string_to_md5(self, text):
        result = self.hashlib.md5(text.encode())
        return result.hexdigest()

    def base64_to_bytesio(self, base64_string):
        img_data = self.base64.b64decode(base64_string)
        return self.io.BytesIO(img_data)

    def bytesio_to_base64(self, bytes_io):
        """
        bytes_io: io.BytesIO()
        """
        bytes_io.seek(0)
        return self.base64.b64encode(bytes_io.getvalue()).decode()

    def hex_to_bytes(self, hex_string):
        return bytes.fromhex(hex_string)

    def bytes_to_hex(self, bytes_data):
        """
        bytes_data: bytes()
        """
        return bytes_data.hex()


if __name__ == "__main__":
    pass
    """
    io = IO()
    zero_and_one_list = io.bytes_to_binary_zero_and_one(b"123")
    print(zero_and_one_list)
    bytes_list = io.binary_zero_and_one_to_bytes(zero_and_one_list)
    print(bytes_list)
    int_list = io.bytes_list_to_int_list(bytes_list)
    print(int_list)
    new_bytes_list = io.int_list_to_bytes_list(int_list)
    int_list = io.bytes_list_to_int_list(new_bytes_list)
    print(int_list)
    """
    """
    a_dict = Yingshaoxo_Dict()
    print(a_dict.get("hi"))
    a_dict.set("hi", "yingshaoxo")
    print(a_dict.get("hi"))
    a_dict.set("hi", "everyone")
    print(a_dict.get("hi"))
    a_dict.delete("hi")
    print(a_dict.get("hi"))
    """
    """
    a_list = Yingshaoxo_List()
    a_list.print()
    a_list.append(1)
    a_list.append(2)
    a_list.append(3)
    a_list.print()
    print(a_list.index(3))
    a_list.set(2,'hi')
    a_list.print()
    a_list.delete(0)
    a_list.print()
    a_list.insert(0, 0)
    a_list.print()
    print(a_list.get(3))
    a_list.append(4)
    a_list.print()
    a_list.sublist(0,4).print()

    a_list.start_iteration()
    while (a_list.iteration_not_done):
        an_element = a_list.get_next_one()
        print(an_element)
    """
