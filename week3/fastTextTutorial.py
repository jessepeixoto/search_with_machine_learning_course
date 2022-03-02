import fasttext

# Train model
model = fasttext.train_supervised(input="fasttext_training_data/cooking.train")

# Test single prediction
model.predict("easy recipe for sourdough bread ?")

# Evaluate on test data
model.test("fasttext_training_data/cooking.test")

# Retrain with 25 epochs, bigrams, and learning rate of 1.0 and evaluate again
model = fasttext.train_supervised(input="fasttext_training_data/cooking.train", lr=1.0, epoch=25, wordNgrams=2)
model.test("fasttext_training_data/cooking.test")
