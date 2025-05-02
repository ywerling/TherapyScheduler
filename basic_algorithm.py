import random
import scheduling_parameters as sp

# # Constants
#
# START_TIME = 13 * 60  # 13h00 in minutes
#
# END_TIME = 19 * 60  # 19h00 in minutes
#
# NUM_PATIENTS = 10
#
# NUM_STATIONS = 5
#
# STATION_NAMES = ["General Practitioner", "Dietitian", "Orthopedist", "Blood Sample", "Electrocardiogram"]
#
# STATION_TIMES = {
#
#     "General Practitioner": 30,  # 30 minutes for GP consultation
#
#     "Dietitian": 30,  # 30 minutes for Dietitian consultation
#
#     "Orthopedist": 30,  # 30 minutes for Orthopedist consultation
#
#     "Blood Sample": 20,  # 20 minutes for Blood Sample collection
#
#     "Electrocardiogram": 20  # 20 minutes for Electrocardiogram
#
# }

class Station:
    def __init__(self, name, process_time):
        self.name = name
        self.process_time = process_time
        self.available_time = sp.START_TIME

    def process_patient(self, arrival_time):
        # Patient may have to wait until the station is available
        start_time = max(arrival_time, self.available_time)
        end_time = start_time + self.process_time
        self.available_time = end_time
        return start_time, end_time

class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.schedule = []
        self.waiting_time = 0

    def visit_station(self, station, arrival_time):
        start_time, end_time = station.process_patient(arrival_time)
        wait = start_time - arrival_time
        self.waiting_time += wait
        self.schedule.append((station.name, start_time, end_time))
        return end_time  # for next arrival_time

def simulate_day():
    patients = [Patient(i) for i in range(sp.NUM_PATIENTS)]
    stations = [Station(name, sp.STATION_TIMES[name]) for name in sp.STATION_NAMES]

    random.shuffle(patients)

    for patient in patients:
        arrival_time = sp.START_TIME
        for station in stations:
            arrival_time = patient.visit_station(station, arrival_time)

    # Print schedules and total waiting times
    for patient in patients:
        print(f"\nPatient {patient.patient_id} Schedule:")
        for station_name, start, end in patient.schedule:
            print(f"  {station_name} from {start // 60}:{start % 60:02d} to {end // 60}:{end % 60:02d}")
        print(f"  Total Waiting Time: {patient.waiting_time} minutes")

if __name__ == "__main__":
    simulate_day()