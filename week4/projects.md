# Level 1: Query Classification
## Prune the category tree to a maximum depth by total of queries

Generate training and test pruned data
```sh 
python3 week4/create_labeled_queries.py --min_queries 1000
```

Split data into train and test 
```sh 
head -n -50000  /workspace/datasets/fasttext/labeled_query_data.txt | shuf -n 50000  > /workspace/datasets/fasttext/labeled_query_data.train

tail -n -50000  /workspace/datasets/fasttext/labeled_query_data.txt | shuf -n 50000  > /workspace/datasets/fasttext/labeled_query_data.test
```

Generate/train the model
```sh 
/workspace/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/labeled_query_data.train -output /workspace/datasets/fasttext/labeled_query_data -lr 0.5 -epoch 25 -wordNgrams 2
```

Test the model over all test data
```sh 
../fastText-0.9.2/fasttext test /workspace/datasets/fasttext/labeled_query_data.bin /workspace/datasets/fasttext/labeled_query_data.test

../fastText-0.9.2/fasttext test /workspace/datasets/fasttext/labeled_query_data.bin /workspace/datasets/fasttext/labeled_query_data.test 3

../fastText-0.9.2/fasttext test /workspace/datasets/fasttext/labeled_query_data.bin /workspace/datasets/fasttext/labeled_query_data.test 5
```