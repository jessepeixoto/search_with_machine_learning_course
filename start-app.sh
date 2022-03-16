pyenv virtualenv 3.9.7 search_with_ml_week4
pyenv local search_with_ml_week4

export SYNONYMS_MODEL_LOC=/workspace/datasets/fasttext/labeled_query_data.bin

export FLASK_ENV=development
export FLASK_APP=week4

flask run --port 3000
# flask run --port 5000