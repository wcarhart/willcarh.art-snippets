import re

# we can't split sentences on abbreviations that end in a '.'
ABB = [
    'etc', 'mr', 'mrs', 'ms', 'dr', 'sr',
    'jr', 'gen', 'rep', 'sen', 'st', 'al',
    'eg', 'ie', 'in', 'phd', 'md', 'ba',
    'dds', 'ma', 'mba', 'inc', 'pm', 'am',
    'jan', 'feb', 'mar', 'apr', 'jun', 'jul',
    'aug', 'sep', 'sept', 'oct', 'nov', 'dec',
    'mon', 'tue', 'wed', 'weds', 'thur',
    'thu', 'thurs', 'fri', 'fig'
]

# if we come across a word with a '.' that ends in one of these common file
# extensions, we should not split on the '.'
EXT = [
    'js', 'py', 'txt', 'json', 'doc', 'docx', 'pdf',
    'bash', 'sh', 'java', 'jsx', 'html', 'css', 'db',
    'md', 'csh', 'zsh', 'xsh', 'cpp', 'swift', 'gpg',
    'pickle', 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'lock',
    'rb', 'git', 'gitignore', 'ico', 'webmanifest',
    'icns', 'xls', 'xlsx', 'ppt', 'pptx', 'asp', 'aspx',
    'yaws', 'pl', 'php', 'xml', 'svg', 'heic', 'mov',
    'bz2', 'csv', 'cs', 'erl', 'asm', 'awk', 'bat', 'bmp',
    'class', 'dll', 'dump', 'exe', 'hpp', 'jar', 'log', 
    'obj', 'rc', 'ts', 'rs', 'wav', 'zip', 'com', 'nl',
    'ms'
]

# we should exclude these common words when scoring sentences to get more
# accurate sentence scores
EXCLUDE = [
    'the', 'of', 'to', 'a', 'and', 'in', 'that',
    'he', 'she', 'on', 'as', 'his', 'hers', 'for',
    'is', 'by', 'was', 'with', 'at', 'from', 'has',
    'its', 'mr', 'mrs', 'ms', 'dr', 'sr', 'jr',
    'sen', 'rep', 'st', 'said', 'it', 'be', 'not',
    'or', 'but', 'who', 'when', 'your', 'those',
    'these', 'you', 'this', 'they', 'we', 'our',
    'will', 'are', 'am', 'can', 'an', 'have', 'how',
    'my', 'which', 'their', 'theirs', 'what', 'her',
    'him', 'had', 'would', 'them', 'like', 'than',
    'could', 'did', 'do'
]

def get_sentences(text):
    # attempt to split sentences on .?!
    sentences = [chunk for chunk in re.split('([.?!])', text) if not chunk == '' and not chunk.isspace()]
    sentences = [x+y for x,y in zip(sentences[0::2], sentences[1::2])]

    # let's assume that we have a list of known abbreviations in a list called ABB
    # and a list of known extensions in a list call EXT
    # we'll need to join our sentences together if they were split on an abbreviation or extension
    index = 0
    while index < len(sentences) - 2:
        last_word_previous_sentence = ''.join(character for character in sentences[index].split()[-1].lower() if character.isalnum()).lower()
        first_word_next_sentence = ''.join(character for character in sentences[index+1].split()[0].lower() if character.isalnum()).lower()
        if (
            last_word_previous_sentence in ABB
            or first_word_next_sentence in EXT
            or len(last_word_previous_sentence) == 1
            or len(first_word_next_sentence) == 1
        ) and (
            not last_word_previous_sentence in ['a', 'i']
            and not first_word_next_sentence in ['a', 'i']
        ):
            sentences[index] = ''.join([sentences[index], sentences[index + 1]])
            del sentences[index + 1]
        else:
            index += 1
    return [sentence.strip() for sentence in sentences]

def calculate_word_frequency(sentences):
    frequencies = {}
    words = ' '.join(sentences).split()
    raw_words = [''.join(character for character in word if character.isalnum()).lower() for word in words]
    for word in raw_words:
        if word in EXCLUDE:
            frequencies[word] = 0
        elif word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

    if '' in frequencies:
        del frequencies['']
    return frequencies

def calculate_sentence_scores(sentences, frequencies):
    scores = []
    for sentence in sentences:
        score = 0
        for word in sentence.split():
            raw_word = ''.join(character for character in word if character.isalnum()).lower()
            if raw_word == '':
                continue
            score += frequencies[raw_word]
        scores.append(score)

    sentence_scores = list(zip(sentences, scores))
    return sentence_scores

def build_summary(scores, limit):
    # build list of sentence indicies
    sentence_indices = []
    for index, score in enumerate(scores):
        sentence_indices.append((index, score[1]))

    # sort based on sentence score
    sorted_sentences = sorted(sentence_indices, key=lambda item: item[1])[::-1]

    # build list of highest ranked sentences
    summary_sentences = []
    for index in range(limit):
        if index < len(scores) - 1:
            summary_sentences.append(scores[sorted_sentences[index][0]][0])

    summary = ' '.join(summary_sentences)
    return summary

if __name__ == '__main__':
    # update text as desired
    text = ''
    sentences = get_sentences(text)
    frequencies = calculate_word_frequency(sentences)
    scores = calculate_sentence_scores(sentences, frequencies)
    summary = build_summary(summary)
    print(summary)
