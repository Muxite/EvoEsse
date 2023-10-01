# this operates the simulation
import pprint
import random

pp = pprint.PrettyPrinter(indent=3)


def update_caret(string):
    index = string.find('|')  # return the location of the caret, -1 if none
    if index == -1:
        new_string = '|' + string  # add a caret at the front
        return new_string
    else:
        if index+2 < len(string):  # if it has not reached the end of the string
            string = string.replace('|', '')
            new_string = string[:index+1] + '|' + string[index+1:]
            return new_string
        else:
            string = string.replace('|', '')  # remove the carat
            new_string = '|' + string  # loop the caret back to the start
            return new_string


def count_behind(string, char, start, count):
    for i in range(0, count):  # checking including start
        position = start-i
        if string[wrap(position, len(string))] != char:
            return i
    return count-1


def find_behind(string, a, b, start):
    for i in range(0, len(string)):  # checking including start
        position = start-i
        if string[wrap(position, len(string))] == a:
            pass
            # whatever
        elif string[wrap(position, len(string))] == b:
            return i
        else:
            return -1
    return -1


def check_front(string, char, start):  # check one ahead
    if string[wrap(start+1, len(string))] == char:
        return True
    else:
        return False


def copy_behind(string, start, count):
    new_string = ''
    for i in range(count):
        new_string += string[wrap(start-(count-i)+1, len(string))]
    return new_string


def wrap(location, length):  # wrap the string into a loop
    return location % length


def select_random_section(string):
    # the string is treated as a circle
    start = random.randint(-len(string), len(string))
    end = random.randint(start, start+len(string)+1)
    # create the section
    new_string = ''
    for i in range(start, end):
        new_string += string[wrap(i, len(string))]

    return new_string  # return the section


def mutate(organism):
    # do stuff to the organism code
    new_organism = ''
    t = ['c', 'k', 'i', 's', 'r']
    for i in range(len(organism)):
        if random.randint(0, 100) < 4:
            new_organism += t[random.randint(0, 4)]
        else:
            new_organism += organism[i]

    return new_organism


def insert(part, into):
    cut = random.randint(0, len(into))
    result = ''
    for i in range(0, cut):
        result += into[i]
    result += part
    for i in range(cut, len(into)):
        result += into[i]
    return result


class Simulation:  # this class is the conversation itself
    def __init__(self):
        # self.name = str(input("NAME OF THE SIMULATION: "))
        # self.seed_location = str(input("SEED FOLDER LOCATION: ")).replace('"', '')
        # self.results_location = str(input("RESULTS FOLDER LOCATION: ")).replace('"', '')
        self.seed_location = 'Experiments/in.txt'
        self.results_location = 'Experiments/'
        self.c = int(input("COEFFICIENT: "))
        self.turns = int(input("MAX TURNS IN SIMULATION: "))
        self.max_organisms = int(input("MAX ORGANISMS: "))
        self.organisms = []  # this is the big file where all the organisms are

    def load(self):  # loads all the organisms from txt
        try:
            txt_file = open(self.seed_location, 'r')
            temp = txt_file.readlines()
            txt_file.close()
            try:
                self.organisms.remove(" ")
                print("empty removed")
            except ValueError:
                pass
            for i in range(len(temp)):
                temp[i] = temp[i].strip('\n')
            self.organisms = temp
        except FileNotFoundError:
            input("ERROR: FOLDER NOT FOUND, CREATE AND POPULATE THE FOLDER, THEN RESTART SIMULATION")

    def update(self):
        old = []

        for o in range(0, len(self.organisms)):

            self.organisms[o] = update_caret(self.organisms[o])
            old.append(self.organisms[o])

        for o in range(len(old)):  # organism is a string
            index = old[o].index('|')
            old[o] = old[o].replace('|', '')  # remove it to avoid mistakes

            # clone 'c' if it is the last 'c' in the chain
            if old[o][index] == 'c' and check_front(old[o], 'c', index) is False:
                char_count = count_behind(old[o], 'c', index, len(old[o]))
                # if there is enough, then copy all
                if char_count*self.c > len(old[o]):
                    self.organisms.append(mutate(old[o]))
                # otherwise copy as much as possible
                else:
                    to_add = copy_behind(old[o], index, char_count*int(self.c))
                    self.organisms.append(mutate(to_add))

            # kill 'k'
            if old[o][index] == 'k':
                # must target first
                target = random.randint(0, len(old) - 1)
                try:
                    self.organisms.remove(self.organisms[target])  # kills one, possibly itself
                except IndexError:
                    pass

            # inject 'i'
            if old[o][index] == 'i' and check_front(old[o], 'i', index) is False:
                target = random.randint(0, len(old) - 1)
                # select a portion to inject
                char_count = count_behind(old[o], 'i', index, len(old[o]))
                # if there is enough, then inject all
                try:
                    if char_count * self.c > len(old[o]):
                        self.organisms[target] = insert(mutate(old[o]), self.organisms[o])
                    # otherwise inject as much as possible
                    else:
                        to_add = copy_behind(old[o], index, char_count * self.c)
                        self.organisms[target] = insert(mutate(to_add), self.organisms[o])
                except IndexError:
                    pass

            # steal 's'
            if old[o][index] == 's' and check_front(old[o], 's', index) is False:
                target = random.randint(0, len(old) - 1)
                # select a portion to inject
                char_count = count_behind(old[o], 's', index, len(old[o]))
                # if there is enough, then inject all
                try:
                    if char_count * self.c > len(old[o]):

                        self.organisms[target] = insert(mutate(old[o]), self.organisms[o])
                    # otherwise inject as much as possible
                    else:
                        to_add = copy_behind(old[o], index, char_count * self.c)
                        self.organisms[target] = insert(mutate(to_add), self.organisms[o])
                except IndexError:
                    pass

            # reinforce 'r'
            if old[o][index] == 'r' and check_front(old[o], 'r', index) is False:
                char_count = count_behind(old[o], 'r', index, len(old[o]))
                # if there is enough, then reinforce with all
                try:
                    if char_count * self.c > len(old[o]):
                        self.organisms[o] = insert(mutate(old[o]), self.organisms[o])
                    # otherwise reinforce as much as possible
                    else:
                        to_add = copy_behind(old[o], index, char_count * self.c)
                        self.organisms[o] = insert(mutate(to_add), self.organisms[o])
                except IndexError:
                    pass

    def save_txt(self, tag):
        location = self.results_location + str(self.c) + '-' + tag + '.txt'
        f = open(location, 'w')
        for i in range(0, len(self.organisms)):
            if i > self.max_organisms:
                break
            f.write(self.organisms[i] + '\n')
        print("num: " + str(len(self.organisms)))


def menu():
    s = Simulation()
    s.load()
    for i in range(0, s.turns):
        print("turn = " + str(i))
        s.update()
        # save every 1
        if i % 1 == 0:
            s.save_txt(str(i))


menu()
