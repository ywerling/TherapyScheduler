import random

import heapq

# Constants

START_TIME = 13 * 60  # 13h00 in minutes

END_TIME = 19 * 60  # 19h00 in minutes

NUM_PATIENTS = 10

NUM_STATIONS = 5

STATION_NAMES = ["General Practitioner", "Dietitian", "Orthopedist", "Blood Sample", "Electrocardiogram"]

STATION_TIMES = {

    "General Practitioner": 30,  # 30 minutes for GP consultation

    "Dietitian": 30,  # 30 minutes for Dietitian consultation

    "Orthopedist": 30,  # 30 minutes for Orthopedist consultation

    "Blood Sample": 20,  # 20 minutes for Blood Sample collection

    "Electrocardiogram": 20  # 20 minutes for Electrocardiogram

}


class Station:

    def __init__(self, name, process_time):

        self.name = name

        self.process_time = process_time

        self.available_time = START_TIME  # Station becomes available at 13h00

    def can_process(self, arrival_time):

        return arrival_time >= self.available_time

    def process_patient(self, arrival_time):

        if self.can_process(arrival_time):

            start_time = max(arrival_time, self.available_time)

            end_time = start_time + self.process_time

            self.available_time = end_time

            return start_time, end_time

        else:

            return None, None


class Patient:

    def __init__(self, patient_id):
        self.patient_id = patient_id

        self.schedule = []

    def visit_station(self, station, arrival_time):
        start_time, end_time = station.process_patient(arrival_time)

        if start_time and end_time:
            self.schedule.append((station.name, start_time, end_time))

        return start_time, end_time


def simulate_day():
    patients = [Patient(i) for i in range(NUM_PATIENTS)]

    stations = [Station(name, STATION_TIMES[name]) for name in STATION_NAMES]

    event_queue = []

    random.shuffle(patients)

    # Initial patient assignments to stations

    for patient in patients:

        arrival_time = START_TIME

        for station in stations:

            start_time, end_time = patient.visit_station(station, arrival_time)

            if start_time and end_time:
                print(
                    f"Patient {patient.patient_id} visits {station.name} from {start_time // 60}:{start_time % 60:02d} to {end_time // 60}:{end_time % 60:02d}")

                arrival_time = end_time


simulate_day()