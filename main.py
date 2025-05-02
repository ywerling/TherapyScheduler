# from unittest import case
import ant_colony_optimization as alg_aco
import simulated_annealing as alg_sa
import basic_algorithm as alg_ba
import greedy_algorithm as alg_gr
import integer_linear_programming as alg_ilp

def main():
    print ("Welcome to the scheduler algorithm comparator\n\n")
    print ("Select the algorithm to use:")
    print ("1 - Basic Algorithm")
    print ("2 - Simulated Annealing Algorithm")
    print ("3 - Ant Colony Algorithm")
    print ("4 - Greedy Algorithm")
    print ("5 - Integer Linear Programming")
    print ("\n")

    selection = int(input("Select an option: "))
    # print(f"Selected algorithm: {selection}")

    match selection:
        case 1:
            alg_ba.simulate_day()
        case 2:
            alg_sa.simulate_day()
        case 3:
            alg_aco.simulate_day()
        case 4:
            alg_gr.simulate_day()
        case 5:
            alg_ilp.main()
        case default:
            print("Algorithm not available")


if __name__ == "__main__":
    main()