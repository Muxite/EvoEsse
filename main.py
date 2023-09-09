# this operates the simulation
import os
import pprint
import random

pp = pprint.PrettyPrinter(indent=3)


def update_caret(string):
    index = string.find('|')  # return the location of the caret, -1 if none
    if index == -1:
        new_string = '|' + string  # add a caret at the front
        return new_string
    else:
        if index+2 < len(string):  # if have not reached the end of the string
            string = string.replace('|', '')
            new_string = string[:index+1] + '|' + string[index+1:]
            return new_string
        else:
            string = string.replace('|', '')  # remove the carat
            new_string = '|' + string  # loop the caret back to the start
            return new_string


def select_random_section(string):
    # the string is treated as a circle
    start = random.randint(-len(string), len(string))
    end = random.randint(start, start+len(string))

    def wrap(location, length):  # wrap the string into a loop
        return location % length

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
        self.name = str(input("NAME OF THE SIMULATION: "))
        self.seed_location = str(input("SEED FOLDER LOCATION: ")).replace('"', '')
        self.results_location = str(input("RESULTS FOLDER LOCATION (CAN BE CREATED): ")).replace('"', '')
        self.max_turn_time = float(input("MAX TIME PER TURN (s): "))
        self.max_turns = int(input("MAX TURNS IN SIMULATION: "))
        self.organisms = []  # this is the big file where all the organisms are
        self.difficulty = 1

    def load(self):  # loads all the organisms from txt
        try:
            txt_files = [f for f in os.listdir(self.seed_location) if f.endswith('.txt')]
            for file in txt_files:
                with open(os.path.join(self.seed_location, file), 'r') as f:
                    self.organisms.append(f.read())  # read the contents of the file and append it to the list
            pp.pprint(self.organisms)
        except FileNotFoundError:
            input("ERROR: FOLDER NOT FOUND, CREATE AND POPULATE THE FOLDER, THEN RESTART SIMULATION")

    def update(self):
        old = self.organisms.copy()  # read from old, write to self.organism
        for o in range(old):  # organism is a string
            update_caret(old[o])  # if there is no caret, then there should be one now
            index = old[o].find('|')+1  # the character after the caret

            # clone 'c'
            if old[o][index] == 'c':
                # clone is viable early, but loses viability long term as the cost increases
                if self.difficulty > 1:  # will require more than 1 c to clone
                    for i in range(index-int(self.difficulty)+1, index):  # check backwards
                        if old[o][i] != 'c':
                            break  # failed cloning
                    # if that all worked, then clone one
                    self.organisms.append(mutate(old[o]))
                else:
                    self.organisms.append(mutate(old[o]))

            # kill 'k'
            if old[o][index] == 'k':
                # select a random to kill
                target = random.randint(0, len(old))
                self.organisms.remove(target)  # kills one, possibly itself

            # inject 'i'
            if old[o][index] == 'i':
                # select a random to inject to
                target = random.randint(0, len(old))
                # select a portion to inject
                to_inject = select_random_section(old[o])
                self.organisms[target] += mutate(to_inject)  # add the injection to end

            # steal 's'
            if old[o][index] == 's':
                # select a random to steal from
                target = random.randint(0, len(old))
                # select a portion to inject
                to_steal = select_random_section(old[target])
                self.organisms[o] += mutate(to_steal)  # add the injection to end of future self

            # reinforce 'r'


def menu():
    s = Simulation()
    s.load()


menu()
