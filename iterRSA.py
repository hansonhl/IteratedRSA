# iterRSA
# Convenience tools to calculate probabilities in the RSA model

import numpy as np
from treelib import Node, Tree

def add_tags(u):
    return '<s> ' + u + ' </s>'

class IterRSA(object):
    def __init__(self, semantics, params=None):
        self.us = []
        self.ws = []
        self.semantics = {}
        self.alpha = 1
        self.epsilon = 0.000000001

        if params is not None:
            self.alpha = self.alpha if 'alpha' not in params else params['alpha']
            self.epsilon = self.epsilon if 'epsilon' not in params else params['epsilon']

        for pair in semantics:
            tagged_pair = (add_tags(pair[0]), pair[1])
            if tagged_pair[0] not in self.us:
                self.us.append(tagged_pair[0])
            if tagged_pair[1] not in self.ws:
                self.ws.append(tagged_pair[1])
            self.semantics[tagged_pair] = semantics[pair]

        self.word_to_cost = {}

        for s in self.us:
            words = s.split()
            for wd in words:
                if wd not in self.word_to_cost:
                    self.word_to_cost[wd] = 1
        self.words = self.word_to_cost.keys()

    def valid(self, c):
        for u in self.us:
            if u.startswith(c):
                return True
        return False

    # [c](w)
    # c: incomplete utterance
    # w: world state
    def cont_sem(self, c, w):
        if not c.startswith('<s>'):
            c = '<s> ' + c
        # check if world is valid
        assert (w in self.ws), 'Invalid world state'
        # check if all words in c are valid:
        words = c.split()
        for wd in words:
            assert (wd in self.words), 'Invalid word in continuation'

        true_extensions = 0
        total_extensions = 0
        for u in self.us:
            if u.startswith(c):
                total_extensions += 1
                true_extensions += self.semantics[(u, w)]

        assert (total_extensions != 0), 'Invalid string'

        return true_extensions / total_extensions

    def L0(self, c, wd, query_w=None, verbose=False):
        return self.L(0, c, wd, query_w, verbose)

    # L_n(query_w | c, wd)
    # n: level of recursion (integer)
    # c: incomplete utterance (string)
    # wd: next word to say
    # query_w: (OPTIONAL) a world state, whose probability we want to find
    # if query_w is None, then a dictionary is returned, with each world state
    # as a key and its probability as value
    def L(self, n, c, wd, query_w=None, verbose=False):
        if c == '':
            c = '<s>'

        res_p = []
        res_w = []
        for w in self.ws:
            res_w.append(w)
            if n == 0:
                res_p.append(self.cont_sem(c + ' ' + wd, w))
            else:
                res_p.append(self.S(n, c, w, wd, verbose))

        s = sum(res_p)
        res_p = [p/s for p in res_p] # normalize
        res = {}
        if query_w is None and verbose:
            print('---- L{}(w=* | c={}, wd={}):'.format(n, c, wd))
        for w, p in zip(res_w, res_p):
            res[w] = p
            if query_w is None and verbose:
                print("    {}: {:.4}".format(w, p))

        if query_w is not None:
            if verbose:
                print('L{}(w={} | c={}, wd={}) = {:.4}'.format(n, query_w, c, wd, res[query_w]))
            return res[query_w]
        else:
            return res

    # L_n(query_wd | c, w)
    # if query_w is None, then a dict
    # n: level of recursion (integer)
    # c: incomplete utterance (string)
    # w: world state (string)
    # query_wd: (OPTIONAL) a word, whose probability we want to find
    # if query_w is None, then a dictionary is returned, with each word
    # as key and its probability as value
    def S(self, n, c, w, query_wd=None, verbose=False):
        if c == '':
            c = '<s>'
        res_p = []
        res_wd = []

        for wd in self.words:
            res_wd.append(wd)
            if not self.valid(c + ' ' + wd):
                res_p.append(0)
            else:
                L_prob = self.L(n-1, c, wd, w, verbose)
                if L_prob == 0:
                    L_prob = self.epsilon
                utility = np.log(L_prob) - self.word_to_cost[wd]
                res_p.append(np.exp(self.alpha * utility))

        s = sum(res_p)
        res_p = [p/s for p in res_p] # normalize
        res = {}
        if query_wd is None and verbose:
            print('---- S{}(wd=* | c={}, w={}):'.format(n, c, w))
        for wd, p in zip(res_wd, res_p):
            res[wd] = p
            if query_wd is None and verbose:
                print("    {}: {:.4}".format(wd, p))

        if query_wd is not None:
            if verbose:
                print('L{}(w={} | c={}, wd={}) = {:.4}'.format(n, query_wd, c, wd, res[query_wd]))
            return res[query_wd]
        else:
            return res

    # given a world w, give the most probable utterance and its probabilities
    # n: level of recursion
    # w: world state
    # u: (OPTIONAL) utterance
    # if u is not none, calculate the total probability of the utterance
    def speak(self, n, w, u=None, verbose=False):
        if u is None:
            c = '<s>'
            wd = '<s>'
            prob = 1
            while wd != '</s>':
                s_res = self.S(n, c, w, verbose=verbose)
                wd = max(s_res, key=s_res.get)
                prob *= s_res[wd]
                c = c + ' ' + wd
            return c, prob
        else:
            if not u.startswith('<s>'):
                u = '<s> ' + u
            if not u.endswith('</s>'):
                u = u + ' </s>'
            assert self.valid(u), 'speak() must take a valid complete utterance!'
            u_words = u.split()
            prob = 1
            for i in range(1, len(u_words)):
                c = ' '.join(u_words[:i])
                wd_prob = self.S(n, c, w, query_wd=u_words[i])
                prob *= wd_prob
            return prob

    # Given a complete utterance u, get the most probable world state
    # n: level of recursion
    # see squib for better description
    def listen_max(self, n, u, latex=True, verbose=False):
        if not u.startswith('<s>'):
            u = '<s> ' + u
        if not u.endswith('</s>'):
            u = u + ' </s>'
        u_words = u.split()
        l_probs = []
        l_ws = []
        for i in range(1, len(u_words)):
            c = ' '.join(u_words[:i])
            l_res = self.L(n, c, u_words[i])
            w = max(l_res, key=l_res.get)
            l_ws.append(w)
            l_probs.append(l_res[w])
        if latex:
            print('---- Iterated utterance reasoning for L' + str(n) +' on \"'+u+'\"')
            print('\\begin{tabular}{...}')
            print('Utterance', end='')
            for wd in u_words[1:]:
                print(' & '+wd, end='')
            print('\\\\')
            print('Inferred world', end='')
            for w in l_ws:
                print(' & '+w, end='')
            print('\\\\')
            print('Probability', end='')
            for prob in l_probs:
                print(' & {:.2}'.format(prob), end='')
            print('\\\\')
            print('\\end{tabular}')
        pairs = list(zip(l_ws, l_probs))
        max_pair = max(pairs, key=lambda p: p[1])
        return max_pair

    # Given a complete utterance u, get the most probable world state
    # n: level of recursion
    # see squib for better description
    def listen_utt(self, n, u, latex=True):
        w_probs = []
        ws = []
        for w in self.ws:
            ws.append(w)
            w_probs.append(self.speak(n, w, u))
        s = sum(w_probs)
        w_probs = [p/s for p in w_probs]
        if latex:
            print('---- Whole utterance reasoning for L' + str(n) +' on \"'+u+'\"')
            print('\\begin{tabular}{...}')
            print('World state', end = '')
            for w in ws:
                print(' & '+w, end='')
            print('\\\\')
            print('Probability', end='')
            for p in w_probs:
                print(' & {:.2}'.format(p), end ='')
            print('\\end{tabular}')
        pairs = list(zip(ws, w_probs))
        max_pair = max(pairs, key=lambda p: p[1])
        return max_pair

    # Return a tree structure that represents pragmatic speaker S_n's reasoning
    # on the world state w.
    def speaker_to_tree(self, n, w, verbose=False):
        tree = Tree()
        c = '<s>'
        tree.create_node(w, c, data=RSANode(1))

        def build_tree(t, cont):
            s_res = self.S(n, cont, w, verbose=verbose)
            for wd in s_res:
                if s_res[wd] != 0:
                    new_cont = cont + ' ' + wd
                    t.create_node(wd, new_cont, parent=cont, data=RSANode(round(s_res[wd], 4)))
                    if wd != '</s>':
                        build_tree(t, new_cont)

        build_tree(tree, c)
        return tree

    # Print out a table for values of L_n(w=* | c, wd=*)
    def visualize_L(self, n, c, latex=True):
        if not latex:
            print('==== L{}(w=* | c={}, wd=*) ===='.format(n, c))
        else:
            print('$L_\{'+str(n)+'\}(w=* \\mid c=\\txt\{'+c+'\},\\ wd=*)$')
            print('\\begin{tabular}{...}\n\\hline')
        print(' & ' + ' & '.join(self.ws))
        for wd in self.words:
            if self.valid(c + ' ' + wd):
                res = self.L(n, c, wd)
                print(wd, end='')
                for w in self.ws:
                    print(' & {:.4}'.format(res[w]), end='')
                print('\\\\')
        print('\\end{tabular}')

    # Print out a table containing values of S_n(wd=* | c, w=*)
    def visualize_S(self, n, c, latex=False):
        if not latex:
            print('==== S{}(wd=* | c={}, w=*) ===='.format(n, c))
        else:
            print('$S_\{'+str(n)+'\}(wd=* \\mid c=\\txt{'+c+'},\\ w=*)$')
            print('\\begin{tabular}{...}\n\\hline')
        for w in self.ws:
            res = self.S(n, c, w)
            print(w, end='')
            for wd in self.words:
                print(' & {}: {:.4}'.format(wd, res[wd]), end='')
            print('\\\\')
        print('\\end{tabular}')


class RSANode(Node):
    def __init__(self, prob):
        self.prob = prob
