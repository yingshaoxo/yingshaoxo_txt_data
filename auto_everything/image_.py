import json


def my_print(message="", end="\n", flush=False):
    import sys
    sys.stdout.write(str(message))
    sys.stdout.write(end)
    if flush == True:
        sys.stdout.flush()


terminal_color_dict = {
    "black": {"value": '\033[40m \033[00m', "rgb": [0,0,0]},
    "red": {"value": '\033[41m \033[00m', "rgb": [255,0,0]},
    "green": {"value": '\033[42m \033[00m', "rgb": [0,255,0]},
    "yellow": {"value": '\033[43m \033[00m', "rgb": [255,255,0]},
    "blue": {"value": '\033[44m \033[00m', "rgb": [0,0,255]},
    "purple": {"value": '\033[45m \033[00m', "rgb": [255,0,255]},
    "cyan": {"value": '\033[46m \033[00m', "rgb": [0,255,255]},
    "lightgrey": {"value": '\033[47m \033[00m', "rgb": [128,128,128]},
    #"white": {"value": '\033[107m \033[00m', "rgb": [255,255,255]},
}


def choose_a_color_from_base_color(r,g,b):
    min_distance = 10000
    the_similar_one = terminal_color_dict["black"]
    for color in terminal_color_dict.values():
        the_color_rgb = color["rgb"]
        r2, g2, b2 = the_color_rgb
        distance = ((r2-r)**2 + (g2-g)**2 + (b2-b)**2)**0.5
        if distance < min_distance:
            min_distance = distance
            the_similar_one = color
    return the_similar_one


def get_main_color_list_from_an_image(a_image, ratio=0.8):
    ratio = 1 - ratio
    counting_dict = {}

    a_image = a_image.copy()
    a_image.resize(30,30)
    height, width = a_image.get_shape()
    for row_index in range(height):
        for column_index in range(width):
            color = [str(one) for one in a_image[row_index][column_index]]
            if color[-1] != '255':
                continue
            color = ",".join(color)
            if color in counting_dict.keys():
                counting_dict[color] += 1
            else:
                counting_dict[color] = 1
    sort_items = list(counting_dict.items())
    sort_items.sort(key=lambda x: -x[1])

    main_color_list = sort_items[:max(int(len(sort_items)*ratio), 3)]
    main_color_list = [[int(each) for each in one[0].split(",")] for one in main_color_list]
    return main_color_list


color_cache_dict = dict()
def get_a_color_from_base_color(r,g,b,a,color_list):
    id_ = str(r) + "," + str(g) + "," + str(a) + str(color_list)
    if id_ in color_cache_dict:
        return color_cache_dict[id_]

    min_distance = 10000
    the_similar_one = color_list[0]
    for color in color_list:
        r2, g2, b2, _ = color
        distance = ((r2-r)**2 + (g2-g)**2 + (b2-b)**2)**0.5
        if distance < min_distance:
            min_distance = distance
            the_similar_one = color

    color_cache_dict[id_] = the_similar_one
    return the_similar_one


def change_image_style_without_ai(source_image, target_image, simple_mode=True, target_color_numbers=900):
    # yingshaoxo image style transformer algorithm:
    # 1. get all colors in target_image
    # 2. for each source image color, choose one that has minimum distance in target image colors
    # 3. use cache result to speed up the processing
    """
    For deep learning version, what they did is: split source images and target images as sub image slots, 1 to 1 link by using dict. For a new input image, first they found most similar one in old source_images database, then for each smaller sub_image in that input image, they found their similar sub_image in target image sub_image database. There has an threshold for similarity, if can't found a target sub_image in target image dataset, then it will try to split that sub_image into a smaller sub_image list, then try to found it again until one pixel level. When the similarity threshold equal to 1, which means every new input image is actually in the dataset, the software is doing 1 to 1 translation with no flexibility. When the similarity threshold equal to 0, the software will output nothing or random noise picture.
    """
    source_image = source_image.copy()

    canvas_size = int(target_color_numbers ** 0.5)
    target_image = target_image.copy().resize(canvas_size,canvas_size)
    target_color_set = set()
    target_image_color_list = []
    for row in target_image.raw_data:
        for color in row:
            color_string = "_".join([str(one) for one in color])
            if color_string in target_color_set:
                continue
            else:
                target_color_set.add(color_string)
                target_image_color_list.append(color)

    image_style_color_dict = dict() #string as key, target_color_as_value
    height, width = source_image.get_shape()
    for y in range(height):
        for x in range(width):
            color = source_image[y][x]
            color_string = "_".join([str(one) for one in color])
            if color_string in image_style_color_dict:
                source_image[y][x] = image_style_color_dict[color_string]
            else:
                min_distance = 99999
                the_best_color = color
                r2, g2, b2, c2 = color
                for target_color in target_image_color_list:
                    r, g, b, c = target_color
                    if simple_mode == True:
                        distance = ((r2-r)**2 + (g2-g)**2 + (b2-b)**2)**0.5
                    else:
                        distance = ((r2-r)**2 + (g2-g)**2 + (b2-b)**2 + (c2-c)**2)**0.5
                    if distance < min_distance:
                        min_distance = distance
                        the_best_color = target_color
                image_style_color_dict[color_string] = the_best_color
                source_image[y][x] = image_style_color_dict[color_string]

    return source_image


def change_image_style_with_random_number(source_image, random_numbers):
    import colorsys

    if random_numbers == None:
        import random
        random_number1 = random.randint(1, 255)
        random_number2 = random.randint(1, 255)
        print("random_numbers:", random_number1, random_number2)
    else:
        random_number1 = random_numbers[0]
        random_number2 = random_numbers[1]

    source_image = source_image.copy()

    color_dict = dict()
    for row in source_image.raw_data:
        for color in row:
            if color[3] != 255:
                continue
            color_string = ",".join([str(one) for one in color])
            if color_string in color_dict:
                continue
            else:
                r, g, b, _ = color
                h,s,v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                h,s,v = h*255, s*255, v*255
                h += random_number1
                s += random_number2
                h = h % 255
                s = s % 255
                r,g,b = colorsys.hsv_to_rgb(h/255, s/255, v/255)
                target_color = [int(r*255),int(g*255),int(b*255),255]
                color_dict[color_string] = target_color

    height, width = source_image.get_shape()
    for y in range(height):
        for x in range(width):
            color = source_image[y][x]
            if color[3] != 255:
                continue
            color_string = ",".join([str(one) for one in color])
            source_image[y][x] = color_dict[color_string]

    return source_image


def to_mosaic(self, ratio=0.99, kernel_number=6):
    """
    ratio: 0 to 1, more close to 1, more simplified

    It removes ratio big pixels for each 8x8 sub_image, for example ratio=0.6 means remove 60% noise pixels from 8x8 sub_image
    """
    new_image = self.copy()
    ratio = 1-ratio

    def get_main_color_list_by_ratio(pixel_list, ratio):
        counting_dict = {}
        a_list = []
        for color in pixel_list:
            color = [str(one) for one in color]
            color = ",".join(color)
            if color in counting_dict.keys():
                counting_dict[color] += 1
            else:
                counting_dict[color] = 1
        sort_items = list(counting_dict.items())
        sort_items.sort(key=lambda x: -x[1])

        main_color_list = sort_items[:max(int(len(sort_items)*ratio), 3)]
        main_color_list = [[int(each) for each in one[0].split(",")] for one in main_color_list]
        return main_color_list

    sub_image_pixel_numbers = kernel_number * kernel_number
    height, width = new_image.get_shape()
    height_step_number = int(height/kernel_number)
    width_step_number = int(width/kernel_number)
    for y_ in range(height_step_number):
        y_start = y_ * kernel_number
        y_end = y_start + kernel_number
        if y_end >= height:
            y_end = height - 1
        for x_ in range(width_step_number):
            x_start = x_ * kernel_number
            x_end = x_start + kernel_number
            if x_end >= width:
                x_end = width - 1
            index_list = [None] * sub_image_pixel_numbers
            real_pixel_list = [None] * sub_image_pixel_numbers
            counting = 0
            red_counting = 0
            green_counting = 0
            blue_counting = 0
            transparent_counting = 0
            for y_index in range(y_start, y_end):
                for x_index in range(x_start, x_end):
                    pixel = new_image.raw_data[y_index][x_index]
                    index_list[counting] = [y_index, x_index]
                    real_pixel_list[counting] = pixel
                    red_counting += pixel[0]
                    green_counting += pixel[1]
                    blue_counting += pixel[2]
                    transparent_counting += pixel[3]
                    counting += 1
            real_sub_image_pixel_numbers = counting
            index_list = [one for one in index_list if one != None]
            real_pixel_list = [one for one in real_pixel_list if one != None]
            r_mean = int(red_counting / real_sub_image_pixel_numbers)
            g_mean = int(green_counting / real_sub_image_pixel_numbers)
            b_mean = int(blue_counting / real_sub_image_pixel_numbers)
            a_mean = int(transparent_counting / real_sub_image_pixel_numbers)
            main_color_list = get_main_color_list_by_ratio(real_pixel_list, ratio)
            new_pixel_dict = {}
            for index, pixel in enumerate(real_pixel_list):
                y,x = index_list[index]
                #this_pixel = [int((r_mean+pixel[0])/2), int((g_mean+pixel[1])/2), int((b_mean+pixel[2])/2), int((transparent_counting+pixel[3])/2)]
                this_pixel = pixel
                pixel_string = str(pixel)
                if pixel_string in new_pixel_dict:
                    new_pixel = new_pixel_dict[pixel_string]
                else:
                    new_pixel = pixel
                    minimum_distance = 99999
                    for safe_color in main_color_list:
                        difference = ((this_pixel[0] - safe_color[0])**2 + (this_pixel[1] - safe_color[1])**2 + (this_pixel[2] - safe_color[2])**2 + (this_pixel[3] - safe_color[3])**2) ** 0.5
                        if difference < minimum_distance:
                            minimum_distance = difference
                            new_pixel = safe_color
                    new_pixel_dict[pixel_string] = new_pixel
                new_image.raw_data[y][x] = new_pixel

    return new_image


def get_simplified_image_in_an_accurate_way(self, level=2, extreme_color_number=None, predefined_color_list=None):
    """
    level: 2 to infinite, the bigger, the more simplified
    extreme_color_number: 20 is enough, it means the whole picture will only use 20 colors

    better use a simple resize to get main_color_list, for example, extreme_color_number == 9, then we have to resize the image to 3x3 to get 9 main colors.
    """
    new_image = self.copy()

    main_color_set = set()

    def get_main_color_for_a_sub_window(pixel_list):
        counting_dict = {}
        a_list = []
        for color in pixel_list:
            color = [str(one) for one in color]
            color = ",".join(color)
            if color in counting_dict.keys():
                counting_dict[color] += 1
            else:
                counting_dict[color] = 1
        sort_items = list(counting_dict.items())
        sort_items.sort(key=lambda x: -x[1])
        color_list_length = len(sort_items)

        target = None
        index = 0
        while True:
            color, counting = sort_items[index]
            if color in main_color_set:
                pass
            else:
                main_color_set.add(color)
                target = color
                break
            index += 1
            if index >= color_list_length:
                break
        return target

    def get_main_color_list_from_set():
        main_color_list = [[int(each) for each in one.split(",")] for one in main_color_set]
        return main_color_list

    height, width = new_image.get_shape()
    #kernel_number = 30
    kernel_number = int((64/1920) * width)
    sub_image_pixel_numbers = kernel_number * kernel_number
    height_step_number = int(height/kernel_number)
    width_step_number = int(width/kernel_number)
    for y_ in range(height_step_number):
        y_start = y_ * kernel_number
        y_end = y_start + kernel_number
        if y_end >= height:
            y_end = height - 1
        for x_ in range(width_step_number):
            x_start = x_ * kernel_number
            x_end = x_start + kernel_number
            if x_end >= width:
                x_end = width - 1
            index_list = [None] * sub_image_pixel_numbers
            real_pixel_list = [None] * sub_image_pixel_numbers
            counting = 0
            for y_index in range(y_start, y_end):
                for x_index in range(x_start, x_end):
                    pixel = new_image.raw_data[y_index][x_index]
                    index_list[counting] = [y_index, x_index]
                    real_pixel_list[counting] = pixel
                    counting += 1
            real_sub_image_pixel_numbers = counting
            index_list = [one for one in index_list if one != None]
            real_pixel_list = [one for one in real_pixel_list if one != None]
            get_main_color_for_a_sub_window(real_pixel_list)

    if predefined_color_list == None:
        main_color_list = get_main_color_list_from_set()
        if extreme_color_number != None:
            from functools import cmp_to_key
            def compare_color(color1, color2):
                difference = ((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2 + (color1[3] - color2[3])**2) ** 0.5
                """
                a_grayscale = max(min(int(0.2989 * color1[0] + 0.5870 * color1[1] + 0.1140 * color1[2]), 255), 0)
                b_grayscale = max(min(int(0.2989 * color2[0] + 0.5870 * color2[1] + 0.1140 * color2[2]), 255), 0)
                difference = abs(a_grayscale - b_grayscale)
                """
                return difference
            main_color_list = list(sorted(main_color_list, key=cmp_to_key(compare_color)))[-extreme_color_number:]
        else:
            length_of_main_color = len(main_color_list)
            if level >= length_of_main_color/2:
                level = int(length_of_main_color/3)
            main_color_list.sort(key=lambda one: max(min(int(0.2989 * one[0] + 0.5870 * one[1] + 0.1140 * one[2]), 255), 0))
            new_main_color_list = []
            for i in range(0, len(main_color_list), level):
                new_main_color_list.append(main_color_list[i])
            main_color_list = new_main_color_list
    else:
        main_color_list = predefined_color_list

    new_pixel_dict = {}
    for y in range(height):
        for x in range(width):
            old_pixel = new_image.raw_data[y][x]
            if old_pixel[3] == 0:
                continue
            pixel_string = str(old_pixel)
            if pixel_string in new_pixel_dict:
                new_pixel = new_pixel_dict[pixel_string]
            else:
                new_pixel = pixel
                minimum_distance = 99999
                for safe_color in main_color_list:
                    #difference = ((old_pixel[0] - safe_color[0])**2 + (old_pixel[1] - safe_color[1])**2 + (old_pixel[2] - safe_color[2])**2 + (old_pixel[3] - safe_color[3])**2) ** 0.5
                    difference = (abs(old_pixel[0] - safe_color[0]) + abs(old_pixel[1] - safe_color[1]) + abs(old_pixel[2] - safe_color[2])) / 3
                    if difference < minimum_distance:
                        minimum_distance = difference
                        new_pixel = safe_color
                new_pixel_dict[pixel_string] = new_pixel
            new_image.raw_data[y][x] = new_pixel

    return new_image

def get_simplified_image_in_a_quick_way(self, level=25):
    """
    level: 2 to infinite, the bigger, the more simplified

    It simplify the old image by "(rgb_value/255)*level". So we can get color group index which representes shapes(groups) in animation or normal picture.
    Then for each color group, we treat it as a list. We get old image pixel list based on that color group pixel index. We sort that list by using greyscale value. For each list, we do a count, we only get first 3 top color.
    Then for all pixel in old picture, we use root error to choose most similar color from top color list. It is very quick, because for each color index list, we only have 3 color to compare with.

    You can think this method as audio multiple tracks, some of them are music, some of them are human voice. We process each track one to one to speed up the process and accuracy.
    """
    new_image = self.copy()
    new_image = new_image.fill_transparent_color([0,0,0,0])
    greyscale_image = rgb_to_greyscale(new_image, simple_mode=True)

    index_tracks = dict()
    color_tracks = dict()
    height, width = greyscale_image.get_shape()
    for y in range(height):
        for x in range(width):
            greyscale_value = greyscale_image.raw_data[y][x]
            if greyscale_value[3] != 255:
                continue
            greyscale_value = greyscale_value[0]
            old_rgb_color_string = str(new_image[y][x])
            class_id = int(greyscale_value / 255 * level)
            if class_id in index_tracks:
                index_tracks[class_id].append([y, x])
                if old_rgb_color_string in color_tracks[class_id]:
                    color_tracks[class_id][old_rgb_color_string][0] += 1
                else:
                    color_tracks[class_id][old_rgb_color_string] = [1, [y,x]]
            else:
                index_tracks[class_id] = [[y, x]]
                color_tracks[class_id] = dict({old_rgb_color_string: [1, [y,x]]})

    the_cache = dict()
    target_color_tracks = dict()
    for track_key in color_tracks.keys():
        temp_color_list = list(color_tracks[track_key].items())
        temp_color_list.sort(key=lambda one: one[1][0])
        # start, middle, end color as main color
        if len(temp_color_list) >= 3:
            main_color_list = [temp_color_list[0][1][1], temp_color_list[int(len(temp_color_list)/3)][1][1], temp_color_list[-1][1][1]]
        elif len(temp_color_list) == 2:
            main_color_list = [temp_color_list[0][1][1], temp_color_list[-2][1][1], temp_color_list[-1][1][1]]
        else:
            main_color_list = [temp_color_list[0][1][1], temp_color_list[0][1][1], temp_color_list[0][1][1]]
        new_main_color_list = []
        for y,x in main_color_list:
            new_main_color_list.append(new_image[y][x])
        for y,x in index_tracks[track_key]:
            old_pixel = new_image[y][x]
            new_pixel = old_pixel
            pixel_string = str(old_pixel)
            if pixel_string in the_cache:
                new_pixel = the_cache[pixel_string]
            else:
                minimum_distance = 99999
                for safe_color in new_main_color_list:
                    difference = ((old_pixel[0] - safe_color[0])**2 + (old_pixel[1] - safe_color[1])**2 + (old_pixel[2] - safe_color[2])**2) ** 0.5
                    if difference < minimum_distance:
                        minimum_distance = difference
                        new_pixel = safe_color
                the_cache[pixel_string] = new_pixel
            new_image[y][x] = new_pixel

    return new_image

def rgb_to_greyscale(image, simple_mode=False):
    new_image = image.copy()
    height, width = new_image.get_shape()
    for y in range(height):
        for x in range(width):
            pixel = new_image.raw_data[y][x]
            red, green, blue, transparent = pixel
            if transparent == 0:
                continue
            if simple_mode == False:
                grayscale = max(min(int(0.2989 * red + 0.5870 * green + 0.1140 * blue), 255), 0)
            else:
                grayscale = int((red + green + blue) / 3)
            new_image.raw_data[y][x] = [grayscale, grayscale, grayscale, 255]
    return new_image

def single_pixel_rgb_to_hsv(r, g, b, no_255=False):
    """
    Here the h,s,v all in range of [0, 255]
    """
    """
    HSV(Hue, Saturation, Value) is a color space created by A. R. Smith in 1978. The parameters of color in this model are hue (H), saturation (S) and brightness (V).
    Hue H: measured by angle, the value range is 0 ~ 360, and calculated counterclockwise from red, with red being 0, green being 120 and blue being 240. Their complementary colors are: yellow is 60, cyan is 180 and magenta is 300;
    Saturation s: the value range is 0.0 ~ 1.0;
    Brightness v: the value range is 0.0 (black) ~ 1.0 (white).
    RGB color model is made for hardware displaying, while HSV(Hue Saturation Value) color is model for virtual world.
    """
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    if no_255 == False:
        return int((h/360)*255), int(s*255), int(v*255)
    else:
        return h,s,v

def single_pixel_hsv_to_rgb(h, s, v, no_255=False):
    """
    Here the r,g,b all in range of [0, 255]
    """
    if no_255 == False:
        h = float((h/255)*360)
        s = float(s/255)
        v = float(v/255)
    else:
        h = float(h)
        s = float(s)
        v = float(v)
    h60 = h / 60.0
    h60f = int(h60)#math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def single_pixel_to_6_main_type_color(pixel, free_mode=False, animation_mode=False, greyscale_mode=False, kernel=11):
    """
    If in a picture, relative to that picture, you can group every pixel into X theme, you win the image segmentation based on color game.
    Because when you use big box blur to know the picture only has [pink, black, yellow] 3 theme, if later you use global color threshold getting a green color segment, you are doing it wrong. The threshold should get dynamically adjusted based on main color theme.

    Another thing to mention is "material or texture detection is bigger than color detection".
        This is special, for example, for human hair, for same person, some part of the hair is black color, some part of the hair is yellow color, you can only know it is hair. If you know it is hair, you can get hair shape.
        Another example is glass, different light on glass will give you different color, but if you know it is glass material, you can get a glass_made object shape easily.

    Another thing to mention is "edge line shape defines an object, not only color". Because in 3D engine, even if you only have edge shape with pure white color, you can still recognize that object.
    """
    """
    red: (255,0,0->255) (255->101,0,255) (255,0->90,0)
    blue: (101->0,0,255) (0,0->255,255)
    green: (0,255,255->0) (0->185,255,0)
    yellow: (185->255,255,0) (255,255->90,0)
    white: hsv, s<7% or s<18%
    black: hsv, v<32%

    main_colors = {
        "Red": (255, 0, 0),
        "Blue": (0, 0, 255),
        "Green": (0, 255, 0),
        "Yellow": (255, 255, 0),
        "White": (255, 255, 255),
        "Black": (0, 0, 0),
    }

    You can turn s and v to 100%, so you get standard rgb color, which belong to 4 colors, do not include white and black.
    """
    if len(pixel) == 4:
        r,g,b,a = pixel
    elif len(pixel) == 3:
        r,g,b = pixel
        a = 255
    new_color = [0, 0, 0, 0]
    h,s,v = single_pixel_rgb_to_hsv(r, g, b)
    black_gate = 30
    white_gate = 18
    if animation_mode == True:
        black_gate = 0
        white_gate = 0
    if v < (black_gate/100) * 255:
        # black
        new_color = [0,0,0,255]
    elif s < (white_gate/100) * 255:
        # white
        new_color = [255,255,255,255]
    else:
        r,g,b = single_pixel_hsv_to_rgb(h, 255, 255)
        if free_mode == True:
            if greyscale_mode == True:
                r,g,b = single_pixel_hsv_to_rgb(round(round(h/255*kernel)/kernel*255), 0, round(round(v/255*3)/3*255))
            elif animation_mode == True:
                r,g,b = single_pixel_hsv_to_rgb(round(round(h/255*kernel)/kernel*255), round(round(s/255*2)/2*255), round(round(v/255*3)/3*255))
            else:
                r,g,b = single_pixel_hsv_to_rgb(round(round(h/255*kernel)/kernel*255), 255, 255)
            new_color = [r,g,b,255]
        else:
            if (r==255 and g==0 and 0<=b<=255) or (101<=r<=255 and g==0 and b==255) or (r==255 and 0<=g<=90 and b==0):
                new_color = [255, 0, 0, 255]
            elif ((0<=r<=101 and g==0 and b==255) or (r==0 and 0<=g<=255 and b==255)):
                new_color = [0, 0, 255, 255]
            elif ((r==0 and g==255 and 0<=b<=255) or (0<=r<=185 and g==255 and b==0)):
                new_color = [0, 255, 0, 255]
            elif ((185<=r<=255 and g==255 and b==0) or (r==255 and 90<=g<=255 and b==0)):
                new_color = [255, 255, 0, 255]
    new_color[3] = a
    return new_color

def rgb_to_hsv(image):
    #import colorsys
    new_image = image.copy()
    height, width = new_image.get_shape()
    for y in range(height):
        for x in range(width):
            pixel = new_image.raw_data[y][x]
            red, green, blue, transparent = pixel
            if transparent == 0:
                continue
            #h,s,v = colorsys.rgb_to_hsv(red/255, green/255, blue/255)
            #h,s,v = int(h*255), int(s*255), int(v*255)
            h,s,v = single_pixel_rgb_to_hsv(red, green, blue)
            new_image.raw_data[y][x] = [h, s, v, 255]
    return new_image

def hsv_to_rgb(image):
    #import colorsys
    new_image = image.copy()
    height, width = new_image.get_shape()
    for y in range(height):
        for x in range(width):
            pixel = new_image.raw_data[y][x]
            h, s, v, transparent = pixel
            if transparent == 0:
                continue
            #r,g,b = colorsys.hsv_to_rgb(h/255, s/255, v/255)
            #r,g,b = int(r*255), int(g*255), int(b*255)
            r,g,b = single_pixel_hsv_to_rgb(h, s, v)
            new_image.raw_data[y][x] = [r, g, b, 255]
    return new_image

def rgb_to_black_and_white(image, threshold=127):
    new_image = image.copy()
    height, width = new_image.get_shape()
    for y in range(height):
        for x in range(width):
            pixel = new_image.raw_data[y][x]
            red, green, blue, transparent = pixel
            if transparent == 0:
                continue
            grayscale = max(min(int(0.2989 * red + 0.5870 * green + 0.1140 * blue), 255), 0)
            if grayscale > threshold:
                new_pixel = [255,255,255,255]
            else:
                new_pixel = [0,0,0,255]
            new_image.raw_data[y][x] = new_pixel
    return new_image

def get_edge_lines_of_a_image_by_using_yingshaoxo_method(a_image, min_color_distance=15, downscale_ratio=3, gaussian_blur=False):
    """
    yingshaoxo: You can use Canny method, but I think it is hard to understand and implement.

    Need a erosion algorithm in here.
    """
    a_image = a_image.copy()
    original_height, original_width = a_image.get_shape()

    a_image = a_image.resize(int(original_height/downscale_ratio), int(original_width/downscale_ratio))
    if gaussian_blur == True:
        a_image = a_image.get_gaussian_blur_image(2, bug_version=False)

    old_height, old_width = a_image.get_shape()
    new_image = a_image.create_an_image(old_height, old_width, [0,0,0,0])

    height, width = a_image.get_shape()
    point_list = []
    for row_index in range(height):
        previous_pixel = None
        for column_index in range(width):
            pixel = a_image.raw_data[row_index][column_index]
            if previous_pixel != None:
                color_distance_in_horizontal = (abs(previous_pixel[0]-pixel[0]) + abs(previous_pixel[1]-pixel[1]) + abs(previous_pixel[2]-pixel[2]))/3
                if row_index > 0:
                    upper_pixel = a_image.raw_data[row_index-1][column_index]
                    color_distance_in_vertical = (abs(upper_pixel[0]-pixel[0]) + abs(upper_pixel[1]-pixel[1]) + abs(upper_pixel[2]-pixel[2])) / 3
                else:
                    color_distance_in_vertical = 0
                if color_distance_in_horizontal >= min_color_distance or color_distance_in_vertical >= min_color_distance:
                    a_point = [row_index, column_index]
                    point_list.append(a_point)
            previous_pixel = pixel

    for y,x in point_list:
        new_image.raw_data[y][x] = [0,0,0,255]

    new_image.resize(original_height, original_width)
    return new_image

def get_simplified_image_by_using_mean_square_and_edge_line(a_image, downscale_ratio=1, fill_transparent=False, pre_process=False):
    """
    You could do the mean for each pixel by using "scale up until edge line", but that speed is very slow.
    You can also use circle than square, it is more accurate.
    """
    a_image = a_image.copy()
    old_height, old_width = a_image.get_shape()

    a_image = a_image.resize(old_height//downscale_ratio, old_width//downscale_ratio)
    height, width = a_image.get_shape()

    new_image = a_image.create_an_image(height, width, [0,0,0,0])

    if pre_process == True:
        a_image = a_image.get_gaussian_blur_image(2, bug_version=False)
        a_image = a_image.get_balanced_image()

    if pre_process == True:
        edge_image = a_image.to_edge_line(downscale_ratio=2)
    else:
        edge_image = a_image.to_edge_line(downscale_ratio=1)

    for kernel in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 50, 100]:
        step_height = int(height/kernel)
        step_width = int(width/kernel)
        for y in range(step_height):
            for x in range(step_width):
                start_y = y * kernel
                end_y = start_y + kernel
                start_x = x * kernel
                end_x = start_x + kernel

                ok_for_mean = True
                edge_sub_image = edge_image.get_inner_image(start_y, end_y, start_x, end_x)
                for row in edge_sub_image.raw_data:
                    for r,g,b,a in row:
                        if a == 255:
                            ok_for_mean = False
                            break
                    if ok_for_mean == False:
                        break

                if ok_for_mean == True:
                    sub_image = a_image.get_inner_image(start_y, end_y, start_x, end_x)
                    all_r, all_g, all_b, _ = 0,0,0,0
                    counting = 0
                    for row in sub_image.raw_data:
                        for pixel in row:
                            r,g,b,a = pixel
                            if a != 0:
                                all_r += r
                                all_g += g
                                all_b += b
                                counting += 1
                    if counting != 0:
                        r = min(max(round(all_r/counting),0),255)
                        g = min(max(round(all_g/counting),0),255)
                        b = min(max(round(all_b/counting),0),255)
                    else:
                        r,g,b,_ = a_image.raw_data[y][x]

                    for y1 in range(start_y, end_y):
                        for x1 in range(start_x, end_x):
                            if y1 < 0 or y1 >= height or x1 < 0 or x1 >= width:
                                continue
                            new_image.raw_data[y1][x1] = [r,g,b,a_image.raw_data[y1][x1][3]]

    if fill_transparent == True:
        kernel = 5
        step_height = int(height/kernel)
        step_width = int(width/kernel)
        for y in range(step_height):
            for x in range(step_width):
                start_y = y * kernel
                end_y = start_y + kernel
                start_x = x * kernel
                end_x = start_x + kernel

                sub_image = new_image.get_inner_image(start_y, end_y, start_x, end_x)
                all_r, all_g, all_b, _ = 0,0,0,0
                counting = 0
                for row in sub_image.raw_data:
                    for pixel in row:
                        r,g,b,a = pixel
                        if a != 0:
                            all_r += r
                            all_g += g
                            all_b += b
                            counting += 1
                if counting != 0:
                    r = min(max(round(all_r/counting),0),255)
                    g = min(max(round(all_g/counting),0),255)
                    b = min(max(round(all_b/counting),0),255)
                else:
                    r,g,b,_ = a_image.raw_data[y][x]

                for y1 in range(start_y, end_y):
                    for x1 in range(start_x, end_x):
                        if y1 < 0 or y1 >= height or x1 < 0 or x1 >= width:
                            continue
                        if new_image.raw_data[y1][x1][3] != 0:
                            continue
                        new_image.raw_data[y1][x1] = [r,g,b,255]

    new_image.resize(old_height, old_width)
    return new_image

def make_a_line_between_two_points(point_a, point_b):
    y1, x1 = point_a
    y2, x2 = point_b
    new_list = []
    upper_part = y1 - y2
    lower_part = x1 - x2
    if upper_part == 0:
        # horizontal_line
        for x in range(min(x1, x2), max(x1, x2)):
            new_list.append([y1, x])
    elif lower_part == 0:
        # vertical line
        for y in range(min(y1, y2), max(y1, y2)):
            new_list.append([y, x1])
    else:
        slop = upper_part / lower_part
        for x_index in range(min(x1, x2), max(x1, x2)):
            y_index = round(slop*(x_index-x2) + y2)
            new_list.append([y_index, x_index])
    return new_list

def range_map(number, from_min, from_max, to_min, to_max, use_int=True):
    result = (((number - from_min) / (from_max - from_min)) * (to_max - to_min)) + to_min
    if use_int == True:
        return round(result)
    return result


class Image:
    """
    This class will represent image as 2D list. For example [[r,g,b,a], [r,g,b,a]] means two RGBA point.
    And with this image, you could do crop, put_on_top operations.
    """
    """
    It is a pure image based library. or RGBA 2-dimensional array based library. The final output and middle representation is pure number and arrays. We can add sub_picture to the top of another picture in a specified position. Anything photoshop_like image editor could do, we could do. Anything a 3D game engine could do, we could do.
    """
    def __init__(self, data=None):
        self.raw_data = None

        if data == None:
            new_image = self.create_an_image(1, 1)
            self.raw_data = new_image.raw_data
        else:
            self.raw_data = data

    def __getitem__(self, idx):
        return self.raw_data[idx]

    def __str__(self):
        text = "An yingshaoxo image object with shape of: "
        text += str(self.get_shape()) + " (height, width)"
        text += "\n"
        text += "The base first RGBA element is: "
        text += str(self.raw_data[0][0])
        return text

    def create_an_image(self, height, width, color=[255,255,255,255]):
        data = []
        for row_index in range(0, height):
            row = [None] * width
            for column_index in range(0, width):
                row[column_index] = color
            data.append(row)
        return Image(data=data)

    def get_shape(self):
        """
        return [height, width]
        """
        rows = len(self.raw_data)
        if rows == 0:
            return [0, 0]
        else:
            return [rows, len(self.raw_data[0])]

    def copy(self):
        data = []
        for row in self.raw_data:
            data.append([one for one in row])
        return Image(data)

    def _resize_an_list(self, a_list, old_length, new_length):
        # for downscale, you use "sub_window_length == int(old_size/new_size)", for each sub_window pixels, you only take the first pixel
        # for upscale, you use "it == int(new_size/old_size)", for each old pixel, you times that pixel by it, if the final pixels data is not meet the required length, we add transparent black color at the bottom
        new_list = []

        if old_length == new_length:
            return a_list
        if old_length > new_length:
            # downscale
            new_list = [None] * new_length
            sub_window_length = old_length/new_length
            index = 0
            counting = 0
            while True:
                first_element = a_list[int(round(index))]
                new_list[counting] = first_element
                counting += 1
                if counting >= new_length:
                    break
                index += sub_window_length
                if index >= old_length:
                    break
        else:
            # upscale
            sub_window_length = new_length/old_length
            new_list = [None] * new_length
            for i in range(new_length):
                old_index = int(i / sub_window_length)
                new_list[i] = a_list[old_index]
            #new_list = []
            #sub_window_length = int(new_length/old_length)
            #for one in a_list:
            #    new_list += [one] * sub_window_length
            #new_list = new_list[:new_length]
            ## add missing pixels at the bottom
            #counting = sub_window_length * old_length
            #new_list += [[0,0,0,0]] * (new_length - counting)

        return new_list

    def resize(self, height, width):
        """
        The image resize or pixel iteration in python is 60 times slower than c version, so don't use it as much as possible
        """
        if type(height) != int or type(width) != int:
            raise Exception("The height and width should be integer.")

        old_height, old_width = self.get_shape()
        if old_height == height and old_width == width:
            return self

        # handle width
        data = []
        for row in self.raw_data:
            data.append(self._resize_an_list(row, old_width, width))

        # handle height
        """
        data_2 = []
        for column in list(zip(*data)):
            data_2.append(self._resize_an_list(column, old_height, height))
        self.raw_data = list(zip(*data_2))
        """
        data_2 = []
        old_width = len(data[0])
        initialized = False
        for column_index in range(old_width):
            temp_column_list = [None] * old_height
            for row_index in range(old_height):
                element = data[row_index][column_index]
                temp_column_list[row_index] = element
            column_list = self._resize_an_list(temp_column_list, old_height, height)
            if initialized == False:
                data_2 += [[one] for one in column_list]
                initialized = True
            else:
                for index, one in enumerate(column_list):
                    data_2[index].append(one)

        self.raw_data = data_2
        return self

    def paste_image_on_top_of_this_image(self, another_image, top, left, height, width):
        """
        top: start_y
        left: start_x
        height: end_y - start_y
        width: end_x - start_x

        paste another image to current image based on (top, left, height, width) position in current image
        """
        base_image_height, base_image_width = self.get_shape()
        another_image_height, another_image_width = another_image.get_shape()
        if another_image_height > base_image_height or another_image_width > base_image_width:
            # overflow_situation: another image bigger than original image
            #raise Exception("The another image height and width should smaller than base image.")
            pass

        if another_image_height != height or another_image_width != width:
            another_image = another_image.copy()
            another_image.resize(height, width)

        y_start = top
        y_end = top + height
        x_start = left
        x_end = left + width

        # overflow_situation: another image smaller than original image, but paste to outside
        if y_end > base_image_height:
            y_end = base_image_height
        if x_end > base_image_width:
            x_end = base_image_width

        for y_index in range(y_start, y_end):
            #row = self.raw_data[y_index]
            #first_part = row[0:x_start]
            #second_part = row[x_end:]
            #new_row = first_part + another_image[y_index] + second_part
            #self.raw_data[y_index] = new_row

            #self.raw_data[y_index][x_start: x_end] = another_image[y_index-y_start]

            old_data = self.raw_data[y_index][x_start: x_end]
            old_data_length = len(old_data)
            new_data = [None] * old_data_length
            for index, one in enumerate(another_image[y_index-y_start][:old_data_length]):
                if one[3] == 0:
                    new_data[index] = old_data[index]
                else:
                    new_data[index] = one
            self.raw_data[y_index][x_start: x_end] = new_data

        return self

    def get_inner_image(self, y_start, y_end, x_start, x_end, padding=True):
        old_height, old_width = self.get_shape()
        height = y_end - y_start
        width = x_end - x_start
        if height <= 0 or width <= 0:
            return self.create_an_image(0, 0, [0,0,0,0])
        new_data = []
        for y in range(y_start, y_end):
            if y < 0 or y >= old_height:
                if padding == True:
                    new_data.append([[0,0,0,0]] * width)
                continue
            row = self.raw_data[y]
            target_row = [[0,0,0,0]] * width
            a_index_ = 0
            for x in range(x_start, x_end):
                if x < 0 or x >= old_width:
                    if padding == True:
                        target_row[a_index_] = [0,0,0,0]
                        a_index_ += 1
                    continue
                target_row[a_index_] = row[x]
                a_index_ += 1
            new_data.append(target_row)
        new_image = self.create_an_image(height, width, [0,0,0,0])
        new_image.raw_data = new_data
        return new_image

    def rotate(self):
        """
        rotate 90 degree in clockwise
        """
        old_height, old_width = self.get_shape()
        new_data = [None] * old_width
        for x in range(old_width):
            x = old_width - x - 1
            one_row = [None] * old_height
            for y in range(old_height):
                one_row[y] = self.raw_data[y][x]
            new_data[x] = one_row
        self.raw_data = new_data
        return self

    def rotate_back(self):
        """
        rotate 90 degree in anti-clockwise to get original image
        """
        for _ in range(3):
            self.rotate()
        return self

    def print(self, width=70, height_scale=0.5):
        """
        print current graph to the console/shell/terminal without numpy or PIL or mathplotlib or ...
        """
        new_image = self.copy()
        old_height, old_width = new_image.get_shape()
        height = int(((width/old_width) * old_height) * height_scale)

        new_image.resize(height, width)
        final_image = self.create_an_image(height=height, width=width)

        for row_index, row in enumerate(new_image.raw_data):
            for column_index, the_color in enumerate(row):
                new_color_raw = choose_a_color_from_base_color(the_color[0], the_color[1], the_color[2])
                new_color = new_color_raw["rgb"]
                new_color = [new_color[0], new_color[1], new_color[2], the_color[3]]
                final_image.raw_data[row_index][column_index] = new_color
                my_print(new_color_raw["value"], end="")
            my_print("\n", end="", flush=True)

        my_print("", end="", flush=True)
        return final_image

    def compare(self, another_image):
        """
        return a float between 0 and 1, 1 means equal, 0 means no relate.

        If it is not accurate, it simply because your camera or rgb_system or computer_color_system is not right. I see things as white, but computer thinks it is black. It happens even when I use HSV color space. If you can link all color into 9 colors, then you solve 99% of the problems related to computer vision. It you can write a function to know if two color is the similar color from real world picture as accuracy as human do, you win every computer vision game.
        """
        r_all_1 = 0
        g_all_1 = 0
        b_all_1 = 0
        height, width = self.get_shape()
        for row in self.raw_data:
            temp_r = 0
            temp_g = 0
            temp_b = 0
            for pixel in row:
                r,g,b,_ = pixel
                temp_r += r
                temp_g += g
                temp_b += b
            r_all_1 += temp_r/width
            g_all_1 += temp_g/width
            b_all_1 += temp_b/width
        r_all_1 = r_all_1/height
        g_all_1 = g_all_1/height
        b_all_1 = b_all_1/height

        r_all_2 = 0
        g_all_2 = 0
        b_all_2 = 0
        height, width = another_image.get_shape()
        for row in another_image.raw_data:
            temp_r = 0
            temp_g = 0
            temp_b = 0
            for pixel in row:
                r,g,b,_ = pixel
                temp_r += r
                temp_g += g
                temp_b += b
            r_all_2 += temp_r/width
            g_all_2 += temp_g/width
            b_all_2 += temp_b/width
        r_all_2 = r_all_2/height
        g_all_2 = g_all_2/height
        b_all_2 = b_all_2/height

        difference = abs(r_all_1-r_all_2) + abs(g_all_1-g_all_2) + abs(b_all_1-b_all_2)
        difference = ((difference*100)/(255*3))/20
        similarity = 1 - difference

        if similarity < 0:
            similarity = 0
        if similarity > 1:
            similarity = 1

        return similarity

    def to_hsv(self):
        self = rgb_to_hsv(self)
        return self

    def to_rgb(self):
        self = hsv_to_rgb(self)
        return self

    def to_edge_line(self, min_color_distance=15, downscale_ratio=2, gaussian_blur=False):
        return get_edge_lines_of_a_image_by_using_yingshaoxo_method(self, min_color_distance=min_color_distance, downscale_ratio=downscale_ratio, gaussian_blur=gaussian_blur)

    def to_greyscale(self):
        return self.get_6_color_simplified_image(balance=True, free_mode=True, animation_mode=True, greyscale_mode=True)

    def get_balanced_image(self):
        """
        For example, light up darker image.
        """
        new_image = self.copy()
        try:
            max_r = -999
            max_g = -999
            max_b = -999
            min_r = 999
            min_g = 999
            min_b = 999
            for row in new_image.raw_data:
                for pixel in row:
                    r,g,b,a = pixel
                    if r > max_r:
                        max_r = r
                    if g > max_g:
                        max_g = g
                    if b > max_b:
                        max_b = b
                    if r < min_r:
                        min_r = r
                    if g < min_g:
                        min_g = g
                    if b < min_b:
                        min_b = b
            r_range = max_r - min_r
            g_range = max_g - min_g
            b_range = max_b - min_b
            height, width = new_image.get_shape()
            for y in range(height):
                for x in range(width):
                    r,g,b,a = new_image.raw_data[y][x]
                    new_image.raw_data[y][x] = [
                        round(((r - min_r)/r_range)*255),
                        round(((g - min_g)/g_range)*255),
                        round(((b - min_b)/b_range)*255),
                        a
                    ]
        except Exception as e:
            print(e)
        return new_image

    def get_gaussian_blur_image(self, kernel=3, bug_version=False):
        a_image = self.copy()
        backup_image = a_image.copy()
        height, width = a_image.get_shape()
        if kernel == None:
            kernel = int(width / 24 / 2)
        for y, row in enumerate(a_image.raw_data):
            for x, pixel in enumerate(row):
                new_color = pixel
                start_y = y - kernel
                end_y = y + kernel
                start_x = x - kernel
                end_x = x + kernel
                if bug_version == True:
                    sub_image = a_image.get_inner_image(start_y, end_y, start_x, end_x)
                else:
                    sub_image = backup_image.get_inner_image(start_y, end_y, start_x, end_x)
                counting = 0
                all_r = 0
                all_g = 0
                all_b = 0
                for a_row in sub_image.raw_data:
                    for temp_pixel in a_row:
                        r,g,b,a = temp_pixel
                        if a == 0:
                            continue
                        all_r += r
                        all_g += g
                        all_b += b
                        counting += 1
                if counting == 0:
                    pass
                else:
                    new_color = [round(all_r/counting), round(all_g/counting), round(all_b/counting), pixel[3]]
                a_image[y][x] = new_color
        return a_image

    def get_6_color_simplified_image(self, balance=False, free_mode=False, animation_mode=False, greyscale_mode=False, accurate_mode=False, kernel=11):
        a_image = self.copy()
        backup_image = a_image.copy()

        if balance == True:
            a_image = a_image.get_balanced_image()
        for y, row in enumerate(a_image.raw_data):
            for x, pixel in enumerate(row):
                new_color = single_pixel_to_6_main_type_color(pixel, free_mode=free_mode, animation_mode=animation_mode, greyscale_mode=greyscale_mode, kernel=kernel)
                a_image[y][x] = new_color

        if accurate_mode == True:
            a_image2 = get_simplified_image_by_using_mean_square_and_edge_line(backup_image, downscale_ratio=1, fill_transparent=True, pre_process=True)
            a_image2 = a_image2.get_6_color_simplified_image(balance=True, free_mode=True, animation_mode=False, accurate_mode=False)
            a_image = a_image2

        return a_image

    def get_simplified_image_based_on_mean_square_and_edge_line(self, downscale_ratio=1, fill_transparent=False):
        return get_simplified_image_by_using_mean_square_and_edge_line(self, downscale_ratio=downscale_ratio, fill_transparent=fill_transparent)

    def get_simplified_image_in_a_slow_way(self, ratio=0.7):
        """
        ratio: 0 to 1, more close to 1, more simplified

        This is also how to compress png file in a way that human could not notice. Similar to https://tinypng.com
        Created by yingshaoxo

        I'm pretty sure if you do this with 0.999 for background color than human body, you will get a small but clear human photo. You can do it by manually draw an interesting area.
        """
        new_image = self.copy()
        color_list = get_main_color_list_from_an_image(new_image, ratio)

        for row_index, row in enumerate(new_image.raw_data):
            for column_index, the_color in enumerate(row):
                if the_color[-1] == 0:
                    new_color = [0,0,0,0]
                else:
                    new_color = get_a_color_from_base_color(the_color[0], the_color[1], the_color[2], the_color[3], color_list)
                new_image.raw_data[row_index][column_index] = new_color

        return new_image

    def get_simplified_image(self, level=7, extreme_color_number=None, predefined_color_list=None):
        """
        level: 2 to infinite, the bigger, the more simplified
        extreme_color_number: 20 is enough, it means the whole picture will only use 20 colors

        When use extreme_color_number, try more times to get different pictures. (I don't know where the bug is)
        """
        """
        How to reduce noise in image or how to reduce color type in image or how to simplify a image or how to convert a image to cartoon?

        1. split image into sub_image or sub_windows, use dict to get main color, each window would only have one color. In a photo shoot from a bad camera, you can see even for a white background wall, the picture would have many other color than white color, those are the noise we should remove.
        2. by doing step1, we can get a bigger map where each 8x8 pixels only have one color. Those color are main colors for that picture. We can even only remain 100 colors as main color. Then for each pixel in the old picture, we do a loop comparation based on main color list, we use the most similar main color to replace old pixel.
        3. For the color_compare part, you can use a global dict to cache some result, so you don't have to do repeat color distance calculation.
        4. c is faster than c++ in 'get element from list by index' about 1.5 times. For some programming language, their dict and list built-in type is garbage, if you use those language to read a 1080x720 pixels list, it would take 0.5 second for a pixel sometimes, but the whole pixels number is 777600. (And cpp compile time is 10 times slower than c compile, 2 times slower than python)

        > author: yingshaoxo
        """
        return get_simplified_image_in_an_accurate_way(self, level, extreme_color_number, predefined_color_list)

    def get_simplified_image_in_a_quick_way(self, level=25):
        return get_simplified_image_in_a_quick_way(self, level)

    def get_simplified_image_in_a_extreme_quick_way(self, level=15, raw=False):
        """
        level: int
            The higher, the more simplified

        We know rgb value is in (0,255), but we don't need that many color to represent things. So we use [0,5] range values for rgb. So all color we could get is 5x5x5x6=750. 750 colors is good enough. --- author: yingshaoxo
        """
        new_image = self.copy()
        height, width = new_image.get_shape()
        for y in range(height):
            for x in range(width):
                pixel = new_image.raw_data[y][x]
                red, green, blue, transparent = pixel
                if transparent == 0:
                    new_pixel = [0,0,0,0]
                else:
                    if raw == False:
                        red = round((round((red/255)*level)/level) * 255)
                        green = round((round((green/255)*level)/level) * 255)
                        blue = round((round((blue/255)*level)/level) * 255)
                    else:
                        red = round((red/255)*level)
                        green = round((green/255)*level)
                        blue = round((blue/255)*level)
                    new_pixel = [red,green,blue,transparent]
                new_image.raw_data[y][x] = new_pixel
        return new_image

    def to_white_and_black(self, threshold=127):
        """
        If there only have 2 colors, think about if you save data sequencely without space as seperator, will you save half of storage?
        """
        return rgb_to_black_and_white(self, threshold=threshold)

    def to_mosaic(self, ratio=0.99, kernel_number=12):
        """
        ratio: 0 to 1, more close to 1, more simplified

        It removes ratio big pixels for each 8x8 sub_image, for example ratio=0.6 means remove 60% noise pixels from 8x8 sub_image
        """
        return to_mosaic(self, ratio, kernel_number)

    def change_image_style(self, target_image, simple_mode=False, random_mode=False, random_numbers=None):
        """
        target_image: another image
            Can be itself if you use other mode
        random_mode: bool
            Default False
        random_numbers: list
            [50, 50, 50]
        """
        if random_mode == True:
            return change_image_style_with_random_number(target_image, random_numbers)
        else:
            return change_image_style_without_ai(self.copy().get_simplified_image(level=6), target_image, simple_mode=simple_mode)

    def fill_transparent_color(self, new_color=[255,255,255,255]):
        a_image = self.copy()
        height, width = a_image.get_shape()
        for y in range(height):
            for x in range(width):
                pixel = a_image.raw_data[y][x]
                if pixel[3] != 255:
                    a_image.raw_data[y][x] = new_color
        return a_image

    def to_hash(self, height=32, width=32, hash_length=64):
        """
        It turns out you have to make sure those picture has same shape in height and width if you want to do a comparation
        """
        # rgb
        a_image = self.copy().get_simplified_image_in_a_extreme_quick_way(level=99, raw=True)
        a_image.resize(height,width)
        text_data = ""
        for y in range(height):
            for x in range(width):
                pixel = a_image.raw_data[y][x]
                pixel_string = "".join(["{:02d}".format(one) for one in pixel[:3]])
                text_data += pixel_string

        old_text_length = len(text_data)
        if old_text_length > hash_length:
            kernel = old_text_length / hash_length
            new_text = ""
            for i in range(hash_length):
                i = int(i * kernel)
                if i >= old_text_length:
                    i = old_text_length-1
                new_text += text_data[i]
            return new_text
        else:
            kernel = hash_length / old_text_length
            new_text = ""
            for i in range(hash_length):
                i = int(i / kernel)
                if i >= old_text_length:
                    i = old_text_length-1
                new_text += text_data[i]
            return new_text

    def read_image_from_string(self, a_string):
        """
        data format: "height, width, 1d pixel hex rgba data"
        """
        height, width, hex_data_string = a_string.split(",")
        height, width = int(height), int(width)
        bytes_data = bytes().fromhex(hex_data_string)
        a_image = self.create_an_image(height, width)
        index = 0
        for y in range(height):
            for x in range(width):
                a_image.raw_data[y][x] = [bytes_data[index], bytes_data[index+1], bytes_data[index+2], bytes_data[index+3]]
                index += 4
        return a_image

    def save_image_as_string(self, bgra=False):
        """
        data format: "height, width, 1d pixel hex rgba data"

        framebuffer or x11 needs bgra
        """
        height, width = self.get_shape()
        rgbx_data_string = str(height)+","+str(width)+","
        rgbx_list = []
        if bgra == False:
            for row in self.raw_data:
                for pixel in row:
                    r,g,b,a = pixel
                    rgbx_list.append(r)
                    rgbx_list.append(g)
                    rgbx_list.append(b)
                    rgbx_list.append(a)
        else:
            for row in self.raw_data:
                for pixel in row:
                    r,g,b,a = pixel
                    rgbx_list.append(b)
                    rgbx_list.append(g)
                    rgbx_list.append(r)
                    rgbx_list.append(a)
        rgbx_data_string += bytes(rgbx_list).hex()
        return rgbx_data_string

    def read_image_from_file(self, file_path):
        if file_path.endswith(".png") or file_path.endswith(".jpg"):
            try:
                from PIL import Image as _Image

                the_image = _Image.open(file_path)
                height, width = the_image.size[1], the_image.size[0]

                new_image = self.create_an_image(height=height, width=width)

                data = the_image.convert('RGBA').getdata()

                for row_index in range(0, height):
                    base_index = row_index * width
                    for column_index in range(0, width):
                        new_image.raw_data[row_index][column_index] = list(data[base_index + column_index])

                return new_image
            except Exception as e:
                e1 = e
                try:
                    import auto_everything.additional.pypng as pypng

                    height, width, raw_data = pypng.read_png_from_file(file_path)

                    a_image = self.create_an_image(height, width)
                    a_image.raw_data = raw_data
                    return a_image
                except Exception as e:
                    print(e1)
                    print(e)
                    print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.txt', then do a text level compression.")
        elif file_path.endswith(".bmp"):
            try:
                import auto_everything.additional.pybmp as pybmp

                height, width, raw_data = pybmp.read_bmp_from_file(file_path)

                a_image = self.create_an_image(height, width)
                a_image.raw_data = raw_data
                return a_image
            except Exception as e:
                print(e)
                print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.txt', then do a text level compression.")
        elif file_path.endswith(".json") or file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

            if file_path.endswith(".json"):
                #json_data = {"height": height, "width": width, "color_dict": the_real_color_dict, "data": []}
                json_data = json.loads(raw_text)
                height, width, the_color_dict, data = json_data["height"], json_data["width"], json_data["color_dict"], json_data["data"]

                a_image = Image().create_an_image(height=height, width=width)
                for row_index, line in enumerate(data):
                    for column_index, id_ in enumerate(line):
                        a_image.raw_data[row_index][column_index] = the_color_dict[str(id_)]

                return a_image
            elif file_path.endswith(".txt"):
                splits = raw_text.split("\n_______\n")
                size_info = splits[1].strip()
                dict_text = splits[2].strip()
                the_text_data = splits[3].strip()

                the_color_dict = dict()
                for index, line in enumerate(dict_text.split("\n")):
                    the_color_dict[str(index)] = [int(one) for one in line.strip().split(",")]

                info_splits = size_info.split(",")
                height = int(info_splits[1])
                width = int(info_splits[3])

                a_image = Image().create_an_image(height=height, width=width)

                if "_" not in the_text_data:
                    # not extreme mode, read pixel one by one
                    for row_index, line in enumerate(the_text_data.split("\n")):
                        for column_index, id_ in enumerate(line.strip().split(" ")):
                            a_image.raw_data[row_index][column_index] = the_color_dict[id_]
                else:
                    row_index = 0
                    lines = the_text_data.split("\n")
                    for line in lines:
                        column_index = 0
                        line = line.strip()
                        parts = line.split(" ")
                        for part in parts:
                            if "_d_" in part:
                                # handle repeated line
                                color_index, repeated_line_number = part.split("_d_")
                                repeated_line_number = int(repeated_line_number)
                                color = the_color_dict[color_index]
                                for i in range(row_index, row_index + repeated_line_number):
                                    a_image.raw_data[i] = [color] * width
                                row_index += repeated_line_number - 1
                                break
                            elif "_" in part:
                                # handle repeated pixel
                                color_index, repeated_pixel_number = part.split("_")
                                repeated_pixel_number = int(repeated_pixel_number)
                                color = the_color_dict[color_index]
                                for i in range(column_index, column_index + repeated_pixel_number):
                                    a_image.raw_data[row_index][i] = color
                                column_index += repeated_pixel_number
                            else:
                                # handle single pixel
                                color_index = part
                                color = the_color_dict[color_index]
                                a_image.raw_data[row_index][column_index] = color
                                column_index += 1
                        row_index += 1

                return a_image
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return Image(json.loads(f.read()))

    def save_image_to_file_path(self, file_path, extreme=False):
        """
        I have a new idea about image representation:
            1. For lines, for example, circuits, you can only use stright line and two_point_with_radius_arc_line to define everything.
            2. For other colorful image, you can only use rectangle to define everything. Square is a special rectangle, especially 1x1 square, which normally means a point.
            3. For 3D world, is can also combined with basic shapes, for example, cube, cuboid, sphere.
        """
        if file_path.endswith(".png") or file_path.endswith(".jpg"):
            try:
                from PIL import Image as _Image
                import numpy
                the_image = _Image.fromarray(numpy.uint8(self.raw_data))
                the_image.save(file_path)
            except Exception as e:
                e1 = e
                try:
                    import auto_everything.additional.pypng as pypng

                    pypng.save_png_to_file(self, file_path)
                except Exception as e:
                    print(e1)
                    print(e)
                    print("Since png or jpg is too complex to implement, we strongly recommand you to save raw_data as text, for example, 'hi.png.txt', then do a text level compression.")
        elif file_path.endswith(".json") or file_path.endswith(".txt"):
            height, width = self.get_shape()

            the_color_dict = dict()
            for row_index, row in enumerate(self.raw_data):
                for column_index, color in enumerate(row):
                    color = tuple(color)
                    if color in the_color_dict.keys():
                        the_color_dict[color] += 1
                    else:
                        the_color_dict[color] = 1
            the_color_dict_list = [(key,value) for key, value in the_color_dict.items()]
            the_color_dict_list.sort(key=lambda x: -x[1])

            the_real_color_dict = dict()
            index = 0
            for key,value in the_color_dict_list:
                key = ",".join([str(one) for one in key])
                the_real_color_dict[key] = index
                index += 1

            if file_path.endswith(".json"):
                reverse_dict = dict()
                for key, value in the_real_color_dict.items():
                    reverse_dict[int(value)] = [int(one) for one in key.split(",")]
                json_data = {"height": height, "width": width, "color_dict": reverse_dict, "data": []}
                data = []
                for row_index, row in enumerate(self.raw_data):
                    data.append([])
                    for column_index, color in enumerate(row):
                        color = ",".join([str(one) for one in color])
                        data[-1].append(the_real_color_dict[color])
                json_data["data"] = data

                text_data = json.dumps(json_data, ensure_ascii=False)
            elif file_path.endswith(".txt"):
                text_data = "format: yingshaoxo_image; version: 2024; help: the second part has the height and width. the third part contains a dict, you have to convert it into a dict where value is what you get by using new_line split, and the key is the element index start from 0. then for part 4, they are real data, each one represent a pixel index, it has rows and columns of pixels split by new_line and space, you have to use the dict you got before to convert those index number into real pixel data. as for some special symbol in real data, 2_200 means 2 repeated for 200 times in the same row, 3_d_4 means the whole row is 3 and the line in down direction repeated 4 times."
                text_data += "\n_______\n\n"
                text_data += "height,"+str(height)+","+"width,"+str(width)
                text_data += "\n_______\n\n"
                for key in the_real_color_dict.keys():
                    text_data += key + "\n"
                text_data += "_______\n\n"
                if extreme == False:
                    for row_index, row in enumerate(self.raw_data):
                        for column_index, color in enumerate(row):
                            color = ",".join([str(one) for one in color])
                            text_data += str(the_real_color_dict[color]) + " "
                        text_data += "\n"
                else:
                    height, width = self.get_shape()
                    row_index = 0
                    while True:
                        if row_index >= height:
                            break
                        column_index = 0
                        while True:
                            if row_index >= height:
                                break
                            if column_index >= width:
                                break
                            color = self.raw_data[row_index][column_index]
                            color_string = ",".join([str(one) for one in color])
                            color_index_string = str(the_real_color_dict[color_string])
                            if column_index == 0:
                                # there has possibility one index could cover the whole line and repeat that line
                                repeated_line_counting = 0
                                for i in range(row_index, height):
                                    a_row = self.raw_data[i]
                                    if all([one == color for one in a_row]):
                                        repeated_line_counting += 1
                                    else:
                                        break
                                if repeated_line_counting != 0:
                                    # has repeated line
                                    text_data += color_index_string + "_d_" + str(repeated_line_counting) + "\n"
                                    row_index += repeated_line_counting
                                    continue
                                else:
                                    # no repeated line, check current line pixel repeatation
                                    repeated_pixel_counting = 0
                                    for i in range(column_index, width):
                                        other_pixel = self.raw_data[row_index][i]
                                        if other_pixel == color:
                                            repeated_pixel_counting += 1
                                        else:
                                            break
                                    if repeated_pixel_counting == 1:
                                        # no repeat pixel
                                        text_data += color_index_string + " "
                                    else:
                                        # has repeat pixel
                                        text_data += color_index_string + "_" + str(repeated_pixel_counting) + " "
                                        column_index += repeated_pixel_counting
                                        continue
                            else:
                                # there could only have repetation in one row
                                repeated_pixel_counting = 0
                                for i in range(column_index, width):
                                    other_pixel = self.raw_data[row_index][i]
                                    if other_pixel == color:
                                        repeated_pixel_counting += 1
                                    else:
                                        break
                                if repeated_pixel_counting == 1:
                                    # no repeat pixel
                                    text_data += color_index_string + " "
                                else:
                                    # has repeat pixel
                                    text_data += color_index_string + "_" + str(repeated_pixel_counting) + " "
                                    column_index += repeated_pixel_counting
                                    continue
                            column_index += 1
                        text_data += "\n"
                        row_index += 1

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_data)
            print("Use 7z/lzma compression software if you want to have a smaller size image. It matchs the size of png. Because png secretly use zlib to do the compression.")
        else:
            """
            For image, maybe convert it to ascii is a good compression idea
            """
            raw_data = json.dumps(self.raw_data, ensure_ascii=False)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(raw_data)


class Animation:
    """
    This class will play Image list as Video, or export them as video file.
    For example, play 20 images per second.
    """
    pass


char_image_container_cache = {} # 'size+char' as key, image_container as value


class Container:
    def __init__(self, height=1.0, width=1.0, children=[], rows=None, columns=None, color=[255,255,255,255], image=None, text="", text_color=[0,0,0,255], text_size=1, center_text=True, parent_height=None, parent_width=None, on_click_function=None, information={}):
        """
        height: "8" means "8px", "0.5" means "50% of its parent container"
        width: "20" means "20px", "0.2" means "20%"
        children: [Container(), ]
        rows: True
        columns: False
        color: [255,255,255,255]
        image: Image()
        text: ""
        text_color: [0,0,0,255]
        text_size: 1
        information: will pass to self.information as a {} dict
        """
        if (type(height) != int and type(height) != float) or (type(width) != int and type(width) != float):
            raise Exception("Height and width for root window must be integer. For example, '20' or '100'")

        self.height = height
        self.width = width
        self.children = children
        self.rows = rows
        self.columns = columns
        self.color = color
        self.image = image
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.center_text = center_text
        self.parent_height = parent_height
        self.parent_width = parent_width
        self.information = information

        self.real_property_dict = {}
        """
        self.real_property_dict["left_top_y"] = 0
        self.real_property_dict["left_top_x"] = 0
        self.real_property_dict["right_bottom_y"] = height
        self.real_property_dict["right_bottom_x"] = width

        self.real_property_dict["one_row_height"] = 0
        self.real_property_dict["one_column_width"] = 0
        """

        self.old_propertys = []
        self.cache_image = None

        if on_click_function != None:
            self.on_click_function = on_click_function
        else:
            def on_click(element=None, y=None, x=None):
                return

            self.on_click_function = on_click


        self.get_ascii_8_times_16_points_data = None

    def _is_ascii(self, char):
        #return all(ord(c) < 128 for c in s)
        return ord(char) < 128

    def _convert_text_to_container_list(self, text, parent_height, parent_width, on_click_function):
        # have a bug, which force you to click text than background
        if self.get_ascii_8_times_16_points_data == None:
            try:
                from auto_everything.font_ import get_ascii_8_times_16_points_data
            except Exception as e:
                from font_ import get_ascii_8_times_16_points_data
            self.get_ascii_8_times_16_points_data = get_ascii_8_times_16_points_data

        children = []

        the_height = 16 * self.text_size
        the_width = 8 * self.text_size
        maximum_character_number_per_row = int(parent_width / the_width)
        maximum_character_number_per_column = int(parent_height / the_height)

        # let the text fill the parent_container
        new_text = ""
        for line in text.split("\n"):
            while len(line) > maximum_character_number_per_row:
                new_text += line[:maximum_character_number_per_row]
                new_text += "\n"
                line = line[maximum_character_number_per_row:]
            if len(line) != "":
                new_text += line
                new_text += "\n"
            new_text += "\n"
        text = new_text.strip()

        # center text
        if text != "" and self.center_text == True:
            real_width = maximum_character_number_per_row
            real_height = maximum_character_number_per_column
            if "\n" in text:
                center_text = False
                horizontal_padding_space_number = 0
            else:
                center_text = True
                horizontal_padding_space_number = int((real_width - len(text))/2) + 1

            lines = text.split("\n")
            actual_text_lines = len(lines)
            vertical_padding_line_number = int((real_height-actual_text_lines) / 2)
        else:
            horizontal_padding_space_number = 0
            vertical_padding_line_number = 0

        space_char_container = Container(height=the_height, width=the_width, color=self.color, children=[], columns=True, information=self.information, on_click_function=on_click_function)
        for line_index, line in enumerate(text.split("\n")):
            text_row_container = Container(height=the_height, width=parent_width, children=[], columns=True, information=self.information)
            for char in line:
                if not self._is_ascii(char):
                    char = " "
                char_points_data = self.get_ascii_8_times_16_points_data(char)
                for row_index, row in enumerate(char_points_data):
                    for column_index, element in enumerate(row):
                        if element == 1:
                            char_points_data[row_index][column_index] = self.text_color
                        else:
                            char_points_data[row_index][column_index] = self.color

                char_id = "{size}+{char}+{color}".format(size=self.text_size, char=char, color=self.color)
                if char_id not in char_image_container_cache:
                    char_image = Image().create_an_image(height=16, width=8, color=self.color)
                    char_image.raw_data = char_points_data
                    char_image.resize(height=the_height, width=the_width)
                    char_image_container = Container(image=char_image, height=the_height, width=the_width, columns=True)
                    char_image_container_cache[char_id] = char_image_container
                else:
                    char_image_container = char_image_container_cache[char_id]

                char_image_container.on_click_function = on_click_function
                char_image_container.information=self.information
                text_row_container.children.append(char_image_container)

            text_row_container.children = [space_char_container]*horizontal_padding_space_number + text_row_container.children + [space_char_container]*(horizontal_padding_space_number) #there may have a bug for adding 2
            children.append(text_row_container)

        # add vertical padding lines
        empty_text_row_container = Container(height=the_height*vertical_padding_line_number, width=parent_width, color=self.color, children=[], rows=True, information=self.information, on_click_function=on_click_function)
        children = [empty_text_row_container] + children + [empty_text_row_container]

        return children

    def _get_propertys_of_a_container(self, one_container):
        return json.dumps([one_container.height, one_container.width, one_container.rows, one_container.columns, one_container.color, id(one_container.image), one_container.text, one_container.parent_height, one_container.parent_width, one_container.real_property_dict])

    def _loop_all_components_in_tree_to_see_if_its_child_got_changed(self, root_container):
        queue = [root_container]
        while len(queue) > 0:
            one_container = queue[0]
            queue = queue[1:]
            queue += one_container.children

            new_propertys = self._get_propertys_of_a_container(one_container)
            if new_propertys != one_container.old_propertys:
                #one_container.old_propertys = new_propertys
                return True
        return False

    def render(self):
        """
        returns a real container that uses fixed pixel values
        """
        if self._loop_all_components_in_tree_to_see_if_its_child_got_changed(self) == False:
            return self.cache_image
        else:
            self.old_propertys = self._get_propertys_of_a_container(self)

        real_image = None

        if (type(self.height) != int and type(self.height) != float) or (type(self.width) != int and type(self.width) != float):
            raise Exception("Height and width must be numbers. For example, 0.2 or 20. (0.2 means 20% of its parent)")

        real_height = None
        real_width = None

        if type(self.height) == float:
            if self.parent_height == None:
                raise Exception("parent_height shoudn't be None")
            real_height = int(self.parent_height * self.height)
        else:
            real_height = self.height

        if type(self.width) == float:
            if self.parent_width == None:
                raise Exception("parent_width shoudn't be None")
            real_width = int(self.parent_width * self.width)
        else:
            real_width = self.width

        if self.image != None:
            temp_image = self.image.copy()
            image_height, image_width = temp_image.get_shape()
            if image_height != real_height or image_width != real_width:
                temp_image.resize(real_height, real_width)
            real_image = temp_image
        else:
            real_image = Image()
            real_image = real_image.create_an_image(real_height, real_width, self.color)

        if self.text != "":
            self.children = self._convert_text_to_container_list(self.text, parent_height=real_height, parent_width=real_width, on_click_function=self.on_click_function)
            self.rows = True
            self.columns = False

        #real_height, real_width = real_image.get_shape()
        self.real_property_dict["height"] = real_height
        self.real_property_dict["width"] = real_width

        if self.rows == None and self.columns == None:
            if self.text != "":
                self.columns = True
            else:
                self.rows = True
        if self.rows != True and self.columns != True:
            self.rows = True
        if self.rows == self.columns:
            raise Exception("You can either set rows to True or set columns to True, but not both.")

        if self.rows == True:
            top = 0
            left = 0
            for one_row_container in self.children:
                one_row_container.parent_height = self.real_property_dict["height"]
                one_row_container.parent_width = self.real_property_dict["width"]
                real_one_row_image = one_row_container.render()

                one_row_height, one_row_width = real_one_row_image.get_shape()
                real_image.paste_image_on_top_of_this_image(real_one_row_image, top=top, left=left, height=one_row_height, width=one_row_width)
                one_row_container.real_property_dict["left_top_y"] = top
                one_row_container.real_property_dict["left_top_x"] = left
                one_row_container.real_property_dict["right_bottom_y"] = top + one_row_height
                one_row_container.real_property_dict["right_bottom_x"] = one_row_width

                top += one_row_height
        elif self.columns == True:
            left = 0
            top = 0
            for one_column_container in self.children:
                one_column_container.parent_height = self.real_property_dict["height"]
                one_column_container.parent_width = self.real_property_dict["width"]
                real_one_column_image = one_column_container.render()

                one_column_height, one_column_width = real_one_column_image.get_shape()
                real_image.paste_image_on_top_of_this_image(real_one_column_image, top=top, left=left, height=one_column_height, width=one_column_width)
                one_column_container.real_property_dict["left_top_y"] = top
                one_column_container.real_property_dict["left_top_x"] = left
                one_column_container.real_property_dict["right_bottom_y"] = one_column_height
                one_column_container.real_property_dict["right_bottom_x"] = left+one_column_width

                left += one_column_width

        self.cache_image = real_image
        return real_image

    def _render_as_text_component_list(self, top_=0, left_=0):
        """
        try to get global absolute position of those components by only doing resize. (do not use paste_image_on_top_of_this_image function.)
        so that we could simply return those components as a list, let the lcd render those things directly will speed up the process. use 'paste_image_on_top_of_this_image' is kind of slow
        """
        data_list = []

        if (type(self.height) != int and type(self.height) != float) or (type(self.width) != int and type(self.width) != float):
            raise Exception("Height and width must be numbers. For example, 0.2 or 20. (0.2 means 20% of its parent)")

        real_height = None
        real_width = None

        if type(self.height) == float:
            if self.parent_height == None:
                raise Exception("parent_height shoudn't be None")
            real_height = int(self.parent_height * self.height)
        else:
            real_height = self.height

        if type(self.width) == float:
            if self.parent_width == None:
                raise Exception("parent_width shoudn't be None")
            real_width = int(self.parent_width * self.width)
        else:
            real_width = self.width

        if self.image != None:
            data_list.append({
                "top": top_,
                "left": left_,
                "height": real_height,
                "width": real_width,
                "image": self.image.copy(),
                "center_text": self.center_text,
            })
        else:
            data_list.append({
                "top": top_,
                "left": left_,
                "height": real_height,
                "width": real_width,
                "text": self.text,
                "center_text": self.center_text,
            })

        self.real_property_dict["height"] = real_height
        self.real_property_dict["width"] = real_width

        if self.rows == None and self.columns == None:
            if self.text != "":
                self.columns = True
            else:
                self.rows = True
        if self.rows != True and self.columns != True:
            self.rows = True
        if self.rows == self.columns:
            raise Exception("You can either set rows to True or set columns to True, but not both.")

        if self.rows == True:
            top = 0
            left = 0
            for one_row_container in self.children:
                one_row_container.parent_height = self.real_property_dict["height"]
                one_row_container.parent_width = self.real_property_dict["width"]
                temp_list = one_row_container._render_as_text_component_list(top_ + top, left_ + left)

                one_row_height = temp_list[0]["height"]
                one_row_width = temp_list[0]["width"]
                one_row_container.real_property_dict["left_top_y"] = top
                one_row_container.real_property_dict["left_top_x"] = left
                one_row_container.real_property_dict["right_bottom_y"] = top + one_row_height
                one_row_container.real_property_dict["right_bottom_x"] = one_row_width

                data_list += temp_list

                top += one_row_height
        elif self.columns == True:
            left = 0
            top = 0
            for one_column_container in self.children:
                one_column_container.parent_height = self.real_property_dict["height"]
                one_column_container.parent_width = self.real_property_dict["width"]
                temp_list = one_column_container._render_as_text_component_list(top_ + top, left_ + left)

                one_column_height = temp_list[0]["height"]
                one_column_width = temp_list[0]["width"]
                one_column_container.real_property_dict["left_top_y"] = top
                one_column_container.real_property_dict["left_top_x"] = left
                one_column_container.real_property_dict["right_bottom_y"] = one_column_height
                one_column_container.real_property_dict["right_bottom_x"] = left + one_column_width

                data_list += temp_list

                left += one_column_width

        return data_list

    def render_as_text(self, text_height=16, text_width=8, pure_text=False, one_dimention_text=False):
        component_list = self._render_as_text_component_list()

        char_number_in_one_row = int(self.real_property_dict["width"] / 8)
        rows_number = int(self.real_property_dict["height"] / 16)

        # raw_data = [[" "] * char_number_in_one_row] * rows_number # this will make bugs, if you change one row, every row will get changed
        raw_data = []
        for row_index in range(rows_number):
            one_row = [" "] * char_number_in_one_row
            raw_data.append(one_row)

        for component in component_list:
            top = component["top"]
            left = component["left"]
            height = component["height"]
            width = component["width"]

            real_top = int(top / text_height)
            real_height = int(height / text_height) # max line number for this container

            real_left = int(left / text_width)
            real_width = int(width / text_width) # max character number per row

            if "image" in component:
                # image
                image = component["image"]
            else:
                # text
                text = component["text"]
                if text == "":
                    continue

                if component["center_text"] == True:
                    if "\n" in text:
                        center_text = False
                        horizontal_padding_space_number = 0
                    else:
                        center_text = True
                        horizontal_padding_space_number = int((real_width - len(text))/2)

                    lines = text.split("\n")
                    actual_text_lines = len(lines) + sum([len(line)/real_width for line in lines])
                    vertical_padding_line_number = int((real_height-actual_text_lines) / 2)
                else:
                    horizontal_padding_space_number = 0
                    vertical_padding_line_number = 0

                index = 0
                text_length = len(text)
                for row_index in range(real_top, real_top+real_height):
                    if vertical_padding_line_number > 0:
                        # for center text
                        vertical_padding_line_number -= 1
                        continue
                    for column_index in range(real_left, real_left+real_width):
                        if horizontal_padding_space_number > 0:
                            # for center text
                            horizontal_padding_space_number -= 1
                            continue
                        if index >= text_length:
                            break
                        char = text[index]
                        index += 1
                        if char == "\n":
                            break
                        raw_data[row_index][column_index] = char

        if pure_text == False:
            return raw_data
        else:
            text = ""
            for row in raw_data:
                if one_dimention_text == False:
                    text += "".join(row) + "\n"
                else:
                    text += "".join(row)
            return text

    def _convert_2d_text_to_image(self, text):
        if type(text) == list:
            text = ""
            for row in text_2d_array:
                text += "".join(row) + "\n"
        root_container = Container(text=text)
        root_container.parent_height=self.real_property_dict["height"]
        root_container.parent_width=self.real_property_dict["width"]
        image = root_container.render()
        return image

    def click(self, y, x):
        """
        When user click a point, we find the root container they click, then we loop that root container to find out which child container that user click...
        """
        if len(self.children) == 0:
            print(self.text)
            try:
                self.on_click_function(self, y, x)
            except Exception as e:
                try:
                    self.on_click_function()
                except Exception as e2:
                    print(e)
                    print(e2)
            return True

        clicked = False
        if self.rows == True:
            top = 0
            for one_row_container in self.children:
                left_top_y = one_row_container.real_property_dict.get("left_top_y")
                left_top_x = one_row_container.real_property_dict.get("left_top_x")
                right_bottom_y = one_row_container.real_property_dict.get("right_bottom_y")
                right_bottom_x = one_row_container.real_property_dict.get("right_bottom_x")

                if left_top_y != None and left_top_x != None and right_bottom_y != None and right_bottom_x != None:
                    if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                        clicked = clicked or one_row_container.click(y-top, x)
                        break

                top += one_row_container.real_property_dict["height"]
        elif self.columns == True:
            left = 0
            for one_column_container in self.children:
                left_top_y = one_column_container.real_property_dict.get("left_top_y")
                left_top_x = one_column_container.real_property_dict.get("left_top_x")
                right_bottom_y = one_column_container.real_property_dict.get("right_bottom_y")
                right_bottom_x = one_column_container.real_property_dict.get("right_bottom_x")

                if left_top_y != None and left_top_x != None and right_bottom_y != None and right_bottom_x != None:
                    if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                        clicked = clicked or one_column_container.click(y, x-left)
                        break

                left += one_column_container.real_property_dict["width"]

        if clicked == False:
            left_top_y = self.real_property_dict.get("left_top_y")
            left_top_x = self.real_property_dict.get("left_top_x")
            right_bottom_y = self.real_property_dict.get("right_bottom_y")
            right_bottom_x = self.real_property_dict.get("right_bottom_x")
            if left_top_y != None and left_top_x != None and right_bottom_y != None and right_bottom_x != None:
                if y >= left_top_y and y <= right_bottom_y and x >= left_top_x and x <= right_bottom_x:
                    # clicked at this container, but no children matchs, the point is at background
                    try:
                        self.on_click_function(self, y, x)
                    except Exception as e:
                        try:
                            self.on_click_function()
                        except Exception as e2:
                            print(e)
                            print(e2)
                    return True

        return clicked

    def advance_click(self, touch_start, touch_move, touch_end, y, x):
        pass


class Container_Helper:
    # Help you handle container related operations
    def iterate_child_container(self, root_container):
        # So that you can get a container that has some id in information, and get its real height and width in "node.real_property_dict"
        queue = [root_container]
        while (len(queue) != 0):
            child = queue.pop()
            if len(child.children) != 0:
                queue += child.children.copy()
            yield child


class GUI(Container):
    """
    This class will use Image class to represent graphic user interface, and also provide a top componet infomation list
    Which contains the touchable area for each component. For example, it has a function called "touch(y,x) -> image_id"

    We have to render the graph whenever the widget/component tree get changed

    The component tree is not a tree, it is a 2d array (matrix), it was combined with rows and columns. Normally row width got change according to parent window change, but height is fixed. It is similar to flutter or web broswer. Those elements inside those list is components. You can call self.render() to render that component matrix.

    In here, for User Interface, the parent big window would always be a rectangle, for example, 54*99 (1080*1980).

    The core feature should be:
    1. when children height or width beyound parent container, use a scroll bar automatically in either y or x direction. (in css, it is overflow-y or overflow-x)
    2. auto re-render a child container when one of global variable they use got changed. and for other container that did not change, we use cached image. someone call this feature "hot reload when variable got changed" (Or when user make change on some variable, or if the user call render function, we loop the container tree, see which container's property got changed, if so, we do a re_render. starts from top containers, level down, if re_rendered, only render its children for once) (Or you could use __setattr__(self, name, value) hook in python class, when a property got changed, you call render. def __setattr__(self, name, value): self.__dict__[name] = value)
    3. when user click a point, the GUI class should know which container the user clicked. so we can call on_click_function in that container.
    4. consider give a special paramater to render() function, let it return a list of rectangle that represent those changed part of the screen. So the LCD can render those pixel block very quickly. (for other UI rendering engine, they could just use changed pixel for screen update)
    """
    def __init__(self, *arguments, **key_arguments):
        super().__init__(*arguments, **key_arguments)


#class TextGUI():
#    """
#    Now, think about this: a character will take 8*16 pixels. 320*240 screen could show 40 * 15 = 600 characters. You can treat characters as pixels. Then you only have to handle 600 rectangles. So in your memory, you should have a 600 elements 2d list as graphic buffer.
#    For a terminal, it only has to have print_char function. So it you have LCD char buffer, for each time, you just have to move the top_left point of those char buffers. Just treat it like a one stream display flow (Don't forget the new line).
#    """
#    def __init__(self, height, width):
#        char_number_in_one_row = int(width // 8)
#        rows_number = int(height // 16)
#
#        self.raw_data = [[" "] * char_number_in_one_row] * rows_number


try:
    from typing import Any

    class MyPillow():
        """
        python3 -m pip install --upgrade Pillow
        """
        def __init__(self):
            from io import BytesIO
            from PIL import Image
            self._Image = Image
            self._BytesIO = BytesIO

            from auto_everything.disk import Disk
            self._disk = Disk()

        def read_image_from_file(self, file_path):
            return self._Image.open(file_path)

        def read_image_from_bytes_io(self, bytes_io):
            return self._Image.open(bytes_io)

        def read_image_from_base64_string(self, base64_string):
            return self.read_image_from_bytes_io(self._disk.base64_to_bytesio(base64_string=base64_string))

        def save_image_to_file_path(self, image, file_path):
            image.save(file_path)

        def save_bytes_io_image_to_file_path(self, bytes_io_image, file_path):
            with open(file_path, "wb") as f:
                f.write(bytes_io_image.getbuffer())

        def get_image_bytes_size(self, image):
            image = image.convert('RGB')
            out = self._BytesIO()
            image.save(out, format="jpeg")
            return out.tell()

        def decrease_the_size_of_an_image(self, image, quality=None):
            image = image.convert('RGB')
            out = self._BytesIO()
            if quality is None:
                image.save(out, format="jpeg")
            else:
                image.save(out, format="jpeg", optimize=True, quality=quality)
            out.seek(0)
            return out

        def force_decrease_image_file_size(self, image, limit_in_kb=1024):
            """
            :param image: PIL image
            :param limit: kb
            :return: bytes_io
            """
            image = image.convert('RGB')
            OK = False
            quality = 100
            out = self._BytesIO()
            while (OK is False):
                out = self._BytesIO()
                image.save(out, format="jpeg", optimize=True, quality=quality)
                size = self._disk.get_file_size(path=None, bytes_size=out.tell(), level="KB")
                if size is None:
                    break
                quality -= 3
                if size <= limit_in_kb or quality <= 3:
                    OK = True
            out.seek(0)
            return out
except Exception as e:
    pass


if __name__ == "__main__":
    from auto_everything.disk import Disk
    disk = Disk()
    image = Image()

    #a_image = image.read_image_from_file(disk._expand_user("~/Downloads/cat.jpg"))
    #print(a_image.get_shape())
    #print(a_image[0][0])
    #print(a_image)
    #a_image.resize(96, 128)
    ##a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/cat2.png.json")
    #a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/cat2.png")

    a_image = image.read_image_from_file(disk._expand_user("~/Downloads/hero.png"))
    a_image.resize(512, 512)
    a_image.paste_image_on_top_of_this_image(a_image, 100, 27, 100, 100)
    a_image.save_image_to_file_path("/home/yingshaoxo/Downloads/hero2.png")
