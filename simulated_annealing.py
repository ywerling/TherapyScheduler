import random
import math
import scheduling_parameters as sp

# # Constants
# NUM_PATIENTS = 10
# NUM_STATIONS = 5
# START_TIME = 13 * 60  # 13:00 in minutes
# END_TIME = 19 * 60  # 19:00 in minutes
#
# STATION_NAMES = ["General Practitioner", "Dietitian", "Orthopedist", "Blood Sample", "Electrocardiogram"]
# STATION_TIMES = {
#     "General Practitioner": 30,
#     "Dietitian": 30,
#     "Orthopedist": 30,
#     "Blood Sample": 20,
#     "Electrocardiogram": 20
# }

INITIAL_TEMP = 1000.0
FINAL_TEMP = 0.01
ANNEALING_RATE = 0.995


class Schedule:
    def __init__(self, visits):
        self.visits = visits  # visits[patient] = list of station indices

    def get_cost_and_times(self):
        """ Calculate waiting time and actual schedule per patient, enforcing non-concurrency """
        station_available = {station: sp.START_TIME for station in sp.STATION_NAMES}
        patient_available = [sp.START_TIME for _ in range (sp.NUM_PATIENTS)]
        waiting_times = [0 for _ in range(sp.NUM_PATIENTS)]

        # Schedule matrix: patient -> list of (station_name, start, end)
        schedule_matrix = [[] for _ in range(sp.NUM_PATIENTS)]

        for step in range(sp.NUM_STATIONS):
            for patient_idx in range(sp.NUM_PATIENTS):
                station_idx = self.visits[patient_idx][step]
                station = sp.STATION_NAMES[station_idx]
                duration = sp.STATION_TIMES[station]

                # Find the earliest time both patient and station are available
                start_time = max(patient_available[patient_idx], station_available[station])
                end_time = start_time + duration

                # Update availabilities
                patient_available[patient_idx] = end_time
                station_available[station] = end_time

                # Record schedule and waiting time
                waiting_times[patient_idx] += start_time - patient_available[patient_idx]
                schedule_matrix[patient_idx].append((station, start_time, end_time))

        return waiting_times, schedule_matrix

    def total_cost(self):
        waiting_times, _ = self.get_cost_and_times()
        return sum(waiting_times)

    def perturb(self):
        new_visits = [list(v) for v in self.visits]
        p1, p2 = random.sample(range(sp.NUM_PATIENTS), 2)
        s1, s2 = random.sample(range(sp.NUM_STATIONS), 2)
        new_visits[p1][s1], new_visits[p2][s2] = new_visits[p2][s2], new_visits[p1][s1]
        return Schedule(new_visits)


def simulated_annealing(initial_schedule):
    current = initial_schedule
    best = current
    current_cost = current.total_cost()
    best_cost = current_cost
    temp = INITIAL_TEMP

    while temp > FINAL_TEMP:
        new_schedule = current.perturb()
        new_cost = new_schedule.total_cost()

        if new_cost < current_cost:
            current = new_schedule
            current_cost = new_cost
            if new_cost < best_cost:
                best = new_schedule
                best_cost = new_cost
        else:
            probability = math.exp((current_cost - new_cost) / temp)
            if random.random() < probability:
                current = new_schedule
                current_cost = new_cost

        temp *= ANNEALING_RATE

    return best


def generate_random_schedule():
    return Schedule([random.sample(range(sp.NUM_STATIONS), sp.NUM_STATIONS) for _ in range(sp.NUM_PATIENTS)])


def print_schedule(schedule):
    _, schedule_matrix = schedule.get_cost_and_times()

    for patient_idx, visits in enumerate(schedule_matrix):
        print(f"Patient {patient_idx + 1}:")
        for station, start, end in visits:
            print(f"  {station}: {start // 60:02d}:{start % 60:02d} to {end // 60:02d}:{end % 60:02d}")
        print()


def main():
    initial_schedule = generate_random_schedule()
    best_schedule = simulated_annealing(initial_schedule)

    print("Best Schedule Found:\n")
    print_schedule(best_schedule)

    waiting_times, _ = best_schedule.get_cost_and_times()
    print("\nTotal Waiting Time per Patient:")
    for idx, wt in enumerate(waiting_times):
        print(f"  Patient {idx + 1}: {wt} minutes")

    print(f"\nTotal Waiting Time (All Patients): {sum(waiting_times)} minutes")


if __name__ == "__main__":
    main()
