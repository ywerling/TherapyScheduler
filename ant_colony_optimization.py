import random

import math

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

INITIAL_PHEROMONE = 1.0

PHEROMONE_EVAPORATION = 0.95

ALPHA = 1.0  # Influence of pheromone

BETA = 2.0  # Influence of heuristic (waiting time)

NUM_ANTS = 20

NUM_ITERATIONS = 100


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


# Ant Colony Optimization Algorithm

def ant_colony_optimization():
    # Initialize pheromone matrix: pheromones for each station pair for each patient

    pheromones = [[INITIAL_PHEROMONE for _ in range(NUM_STATIONS)] for _ in range(NUM_STATIONS)]

    # Initialize the best solution and its cost

    best_schedule = None

    best_cost = float('inf')

    for iteration in range(NUM_ITERATIONS):

        all_schedules = []

        # Step 1: Generate solutions using ants

        for ant in range(NUM_ANTS):

            visits = []

            # Create a random solution (schedule) for each ant

            for patient in range(NUM_PATIENTS):
                # Choose station visit order for the patient based on pheromones and heuristic

                visited_stations = random.sample(range(NUM_STATIONS), NUM_STATIONS)

                visits.append(visited_stations)

            # Create a schedule from the generated visits

            schedule = Schedule(visits)

            all_schedules.append(schedule)

        # Step 2: Evaluate all schedules and update pheromones

        for schedule in all_schedules:

            cost = schedule.get_cost()

            # If this solution is better, update the best solution

            if cost < best_cost:
                best_schedule = schedule

                best_cost = cost

        # Step 3: Update pheromones based on the solutions

        pheromones = [[pheromone * PHEROMONE_EVAPORATION for pheromone in row] for row in pheromones]

        for schedule in all_schedules:

            cost = schedule.get_cost()

            # Inverse of cost is used for pheromone deposit (better schedules get more pheromone)

            pheromone_deposit = 1.0 / (cost + 1e-10)

            for patient in range(NUM_PATIENTS):

                for station in range(NUM_STATIONS):
                    # Add pheromone deposit to the selected station

                    pheromones[schedule.visits[patient][station]][station] += pheromone_deposit

        # Optional: Print the progress of the iterations

        print(f"Iteration {iteration + 1}/{NUM_ITERATIONS}, Best Cost: {best_cost}")

    return best_schedule


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
    # Perform Ant Colony Optimization to find the best schedule

    best_schedule = ant_colony_optimization()

    # Print the best schedule found

    print("Best Schedule found:")

    print_schedule(best_schedule)

    # Print the total waiting time (cost) of the best schedule

    print(f"Total waiting time (cost): {best_schedule.get_cost()} minutes")


if __name__ == "__main__":
    main()
