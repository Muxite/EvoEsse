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
        self.name = str(input("NAME OF THE SIMULATION: "))
        self.seed_location = str(input("SEED FOLDER LOCATION: ")).replace('"', '')
        self.results_location = str(input("RESULTS FOLDER LOCATION (CAN BE CREATED): ")).replace('"', '')
        self.turns = int(input("MAX TURNS IN SIMULATION: "))
        self.organisms = []  # this is the big file where all the organisms are
        self.difficulty = 1

    def load(self):  # loads all the organisms from txt
        try:
            txt_files = [f for f in os.listdir(self.seed_location) if f.endswith('.txt')]
            for i in range(len(txt_files)):
                with open(os.path.join(self.seed_location, txt_files[i]), 'r') as f:
                    self.organisms.append(f.read())  # read the contents of the file and append it to the list
                    self.organisms[i] = update_caret(self.organisms[i])  # add carets
            pp.pprint(self.organisms)
        except FileNotFoundError:
            input("ERROR: FOLDER NOT FOUND, CREATE AND POPULATE THE FOLDER, THEN RESTART SIMULATION")

    def update(self):
        old = self.organisms.copy()  # read from old, write to self.organism
        for o in range(len(old)):  # organism is a string
            update_caret(self.organisms[o])
            index = old[o].find('|')+1  # the character after the caret
            old[o] = old[o].replace('|', '')  # remove it to avoid mistakes
            # clone 'c'
            if old[o][index] == 'c':
                # clone is viable early, but loses viability long term as the cost increases
                if self.difficulty > 1:  # will require more than 1 c to clone
                    # check backwards
                    do_clone = True
                    for i in range(wrap(index-self.difficulty+1, len(old[o])), index):
                        if old[o][wrap(i, len(old[o]))] != 'c':
                            do_clone = False
                            break  # failed cloning
                    if do_clone:
                        # if that all worked, then clone one
                        print("cloned with " + str(self.difficulty))
                        self.organisms.append(mutate(old[o]))
                else:
                    print("cloned")
                    self.organisms.append(mutate(old[o]))

            # kill 'k'
            if old[o][index] == 'k':
                # select a random to kill
                target = random.randint(0, len(old))
                print("killed " + str(target))
                self.organisms.remove(target)  # kills one, possibly itself

            # inject 'i'
            if old[o][index] == 'i':
                # select a random to inject to
                target = random.randint(0, len(old))
                # select a portion to inject
                to_inject = select_random_section(old[o])
                print("injected " + str(to_inject) + " to " + str(target))
                self.organisms[target] += mutate(to_inject)  # add the injection to end

            # steal 's'
            if old[o][index] == 's':
                # select a random to steal from
                target = random.randint(0, len(old))
                # select a portion to inject
                to_steal = select_random_section(old[target])
                print("stolen " + str(to_steal) + " from " + str(target))
                self.organisms[o] += mutate(to_steal)  # add the injection to end of future self

            # reinforce 'r'
            if old[o][index] == 'r':
                # take from self
                to_reinforce = select_random_section(old[o])
                print("reinforced " + str(to_reinforce))
                self.organisms[o] += mutate(to_reinforce)  # add to future self

    def update_difficulty(self):
        if len(self.organisms) < 100:
            self.difficulty = 1
        else:
            self.difficulty = int(1 + 0.0001*pow(len(self.organisms), 1.8))
            print("difficulty =" + str(1 + 0.0001*pow(len(self.organisms), 1.8)))

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
        s.update_difficulty()
    s.save_txt(2000)


menu()
