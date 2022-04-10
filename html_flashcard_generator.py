import math
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
import glob
import os
import random
MAX_WIDTH = 285
TEXT_SIZE = 15
NUMBER_CARD_PER_PAGE = 20
NUMBER_CARD_PER_ROW = 4
WORD_PER_PART = 1600

LIST_LEVEL = ["A1", "A2", "B1", "B2", "C1", "C2"]
LIST_TOPIC = ['animals', 'arts and media', 'body and health', 'clothes', 'communication', 'crime', 'describing things', 'education', 'food and drink', 'homes and buildings',
              'money', 'natural world', 'people: actions', 'people: appearance', 'people: personality', 'politics', 'relationships', 'shopping', 'technology', 'travel', 'work']

LIST_TOPIC_COLOR = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
                    '#008080', '#e6beff', '#9a6324', '#fffac8', '#a10000', '#aaffc3', '#808000', '#ffd8b1', '#00aafc', '#808080', '#cccccc']


class HTMLFlashCardGenerator():
    def __init__(self) -> None:
        self.FILE_NAME = "complete_detail_word"
        self.NUMBER_CARD_PER_PAGE = NUMBER_CARD_PER_PAGE
        self.NUMBER_CARD_PER_ROW = NUMBER_CARD_PER_ROW
        self.MAX_WIDTH = MAX_WIDTH
        self.TEXT_SIZE = TEXT_SIZE
        # init font
        font = TTFont('font/Voces-Regular.ttf')
        cmap = font['cmap']
        self.t = cmap.getcmap(3, 1).cmap
        self.s = font.getGlyphSet()
        self.units_per_em = font['head'].unitsPerEm

    def getTextWidth(self, text, pointSize):
        total = 0
        for c in text:
            if ord(c) in self.t and self.t[ord(c)] in self.s:
                total += self.s[self.t[ord(c)]].width
            else:
                total += self.s['.notdef'].width
        total = total*float(pointSize)/self.units_per_em
        return total

    def get_split_description(self, text):

        list_splitted_text = text.split(' ')
        start_index_line = 0
        description = []
        for i, word in enumerate(list_splitted_text):
            if self.getTextWidth(" ".join(list_splitted_text[start_index_line:i]), TEXT_SIZE) > MAX_WIDTH:
                description += [" ".join(list_splitted_text[start_index_line:i-1])]
                start_index_line = i-1
            if i+1 == len(list_splitted_text) and self.getTextWidth(" ".join(list_splitted_text[start_index_line:i+1]), TEXT_SIZE) > MAX_WIDTH:
                description += [" ".join(list_splitted_text[start_index_line:i-1])]
                start_index_line = i-1

        description += [" ".join(list_splitted_text[start_index_line:i+1])]
        return description

    def create_html_flash_card(self, min_level="A1", max_level="C2", print_topic_color=False):
        with open(f'data_csv/{self.FILE_NAME}.csv', 'r') as f:
            word_list = [word for word in f.readlines() if word.split(
                '|')[3] <= max_level and word.split('|')[3] >= min_level]
            num_of_part = math.ceil(len(word_list)/WORD_PER_PART)

        for part_idx in range(num_of_part):
            if num_of_part == 1:
                file_name = f"cambridge_flashcard_{min_level}_{max_level}_full_part"
            else:
                file_name = f"cambridge_flashcard_{min_level}_{max_level}_part_{part_idx+1}"
            with open(f"data_csv/{file_name}.csv", 'a') as f:
                for word_idx in range(part_idx*WORD_PER_PART, part_idx*WORD_PER_PART+WORD_PER_PART):
                    if word_idx >= len(word_list):
                        break
                    f.writelines(word_list[word_idx])
            self.create_html_flashcard_from_csv(f"{file_name}")
            os.system(f'rm "data_csv/{file_name}.csv"')

    def create_html_flashcard_from_csv(self, file_name, print_topic_color=False):
        with open(f'data_csv/{file_name}.csv', 'r') as f:
            word_list = [word for word in f.readlines()]
        number_of_word = len(word_list)
        number_of_page = math.ceil(len(word_list)/NUMBER_CARD_PER_PAGE)
        with open(f'output_html/{file_name}.html', 'w') as f:
            style_css = " <style>{style_css}</style>"

            f.writelines(
                f'<!DOCTYPE html><html lang="en"><head> <link rel="stylesheet" href="index.css">  <meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{file_name}_without_line</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;500;700&display=swap" rel="stylesheet"></head><body>')

        with open(f'output_html/{file_name}.html', 'a') as f:
            for page_index in range(number_of_page):
                for row in range(NUMBER_CARD_PER_PAGE//NUMBER_CARD_PER_ROW):
                    f.writelines('<div class="container">')
                    base_index = page_index*NUMBER_CARD_PER_PAGE+row*NUMBER_CARD_PER_ROW
                    for card in range(NUMBER_CARD_PER_ROW):
                        # 0{topic} 1{en_word} 2{guide_word} 3{cefr} 4{type} 5{description} 6{dictionary_examples} 7{learner_example} 8{BASE_URL + mp3} 9{clean_word_url}

                        card_index = base_index + card
                        if card_index < number_of_word:
                            type_of_speech = word_list[card_index].split('|')[
                                4]
                            en_word = word_list[card_index].split('|')[1]
                            description = word_list[card_index].split('|')[5]
                            if len(description) > 170:
                                description = description.split('.')[0]
                            if len(description) > 170:
                                description = description.split(';')[0]
                            split_description = self.get_split_description(
                                description)
                            main_description = ""
                            additional_description = ""
                            for i, _ in enumerate(split_description):
                                if i < 3:
                                    main_description += " " + \
                                        split_description[i]
                                else:
                                    additional_description += " " + \
                                        split_description[i]
                            topic = word_list[card_index].split('|')[0]
                            try:
                                idx_color = LIST_TOPIC.index(topic)
                                topic_color = LIST_TOPIC_COLOR[idx_color]
                            except:
                                topic_color = "#fff"
                            if word_list[card_index].split('|')[2] == en_word:
                                guide_word = "&emsp;&emsp;&emsp;"
                            else:
                                guide_word = word_list[card_index].split(
                                    '|')[2].replace(f"{en_word} ", "")[1:-1]
                            # print(guide_word)

                        else:
                            guide_word = "&emsp;&emsp;&emsp;"
                            type_of_speech = "noun"
                            en_word = "BatDauLapTrinh"
                            main_description = "A blog where  wrote about lesson experience I have learned along my career path"
                        if len(guide_word) < 15:
                            front_card_html = f'<div class="front_card"><span class="type_of_word" >{type_of_speech}</span><span class="guide_word" style="background-color:{topic_color};">{guide_word}</span><h2 class="word">{en_word}</h2><p class="describe">{main_description}</p><p class="additional_describe">{additional_description}</p></div>'
                        elif len(guide_word) > 22:
                            front_card_html = f'<div class="front_card"><span class="type_of_word" >{type_of_speech}</span><span class="guide_word" style="background-color:{topic_color}; font-size:12px">{guide_word}</span><h2 class="word">{en_word}</h2><p class="describe">{main_description}</p><p class="additional_describe">{additional_description}</p></div>'
                        else:
                            front_card_html = f'<div class="front_card"><span class="type_of_word" >{type_of_speech}</span><span class="guide_word" style="background-color:{topic_color}; font-size:14px">{guide_word}</span><h2 class="word">{en_word}</h2><p class="describe">{main_description}</p><p class="additional_describe">{additional_description}</p></div>'
                        f.write(front_card_html)
                    f.writelines('</div>')

                for row in range(NUMBER_CARD_PER_PAGE//NUMBER_CARD_PER_ROW):
                    f.writelines('<div class="container">')
                    base_index = page_index*NUMBER_CARD_PER_PAGE+row*NUMBER_CARD_PER_ROW
                    for card in range(NUMBER_CARD_PER_ROW-1, -1, -1):
                        card_index = base_index + card
                        if card_index < number_of_word:
                            # ipa_us = word_list[card_index].split('|')[6]
                            ipa_us = word_list[card_index].split('|')[-1]
                            example = word_list[card_index].split(
                                '|')[6].split('^')[-1]
                            try:
                                example_x = word_list[card_index].split('|')[
                                    6].split('^')[-2]
                            except:
                                example_x = ""
                            if len(BeautifulSoup(example, features="lxml").text) < 50:
                                try:
                                    example_x = word_list[card_index].split(
                                        '|')[9].split(';')[-2].replace('li', 'span')
                                    if len(BeautifulSoup(example_x).text) > 50:
                                        example_x = ""
                                except:
                                    pass
                        else:
                            ipa_us = "   BatDauLapTrinh"
                            example = "How to create English Flashcard for printing"
                            example_x = "Use study set to learn anything you want in ELSA SPEAK FREE"
                        f.write(
                            f'<div class="back_card"><h2 class="ipa">{ipa_us}</h2><div class="container_example"><p class="example">{example}</p><p class="example">{example_x}</p></div></div>')
                    f.writelines('</div>')
                f.writelines('<div class="pagebreak"> </div>')
            if print_topic_color:
                self.add_topic_color(f)
            f.writelines('</body></html>')

    def add_topic_color(self, f):
        CARD_PER_ROW = 4
        for idx_row in range(len(LIST_TOPIC)//CARD_PER_ROW):
            f.writelines('<div class = "container">')
            for idx_column in range(CARD_PER_ROW):
                f.writelines(
                    f'<div class="front_card" style="background-color:{LIST_TOPIC_COLOR[idx_row*CARD_PER_ROW+idx_column]};" ></span><h2  style="color:black; top: 28px; margin: 40px 20px 20px; text-align: center;"> {LIST_TOPIC[idx_row*CARD_PER_ROW+idx_column]}<br>{LIST_TOPIC_COLOR[idx_row*CARD_PER_ROW+idx_column]}</h2></div>')
            f.writelines('</div>')

    def print_topic_color(self):
        with open(f'output_html/cambridge_topic_color.html', 'w') as f:
            f.writelines("")
        with open(f'output_html/cambridge_topic_color.html', 'a') as f:
            style_css = " <style>{style_css}</style>"
            f.writelines(f'<!DOCTYPE html><html lang="en"><head> <link rel="stylesheet" href="index.css">  <meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>FLASHCARD_CAMBRIDGE_TOPIC_COLOR</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;500;700&display=swap" rel="stylesheet"></head><body>')
            self.add_topic_color(f)
            f.writelines('</body></html>')

    def create_demo_csv(self):
        with open("data_csv/complete_detail_word.csv", 'r') as f:
            word_list = f.readlines()
        with open("data_csv/demo_file.csv", 'w') as f:
            f.writelines("")
        count_down = 38
        list_topic = LIST_TOPIC
        while count_down != 0:
            word_idx = random.randint(0, len(word_list))
            if ((word_list[word_idx].split("|")[0] in list_topic or (word_list[word_idx].split("|")[0] not in list_topic and word_idx % 8 == 0)) and word_list[word_idx].split("|")[1] != word_list[word_idx].split("|")[2]):
                with open("data_csv/demo_file.csv", 'a') as f:
                    f.writelines(word_list[word_idx])
                    count_down -= 1

    def create_all_flash_card_group_by_CEFR(self):
        for level in LIST_LEVEL:
            self.create_html_flash_card(level, level)
