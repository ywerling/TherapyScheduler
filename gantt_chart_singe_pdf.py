import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages

def time_to_minutes(t):
    h, m = map(int, t.split(':'))
    return h * 60 + m

def load_data(csv_file):
    df = pd.read_csv(csv_file)
    df['Start Min'] = df['Start Time'].apply(time_to_minutes)
    df['End Min'] = df['End Time'].apply(time_to_minutes)
    df['Duration'] = df['End Min'] - df['Start Min']
    df['StationGroup'] = df['Station'] + " #" + df['Station ID'].astype(str)
    return df

def plot_patient_gantt(df, pdf):
    fig, ax = plt.subplots(figsize=(16, 12))
    station_colors = {
        'doctor': 'tab:blue',
        'therapist': 'tab:green',
        'dietitian': 'tab:orange',
        'ecg': 'tab:red',
        'blood': 'tab:purple',
    }

    patient_order = sorted(df['Patient ID'].unique())
    y_pos = {pid: i for i, pid in enumerate(patient_order)}

    for _, row in df.iterrows():
        color = station_colors.get(row['Station'], 'gray')
        ax.barh(
            y=y_pos[row['Patient ID']],
            width=row['Duration'],
            left=row['Start Min'],
            height=0.6,
            color=color,
            edgecolor='black'
        )
        ax.text(
            row['Start Min'] + 1,
            y_pos[row['Patient ID']] - 0.2,
            f"{row['Station']}#{row['Station ID']}",
            fontsize=6,
            color='white'
        )

    ax.set_yticks(list(y_pos.values()))
    ax.set_yticklabels([f"Patient {pid}" for pid in y_pos.keys()])
    ax.set_xlabel("Time (HH:MM)")
    ax.set_title("Patient Appointment Gantt Chart")
    xticks = range(time_to_minutes("13:00"), time_to_minutes("19:31"), 30)
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{t//60:02d}:{t%60:02d}" for t in xticks], rotation=45)
    patches = [mpatches.Patch(color=clr, label=station) for station, clr in station_colors.items()]
    ax.legend(handles=patches, title="Stations", loc='upper right')
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)

def plot_station_gantt(df, pdf):
    fig, ax = plt.subplots(figsize=(16, 12))
    station_colors = {
        'doctor': 'tab:blue',
        'therapist': 'tab:green',
        'dietitian': 'tab:orange',
        'ecg': 'tab:red',
        'blood': 'tab:purple',
    }

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
    ax.set_title("Station Utilization Gantt Chart")
    xticks = range(time_to_minutes("13:00"), time_to_minutes("19:31"), 30)
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{t//60:02d}:{t%60:02d}" for t in xticks], rotation=45)
    patches = [mpatches.Patch(color=clr, label=station) for station, clr in station_colors.items()]
    ax.legend(handles=patches, title="Stations", loc='upper right')
    plt.tight_layout()
    pdf.savefig(fig)
    plt.close(fig)

def generate_combined_report(csv_file='patient_schedule.csv', output_pdf='combined_gantt_report.pdf'):
    df = load_data(csv_file)
    with PdfPages(output_pdf) as pdf:
        plot_patient_gantt(df, pdf)
        plot_station_gantt(df, pdf)
    print(f"✅ Combined Gantt report saved as '{output_pdf}'")

if __name__ == "__main__":
    generate_combined_report()
