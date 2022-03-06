1. **For classifying product names to categories:** 
    - What precision (P@1) were you able to achieve?
        - 0.824
    - What fastText parameters did you use?
        - `-lr 1.0 -epoch 25 -wordNgrams 2 -minProducts 50`
    - How did you transform the product names?
      - Lowercase tokens
      - Removed english stop words
      - Stemmed with english snowball stemmer
      - Remove special characters
    - How did you prune infrequent category labels, and how did that affect your precision?
      - Filtered out categories with less than 50 products, it increased precision.
    - How did you prune the category tree, and how did that affect your precision?
      - Retrieved only the second or the 3rd level of category, it increased precision.


2. **For deriving synonyms from content:**
    - What 20 tokens did you use for evaluation?
      - Types: [Game, Software, Drive, GPS, Printers]
      - Manufacturer: [Samsung, HP, LG, Philips, Apple]
      - Departments: [COMPUTERS, ACCESSORIES]
      - Subclass: [KARAOKE, CHARGERS, NETBOOKS, DISHWASHER, SPEAKERS, GUITARS, BAGS]
    - What fastText parameters did you use?
      - `-minCount 50`
    - How did you transform the product names?
      - Lowercase tokens
      - Removed english stop words
      - Stemmed with english snowball stemmer
    - What threshold score did you use?
      - 0.9
    - What synonyms did you obtain for those tokens?
      - Game: prepaid, airtime, virgin, no-contract 
      - Software: galaxy
      - Drive: glove, universal, body, small
      - GPS: - 
      - Printers: 
      - Samsung: ii, galaxy
      - HP: -
      - LG: -
      - Phillips: silicone, defender, commuter, pink, shell, otterbox
      - Apple: purple, incase, griffin
      - COMPUTERS: -
      - ACCESSORIES: -
      - KARAOKE: -
      - CHARGERS: -
      - NETBOOKS: -
      - DISHWASHER: -
      - SPEAKERS: -
      - GUITARS: -
      - BAGS: -


3. **For integrating synonyms with search:**
    - How did you transform the product names (if different from previously)?
      - The same way as previous
    - What threshold score did you use?
      - 0.93
    - Were you able to find the additional results by matching synonyms?
      - Yes, it increased the recall for search `airtime` for example. No sure if it is a good thing.


4. **For classifying reviews:**
    - What precision (P@1) were you able to achieve?
    - What fastText parameters did you use?
    - How did you transform the review content?
    - What else did you try and learn?