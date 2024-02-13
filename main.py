import random
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor

width, height = 1920, 1080
fps = 30
seconds = 10

cursor_x = 0
cursor_y = 0
cursor_width = 3
cursor_height = 15
cursor_fill1 = (0, 195, 255)
cursor_fill2 = (0, 0, 0)
cursor_fill = cursor_fill1


def generate_video():
    global cursor_x, cursor_y, cursor_fill
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))
    line_height = 36
    line_left = 50
    line_top = 50
    word_space = 12

    frame = np.zeros((height, width, 3), dtype=np.uint8)
    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)
    font_path = "JetBrainsMono-Medium.ttf"
    font_size = 20
    font_color = (255, 255, 255)
    common_font = ImageFont.truetype(font_path, font_size)

    chinese_font = ImageFont.truetype("MiSans-Medium.ttf", font_size)

    font = common_font
    with open("code.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    line_count = 1
    for line in lines:
        sys.stdout.write(f'\r{line_count} |{len(lines)}')
        sys.stdout.flush()
        clear_line = line.replace(" ", "").strip()
        if len(clear_line) == 0:
            continue
        text = "[{}] ".format(line_count)
        # keep line first space same
        # text_width = draw.textlength(text, font)
        text_width = 50
        draw.text((line_left, line_top), text, font=common_font, fill=font_color)
        line_left += text_width + word_space
        line_count = line_count + 1
        line = format_code(line)
        words = line.split(" ")
        img = np.array(image)
        write_img(out, img)
        for word in words:
            word = word.strip()
            if len(word) == 0:
                # space
                word = " "
            word_color = code_color(word)
            for ch in word:
                draw.rectangle([cursor_x, cursor_y, cursor_x + cursor_width, cursor_y + cursor_height],
                               fill=(0, 0, 0))
                text = ch
                if is_chinese(text):
                    font = chinese_font
                else:
                    font = common_font
                text_width = draw.textlength(text, font)

                draw.text((line_left, line_top), text, font=font, fill=word_color)
                line_left += text_width
                cursor_x, cursor_y = line_left, line_top + 8
                draw.rectangle([cursor_x, cursor_y, cursor_x + cursor_width, cursor_y + cursor_height],
                               fill=cursor_fill)
                if cursor_fill == cursor_fill1:
                    cursor_fill = cursor_fill2
                else:
                    cursor_fill = cursor_fill1
                img = np.array(image)
                write_img(out, img)
            line_left += word_space
        line_top = line_top + line_height
        line_left = 50
        # fill screen
        if line_top > height - 20:
            clear_code(out, draw, image)
            line_top = 50

    # release video file
    cursor_delay(5, out, draw, image)
    out.release()


def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'


def format_code(code):
    return code.replace('(', " ( ").replace(')', " ) ").replace('{', " { ").replace('}', " } ").replace("(  )", "()")


code_color_scheme = {"(": "#FFC300", ")": "#FFC300", "{": "#607D8B", "}": "#607D8B", "()": "#FFC300", "=": "#FFC300",
                     ";": "#651FFF", "'": "#304FFE"}

code_color_list = ["#F57F17", "#AFB42B", "#689F38", "#009688", "#0091EA", "#2962FF", "#651FFF"]


def cursor_delay(second, out, draw, image):
    global cursor_fill
    for i in range(second):
        draw.rectangle([cursor_x, cursor_y, cursor_x + cursor_width, cursor_y + cursor_height],
                       fill=cursor_fill)
        if cursor_fill == cursor_fill1:
            cursor_fill = cursor_fill2
        else:
            cursor_fill = cursor_fill1
        img = np.array(image)
        for j in range(fps):
            write_img(out, img)


def code_color(word):
    if word in code_color_scheme:
        color = ImageColor.getrgb(code_color_scheme[word])
    else:
        color = ImageColor.getrgb(random.choice(code_color_list))
    return color


def clear_code(out, draw, image):
    for i in range(0, int(height / 20) + 1):
        draw.rectangle([0, i * 20, 0 + width, i * 20 + 20],
                       fill=(0, 0, 0))
        out.write(np.array(image))


def write_img(out, img):
    for i in range(1):
        out.write(img)


if __name__ == '__main__':
    generate_video()
