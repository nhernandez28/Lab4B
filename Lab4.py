from AVL_Tree import AVLTree
from Red_Black_Tree import RedBlackTree

class BTreeNode:
    # Constructor
    def __init__(self, keys=[], children=[], is_leaf=True, max_num_keys=5):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf
        if max_num_keys < 3:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys = 3
        if max_num_keys % 2 == 0:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys += 1
        self.max_num_keys = max_num_keys

    def is_full(self):
        return len(self.keys) >= self.max_num_keys


class BTree:
    # Constructor
    def __init__(self, max_num_keys=5):
        self.max_num_keys = max_num_keys
        self.root = BTreeNode(max_num_keys=max_num_keys)

    def find_child(self, k, node=None):
        # Determines value of c, such that k must be in subtree node.children[c], if k is in the BTree
        if node is None:
            node = self.root

        for i in range(len(node.keys)):
            if k < node.keys[i]:
                return i
        return len(node.keys)

    def insert_internal(self, i, node=None):

        if node is None:
            node = self.root

        # node cannot be Full
        if node.is_leaf:
            self.insert_leaf(i, node)
        else:
            k = self.find_child(i, node)
            if node.children[k].is_full():
                m, l, r = self.split(node.children[k])
                node.keys.insert(k, m)
                node.children[k] = l
                node.children.insert(k + 1, r)
                k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def split(self, node=None):
        if node is None:
            node = self.root
        # print('Splitting')
        # PrintNode(T)
        mid = node.max_num_keys // 2
        if node.is_leaf:
            left_child = BTreeNode(node.keys[:mid], max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], max_num_keys=node.max_num_keys)
        else:
            left_child = BTreeNode(node.keys[:mid], node.children[:mid + 1], node.is_leaf,
                                   max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], node.children[mid + 1:], node.is_leaf,
                                    max_num_keys=node.max_num_keys)
        return node.keys[mid], left_child, right_child

    def insert_leaf(self, i, node=None):
        if node is None:
            node = self.root

        node.keys.append(i)
        node.keys.sort()

    def leaves(self, node=None):
        if node is None:
            node = self.root
        # Returns the leaves in a b-tree
        if node.is_leaf:
            return [node.keys]
        s = []
        for c in node.children:
            s = s + self.leaves(c)
        return s

    def insert(self, i, node=None):
        if node is None:
            node = self.root
        if not node.is_full():
            self.insert_internal(i, node)
        else:
            m, l, r = self.split(node)
            node.keys = [m]
            node.children = [l, r]
            node.is_leaf = False
            k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def height(self, node=None):
        if node is None:
            node = self.root
        if node.is_leaf:
            return 0
        return 1 + self.height(node.children[0])

    def print(self, node=None):
        # Prints keys in tree in ascending order
        if node is None:
            node = self.root

        if node.is_leaf:
            for t in node.keys:
                print(t, end=' ')
                print('\n')
        else:
            for i in range(len(node.keys)):
                self.print(node.children[i])
                print(node.keys[i], end=' ')
                print('\n')
            self.print(node.children[len(node.keys)])

    def search(self, k, node=None):
        if node is None:
            node = self.root
        # Returns node where k is, or None if k is not in the tree
        if k in node.keys:
            return node
        if node.is_leaf:
            return None
        return self.search(k, node.children[self.find_child(k, node)])


def print_anagrams(word, english_words, prefix=""):
    anagram_list = []
    if len(word) <= 1:
        str = prefix + word
        if english_words.search(str, english_words.root):
            anagram_list.append(str)
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]
            after = word[i + 1:]
            if cur not in before:
                print_anagrams(before + after, english_words, prefix + cur)


def count_anagrams(word, english_words, prefix=""):
    count = 0
    if len(word) <= 1:
        str = prefix + word

        if english_words.search(str, english_words.root):
            count += 1
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]
            after = word[i + 1:]

            if cur not in before:
                count += count_anagrams(before + after, english_words, prefix + cur)
    return count


def biggest_anagram(english_words):
    file = open("english_words_two.txt", "r")
    biggest = 0
    word = ""
    for singleLine in file:
        a = str(singleLine.replace("\n", ""))
        q = count_anagrams(a, english_words)
        if q > biggest:
            word = a
            biggest = q
    print(word, biggest)

def read_file():
    word_file = open("english_words_two.txt", "r")
    line = word_file.readline()
    btree = BTree(max_num_keys=5)

    for line in word_file:
        word = line.replace("\n", "")
        btree.insert(word)
    return btree

def main():
    user_word = input("Pick a word ")
    english_words = read_file()
    print()
    print("BTree:")
    english_words.print(english_words.root)
    print("")

    print(user_word, "number of anagrams:")
    count_anagrams(user_word, english_words)
    print("")

    print("Anagrams are:")
    print(print_anagrams(user_word, english_words))
    print("")

    print("Has biggest number of anagrams:")
    biggest_anagram(english_words)

main()
