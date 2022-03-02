pyenv virtualenv 3.9.7 search_with_ml_week3
pyenv local search_with_ml_week3

export SYNONYMS_MODEL_LOC=/workspace/datasets/fasttext/title_model.bin

export FLASK_ENV=development
export FLASK_APP=week3

flask run