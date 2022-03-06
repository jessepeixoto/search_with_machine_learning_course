import argparse
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path

import nltk
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

special_characters = ['!', '#', '$', '%', '&', '@', '[', ']', ']', '_', '-', '®', '?', ':', '(', ')', '™', '/',
                      '\'', ',', '+']


def transform_name(product_name):
    tokens = nltk.word_tokenize(product_name)
    tokens = [token.lower() for token in tokens]
    tokens = [token for token in tokens if (token not in nltk.corpus.stopwords.words('english'))]
    tokens = [nltk.stem.snowball.SnowballStemmer("english").stem(token) for token in tokens]
    product_name = ' '.join(tokens)
    for special_character in special_characters:
        product_name = product_name.replace(special_character, ' ')
    return product_name


# Directory for product data
directory = r'/workspace/search_with_machine_learning_course/data/pruned_products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory, help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")

# Consuming all of the product data will take over an hour! But we still want to be able to obtain a representative sample.
general.add_argument("--sample_rate", default=1.0, type=float,
                     help="The rate at which to sample input (default is 1.0)")

general.add_argument("--min_products", default=0, type=int,
                     help="The minimum number of products per category (default is 0).")

args = parser.parse_args()
output_file = args.output
path = Path(output_file)
output_dir = path.parent
if os.path.isdir(output_dir) == False:
    os.mkdir(output_dir)

if args.input:
    directory = args.input
min_products = args.min_products
sample_rate = args.sample_rate

df_cols = ["cat", "name"]
rows = []

print("Writing results to %s" % output_file)
with open(output_file, 'w') as output:
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            print("Processing %s" % filename)
            f = os.path.join(directory, filename)
            tree = ET.parse(f)
            root = tree.getroot()
            for child in root:
                if random.random() > sample_rate:
                    continue
                # Check to make sure category name is valid
                if (child.find('name') is not None and child.find('name').text is not None and
                        child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
                        child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None):
                    catId = child.find('categoryPath')

                    # Choose last element in categoryPath as the leaf categoryId
                    if [len(child.find('categoryPath'))][0] > 3:
                        cat = child.find('categoryPath')[2][0].text
                    elif [len(child.find('categoryPath'))][0] > 2:
                        cat = child.find('categoryPath')[1][0].text
                    else:
                        cat = child.find('categoryPath')[0][0].text
                    # Replace newline chars with spaces so fastText doesn't complain
                    name = child.find('name').text.replace('\n', ' ')
                    rows.append({"cat": cat, "name": transform_name(name)})

    df = pd.DataFrame(rows, columns=df_cols)
    dfFiltered = df.groupby(['cat']).filter(lambda x: len(x) >= min_products)
    dfFiltered['output'] = '__label__' + dfFiltered['cat'] + ' ' + dfFiltered['name']
    dfFiltered.output.to_csv(output, header=False, index=False, sep='\t')
