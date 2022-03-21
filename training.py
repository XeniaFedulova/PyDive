dic = {}

word_list = ["hello", "hela", "hellk", "how", "are"]
wildcard = "he*"


for word in word_list:
    lvl = dic
    for letter in word:
        if letter not in lvl:
            lvl[letter] = {}
        lvl = lvl[letter]


def recursive_search(key, subtree):

    # print(subtree)
    if len(subtree) == 0:
        print(key)
        print(subtree)
        print([key])
        print('---------------')
        return [key]

    ans = []
    for subtree_key, subrtree_item in subtree.items():
        subtree_ans = recursive_search(subtree_key, subrtree_item)
        for item in subtree_ans:
            print(subtree_ans)
            print("**")
            ans.append(key + item)
    print(key)
    print(ans)
    print(item)
    print('---------------')
    return ans

def search_words(dic, wildcard):
    lvl = dic
    for letter in wildcard:
        if letter == "*":
            return recursive_search(wildcard[:-1], lvl)
        elif letter in lvl:
            lvl = lvl[letter]
        else:
            "word not in list"


print(search_words(dic, wildcard))