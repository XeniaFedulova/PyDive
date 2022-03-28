import re

class Phonebook:
    file_name = None
    phone_book = None
    similar_names = None


    def __init__(self, file_name):
            self.file_name = file_name

            self.phone_file = self.open_file()
            self.phone_dict = {}
            self.name_dict = {}

            # делаем префиксные деревья имен и телефонов

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

    def open_file(self):
        if self.file_name:
            return open(self.file_name)

    def search_by_name(self, name):
        return self.name_dict[name]

    def search_by_phone(self, phone):
        return self.phone_dict[phone]

    def search_similar_names(self):
        similar_names = []
        for i in self.name_dict:
            if len(self.name_dict[i]) > 1:
                similar_names.append(i)

        return similar_names

    def recursive_search(self, key, subtree):

        if len(subtree) == 0:
            return [key]

        answer = []
        for subtree_key, subtree_item in subtree.items():
            subtree_ans = self.recursive_search(subtree_key, subtree_item)
            for item in subtree_ans:
                answer.append(key + item)

        return answer

    def search_by_name_wildcard(self, name_wildcard):
        lvl = self.tree
        for letter in name_wildcard:
            if letter == "*":
                names = self.recursive_search(name_wildcard[:-1], lvl)
                for name in names:
                    print(self.name_dict[name])
            elif letter in lvl:
                lvl = lvl[letter]
            else:
                return "name not in book"

    def search_by_phone_wildcard(self, phone_wildcard):
        lvl = self.phone_tree
        for number in phone_wildcard:
            if number == "*":
                phones = self.recursive_search(phone_wildcard[:-1], lvl)
                for phone in phones:
                    print(self.phone_dict[phone])
            elif number in lvl:
                lvl = lvl[number]
            else:
                return "phone not in book"

    def search_all_intersections(self, phone_wildcard, name_wildcard):

        self.phone_file = self.open_file()
        name_pattern = name_wildcard.replace("*", "[A-Z a-z\s]+")
        phone_pattern = phone_wildcard.replace("*", "[^a-zA-Z\n]+")

        for line in self.phone_file.readlines():
            line_stripped = line.replace(" ", "")
            l = re.findall(name_pattern+","+phone_pattern, line_stripped)
            if l != []:
                print(line, end = "")


book = Phonebook("1_WildcardSearchData.txt")
data = input()
if "*" not in data:
    if data[0].isdigit():
        print(book.search_by_phone(data))
    else:
        print(book.search_by_name(data))
else:
    flag = [0, 0]
    for i in data:
        if i.isdigit():
            flag[0] = "phone"
        elif i.isalpha():
            flag[1] = "name"
        else:
            continue
    if flag == ["phone", 0]:
        book.search_by_phone_wildcard(data)
    elif flag == [0, "name"]:
        book.search_by_name_wildcard(data)
    elif flag == ["phone", "name"]:
        for symbol_id in range(len(data)):
            if data[symbol_id].isalpha():
                phone_wildcard = data[0:(symbol_id - 1)].strip(" ")
                name_wildcard = data[symbol_id:len(data)]
                print(phone_wildcard)
                print(name_wildcard)
                book.search_all_intersections(phone_wildcard, name_wildcard)
                break

