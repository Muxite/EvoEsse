# this operates the simulation
import os
import pprint
pp = pprint.PrettyPrinter(indent=3)


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
