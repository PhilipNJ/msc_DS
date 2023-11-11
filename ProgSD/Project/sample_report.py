import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

pathdb = str(os.path.dirname(os.path.abspath(__file__)))
db_path = pathdb+"/register.db"

# Function to establish a database connection and fetch data into Pandas DataFrames
def fetch_data_from_db():
    connection = sqlite3.connect(db_path)
    logindetails_df = pd.read_sql_query("SELECT * FROM logindetails", connection)
    tripdetails_df = pd.read_sql_query("SELECT * FROM tripdetails", connection)
    vehicledetails_df = pd.read_sql_query("SELECT * FROM vehicledetails", connection)
    walletdetails_df = pd.read_sql_query("SELECT * FROM walletdetails", connection)
    connection.close()
    return logindetails_df, tripdetails_df, vehicledetails_df, walletdetails_df

# Load data from SQLite into Pandas DataFrames
logindetails_df, tripdetails_df, vehicledetails_df, walletdetails_df = fetch_data_from_db()

def table_stats():
    mean_df = pd.DataFrame(tripdetails_df[['trip_duration','trip_fare','rating']].mean().reset_index())
    mean_df.columns = ['Type','Mean']
    max_df = pd.DataFrame(tripdetails_df[['trip_duration','trip_fare','rating']].max().reset_index())
    max_df.columns = ['Type','max']
    stat_df = mean_df.merge(max_df,how='left',on='Type')
    print(stat_df)

    stat_tree = ttk.Treeview(tree_frame, columns=("Type", "Mean", "Max"), displaycolumns=("Type", "Mean", "Max"))
    stat_tree.heading("#1", text="Type")
    stat_tree.heading("#2", text="Mean")
    stat_tree.heading("#3", text="Max")

    stat_tree.column("#0", width=0)
    stat_tree.column("#1", width=150, anchor="center")
    stat_tree.column("#2", width=150, anchor="center")
    stat_tree.column("#3", width=150, anchor="center")
    stat_tree.grid(row=4,column=0,padx=10,pady=5)
    # Insert data into Treeview
    for index, row in stat_df.iterrows():
        stat_tree.insert("", "end", values=(row["Type"], row["Mean"], row["Max"]))

def table_mostfreq():    
    # Assuming tripdetails_df is your DataFrame
    column_frequencies = {}

    # Iterate through columns and find the most frequent value for each column
    for column in ['vehicle_no','start_location','end_location','rating','user_id']:
        value_counts = tripdetails_df[column].value_counts()
        max_frequency = value_counts.max()
        frequent_values = value_counts[value_counts == max_frequency].index.tolist()
        column_frequencies[column] = {
            "Frequency": max_frequency,
            "Values": ", ".join([str(value) for value in frequent_values])
        }

    # Create a new DataFrame with the desired format
    most_frequent_df = pd.DataFrame.from_dict(column_frequencies, orient='index')
    most_frequent_df.reset_index(inplace=True)
    most_frequent_df.columns = ['Column_name', 'Frequency', 'Values']

    # Now, most_frequent_df contains the most frequent values from tripdetails_df for each column

    most_frequent_df = most_frequent_df.rename({'Column_name':'Type'},axis=1)
    most_frequent_df= most_frequent_df[['Type','Values','Frequency']]
    
    mostfreq_tree = ttk.Treeview(tree_frame, columns=("Type", "Values", "Frequency"), displaycolumns=("Type", "Values", "Frequency"))
    mostfreq_tree.heading("#1", text="Type")
    mostfreq_tree.heading("#2", text="Values")
    mostfreq_tree.heading("#3", text="Frequency")

    mostfreq_tree.column("#0", width=0)
    mostfreq_tree.column("#1", width=150, anchor="center")
    mostfreq_tree.column("#2", width=150, anchor="center")
    mostfreq_tree.column("#3", width=150, anchor="center")
    mostfreq_tree.grid(row=4,column=0,padx=10,pady=5)
    # Insert data into Treeview
    for index, row in most_frequent_df.iterrows():
        mostfreq_tree.insert("", "end", values=(row["Type"], row["Values"], row["Frequency"]))
    


# Function to plot Trip Duration Distribution
def plot_trip_duration_distribution():
    plt.figure(figsize=(12, 6))
    sns.histplot(tripdetails_df['trip_duration'], bins=30, kde=True)
    plt.title('Trip Duration Distribution')
    plt.xlabel('Trip Duration (minutes)')
    plt.ylabel('Count')
    plt.show()

# Function to plot Trip Fare Distribution
def plot_trip_fare_distribution():
    plt.figure(figsize=(12, 6))
    sns.histplot(tripdetails_df['trip_fare'], bins=30, kde=True)
    plt.title('Trip Fare Distribution')
    plt.xlabel('Trip Fare')
    plt.ylabel('Count')
    plt.show()

# Function to plot Vehicle Status Count
def plot_vehicle_status_count():
    plt.figure(figsize=(6, 6))
    sns.countplot(x='vehicle_status', data=vehicledetails_df)
    plt.title('Vehicle Status')
    plt.xlabel('Status (0: Available, 1: In Use)')
    plt.ylabel('Count')
    plt.show()

# Function to plot User Type Distribution
def plot_user_type_distribution():
    plt.figure(figsize=(6, 6))
    sns.countplot(x='usertype', data=logindetails_df)
    plt.title('User Type Distribution')
    plt.xlabel('User Type')
    plt.ylabel('Count')
    plt.show()

# Function to plot User Wallet Balance Distribution
def plot_wallet_balance_distribution():
    plt.figure(figsize=(12, 6))
    sns.histplot(walletdetails_df['balance'], bins=30, kde=True)
    plt.title('User Wallet Balance Distribution')
    plt.xlabel('Wallet Balance')
    plt.ylabel('Count')
    plt.show()


# Function to update the visualization based on the selected option
def update_visualization():
    selected_option = dropdown_var.get()
    if selected_option == "Trip Duration Distribution":
        plot_trip_duration_distribution()
    elif selected_option == "Trip Fare Distribution":
        plot_trip_fare_distribution()
    elif selected_option == "Vehicle Status Count":
        plot_vehicle_status_count()
    elif selected_option == "User Type Distribution":
        plot_user_type_distribution()
    elif selected_option == "User Wallet Balance Distribution":
        plot_wallet_balance_distribution()
    elif selected_option == "Average and Max Metrics":
        table_stats()
    elif selected_option == "Most Occuring Items":
        table_mostfreq()


# Create a tkinter window
root = tk.Tk()
root.title("Visualization Selector")

# Dropdown menu options
options = ["Trip Duration Distribution", "Trip Fare Distribution", "Vehicle Status Count",
           "User Type Distribution", "User Wallet Balance Distribution","Average and Maximum Metrics",
           "Most Occuring Items"]

# Create a dropdown menu
dropdown_var = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=dropdown_var, values=options)
dropdown.set("Select Visualization")
dropdown.pack(pady=20)

#add frame for treeview
tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

# Button to update visualization
update_button = tk.Button(root, text="View Visualization", command=update_visualization)
update_button.pack(pady=10)

# Function to exit the application
def close_window():
    root.destroy()

# Exit button
exit_button = tk.Button(root, text="Exit", command=close_window)
exit_button.pack(pady=10)

# Run the tkinter main loop
root.mainloop()