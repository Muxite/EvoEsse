# this operates the simulation
import os
import pprint
import random
import math

pp = pprint.PrettyPrinter(indent=3)


def update_caret(string):
    index = string.find('|')  # return the location of the caret, -1 if none
    if index == -1:
        new_string = '|' + string  # add a caret at the front
        print(new_string)
        return new_string
    else:
        if index+2 < len(string):  # if have not reached the end of the string
            string = string.replace('|', '')
            new_string = string[:index+1] + '|' + string[index+1:]
            print(new_string)
            return new_string
        else:
            string = string.replace('|', '')  # remove the carat
            new_string = '|' + string  # loop the caret back to the start
            print(new_string)
            return new_string


def check_behind(string, char, start, count):
    for i in range(0, count):  # checking including start
        position = start-i
        if string[wrap(position, len(string))] != char:
            return i
    return count


def check_front(string, char, start):  # check one ahead
    return string[wrap(start+1, len(string))] == char


def copy_behind(string, start, count):
    new_string = ''
    for i in range(count):
        new_string = string[wrap(i, len(string))]
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
    return organism


class Simulation:  # this class is the conversation itself
    def __init__(self):
        #self.name = str(input("NAME OF THE SIMULATION: "))
        #self.seed_location = str(input("SEED FOLDER LOCATION: ")).replace('"', '')
        #self.results_location = str(input("RESULTS FOLDER LOCATION: ")).replace('"', '')
        self.seed_location = 'F:\in'
        self.results_location = 'F:\out'
        self.c = int(input("COEFFICIENT: "))
        self.turns = int(input("MAX TURNS IN SIMULATION: "))
        self.organisms = []  # this is the big file where all the organisms are

    def load(self):  # loads all the organisms from txt
        try:
            txt_files = [f for f in os.listdir(self.seed_location) if f.endswith('.txt')]
            for i in range(len(txt_files)):
                with open(os.path.join(self.seed_location, txt_files[i]), 'r') as f:
                    self.organisms.append(f.read())  # read the contents of the file and append it to the list
            pp.pprint(self.organisms)
        except FileNotFoundError:
            input("ERROR: FOLDER NOT FOUND, CREATE AND POPULATE THE FOLDER, THEN RESTART SIMULATION")

    def update(self):
        for o in range(len(self.organisms)):
            self.organisms[o] = update_caret(self.organisms[o])
        old = self.organisms.copy()  # read from old, write to self.organism
        for o in range(len(old)):  # organism is a string
            index = old[o].find('|')
            old[o] = old[o].replace('|', '')  # remove it to avoid mistakes

            # clone 'c' if it is the last 'c' in the chain
            if old[o][index] == 'c' and check_front(old[o], 'c', index) is False:
                char_count = check_behind(old[o], 'c', 99, index)
                # if there is enough, then copy all
                if char_count*self.c > len(old[o]):
                    print("cloned")
                    self.organisms.append(mutate(old[o]))
                # otherwise copy as much as possible
                else:
                    to_add = copy_behind(old[o], index, char_count*self.c)
                    print("cloned")
                    self.organisms.append(mutate(to_add))

            # kill 'k'
            if old[o][index] == 'k':
                # must target first
                if old[o][wrap(index-1, len(old[o]))] == 't':  # t for target
                    target = random.randint(0, len(old) - 1)
                    try:
                        print("killed " + str(target))
                        self.organisms.remove(self.organisms[target])  # kills one, possibly itself
                    except IndexError:
                        print("failed kill")

            # inject 'i'
            if old[o][index] == 'i':
                if old[o][wrap(index - 1, len(old[o]))] == 't':  # t for target
                    target = random.randint(0, len(old) - 1)
                    # select a portion to inject
                    to_inject = select_random_section(old[o])
                    try:
                        print("injected " + str(to_inject) + " to " + str(target))
                        self.organisms[target] += mutate(to_inject)  # add the injection to end
                    except IndexError:
                        print("failed injection")

            # steal 's'
            if old[o][index] == 's':
                if old[o][wrap(index - 1, len(old[o]))] == 't':  # t for target
                    target = random.randint(0, len(old) - 1)
                    # select a portion to inject
                    to_steal = select_random_section(old[target])
                    try:
                        print("stolen " + str(to_steal) + " from " + str(target))
                        self.organisms[o] += mutate(to_steal)  # add the injection to end of future self
                    except IndexError:
                        print("failed steal")

            # reinforce 'r'
            if old[o][index] == 'r':
                # take from self
                to_reinforce = select_random_section(old[o])
                try:
                    print("reinforced " + str(to_reinforce))
                    self.organisms[o] += mutate(to_reinforce)  # add to future self
                except IndexError:
                    print("failed reinforce")

    def save_txt(self, max_files):
        for i in range(0, len(self.organisms)):
            if i > max_files:
                break
            filename = os.path.join(self.results_location, f'file{i}.txt')
            with open(filename, 'w') as f:
                f.write(self.organisms[i])


def menu():
    s = Simulation()
    s.load()
    for i in range(0, s.turns):
        s.update()

    s.save_txt(2000)


menu()
