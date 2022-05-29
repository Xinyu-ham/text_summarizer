import enum
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
import numpy as np


class Summarizer:
    def __init__(self, strength=0.3, model_path='sentence-transformers_all-mpnet-base-v2'):
        self.strength = strength
        self.model = SentenceTransformer(model_path)
        self.txt = ''
        self.sentences = []

    def fit(self, txt):
        self.txt = txt
        self.sentences = np.array(sent_tokenize(txt))

    def set_strength(self, strength):
        self.strength = strength

    def _embed_sentences(self):
        return np.array([self.model.encode(sent) for sent in self.sentences])

    def _pagerank_iter(self, page_rank, similarity, damp):
        n = len(page_rank)
        walk = damp / n
        
        for i, child_row in enumerate(similarity):
            v = 0
            for j, parent_row in enumerate(similarity):
                if i != j:
                    v += page_rank[j] * child_row[j] / sum(parent_row)
            page_rank[i] = walk + (1 - damp) * v


    def _get_ranked_index(self, arr, k):
        """ Return array size of arr with top k index = True else False """
        ranked = np.argsort(arr)
        return list(sorted([ranked[-i-1] for i in range(k)]))

    def summarize(self, iter=200, damp=0.10):
        k_output = max(int(self.strength * len(self.sentences)), 1)
        embeded = self._embed_sentences()
        similarity_matrix = cosine_similarity(embeded)
        n = len(similarity_matrix)
        page_rank = [1 for _ in similarity_matrix]

        for _ in range(iter):
            self._pagerank_iter(page_rank, similarity_matrix, damp)
        
        top_n = self._get_ranked_index(page_rank, k_output)
        return ' '.join(self.sentences[top_n])


if __name__ == '__main__':
    MODEL_PATH = '../sentence-transformers_all-mpnet-base-v2'
    summarizer = Summarizer(strength=0.5, model_path=MODEL_PATH)
    
    with open('../../test.txt', 'r') as f:
        test = f.read()

    summarizer.fit(test)
    print(summarizer.summarize())