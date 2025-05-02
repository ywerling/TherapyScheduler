**BASIC ALGORITHM**

How the code works:

    Station Class: This class represents each medical station. It has:
        A process_time which indicates how long each visit takes (e.g., 30 minutes for GP).
        The available_time, which tracks when the station is free to accept another patient.
        The can_process() method checks if a station can process a patient based on the current time.
        The process_patient() method updates the station's availability and records the start and end times for a patient's visit.
    Patient Class: This class represents a patient. It has:
        A patient_id to uniquely identify each patient.
        A schedule to store the patient's visits to each station.
        The visit_station() method which makes a patient visit a station and records the visit's start and end time.
    simulate_day():
        This function initializes 10 patients and 5 stations.
        It then simulates each patient's visit to the stations by iterating over the stations.
        The schedule for each patient is printed with the station name and the time they visited each station.


**SIMULATED ANNEALING**

Explanation:

    Schedule Class:
        The Schedule class represents a schedule where each patient has a list of stations they need to visit in a specific order.
        The get_cost() method calculates the total waiting time for all patients, considering the processing time of each station and the station availability.
        The perturb() method creates a new schedule by swapping the visits of two random patients at two random stations.
    Simulated Annealing:
        The simulated_annealing() function iterates through the process of perturbing the schedule, accepting better solutions (lower cost), and probabilistically accepting worse solutions (to avoid local minima).
        The temperature gradually decreases, making the algorithm focus on exploiting good solutions rather than exploring new ones.
    Generate Random Schedule:
        The generate_random_schedule() function creates an initial random schedule by randomly assigning a visiting order for each patient to the stations.
    Printing the Schedule:
        The print_schedule() function prints out the schedule in a human-readable format with times for each patient's visits to each station.

 **ANT COLONY OPTIMIZATION**
Explanation:

    Schedule Class:
        The Schedule class stores a patient's visit order to each station.
        The get_cost() function calculates the total waiting time for all patients. It ensures that each station can only handle one patient at a time and tracks the station availability.
    Ant Colony Optimization:
        Pheromone Matrix: Each pair of stations has a pheromone level indicating how favorable it is to select that station. Initially, all pheromone levels are set to the same value (INITIAL_PHEROMONE).
        Ants' Path Construction: Each "ant" creates a random schedule by choosing a station order for each patient, considering pheromone levels and heuristic values (i.e., waiting time).
        Pheromone Update: After all ants generate their schedules, the pheromones are updated based on the quality of the solutions. Better solutions (with lower waiting times) deposit more pheromone, reinforcing their selection.
    Main Function:
        The ant_colony_optimization() function runs the ACO algorithm for a specified number of iterations.
        The best schedule and its cost are tracked and printed at the end.
    Schedule Output:
        The program prints the best schedule found with the times for each patient at each station, as well as the total waiting time.

 