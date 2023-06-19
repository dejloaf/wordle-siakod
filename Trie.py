class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def pick_secret_words(self):
        secret_words = []
        queue = [(self.root, "")]
        while queue:
            node, prefix = queue.pop(0)
            if node.is_word:
                secret_words.append(prefix)

            for char, child in node.children.items():
                queue.append((child, prefix + char))
        return secret_words


trie = Trie()

with open("dictionary.txt", "r", encoding='utf-8') as file:
    for word in file:
        word = word.strip().lower()
        trie.add_word(word)
    print("Добавленные слова:")
    queue = [(trie.root, "")]
    while queue:
        node, prefix = queue.pop(0)
        if node.is_word:
            print(prefix)
        for char, child in node.children.items():
            queue.append((child, prefix + char))
