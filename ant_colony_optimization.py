import random
import math
import scheduling_parameters as sp

# Constants
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

INITIAL_PHEROMONE = 1.0
PHEROMONE_EVAPORATION = 0.95
ALPHA = 1.0  # Influence of pheromone
BETA = 2.0   # Influence of heuristic (processing time)
NUM_ANTS = 20
NUM_ITERATIONS = 100


# Schedule class with non-concurrent cost calculation
class Schedule:
    def __init__(self, visits):
        self.visits = visits

    def get_cost(self):
        station_available = {station: sp.START_TIME for station in sp.STATION_NAMES}
        patient_available = [sp.START_TIME for _ in range(sp.NUM_PATIENTS)]
        total_waiting_time = 0

        # Validate schedule while calculating cost
        for patient_idx in range(sp.NUM_PATIENTS):
            for station_idx in self.visits[patient_idx]:
                station = sp.STATION_NAMES[station_idx]
                processing_time = sp.STATION_TIMES[station]

                start_time = max(patient_available[patient_idx], station_available[station])
                end_time = start_time + processing_time

                # Reject invalid assignments if station is already occupied
                if start_time < station_available[station]:
                    return float('inf')  # Infeasible solution with conflict

                # Update timelines
                total_waiting_time += (start_time - patient_available[patient_idx])
                station_available[station] = end_time
                patient_available[patient_idx] = end_time

        return total_waiting_time


# Select next station using ACO rules
def select_next_station(current_station, unvisited, pheromones, alpha, beta):
    probabilities = []
    for station in unvisited:
        pheromone = pheromones[current_station][station] if current_station is not None else INITIAL_PHEROMONE
        heuristic = 1.0 / sp.STATION_TIMES[sp.STATION_NAMES[station]]
        probability = (pheromone ** alpha) * (heuristic ** beta)
        probabilities.append(probability)

    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]

    return random.choices(unvisited, weights=probabilities, k=1)[0]


# Ant Colony Optimization
def ant_colony_optimization():
    pheromones = [[INITIAL_PHEROMONE for _ in range(sp.NUM_STATIONS)] for _ in range(sp.NUM_STATIONS)]

    best_schedule = None
    best_cost = float('inf')

    for iteration in range(NUM_ITERATIONS):
        all_schedules = []

        for ant in range(NUM_ANTS):
            visits = []

            # Construct the visit schedule for each patient
            for patient in range(sp.NUM_PATIENTS):
                unvisited = list(range(sp.NUM_STATIONS))
                visit_order = []
                current_station = None

                # Select stations for the patient while respecting availability and pheromones
                while unvisited:
                    next_station = select_next_station(current_station, unvisited, pheromones, ALPHA, BETA)
                    visit_order.append(next_station)
                    unvisited.remove(next_station)
                    current_station = next_station

                visits.append(visit_order)

            # Create a Schedule and check its feasibility
            schedule = Schedule(visits)

            # Only add to all_schedules if the schedule is feasible
            if schedule.get_cost() != float('inf'):
                all_schedules.append(schedule)

        # If no feasible schedule was found, skip pheromone updates
        if not all_schedules:
            print(f"Iteration {iteration + 1}/{NUM_ITERATIONS}: No feasible schedules found.")
            continue

        # Evaluate all schedules and update the best schedule
        for schedule in all_schedules:
            cost = schedule.get_cost()
            if cost < best_cost:
                best_schedule = schedule
                best_cost = cost

        # Evaporate pheromones
        pheromones = [[pheromone * PHEROMONE_EVAPORATION for pheromone in row] for row in pheromones]

        # Update pheromones based on schedule costs
        for schedule in all_schedules:
            cost = schedule.get_cost()
            pheromone_deposit = 1.0 / (cost + 1e-10)

            for patient in range(sp.NUM_PATIENTS):
                for i in range(sp.NUM_STATIONS - 1):
                    from_station = schedule.visits[patient][i]
                    to_station = schedule.visits[patient][i + 1]
                    pheromones[from_station][to_station] += pheromone_deposit

        print(f"Iteration {iteration + 1}/{NUM_ITERATIONS}, Best Cost: {best_cost}")

    return best_schedule


# Print the best schedule
def print_schedule(schedule):
    for patient_idx in range(sp.NUM_PATIENTS):
        print(f"Patient {patient_idx + 1}:")

        station_available = {station: sp.START_TIME for station in sp.STATION_NAMES}
        patient_available = sp.START_TIME

        for station_idx in schedule.visits[patient_idx]:
            station = sp.STATION_NAMES[station_idx]
            processing_time = sp.STATION_TIMES[station]

            start_time = max(patient_available, station_available[station])
            end_time = start_time + processing_time

            print(f"  {station}: {start_time // 60:02d}:{start_time % 60:02d} to {end_time // 60:02d}:{end_time % 60:02d}")

            station_available[station] = end_time
            patient_available = end_time

        print()


# Main
def simulate_day():
    best_schedule = ant_colony_optimization()
    print("\nBest Schedule found:\n")
    print_schedule(best_schedule)
    print(f"Total waiting time (cost): {best_schedule.get_cost()} minutes")


if __name__ == "__main__":
    simulate_day()
