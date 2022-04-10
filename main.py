from html_flashcard_generator import HTMLFlashCardGenerator
from cambridge_word_crawler import CambridgeWordCrawler
def crawl_cambridge_file():
    cambridgeWordCrawler = CambridgeWordCrawler()
    cambridgeWordCrawler.get_word_list_from_directory()
    cambridgeWordCrawler.remove_phrases_in_file("word_list_from_directory")
    cambridgeWordCrawler.crawl_all_cambridge_words()
    cambridgeWordCrawler.merge_directory_and_all_word()
    cambridgeWordCrawler.sort_csv_file_by_topic("complete_detail_word")
    cambridgeWordCrawler.get_statistic_from_all()
    cambridgeWordCrawler.get_statistic_from_directory()

def generate_flashcard_html():
    html_flashcard_generator = HTMLFlashCardGenerator()
    html_flashcard_generator.create_all_flash_card_group_by_CEFR()
    html_flashcard_generator.print_topic_color()
    html_flashcard_generator.create_demo_csv()
    html_flashcard_generator.create_html_flashcard_from_csv("demo_file")

# crawl_cambridge_file()
generate_flashcard_html()