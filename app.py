# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

import re

import xlsxwriter

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def is_positive(text_line):
    """ Return us True if the comment end with 1 """

    return True if text_line[-2] == '1' else False


def remove_stop_words(text_line):
    """ Remove the stpo words from the text given and also return a list with-out stop-words """

    text_tokens = word_tokenize(text_line)
    tokens_without_sw = [stop_word for stop_word in text_tokens if not stop_word in stop_words]
    return tokens_without_sw


def stemming_words(words):
    """ This Function try his best to return us a set list with the
     stemmed word of the list given """

    porter = PorterStemmer()
    wnl = WordNetLemmatizer()
    stemming_words_list = set()
    for un_stemmed_word in words: stemming_words_list.add(
        wnl.lemmatize(un_stemmed_word, pos="v") if wnl.lemmatize(un_stemmed_word).endswith('e') or
                                                   wnl.lemmatize(un_stemmed_word).endswith('y') or
                                                   wnl.lemmatize(un_stemmed_word).endswith('thing') or
                                                   wnl.lemmatize(un_stemmed_word).endswith('ly')
        else porter.stem(un_stemmed_word))
    return stemming_words_list


# Trying to make our custom stop-words to easily remove them
stop_words = stopwords.words('english')

stop_words_extra_list = [',', '-', '.', 'A', 'a', '1', '0', '?', '!', '@', '#', '$', '%', '^', '&', '*',
                         '(', ')', '-', '_', "'", '.', '/', '|', '|', '`', ';', ':', '~', '{', '}', '[',
                         ']', '..', '"', '+', "'",
                         ]

stop_words.extend(stop_words_extra_list)

# At the first, Program creat a word-list and list for each positive & negative sentences that we store words in
# words-list and a binary list for each line of our dataset to connect us to the words init
positive_list_words = set()
positive_list = []
negative_list_words = set()
negative_list = []

# Here we can define the file name withOut any pos-fix
# The Path we used is in subFolder called datasets
# This program planed Scheduled for txt dataset with exactly 1000 line of data
file_name = "dataset-name"

with open('datasets/' + file_name + '.txt') as file:
    text = file.readline()
    while text:
        if is_positive(text):
            positive_list_words = positive_list_words | stemming_words(remove_stop_words(
                re.sub(r'\d+', '', text.lower().replace("'", "").replace('"', '').replace('-', ' ').replace('.', ' '))))
        else:
            negative_list_words = negative_list_words | stemming_words(remove_stop_words(
                re.sub(r'\d+', '', text.lower().replace("'", "").replace('"', '').replace('-', ' ').replace('.', ' '))))
        text = file.readline()

positive_list_words = sorted(list(positive_list_words))
negative_list_words = sorted(list(negative_list_words))

with open('datasets/' + file_name + '.txt') as file:
    for x in range(1, 1001):
        line = file.readline()
        text_list = list(stemming_words(remove_stop_words(
            re.sub(r'\d+', '', line.lower().replace("'", "").replace('"', '').replace('-', ' ').replace('.', ' ')))))
        if is_positive(line):
            text = "0" * len(positive_list_words)
            text = list(text)
            for word in text_list:
                text[positive_list_words.index(word)] = "1"
            positive_list.append(text)
        else:
            text = "0" * len(negative_list_words)
            text = list(text)
            for word in text_list:
                text[negative_list_words.index(word)] = "1"
            negative_list.append(text)

# Combine words list with our binary list so we can easily iterate over them and have them all once below each other
final_positive_list = [positive_list_words] + positive_list
final_negative_list = [negative_list_words] + negative_list

# Write our final list in to excel file
# First Sheet will creat for positives list and the second one creat for negatives
with xlsxwriter.Workbook('datasets/' + file_name + '.xlsx') as workbook:
    for flag in range(2):
        if flag == 0:
            worksheet = workbook.add_worksheet(name="positive")
        else:
            worksheet = workbook.add_worksheet(name="negative")
        for row_num, data in enumerate(final_positive_list if flag == 0 else final_negative_list):
            if type(data) == 'str':
                worksheet.write_string(0, row_num, data)
            else:
                worksheet.write_row(row_num, 0, data)
