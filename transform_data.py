import nltk

special_characters = ['!', '#', '$', '%', '&', '@', '[', ']', ']', '_', '-', '®', '?', ':', '(', ')', '™', '/',
                      '\'', ',', '+']


def transform_data(data):
    tokens = nltk.word_tokenize(data)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if (token not in nltk.corpus.stopwords.words('english'))]
    tokens = [nltk.stem.snowball.SnowballStemmer("english").stem(token) for token in tokens]
    data = ' '.join(tokens)
    for special_character in special_characters:
        data = data.replace(special_character, ' ')
    return data
