import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def time_to_minutes(t):
    h, m = map(int, t.split(':'))
    return h * 60 + m

def plot_station_gantt(csv_file='patient_schedule.csv', output_prefix='station_gantt'):
    df = pd.read_csv(csv_file)
    df['Start Min'] = df['Start Time'].apply(time_to_minutes)
    df['End Min'] = df['End Time'].apply(time_to_minutes)
    df['Duration'] = df['End Min'] - df['Start Min']
    df['StationGroup'] = df['Station'] + " #" + df['Station ID'].astype(str)

    station_colors = {
        'doctor': 'tab:blue',
        'therapist': 'tab:green',
        'dietitian': 'tab:orange',
        'ecg': 'tab:red',
        'blood': 'tab:purple',
    }

    fig, ax = plt.subplots(figsize=(16, 12))

    station_order = sorted(df['StationGroup'].unique())
    y_pos = {sg: i for i, sg in enumerate(station_order)}

    for _, row in df.iterrows():
        color = station_colors.get(row['Station'], 'gray')
        ax.barh(
            y=y_pos[row['StationGroup']],
            width=row['Duration'],
            left=row['Start Min'],
            height=0.6,
            color=color,
            edgecolor='black'
        )
        ax.text(
            row['Start Min'] + 1,
            y_pos[row['StationGroup']] - 0.2,
            f"P{row['Patient ID']}",
            fontsize=6,
            color='white'
        )

    ax.set_yticks(list(y_pos.values()))
    ax.set_yticklabels(list(y_pos.keys()))
    ax.set_xlabel("Time (HH:MM)")
    ax.set_title("Gantt Chart by Station and Station ID")

    # Format time on x-axis
    xticks = range(time_to_minutes("13:00"), time_to_minutes("19:31"), 30)
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{t//60:02d}:{t%60:02d}" for t in xticks], rotation=45)

    # Legend
    patches = [mpatches.Patch(color=clr, label=station) for station, clr in station_colors.items()]
    ax.legend(handles=patches, title="Stations", loc='upper right')

    plt.tight_layout()

    # Save outputs
    plt.savefig(f"{output_prefix}.png", dpi=300)
    plt.savefig(f"{output_prefix}.pdf")
    print(f"📁 Gantt chart saved as: {output_prefix}.png and {output_prefix}.pdf")

    plt.show()

if __name__ == "__main__":
    plot_station_gantt()
