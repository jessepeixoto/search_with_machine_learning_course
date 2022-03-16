1. **For query classification:**
   - How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 100? To 1000?
       - `--min_queries 100 -> 815 categories`
       - `--min_queries 1000 ->  298 categories`
   - What values did you achieve for P@1, R@3, and R@5? You should have tried at least a few different models, varying the minimum number of queries per category as well as trying different fastText parameters or query normalization. Report at least 3 of your runs.
     - Minimum 1000
       - `-lr 0.5 -epoch 25 -wordNgrams 2`
         - P@1 = 0.102    | R@1 = 0.102
         - P@3 = 0.0592  | R@3 = 0.178
         - P@5 = 0.0444  | R@5 = 0.222
       - `-lr 0.2 -epoch 25 -wordNgrams 2`
         - P@1 = 0.109    | R@1 = 0.109
         - P@3 = 0.0594  | R@3 = 0.178
         - P@5  = 0.0418 | R@5 = 0.209
       - `-lr 0.1 -epoch 25 -wordNgrams 2`
         - P@1 = 0.110    | R@1 = 0.110
         - P@3 = 0.0579  | R@3 = 0.174
         - P@5  = 0.0425 | R@5 = 0.212
     - Minimum 100
       - `-lr 0.1 -epoch 25 -wordNgrams 2`
         - P@1 = 0.110  | R@1 = 0.110
         - P@3 = 0.0592 | R@3 = 0.178
         - P@5 = 0.0424 | R@5 = 0.212
         - 
2. For integrating query classification with search:
   - Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering. Make sure to include the classifier output for those queries.
     - `missing`
   - Given 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other reason. Again, include the classifier output for those queries.
     - `missing`
         