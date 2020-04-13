# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief: 配置文件


import os

train_path = "data/train.txt"
test_path = "data/test.txt"
#train_seg_path = "data/train_words_update"  # segment of train file
#train_seg_path = "/ssd1/zhubenchang/data/train.txt"  # segment of train file
train_seg_path = "/ssd1/zhubenchang/data/mix_train_seg"  # segment of train file
test_seg_path = "data/test_seg_sample.txt"    # segment of test file
col_sep = '\t'                                # separate label and content of train data

sentence_symbol_path = 'data/sentence_symbol.txt'
stop_words_path = 'data/stop_words.txt'
is_debug = False                               # open debug mode, default "True"

# one of "logistic_regression, random_forest, bayes, decision_tree, svm, knn, xgboost, xgboost_lr,
# mlp, ensemble, stack, fasttext, cnn, rnn, han"
#model_type = "logistic_regression"
#model_type = "fasttext"
#model_type = "xgboost"
model_type = "cnn"

# feature type usage
# classic text classification usage:  one of "tfidf_char, tfidf_word, tf_word",
# deep text classification usage: han is "doc_vectorize"; cnn, fasttext, rnn is "vectorize"
feature_type = 'vectorize'
#feature_type = 'tf_word'
#feature_type = 'tfidf_word'

output_dir = "/ssd1/zhubenchang/output"                                                                # output dir
output_dir_local = "output"                                                                # output dir
word_vocab_path = output_dir + "/vocab_" + feature_type + "_" + model_type + ".txt"  # vocab path
label_vocab_path = output_dir_local + "/label_" + feature_type + "_" + model_type + ".txt" # label path
pr_figure_path = output_dir_local + "/R_P_" + feature_type + "_" + model_type + ".png"     # precision recall figure
feature_vec_path = output_dir + "/feature_" + feature_type + ".pkl"                # vector path
model_save_path = output_dir + "/model_" + feature_type + "_" + model_type + ".pkl"  # save model path

# --- deep model for train ---
max_len = 200  # max len words of sentence
min_count = 5  # word will not be added to dictionary if it's frequency is less than min_count
batch_size = 128
nb_epoch = 3
embedding_dim = 128
hidden_dim = 128
dropout = 0.5

# predict
pred_save_path = output_dir + "/pred_result_" + feature_type + "_" + model_type + ".txt"  # predict data result

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
