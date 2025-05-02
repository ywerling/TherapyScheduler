import random

import math

import time

# Constants

NUM_PATIENTS = 10

NUM_STATIONS = 5

START_TIME = 13 * 60  # 13:00 in minutes

END_TIME = 19 * 60  # 19:00 in minutes

STATION_NAMES = ["General Practitioner", "Dietitian", "Orthopedist", "Blood Sample", "Electrocardiogram"]

STATION_TIMES = {

    "General Practitioner": 30,  # 30 minutes

    "Dietitian": 30,  # 30 minutes

    "Orthopedist": 30,  # 30 minutes

    "Blood Sample": 20,  # 20 minutes

    "Electrocardiogram": 20  # 20 minutes

}

INITIAL_TEMP = 1000.0  # Initial temperature for simulated annealing

FINAL_TEMP = 0.01  # Final temperature

ANNEALING_RATE = 0.995  # Annealing rate


# State representation (schedule)

class Schedule:

    def __init__(self, visits):

        # visits is a list of lists representing patient visit orders to stations

        self.visits = visits

    def get_cost(self):

        """ Calculate the total waiting time (cost) for the current schedule """

        # Station availability time (when each station becomes free)

        station_available = {station: START_TIME for station in STATION_NAMES}

        total_waiting_time = 0

        # For each patient

        for patient_idx in range(NUM_PATIENTS):

            arrival_time = START_TIME

            for station_idx in self.visits[patient_idx]:
                station = STATION_NAMES[station_idx]

                processing_time = STATION_TIMES[station]

                # The patient can only visit the station when it's free

                start_time = max(arrival_time, station_available[station])

                end_time = start_time + processing_time

                # Update station availability

                station_available[station] = end_time

                # Add waiting time for this visit

                total_waiting_time += (start_time - arrival_time)

                # Update the arrival time for the next station

                arrival_time = end_time

        return total_waiting_time

    def perturb(self):

        """ Generate a new schedule by swapping visits between two random patients """

        new_visits = [list(patient_visits) for patient_visits in self.visits]  # Copy of visits list

        # Select two random patients

        patient1, patient2 = random.sample(range(NUM_PATIENTS), 2)

        # Select two random stations for each patient

        station1, station2 = random.sample(range(NUM_STATIONS), 2)

        # Swap the visit order of the two stations for the two patients

        new_visits[patient1][station1], new_visits[patient2][station2] = new_visits[patient2][station2], \
        new_visits[patient1][station1]

        return Schedule(new_visits)


def simulated_annealing(initial_schedule):
    """ Perform the simulated annealing process """

    current_schedule = initial_schedule

    current_cost = current_schedule.get_cost()

    best_schedule = current_schedule

    best_cost = current_cost

    temperature = INITIAL_TEMP

    while temperature > FINAL_TEMP:

        # Perturb the schedule (make a small change)

        new_schedule = current_schedule.perturb()

        new_cost = new_schedule.get_cost()

        # If the new schedule is better, accept it

        if new_cost < current_cost:

            current_schedule = new_schedule

            current_cost = new_cost

            # If it's also the best we've found, update best_schedule

            if new_cost < best_cost:
                best_schedule = new_schedule

                best_cost = new_cost

        else:

            # Otherwise, accept it with some probability

            probability = math.exp((current_cost - new_cost) / temperature)

            if random.random() < probability:
                current_schedule = new_schedule

                current_cost = new_cost

        # Decrease the temperature

        temperature *= ANNEALING_RATE

    return best_schedule


def generate_random_schedule():
    """ Generate an initial random schedule for the patients """

    visits = []

    for _ in range(NUM_PATIENTS):
        # Randomize the order of stations for each patient

        visits.append(random.sample(range(NUM_STATIONS), NUM_STATIONS))

    return Schedule(visits)


def print_schedule(schedule):
    """ Print the schedule in a readable format """

    for patient_idx in range(NUM_PATIENTS):

        print(f"Patient {patient_idx + 1}:")

        arrival_time = START_TIME

        for station_idx in schedule.visits[patient_idx]:
            station = STATION_NAMES[station_idx]

            processing_time = STATION_TIMES[station]

            start_time = arrival_time

            end_time = arrival_time + processing_time

            print(
                f"  {station}: {start_time // 60:02d}:{start_time % 60:02d} to {end_time // 60:02d}:{end_time % 60:02d}")

            arrival_time = end_time

        print()


# Main function to run the simulation

def main():
    # Step 1: Generate an initial random schedule

    initial_schedule = generate_random_schedule()

    # Step 2: Perform simulated annealing to find an optimal schedule

    best_schedule = simulated_annealing(initial_schedule)

    # Step 3: Print the best schedule found

    print("Best Schedule found:")

    print_schedule(best_schedule)

    # Step 4: Print the total waiting time (cost) of the best schedule

    print(f"Total waiting time (cost): {best_schedule.get_cost()} minutes")


if __name__ == "__main__":
    main()

