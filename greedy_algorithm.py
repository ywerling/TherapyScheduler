import random
from datetime import datetime, timedelta
import scheduling_parameters as sp

class Station:
    def __init__(self, name):
        self.name = name
        self.available_time = datetime.strptime("13:00", "%H:%M")

    def is_available(self, start_time, duration):
        return start_time >= self.available_time

    def schedule(self, start_time, duration):
        # Update the station's available time after scheduling
        self.available_time = start_time + duration

class Patient:
    def __init__(self, id):
        self.id = id
        self.schedule = []

    def add_to_schedule(self, station, start_time, duration):
        end_time = start_time + duration
        self.schedule.append((station.name, start_time.strftime("%H:%M"), end_time.strftime("%H:%M")))

def greedy_assignment(patients, stations, visit_duration):
    for patient in patients:
        for station in stations:
            start_time = station.available_time
            if station.is_available(start_time, visit_duration):
                patient.add_to_schedule(station, start_time, visit_duration)
                station.schedule(start_time, visit_duration)
                break

def simulate_day():
    visit_duration = timedelta(minutes=30)
    stations = [Station(name) for name in sp.STATION_NAMES]
    patients = [Patient(i) for i in range(sp.NUM_PATIENTS)]

    greedy_assignment(patients, stations, visit_duration)

    for patient in patients:
        print(f"Patient {patient.id} schedule: {patient.schedule}")

if __name__ == "__main__":
    simulate_day()
