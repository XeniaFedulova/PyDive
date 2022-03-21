class Phonebook:
    file_name = None
    phone_book = None
    similar_names = None

    def open_file(self):
        if self.file_name:
            return open(self.file_name)

    def recursive_search(self, key, subtree):

        if len(subtree) == 0:
            return [key]

        answer = []
        for subtree_key, subtree_item in subtree.items():
            subtree_ans = self.recursive_search(subtree_key, subtree_item)
            for item in subtree_ans:
                answer.append(key + item)

        return answer

    def search_by_name_wildcard(self):
        name_wildcard = input()
        lvl = self.tree
        for letter in name_wildcard:
            if letter == "*":
                names = self.recursive_search(name_wildcard[:-1], lvl)
                for name in names:
                    print(self.name_dict[name])
            elif letter in lvl:
                lvl = lvl[letter]
            else:
                print("name not in book")

    def search_by_phone_wildcard(self):
        phone_wildcard = input()
        lvl = self.phone_tree
        for number in phone_wildcard:
            if number == "*":
                phones = self.recursive_search(phone_wildcard[:-1], lvl)
                for phone in phones:
                    print(self.phone_dict[phone])
            elif number in lvl:
                lvl = lvl[number]
            else:
                print("phone not in book")


    def __init__(self, file_name):
        self.file_name = file_name
        self.phone_file = self.open_file()
        self.name_dict = {}
        self.phone_dict = {}

    #делаем префиксные деревья имен и телефонов

        self.tree = {}
        self.phone_tree = {}

        for i in self.phone_file.readlines():
            name, phone = i.strip().split(",")
            lvl_name = self.tree
            lvl_phone = self.phone_tree
            for letter in name:
                if letter not in lvl_name:
                    lvl_name[letter] = {}
                lvl_name = lvl_name[letter]

            for number in phone:
                if number not in lvl_phone:
                    lvl_phone[number] = {}
                lvl_phone = lvl_phone[number]
    # делаем словарь с ключами-именами и словарь с ключами-телефонами

            self.phone_dict[phone] = name

            if name not in self.name_dict:
                self.name_dict[name] = []
            self.name_dict[name].append(phone)

book = Phonebook("1_WildcardSearchData.txt")
book.search_by_phone_wildcard()
book.search_by_name_wildcard()



