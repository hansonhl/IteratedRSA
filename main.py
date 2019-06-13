# main.py

from iterRSA import IterRSA
from treelib import Node, Tree

def main():
    # simple scalar implicature
    simple_semantics = {
        ('some', 'ENA'): 1,
        ('some', 'A'): 1,
        ('all', 'ENA'): 0,
        ('all', 'A'): 1
    }
    simple_model = IterRSA(simple_semantics)
    # tree = simple_model.speaker_to_tree(1, 'ENA', verbose=False)
    # tree.show()
    # tree.show(data_property='prob')
    # simple_model.visualize_S(1, '<s>', latex=True)
    # simple_model.listen_max(1, 'some')
    # simple_model.listen_utt(1, 'some')

    # Simple scalar implicature with "some but not all"
    symmetry_semantics = {
        ('some', 'ENA'): 1,
        ('some', 'A'): 1,
        ('all', 'ENA'): 0,
        ('all', 'A'): 1,
        ('some but not all', 'ENA'): 1,
        ('some but not all', 'A'): 0
    }

    print('Loading semantics for simple scalar implicature')
    model1 = IterRSA(symmetry_semantics)
    tree = model1.speaker_to_tree(5, 'ENA')
    # tree.show()
    # tree.show(data_property='prob')

    dress_semantics = {
        ('dress', 'R1'): 1,
        ('dress', 'R2'): 1,
        ('dress', 'R3'): 0,
        ('red dress', 'R1'): 1,
        ('red dress', 'R2'): 0,
        ('red dress', 'R3'): 0,
        ('red object', 'R1'): 1,
        ('red object', 'R2'): 0,
        ('red object', 'R3'): 1,
    }

    dress_model = IterRSA(dress_semantics)
    tree = dress_model.speaker_to_tree(1, 'R1')
    # tree.show()
    # tree.show(data_property='prob')

    emb_semantics = {
        ('not sue or mary', '0'): 1,
        ('not sue or mary', 'M'): 0,
        ('not sue or mary', 'S'): 0,
        ('not sue or mary', 'MS'): 0,
        ('not mary or sue', '0'): 1,
        ('not mary or sue', 'M'): 0,
        ('not mary or sue', 'S'): 0,
        ('not mary or sue', 'MS'): 0,
        ('not sue and mary', '0'): 1,
        ('not sue and mary', 'M'): 1,
        ('not sue and mary', 'S'): 1,
        ('not sue and mary', 'MS'): 0,
        ('not mary and sue', '0'): 1,
        ('not mary and sue', 'M'): 1,
        ('not mary and sue', 'S'): 1,
        ('not mary and sue', 'MS'): 0,
        ('sue or mary', '0'): 0,
        ('sue or mary', 'M'): 1,
        ('sue or mary', 'S'): 1,
        ('sue or mary', 'MS'): 1,
        ('mary or sue', '0'): 0,
        ('mary or sue', 'M'): 1,
        ('mary or sue', 'S'): 1,
        ('mary or sue', 'MS'): 1,
        ('sue and mary', '0'): 0,
        ('sue and mary', 'M'): 0,
        ('sue and mary', 'S'): 0,
        ('sue and mary', 'MS'): 1,
        ('mary and sue', '0'): 0,
        ('mary and sue', 'M'): 0,
        ('mary and sue', 'S'): 0,
        ('mary and sue', 'MS'): 1,
        ('not sue', '0'): 1,
        ('not sue', 'M'): 1,
        ('not sue', 'S'): 0,
        ('not sue', 'MS'): 0,
        ('not mary', '0'): 1,
        ('not mary', 'M'): 0,
        ('not mary', 'S'): 1,
        ('not mary', 'MS'): 0,
        ('sue', '0'): 0,
        ('sue', 'M'): 0,
        ('sue', 'S'): 1,
        ('sue', 'MS'): 1,
        ('mary', '0'): 0,
        ('mary', 'M'): 1,
        ('mary', 'S'): 0,
        ('mary', 'MS'): 1
    }

    emb_model = IterRSA(emb_semantics)
    tree = emb_model.speaker_to_tree(2, '0')
    emb_model.listen_max(1, 'not mary or sue')
    emb_model.listen_utt(1, 'not mary or sue')
    # tree.show()
    # tree.show(data_property='prob')
    # emb_model.listen_all(2)
    # emb_model.visualize_L(0, '<s> not mary')
    # emb_model.visualize_S(1, '<s> not mary')
    # emb_model.visualize_L(1, '<s> not mary')



if __name__ == '__main__':
    main()
