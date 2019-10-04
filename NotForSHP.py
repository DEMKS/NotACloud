class DEduapp:
    class DStudent:
        def __init__(self, string):
            string = string.split(' ')
            self.name = string[0]
            self.surname = string[1]
            self.marks = []
            for i in range(2, len(string)):
                self.marks.append(string[i])

    def __init__(self, studentcount):
        self.StudentArr = []
        self.StudentCount = int(studentcount)


if __name__ == '__main__':
    eduapp = DEduapp(5)
    for i in range(eduapp.StudentCount):
        eduapp.StudentArr.append(DEduapp.DStudent(input().replace('\n', '')))
    for i in eduapp.StudentArr:
        print(i.name + i.surname)
        for j in i.marks:
            print(j, end=' ')
        print()
# Made by DEMKA, member of NAD developers group
