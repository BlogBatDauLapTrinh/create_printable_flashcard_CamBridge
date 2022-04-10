import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import bs4
MAX_INDEX = 6778 + 1
LIST_type_of_speech = ['adjective', 'adverb', 'auxiliary verb', 'determiner', 'exclamation',
             'modal verb', 'noun', 'phrasal verb', 'phrase', 'preposition', 'pronoun', 'verb']
LIST_CEFR = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
LIST_TOPIC = ['animals', 'arts and media', 'body and health', 'clothes', 'communication', 'crime', 'describing things', 'education', 'food and drink', 'homes and buildings',
              'money', 'natural world', 'people: actions', 'people: appearance', 'people: personality', 'politics', 'relationships', 'shopping', 'technology', 'travel', 'work']
BASE_URL = "https://www.englishprofile.org"


class CambridgeWordCrawler():
    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=op)
        self.BASE_URL = f"https://www.englishprofile.org/"
        self.get_html_from_local_html()        

    def get_html_from_local_html(self):
        with open('English Profile - EVP Online.html', 'r') as f:
            self.html_content = '\n'.join(f.readlines())

    def get_detail_word_from_url(self,clean_word_url):
        self.driver.get(clean_word_url)
        detail_word_html = self.driver.page_source
        soup = bs4.BeautifulSoup(detail_word_html)
        guide_word = ""
        cefr = ""
        description = ""
        dictionary_examples = ""
        learner_examples = ""
        en_word = ""
        type_of_speech = ""
        mp3 = ""
        for pos_section in soup.find_all('div', class_="pos_section"):
            en_word = pos_section.find('span', class_='headword').get_text()
            type_of_speech = pos_section.find('span', class_='pos').get_text()
            mp3 = pos_section.find('audio').find('source')['src']
            ipa= pos_section.find('span',class_="written").get_text()
            print(f"{en_word}\t{type_of_speech}\t{mp3}")
            for info_sense in pos_section.find_all("div", class_='sense'):
                guide_word = info_sense.find(
                    'div', class_="sense_title").get_text()
                cefr = info_sense.find(
                    'div', class_="body").find_all('span')[0].get_text()
                description = info_sense.find(
                    'div', class_="body").find('span',class_="definition").get_text()
                try:
                    dictionary_examples = [example.get_text() for example in info_sense.find(
                        'div', class_="example").find_all("p")]
                    dictionary_examples = "^".join(dictionary_examples)
                except:
                    pass
                try:
                    learner_examples = [example.get_text() for example in info_sense.find(
                        'div', class_="learner").find_all("p")]
                    learner_examples = "^".join(learner_examples)
                except:
                    pass

                with open('data_csv/all_cambridge_words.csv', 'a') as f_detail:
                    f_detail.writelines(
                        f"{en_word}|{guide_word}|{cefr}|{type_of_speech}|{description}|{dictionary_examples}|{learner_examples}|{BASE_URL + mp3}|{clean_word_url}|{ipa}\n")
                    
    def crawl_all_cambridge_words(self):
        index = 0
        while index < MAX_INDEX:
            clean_word_url = f"https://www.englishprofile.org/british-english/words/detail/{index}"
            self.get_detail_word_from_url(clean_word_url)
            index += 1

    def get_word_list_from_directory(self):
        soup = bs4.BeautifulSoup(self.html_content, "html.parser")
        with open('data_csv/word_list_from_directory.csv', 'w') as f:
            f.writelines("")
        
        for tr in [tr for tr in soup.find('tbody').find_all('tr')]:
            base_word = tr.find_all('td')[0].get_text().strip().replace('\t', ' ').replace('  ', ' ').replace(
                '  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('\n', ' ').replace('\n', ' ')
            guide_word = tr.find_all('td')[1].get_text().strip()
            cefr = tr.find_all('td')[2].get_text().strip()
            type_of_speech = tr.find_all('td')[3].get_text().strip()
            topic = tr.find_all('td')[4].get_text().strip()
            url = tr.find_all('td')[5].find('a')['href'].strip()
            with open('data_csv/word_list_from_directory.csv', 'a') as f:
                f.writelines(
                    f'{base_word}|{guide_word}|{cefr}|{type_of_speech}|{topic}|{url}\n')

    def get_statistic_from_directory(self):
        with open("data_csv/word_list_from_directory.csv", 'r') as f:
            word_list = f.readlines()

        origin_list_type_of_speech = [word.split("|")[3] for word in word_list]
        list_type_of_speech = sorted((set(origin_list_type_of_speech)))
        print(list_type_of_speech)

        origin_list_cefr = [word.split("|")[2] for word in word_list]
        list_cefr = sorted(set(origin_list_cefr))
        print(list_cefr)

        origin_list_topic = [word.split("|")[4] for word in word_list]
        list_topic = sorted(set(origin_list_topic))
        print(list_topic)


    def get_statistic_from_all(self):
        with open("data_csv/all_cambridge_words.csv", 'r') as f:
            word_list = f.readlines()

        origin_list_type_of_speech = [word.split("|")[3] for word in word_list]
        list_type_of_speech = sorted((set(origin_list_type_of_speech)))
        print(list_type_of_speech)
        origin_list_cefr = [word.split("|")[2] for word in word_list]
        list_cefr = sorted(set(origin_list_cefr))
        print(list_cefr)

    def sort_csv_files_by_enword(self, file_name):
        reader = csv.reader(open(f"data_csv/{file_name}.csv"), delimiter="|")
        sortedlist = sorted(reader, key=lambda row: row[0], reverse=False)
        with open(f'data_csv/sorted_{file_name}.csv', 'w') as f:
            f.writelines("")
        for row in sortedlist:
            with open(f'data_csv/sorted_{file_name}.csv', 'a') as f:
                f.writelines(f"{'|'.join(row)}\n")
    
    def sort_csv_file_by_topic(self, file_name="complete_detail_word"):
        reader = csv.reader(open(f"data_csv/{file_name}.csv"), delimiter="|")
        sortedlist = sorted(reader, key=lambda row: row[0], reverse=False)
        with open(f'data_csv/sorted_{file_name}.csv', 'w') as f:
            f.writelines("")
        for row in sortedlist:
            with open(f'data_csv/sorted_{file_name}.csv', 'a') as f:
                f.writelines(f"{'|'.join(row)}\n")

    def remove_phrases_in_file(self,file_name):
        with open(f'data_csv/{file_name}.csv', 'r') as f:
            raw_list = f.readlines()
        clean_list = [row for row in raw_list if "|phrase|" not in row and "|phrasal verb|" not in row]
        with open(f'data_csv/{file_name}.csv', 'w') as f:
            f.writelines(clean_list)
        
    def count_unique_detail_words(self,level="Z"):
        with open('data_csv/complete_detail_word.csv', 'r') as f:
            list_unique = [word.split("|")[1] for word in f.readlines() if word.split("|")[3] <= level]        
        print(len(set(list_unique)))

    def merge_directory_and_all_word(self,max_level = "Z"):

        with open('data_csv/complete_detail_word.csv', 'w') as f_detail:
            f_detail.writelines('')
        with open('data_csv/all_cambridge_words.csv','r') as f:
            self.all_word = f.readlines()
        
        with open('data_csv/word_list_from_directory.csv','r') as f:
            self.list_word_in_directory = f.readlines()

        with open('data_csv/complete_detail_word.csv', 'a') as f_detail:
            with open('data_csv/not_found_in_directory.csv', 'a') as f_not_found:
        
                for index,word_in_directory in enumerate(self.list_word_in_directory):
                    _en_word = word_in_directory.split("|")[0]
                    _guide_word = word_in_directory.split("|")[1]
                    _cefr = word_in_directory.split("|")[2]
                    _type_of_speech = word_in_directory.split("|")[3]
                    topic = word_in_directory.split("|")[4]

                    if _cefr > max_level: continue

                    for word in self.all_word:
                        cefr = word.split("|")[2]
                        en_word = word.split("|")[0]
                        type_of_speech = word.split("|")[3]
                        guide_word = word.split("|")[1]

                        if en_word == _en_word and cefr == _cefr and (type_of_speech == _type_of_speech or type_of_speech == "number" or type_of_speech == "ordinal number") and (_guide_word in guide_word or guide_word == en_word):
                            if topic == "" or topic == " ":
                                topic = "other"
                            f_detail.writelines(f"{topic}|{word}")
                            break

                            
                    else:
                        for word in self.all_word:
                            cefr = word.split("|")[2]
                            en_word = word.split("|")[0]
                            type_of_speech = word.split("|")[3]
                            guide_word = word.split("|")[1]

                            if en_word == _en_word and cefr == _cefr and (type_of_speech == _type_of_speech or type_of_speech == "number" or type_of_speech == "ordinal number") and (_guide_word in guide_word or guide_word == en_word):
                                if topic == "" or topic == " ":
                                    topic = "other"
                                f_detail.writelines(f"{topic}|{word}")
                                break

                        else: 
                            f_not_found.writelines(f"{word_in_directory}")
