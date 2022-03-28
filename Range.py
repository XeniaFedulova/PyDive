from pydoc import doc
class Range:

    def __init__(self, start, stop, step):
        self.stop = stop
        self.step = step
        self.start = start
        self.current = start

    def __iter__(self):
        return Range(self.start, self.stop, self.step)

    def __next__(self):
        current = self.current

        if self.current == self.stop:
            raise StopIteration
        self.current += self.step

        return current

range = Range(2, 10, 2)
for i in range:
    print(i)



string = "Fallon Capece"

list = [i.isdigit() for i in string]
print(list)
print(any(i.isdigit() for i in string))




