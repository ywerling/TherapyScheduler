import random
import math

# Constants
NUM_PATIENTS = 10
NUM_STATIONS = 5
START_TIME = 13 * 60  # 13:00 in minutes
END_TIME = 19 * 60  # 19:00 in minutes

STATION_NAMES = ["General Practitioner", "Dietitian", "Orthopedist", "Blood Sample", "Electrocardiogram"]
STATION_TIMES = {
    "General Practitioner": 30,
    "Dietitian": 30,
    "Orthopedist": 30,
    "Blood Sample": 20,
    "Electrocardiogram": 20
}

INITIAL_TEMP = 1000.0
FINAL_TEMP = 0.01
ANNEALING_RATE = 0.995


class Schedule:
    def __init__(self, visits):
        self.visits = visits

    def get_cost(self):
        """Calculate waiting time for each patient and return the list."""
        station_available = {station: START_TIME for station in STATION_NAMES}
        waiting_times = [0] * NUM_PATIENTS

        for patient_idx in range(NUM_PATIENTS):
            arrival_time = START_TIME

            for station_idx in self.visits[patient_idx]:
                station = STATION_NAMES[station_idx]
                processing_time = STATION_TIMES[station]

                # Wait until both the patient and the station are available
                start_time = max(arrival_time, station_available[station])
                end_time = start_time + processing_time

                # Update the station's next available time
                station_available[station] = end_time

                # Waiting time is difference between arrival and actual start
                waiting_times[patient_idx] += (start_time - arrival_time)

                # Update arrival time for next station
                arrival_time = end_time

        return waiting_times

    def total_cost(self):
        return sum(self.get_cost())

    def perturb(self):
        new_visits = [list(v) for v in self.visits]
        p1, p2 = random.sample(range(NUM_PATIENTS), 2)
        s1, s2 = random.sample(range(NUM_STATIONS), 2)
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
    return Schedule([random.sample(range(NUM_STATIONS), NUM_STATIONS) for _ in range(NUM_PATIENTS)])


def print_schedule(schedule):
    for patient_idx in range(NUM_PATIENTS):
        print(f"Patient {patient_idx + 1}:")
        arrival_time = START_TIME
        for station_idx in schedule.visits[patient_idx]:
            station = STATION_NAMES[station_idx]
            processing_time = STATION_TIMES[station]
            start_time = arrival_time
            end_time = start_time + processing_time
            print(f"  {station}: {start_time // 60:02d}:{start_time % 60:02d} to {end_time // 60:02d}:{end_time % 60:02d}")
            arrival_time = end_time
        print()


def main():
    initial_schedule = generate_random_schedule()
    best_schedule = simulated_annealing(initial_schedule)

    print("Best Schedule Found:\n")
    print_schedule(best_schedule)

    waiting_times = best_schedule.get_cost()
    print("\nTotal Waiting Time per Patient:")
    for idx, wt in enumerate(waiting_times):
        print(f"  Patient {idx + 1}: {wt} minutes")

    print(f"\nTotal Waiting Time (All Patients): {sum(waiting_times)} minutes")


if __name__ == "__main__":
    main()
