# -*- coding: gbk -*-
"""
@author:XuMing��xuming624@qq.com)
@description: 
"""

import os
import pickle
from collections import Counter

import jieba
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from config import stop_words_path

# �Զ���ͣ���ִ�
CUSTOM_STOP_WORDS = ["����", "Ͷ��", "�ؼ���"]
# �ı���ʼ����λ��
CONTENT_START_INDEX = 1
# �������������
N_CLUSTERS = 6


def read_words(file_path):
    words = set()
    with open(file_path, "r", encoding='gbk') as f:
        for line in f:
            line = line.strip()
            words.add(line)
    words |= set(CUSTOM_STOP_WORDS)
    return words


def trim_stopwords(words, stop_words_set):
    """
    ȥ���д��ı��е�ͣ�ô�
    :param words:
    :param stop_words_set:
    :return:
    """
    new_words = []
    for w in words:
        if w in stop_words_set:
            continue
        new_words.append(w)
    return new_words


def segment(file_path, stopwords, is_cut = False):
    word_set = set()
    docs = []
    with open(file_path, 'r', encoding='gbk')as f:
        for line in f:
            line = line.strip()
            cols = line.split("\t")
            content = " ".join(cols[CONTENT_START_INDEX:])
            content = content.lower().replace("", "").replace("{}", "")
            if is_cut:
                words = jieba.lcut(content)
            else:
                words = content.split(" ")
            doc = trim_stopwords(words, stopwords)
            docs.append(" ".join(doc))
            word_set |= set(doc)
    print('word set size:%s; line size:%s' % (len(word_set), len(docs)))
    return word_set, docs


def feature(feature_file_path):
    if not os.path.exists(feature_file_path):
        stopwords = read_words(stop_words_path)
        word_set, docs = segment(input_file_path, stopwords=stopwords)
        tfidf_vectorizer = TfidfVectorizer(max_df=0.9, min_df=0.1, analyzer='word', ngram_range=(1, 2),
                                           vocabulary=list(word_set))
        feature_matrix = tfidf_vectorizer.fit_transform(docs)  # fit the vectorizer to synopses
        # terms is just a ���� of the features used in the tf-idf matrix. This is a vocabulary
        terms = tfidf_vectorizer.get_feature_names()  # ����258
        print('vocab name size:%s' % len(terms))
        print(terms[:10])

        with open(feature_file_path, 'wb') as f:
            pickle.dump(feature_matrix, f)
    else:
        with open(feature_file_path, "rb") as f:
            feature_matrix = pickle.load(f)

    print(feature_matrix.shape)  # (10, 258)��10ƪ�ĵ���258��feature
    return feature_matrix


def kmeans_train(feature_matrix, output_file):
    kmeans = MiniBatchKMeans(init='k-means++', n_clusters=N_CLUSTERS, batch_size=100,
                             n_init=10, max_no_improvement=10, verbose=0)
    kmeans.fit(feature_matrix)
    print(kmeans.cluster_centers_)
    labels = kmeans.labels_
    print(labels)
    print(Counter(labels))
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in kmeans.labels_:
            f.write("%s\n" % i)
    print("save to:%s" % output_file)
    return labels


def show_plt(feature_matrix, labels):
    from sklearn.decomposition import TruncatedSVD
    import matplotlib.pyplot as plt
    svd = TruncatedSVD()
    plot_columns = svd.fit_transform(feature_matrix)
    plt.scatter(x=plot_columns[:, 0], y=plot_columns[:, 1], c=labels)
    plt.savefig("output/kmeans.png")
    #plt.show()


if __name__ == "__main__":
    #input_file_path = './data/train_seg_sample.txt'
    input_file_path = './data/train_words.txt'
    output_file = 'out.txt'
    feature_file_path = input_file_path + '_feature.pkl'

    feature_matrix = feature(feature_file_path)
    labels = kmeans_train(feature_matrix, output_file)
    show_plt(feature_matrix, labels)
