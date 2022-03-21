class Phonebook:
    file_name = None
    phone_book = None
    similar_names = None

    def open_file(self):
        if self.file_name:
            return open(self.file_name)

    def search_by_name(self):
        name = input()
        return self.name_dict[name]

    def search_by_phone(self):
        phone = input()
        return self.phone_dict[phone]

    def search_similar_names(self):
        similar_names = []
        for i in self.name_dict:
            if len(self.name_dict[i]) > 1:
                similar_names.append(i)

        return similar_names

    def __init__(self, file_name):
        self.file_name = file_name

        self.phone_file = self.open_file()
        self.phone_dict = {}
        self.name_dict = {}

        # создаем словарь с ключами-телефонами и словарь с ключами-именами

        for i in self.phone_file.readlines():
            name, phone = i.strip().split(",")

            self.phone_dict[phone] = name

            if name not in self.name_dict:
                self.name_dict[name] = []
            self.name_dict[name].append(phone)

        # print(self.phone_dict)
        # print(self.name_dict)


book = Phonebook("1_WildcardSearchData.txt")
print(book.search_by_phone())
print(book.search_by_name())
print(book.search_similar_names())
