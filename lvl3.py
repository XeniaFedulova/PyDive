import re

class Phonebook:
    file_name = None

    def __init__(self, file_name):
        self.file_name = file_name
        self.phone_file = self.open_file()

    def open_file(self):
        if self.file_name:
            return open(self.file_name)

    def search_all_intersections(self, phone_wildcard, name_wildcard):

        name_pattern = name_wildcard.replace("*", "[A-Z a-z\s]+")
        phone_pattern = phone_wildcard.replace("*", "[^a-zA-Z\n]+")
        print(name_pattern)
        for line in self.phone_file.readlines():
            line_stripped = line.replace(" ", "")
            l = re.findall(name_pattern+","+phone_pattern, line_stripped)
            if l != []:
                print(line, end = "")


book = Phonebook("1_WildcardSearchData.txt")
book.search_all_intersections("0", "Er*")


