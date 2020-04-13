# -*- coding: gbk -*-
# Author: XuMing <xuming624@qq.com>
# Brief:
import collections
import re

import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from scipy import sparse
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2

from utils.data_utils import dump_pkl, load_pkl, get_word_segment_data, get_char_segment_data, load_list
from utils.io_utils import get_logger

logger = get_logger(__name__)


class Feature(object):
    """
    get feature from raw text
    """

    def __init__(self, data=None,
                 feature_type='tfidf_char',
                 feature_vec_path=None,
                 is_infer=False,
                 min_count=1,
                 word_vocab=None,
                 max_len=400):
        self.data_set = data
        self.feature_type = feature_type
        self.feature_vec_path = feature_vec_path
        self.sentence_symbol = load_list(path='data/sentence_symbol.txt')
        self.stop_words = load_list(path='data/stop_words.txt')
        self.is_infer = is_infer
        self.min_count = min_count
        self.word_vocab = word_vocab
        self.max_len = max_len

    def get_feature(self):
        if self.feature_type == 'tfidf_word':
            data_feature = self.tfidf_word_feature(self.data_set)
        elif self.feature_type == 'tf_word':
            data_feature = self.tf_word_feature(self.data_set)
        elif self.feature_type == 'language':
            data_feature = self.language_feature(self.data_set)
        elif self.feature_type == 'tfidf_char_language':
            data_feature = self.tfidf_char_language(self.data_set)
        elif self.feature_type == 'vectorize':
            data_feature = self.vectorize(self.data_set)
        elif self.feature_type == 'doc_vectorize':
            data_feature = self.doc_vectorize(self.data_set)
        else:
            # tfidf_char
            data_feature = self.tfidf_char_feature(self.data_set)
        return data_feature

    def vectorize(self, data_set):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(data_set)
        sequences = tokenizer.texts_to_sequences(data_set)

        word_index = tokenizer.word_index
        logger.info('Number of Unique Tokens: %d' % len(word_index))
        data_feature = pad_sequences(sequences, maxlen=self.max_len)
        logger.info('Shape of Data Tensor:%s' % ",".join(list(map(str,data_feature.shape))))
        return data_feature

    def doc_vectorize(self, data_set, max_sentences=16):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(data_set)
        data_feature = np.zeros((len(data_set), max_sentences, self.max_len), dtype='int32')
        for i, sentence in enumerate(data_set):
            sentence_symbols = "".join(self.sentence_symbol)
            split = "[" + sentence_symbols + "]"
            short_sents = re.split(split, sentence)
            for j, sent in enumerate(short_sents):
                if j < max_sentences and sent.strip():
                    words = text_to_word_sequence(sent)
                    k = 0
                    for w in words:
                        if k < self.max_len:
                            if w in tokenizer.word_index:
                                data_feature[i, j, k] = tokenizer.word_index[w]
                            k += 1
        word_index = tokenizer.word_index
        logger.info('Number of Unique Tokens: %d' % len(word_index))
        logger.info('Shape of Data Tensor:%s' % data_feature.shape)
        return data_feature

    def tfidf_char_feature(self, data_set):
        """
        Get TFIDF feature by char
        :param data_set:
        :return:
        """
        data_set = get_char_segment_data(data_set)
        if self.is_infer:
            self.vectorizer = load_pkl(self.feature_vec_path)
            data_feature = self.vectorizer.transform(data_set)
        else:
            self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 2), sublinear_tf=True)
            data_feature = self.vectorizer.fit_transform(data_set)
        vocab = self.vectorizer.vocabulary_
        logger.info('Vocab size:%d' % len(vocab))
        logger.debug('Vocab list:')
        count = 0
        for k, v in self.vectorizer.vocabulary_.items():
            if count < 10:
                logger.debug("%s	%s" % (k, v))
                count += 1

        logger.info(data_feature.shape)
        if not self.is_infer:
            dump_pkl(self.vectorizer, self.feature_vec_path, overwrite=True)
        return data_feature

    def tfidf_word_feature(self, data_set):
        """
        Get TFIDF ngram feature by word
        :param data_set:
        :return:
        """
        data_set = get_word_segment_data(data_set)
        if self.is_infer:
            self.vectorizer = load_pkl(self.feature_vec_path)
            data_feature = self.vectorizer.transform(data_set)
        else:
            self.vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2),
                                              vocabulary=self.word_vocab, sublinear_tf=True)
            data_feature = self.vectorizer.fit_transform(data_set)
        vocab = self.vectorizer.vocabulary_
        logger.info('Vocab size:%d' % len(vocab))
        logger.debug('Vocab list:')
        count = 0
        for k, v in self.vectorizer.vocabulary_.items():
            if count < 10:
                logger.debug("%s	%s" % (k, v))
                count += 1

        logger.info(data_feature.shape)
        # if not self.is_infer:
        dump_pkl(self.vectorizer, self.feature_vec_path, overwrite=True)
        return data_feature

    def tf_word_feature(self, data_set):
        """
        Get TF feature by word
        :param data_set:
        :return:
        """
        data_set = get_word_segment_data(data_set)
        if self.is_infer:
            self.vectorizer = load_pkl(self.feature_vec_path)
            data_feature = self.vectorizer.transform(data_set)
        else:
            self.vectorizer = CountVectorizer(analyzer='word',
                                              encoding='utf-8',
                                              lowercase=True,
                                              vocabulary=self.word_vocab)
            data_feature = self.vectorizer.fit_transform(data_set)
        vocab = self.vectorizer.vocabulary_
        logger.info('Vocab size:%d' % len(vocab))
        logger.debug('Vocab list:')
        count = 0
        for k, v in self.vectorizer.vocabulary_.items():
            if count < 10:
                logger.debug("%s	%s" % (k, v))
                count += 1
        feature_names = self.vectorizer.get_feature_names()
        logger.info('feature_names:%s' % feature_names[:20])

        logger.info(data_feature.shape)
        if not self.is_infer:
            dump_pkl(self.vectorizer, self.feature_vec_path, overwrite=True)
        return data_feature

    def language_feature(self, data_set, word_sep=' ', pos_sep='/'):
        """
        Get Linguistics feature
        ���Ա�
        n ����
        v ����
        a ���ݴ�
        m ����
        r ����
        q ����
        d ����
        p ���
        c ����
        x ���
        :param data_set:
        :param word_sep:
        :return:
        """
        features = []
        self.word_counts_top_n = self.get_word_counts_top_n(self.data_set, n=30)
        for line in data_set:
            if pos_sep not in line:
                continue
            word_pos_list = line.split(word_sep)
            feature = self._get_text_feature(word_pos_list, pos_sep)
            for pos in ['n', 'v', 'a', 'm', 'r', 'q', 'd', 'p', 'c', 'x']:
                pos_feature, pos_top = self._get_word_feature_by_pos(word_pos_list,
                                                                     pos=pos, most_common_num=10)
                feature.extend(pos_feature)
                # logger.info(pos_top)
            for i in range(len(feature)):
                if feature[i] == 0:
                    feature[i] = 1e-5
            feature = [float(i) for i in feature]
            features.append(feature)
            if len(feature) < 97:
                logger.error('error:%d, %s' % (len(feature), line))
        features_np = np.array(features, dtype=float)
        X = sparse.csr_matrix(features_np)
        return X

    def add_feature(self, X, feature_to_add):
        '''
        Returns sparse feature matrix with added feature.
        feature_to_add can also be a list of features.
        '''
        from scipy.sparse import csr_matrix, hstack
        return hstack([X, csr_matrix(feature_to_add)], 'csr')

    def tfidf_char_language(self, data_set):
        """
        Get TFIDF feature base on char segment
        :param data_set:
        :return:
        """
        tfidf_feature = self.tfidf_char_feature(data_set)
        linguistics_feature = self.language_feature(data_set)
        linguistics_feature_np = linguistics_feature.toarray()
        data_feature = self.add_feature(tfidf_feature, linguistics_feature_np)
        logger.info('data_feature shape: %s' % data_feature.shape)
        return data_feature

    def _get_word_feature_by_pos(self, word_pos_list, pos='n', most_common_num=10):
        n_set = sorted([w for w in word_pos_list if w.endswith(pos)])
        n_len = len(n_set)
        n_ratio = float(len(n_set) / len(word_pos_list))
        n_top = collections.Counter(n_set).most_common(most_common_num)
        return [n_len, n_ratio], n_top

    def _get_text_feature(self, word_pos_list, pos_sep='/'):
        features = []
        # 1.������
        num_word = len(word_pos_list)
        assert num_word > 0
        features.append(num_word)

        # 2.������
        num_char = sum(len(w.split(pos_sep)[0]) for w in word_pos_list)
        features.append(num_char)
        average_word_len = float(num_char / num_word)
        # 3.����ƽ������
        features.append(average_word_len)

        word_list = [w.split(pos_sep)[0] for w in word_pos_list]
        sentence_list_long = [w for w in word_list if w in self.sentence_symbol[:6]]  # ����
        sentence_list_short = [w for w in word_list if w in self.sentence_symbol]  # �̾�
        num_sentence_long = len(sentence_list_long)
        num_sentence_short = len(sentence_list_short)
        # 4.������(�̾�)
        features.append(num_sentence_short)
        # 5.����ƽ���������̾䣩
        features.append(float(num_char / num_sentence_short) if num_sentence_short > 0 else 0.0)
        # 6.�����������䣩
        features.append(num_sentence_long)
        # 7.����ƽ�����������䣩
        features.append(float(num_char / num_sentence_long) if num_sentence_long > 0 else 0.0)

        word_counts = collections.Counter(word_list)
        # 8.ǰ30����ִʸ��������ڱ��ĵ���ռ��
        for i in self.word_counts_top_n:
            num_word_counts = word_counts.get(i) if word_counts.get(i) else 0
            features.append(num_word_counts)
            features.append(float(num_word_counts / num_word))

        word_no_pos_len_list = [len(w.split(pos_sep)[0]) for w in word_pos_list]
        # ����collections���е�Counterģ�飬���Ժ����ɵصõ�һ���ɵ��ʺʹ�Ƶ��ɵ��ֵ䡣
        len_counts = collections.Counter(word_no_pos_len_list)
        # 9.һ�����ִʸ�������ռ��
        for i in range(1, 5):
            num_word_len = len_counts.get(i) if len_counts.get(i) else 0
            features.append(num_word_len)
            features.append(float(num_word_len / num_word))

        # 10.ͣ�ôʵĸ�������ռ��
        stop_words = [w for w in word_list if w in self.stop_words]
        features.append(len(stop_words))
        features.append(float(len(stop_words) / num_word))

        return features

    def get_word_counts_top_n(self, data_set, n=30, word_sep=' '):
        data_set = get_word_segment_data(data_set)
        words = []
        for content in data_set:
            content_list = [w for w in content.strip().split(word_sep) if w not in self.stop_words]
            words.extend(content_list)
        word_counts = collections.Counter(words)
        return word_counts.most_common(n)

    def label_encoder(self, labels):
        encoder = preprocessing.LabelEncoder()
        corpus_encode_label = encoder.fit_transform(labels)
        logger.info('corpus_encode_label shape:%s' % corpus_encode_label.shape)
        return corpus_encode_label

    def select_best_feature(self, data_set, data_lbl):
        ch2 = SelectKBest(chi2, k=10000)
        return ch2.fit_transform(data_set, data_lbl), ch2
