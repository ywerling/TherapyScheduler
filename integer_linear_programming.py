import csv
from ortools.sat.python import cp_model

def minutes(h, m=0):
    return h * 60 + m

def format_time(minutes_since_midnight):
    hours = minutes_since_midnight // 60
    minutes = minutes_since_midnight % 60
    return f"{hours:02d}:{minutes:02d}"

def main():
    NUM_PATIENTS = 50
    STATIONS = {
        'doctor': {'count': 5, 'duration': 30},
        'therapist': {'count': 9, 'duration': 30},
        'dietitian': {'count': 7, 'duration': 30},
        'ecg': {'count': 8, 'duration': 20},
        'blood': {'count': 11, 'duration': 20},
    }

    START_TIME = minutes(13, 0)
    END_TIME = minutes(19, 30)
    HORIZON = END_TIME - START_TIME

    model = cp_model.CpModel()
    all_tasks = {}
    all_assignments = {}
    resource_to_intervals = {station: [[] for _ in range(info['count'])] for station, info in STATIONS.items()}

    for p in range(NUM_PATIENTS):
        for station, info in STATIONS.items():
            duration = info['duration']
            suffix = f'p{p}_{station}'

            start_var = model.NewIntVar(0, HORIZON - duration, f'start_{suffix}')
            end_var = model.NewIntVar(0, HORIZON, f'end_{suffix}')
            interval_var = model.NewIntervalVar(start_var, duration, end_var, f'interval_{suffix}')

            all_tasks[(p, station)] = (start_var, end_var, interval_var)
            all_assignments[(p, station)] = []

            # Assign to exactly one resource
            for i in range(info['count']):
                assigned_bool = model.NewBoolVar(f'assigned_{suffix}_res{i}')
                optional_interval = model.NewOptionalIntervalVar(
                    start_var, duration, end_var, assigned_bool, f'opt_interval_{suffix}_res{i}')
                resource_to_intervals[station][i].append(optional_interval)
                all_assignments[(p, station)].append(assigned_bool)

            model.AddExactlyOne(all_assignments[(p, station)])

    # No overlaps
    for station, resource_lists in resource_to_intervals.items():
        for resource in resource_lists:
            model.AddNoOverlap(resource)

    # Minimize total patient time on site
    total_time_on_site = []
    for p in range(NUM_PATIENTS):
        start_vars = [all_tasks[(p, s)][0] for s in STATIONS]
        end_vars = [all_tasks[(p, s)][1] for s in STATIONS]

        min_start = model.NewIntVar(0, HORIZON, f'min_start_p{p}')
        max_end = model.NewIntVar(0, HORIZON, f'max_end_p{p}')

        model.AddMinEquality(min_start, start_vars)
        model.AddMaxEquality(max_end, end_vars)

        time_on_site = model.NewIntVar(0, HORIZON, f'time_on_site_p{p}')
        model.Add(time_on_site == max_end - min_start)
        total_time_on_site.append(time_on_site)

    model.Minimize(sum(total_time_on_site))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    status = solver.Solve(model)

    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print(f"\n✅ Schedule Found! Total time on site: {solver.ObjectiveValue()} minutes\n")
        with open('patient_schedule.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Patient ID', 'Station', 'Station ID', 'Start Time', 'End Time'])

            for p in range(NUM_PATIENTS):
                for station, info in STATIONS.items():
                    start = solver.Value(all_tasks[(p, station)][0]) + START_TIME
                    end = solver.Value(all_tasks[(p, station)][1]) + START_TIME

                    # Find the assigned resource ID
                    assigned_bools = all_assignments[(p, station)]
                    station_id = next(i for i, b in enumerate(assigned_bools) if solver.Value(b) == 1)

                    writer.writerow([
                        p,
                        station,
                        station_id,
                        format_time(start),
                        format_time(end)
                    ])
        print("📄 CSV export completed: 'patient_schedule.csv'")
    else:
        print("❌ No feasible schedule found.")

if __name__ == "__main__":
    main()
