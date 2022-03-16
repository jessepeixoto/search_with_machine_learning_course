import argparse
import csv
import os
import sys
import time
import xml.etree.ElementTree as ET

import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from transform_data import transform_data
from pandarallel import pandarallel

start = time.time()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/fasttext/labeled_query_data.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1, help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
categories_tree_df = pd.DataFrame(zip(categories, parents), columns=['category', 'category_parent'])

# read queries file and transform query
pandarallel.initialize()
queries_and_categories_df = pd.read_csv(queries_file_name)[['category', 'query']]
queries_and_categories_df["query"] = queries_and_categories_df['query'].parallel_apply(transform_data)

queries_per_category_df = queries_and_categories_df.groupby(['category']).size().to_frame('total_queries')

total_queries_per_category_df = pd.merge(categories_tree_df, queries_per_category_df, on="category", how='left').fillna(0)

valid_categories = total_queries_per_category_df[(total_queries_per_category_df['total_queries'] > min_queries)].category.tolist()

def get_ancestor_category(cat):
    if cat in valid_categories:
        return cat

    while cat not in valid_categories:
        parent_cat = categories_tree_df[(categories_tree_df['category'] == cat)].iloc[0]['category_parent']
        cat = parent_cat
        if cat == 'cat00000':
            return None
    return cat


total_queries_per_category_df['valid_category'] = total_queries_per_category_df.category.parallel_apply(get_ancestor_category)

total_queries_per_category_df['label'] = '__label__' + total_queries_per_category_df['valid_category']

query_and_category_merged_df = pd.merge(queries_and_categories_df, total_queries_per_category_df, on="category")
query_and_category_merged_df = query_and_category_merged_df[query_and_category_merged_df.valid_category.notnull()]

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
query_and_category_merged_df = query_and_category_merged_df[query_and_category_merged_df['category'].isin(categories)]
query_and_category_merged_df['output'] = query_and_category_merged_df['label'] + ' ' + query_and_category_merged_df['query']

end = time.time()
print(end - start)

# Export file
query_and_category_merged_df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)

end = time.time()
print(end - start)

print('Total of filtered categories: ', len(valid_categories))