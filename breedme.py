# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from ipywidgets import FileUpload, Button, Output
from IPython.display import display 
import io

# File Upload Functionality
upload = FileUpload(accept='.xlsx', multiple=False)
process_button = Button(description='Verarbeite Daten')
output_area = Output()

def process_data(df):
    # Convert 'Geb.' column to datetime and calculate age in weeks
    df['Geb.'] = pd.to_datetime(df['Geb.'])
    df['age'] = (pd.Timestamp.now() - df['Geb.']).dt.days / 7

    # Create age groups
    bins = [0, 7, 8, 10, 14, np.inf]
    labels = ['<7 weeks', '7-8 weeks', '8-10 weeks', '10-14 weeks', '>14 weeks']
    df['age_groups'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Filter data based on 'Käfignummer' and 'G'
    df_breeding = df[df['Käfig-Name'].str.contains('ZK')]
    df_males = df[(df['G'] == 'm') & -df['Käfig-Name'].str.contains('ZK')]
    df_females = df[(df['G'] == 'f') & -df['Käfig-Name'].str.contains('ZK')]

    # Summarize data
    summary_breeding = df_breeding.groupby(['Stamm', 'Genotyp', 'age_groups', 'G', 'Käfig-Name']).size().reset_index(name='count')
    summary_males = df_males.groupby(['Stamm', 'Genotyp', 'age_groups']).size().reset_index(name='count')
    summary_females = df_females.groupby(['Stamm', 'Genotyp', 'age_groups']).size().reset_index(name='count')

    # Plotting the data
    plot_breeding(summary_breeding)
    plot_breeding_2(summary_breeding)
    plot_males(summary_males)
    plot_males_2(summary_males)
    plot_females(summary_females)
    plot_females_2(summary_females)

# +
def plot_breeding(data):
    plt.figure(figsize=(20, 6))

    # Erstellen eines Pivots für gestapelte Balkendiagramme mit Summierung der Werte
    pivot_data = data.pivot_table(index='Genotyp', columns='Käfig-Name', values='count', fill_value=0, aggfunc='sum')

    # Erstellen des gestapelten Balkendiagramms
    ax = pivot_data.plot(kind='bar', stacked=True)

    # Iteration durch jede Gruppe (jede Bar)
    for rect in ax.patches:
        height = rect.get_height()
        if height > 0:  # Anzeige nur, wenn der Wert größer als 0 ist
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=8)

    plt.title("Breeding Pairs")
    plt.xticks(rotation=45, fontsize=8)
    plt.legend(title='Käfig-Name', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()




# +
def plot_breeding_2(data):
    plt.figure(figsize=(25, 6))

    pivot_data = data.pivot_table(index='Stamm', columns='Käfig-Name', values='count', fill_value=0, aggfunc='sum')
    ax = pivot_data.plot(kind='bar', stacked=True)

    for rect in ax.patches:
        height = rect.get_height()
        if height > 0:
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=8)

    plt.title("Breeding Pairs")
    plt.xticks(rotation=45, fontsize=8)
    plt.legend(title='Käfig-Name', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()


# -

def plot_males(data):
    plt.figure(figsize=(20, 6))

    # Erstellen eines Pivots für gestapelte Balkendiagramme mit Summierung der Werte
    pivot_data = data.pivot_table(index='Genotyp', columns='age_groups', values='count', fill_value=0, aggfunc='sum')

    # Erstellen des gestapelten Balkendiagramms
    ax = pivot_data.plot(kind='bar', stacked=True)

    # Iteration durch jede Gruppe (jede Bar)
    for rect in ax.patches:
        height = rect.get_height()
        if height > 0:  # Anzeige nur, wenn der Wert größer als 0 ist
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=8)

    plt.title("Males")
    plt.xticks(rotation=90, fontsize=8)
    plt.legend(title='Age Groups', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()


# +
def plot_males_2(data):
    plt.figure(figsize=(30, 6))

    # Erstellen eines Pivots für gestapelte Balkendiagramme mit Summierung der Werte
    pivot_data = data.pivot_table(index='Stamm', columns='age_groups', values='count', fill_value=0, aggfunc='sum')
    


    # Erstellen des gestapelten Balkendiagramms
    ax = pivot_data.plot(kind='bar', stacked=True)

    # Iteration durch jede Gruppe (jede Bar)
    for rect in ax.patches:
        height = rect.get_height()
        if height > 0:  # Anzeige nur, wenn der Wert größer als 0 ist
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=8)

    plt.title("Males")
    plt.xticks(rotation=90, fontsize=8)
    plt.legend(title='Age Groups', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()

# Rufen Sie die Funktion mit Ihren Daten auf
# plot_males_2(Ihre_Daten)


# -

def plot_females(data):
    plt.figure(figsize=(20, 6))

    # Erstellen eines Pivots für gestapelte Balkendiagramme mit Summierung der Werte
    pivot_data = data.pivot_table(index='Genotyp', columns='age_groups', values='count', fill_value=0, aggfunc='sum')

    # Erstellen des gestapelten Balkendiagramms
    ax = pivot_data.plot(kind='bar', stacked=True)

    # Iteration durch jede Gruppe (jede Bar)
    for rect in ax.patches:
        height = rect.get_height()
        if height > 0:  # Anzeige nur, wenn der Wert größer als 0 ist
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=8)

    plt.title("Females")
    plt.xticks(rotation=90, fontsize=8)
    plt.legend(title='Age Groups', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()


def plot_females_2(data):
    plt.figure(figsize=(25, 6))

    pivot_data = data.pivot_table(index='Stamm', columns='age_groups', values='count', fill_value=0, aggfunc='sum')
    ax = pivot_data.plot(kind='bar', stacked=True)

    for rect in ax.patches:
        height = rect.get_height()
        if height > 0:
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + height / 2
            ax.text(x, y, str(int(height)), ha='center', va='center', fontsize=8)

    plt.title("Females")
    plt.xticks(rotation=45, fontsize=8)
    plt.legend(title='Age Groups', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()


# +
def on_button_clicked(b):
    with output_area:
        output_area.clear_output()
        if not upload.value:
            print("Bitte laden Sie zuerst eine Datei hoch.")
            return
        # Zugriff auf das erste Element des Tupels, das ein Dictionary ist
        file_info = upload.value[0]
        content = file_info['content']
        df = pd.read_excel(io.BytesIO(content))
        # Weiterer Code für die Datenverarbeitung...
        process_data(df)

process_button.on_click(on_button_clicked)

# -

display(upload, process_button, output_area)


