import email
import numpy
from datetime import datetime

def get_subject_factors(subject):
    # number of words
    # average word length
    word_list = subject.split()

    total_word_length = 0
    for i in word_list:
        total_word_length += len(i)

    avg_word_length = total_word_length / len(word_list)
    num_words = len(word_list)

    return [num_words, avg_word_length]


def get_date_factors(date):
    # time of day (hour)
    # day of week
    new_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")

    hour = new_date.hour
    weekday = new_date.weekday()

    return [hour, weekday]


def get_email_factors(email_address):
    # site name
    # site suffix

    # name: <could not parse> <gmail> <yahoo> <other>
    # suffix: <could not parse> <com> <org> <edu> <other>

    email_addr = email.utils.parseaddr(email_address)[1]
    email_suffix = email_addr.split('@')
    site_name_code = [0,0,0,0]
    site_suffix_code = [0,0,0,0,0]

    if len(email_suffix) >= 2:
        email_suffix = email_suffix[1]
        site_suffix = email_suffix.split('.')
        site_name = site_suffix[0]
        top_level_domain = site_suffix[-1]

        if site_name == 'gmail':
            site_name_code[1] = 1
        elif site_name == 'yahoo':
            site_name_code[2] = 1
        else:
            site_name_code[3] = 1

        if top_level_domain == 'com':
            site_suffix_code[1] = 1
        elif top_level_domain == 'org':
            site_suffix_code[2] = 1
        elif top_level_domain == 'edu':
            site_suffix_code[3] = 1
        else:
            site_suffix_code[4] = 1

    else:
        site_name_code[0] = 1
        site_suffix_code[0] = 1

    name_and_suffix = site_name_code + site_suffix_code
    return name_and_suffix


def get_message_factors(message):
    # number of lines
    # number of words
    # average word length
    # standard deviation of word length
    # number of question marks

    message = str(message)
    num_lines = len(message.split('\n'))

    words = message.split()
    num_words = len(words)

    words_length_list = []
    for word in words:
        words_length_list.append(len(word))

    arr = numpy.array([words_length_list])
    avg_word_length = numpy.mean(arr)
    word_std_dev = numpy.std(arr)

    num_question_marks = message.count('?')

    return [num_lines, num_words, avg_word_length, word_std_dev, num_question_marks]
