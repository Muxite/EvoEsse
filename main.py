# this operates the simulation
import os
import pprint
pp = pprint.PrettyPrinter(indent=3)


def update_carat(string):
    initialized = False   # has a carat been added already?
    new_string = ''
    index = string.find('|')  # return the location of the carat, -1 if none
    if index == -1:
        new_string = '|' + string  # add acarat at the front
        return new_string
    else:
        if index+2 < len(string):  # if have not reached the end of the string
            string = string.replace('|', '')
            new_string = string[:index+1] + '|' + string[index+1:]
            return new_string
        else:
            string = string.replace('|', '')  # remove the carat
            new_string = '|' + string  # loop the carat back to the start
            return new_string


class Simulation:  # this class is the conversation itself
    def __init__(self):
        self.name = str(input("NAME OF THE SIMULATION: "))
        self.seed_location = str(input("SEED FOLDER LOCATION: ")).replace('"', '')
        self.results_location = str(input("RESULTS FOLDER LOCATION (CAN BE CREATED): ")).replace('"', '')
        self.max_turn_time = float(input("MAX TIME PER TURN (s): "))
        self.max_turns = int(input("MAX TURNS IN SIMULATION: "))
        self.organisms = []  # this is the big file where all the organisms are

    def load(self):  # loads all the organisms from txt
        try:
            txt_files = [f for f in os.listdir(self.seed_location) if f.endswith('.txt')]
            for file in txt_files:
                with open(os.path.join(self.seed_location, file), 'r') as f:
                    self.organisms.append(f.read())  # read the contents of the file and append it to the list
            pp.pprint(self.organisms)
        except FileNotFoundError:
            input("ERROR: FOLDER NOT FOUND, CREATE AND POPULATE THE FOLDER, THEN RESTART SIMULATION")


def menu():
    s = Simulation()
    s.load()


menu()