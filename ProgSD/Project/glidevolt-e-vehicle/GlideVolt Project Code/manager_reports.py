import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud

pathdb = str(os.path.dirname(os.path.abspath(__file__)))
db_path = pathdb+"/register.db"

# Function to establish a database connection and fetch data into Pandas DataFrames
def fetch_data_from_db(st=None,dt=None):
    connection = sqlite3.connect(db_path)
    logindetails_df = pd.read_sql_query("SELECT * FROM logindetails", connection)
    if st ==None and dt ==None:
        tripdetails_df = pd.read_sql_query("SELECT * FROM tripdetails", connection)
    else:
        query = '''SELECT * FROM tripdetails where date(trip_start_time)>= "'''+str(st)+'''" and date(trip_end_time)<= "'''+str(dt)+'''" '''
        # print(query)
        tripdetails_df = pd.read_sql_query(query, connection)
    vehicledetails_df = pd.read_sql_query("SELECT * FROM vehicledetails", connection)
    walletdetails_df = pd.read_sql_query("SELECT * FROM walletdetails", connection)
    feedback_df = pd.read_sql_query("SELECT * FROM feedback", connection)
    connection.close()
    return logindetails_df, tripdetails_df, vehicledetails_df, walletdetails_df,feedback_df




# Function to plot Trip Duration Distribution
def plot_trip_duration_distribution(tripdetails_df):
    plt.figure(figsize=(12, 6), num="Trip Duration Distribution")
    sns.histplot(tripdetails_df['trip_duration'], bins=30, kde=True)
    plt.title('Trip Duration Distribution')
    plt.xlabel('Trip Duration (minutes)')
    plt.ylabel('Count')
    plt.show()

# Function to plot Trip Fare Distribution
def plot_trip_fare_distribution(tripdetails_df):
    plt.figure(figsize=(12, 6),num="Trip Fare Distribution")
    sns.histplot(tripdetails_df['trip_fare'], bins=30, kde=True)
    plt.title('Trip Fare Distribution')
    plt.xlabel('Trip Fare')
    plt.ylabel('Count')
    plt.show()

def app_rating_distribution(feedback_df):
    plt.figure(figsize=(6, 6),num="App Ratings")
    ax = sns.countplot(x='app_rating', data=feedback_df)
    ax.bar_label(ax.containers[0])
    plt.title('App Ratings')
    plt.xlabel('Ratings (5:Highest, 1:Lowest)')
    plt.ylabel('Count')
    plt.show()

# Function to plot User Wallet Balance Distribution
def plot_wallet_balance_distribution(walletdetails_df):
    plt.figure(figsize=(12, 6),num="User Wallet Balance Distribution")
    sns.histplot(walletdetails_df['balance'], bins=30, kde=True)
    plt.title('User Wallet Balance Distribution')
    plt.xlabel('Wallet Balance')
    plt.ylabel('Count')
    plt.show()

def ride_issues_word_cloud(feedback_df):
    # Combine the lists of words into a single string
    text = ','.join(feedback_df['ride_issues'].dropna())
    text = text.replace("'","")
    text = text.replace("problem","")

 
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
 
    # Plot the word cloud using Seaborn
    plt.figure(figsize=(10, 5),num="Most Common Problems")
    plt.title('Most Common Problems')
    sns.set()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def referral_word_cloud(feedback_df):
    # Combine the lists of words into a single string
    text = ','.join(feedback_df['how_found'].dropna()).replace("'","")
 
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
 
    # Plot the word cloud using Seaborn
    plt.figure(figsize=(10, 5),num="Most Common Referrals")
    plt.title('Most Common Referrals')
    sns.set()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def ride_rating_distribution(feedback_df):
    plt.figure(figsize=(6, 6),num="Ride Ratings")
    ax = sns.countplot(x='ride_rating', data=feedback_df)
    ax.bar_label(ax.containers[0])
    plt.title('Ride Ratings')
    plt.xlabel('Ratings (5:Highest, 1:Lowest)')
    plt.ylabel('Count')
    plt.show()


def plot_user_type_distribution(logindetails_df):
    plt.figure(figsize=(6, 6),num="User Type Distribution")
    ax = sns.countplot(x='usertype', data=logindetails_df)
    ax.bar_label(ax.containers[0])
    plt.title('User Type Distribution')
    plt.xlabel('User Type')
    plt.ylabel('Count')
    plt.show()


def table_stats(tripdetails_df):
    mean_df = pd.DataFrame(tripdetails_df[['trip_duration','trip_fare']].mean().reset_index())
    mean_df.columns = ['Type','Mean']
    max_df = pd.DataFrame(tripdetails_df[['trip_duration','trip_fare']].max().reset_index())
    max_df.columns = ['Type','max']
    stat_df = mean_df.merge(max_df,how='left',on='Type')
    fig, ax = plt.subplots(figsize=(5,5))

    ax.axis('off')  # Turn off axis for table-like appearance
    table_data = []

    for row in stat_df.itertuples(index=True):

        row_data = [row.Index,row.Type,row.Mean, row.max]

        table_data.append(row_data)
 
    num_columns = len(stat_df.columns) + 1  # Add 1 for the index column
 
    table = ax.table(cellText=table_data, colLabels=[''] + list(stat_df.columns), 

                     cellLoc='center', loc='center', colColours=['lightblue'] * num_columns, 

                     bbox=[0, 0, 1, 1])

    table.auto_set_font_size(False)

    table.set_fontsize(10)

    table.auto_set_column_width(col=list(range(num_columns)))  # Adjust column widths

    plt.title('Trip Duration and Fare Statistics')
    plt.tight_layout()  # Ensure tight layout to remove extra whitespace
    plt.show()


def table_mostfreq(tripdetails_df):    
    
    column_frequencies = {}
 
    for column in ['vehicle_no','start_location','end_location','user_id']:
        value_counts = tripdetails_df[column].value_counts()
        max_frequency = value_counts.max()
        frequent_values = value_counts[value_counts == max_frequency].index.tolist()
        column_frequencies[column] =   {
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
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(5,5))
    ax.axis('off')  # Turn off axis for table-like appearance
    
    # Create a table-like visualization with custom colors and styles
    table_data = []
    for row in most_frequent_df.itertuples(index=True):
        row_data = [row.Index,row.Type,row.Values, row.Frequency]
        table_data.append(row_data)
 
    # Plot the table with adjusted bbox to remove extra whitespace
    num_columns = len(most_frequent_df.columns) + 1  # Add 1 for the index column
    table = ax.table(cellText=table_data, colLabels=[''] + list(most_frequent_df.columns), 
                     cellLoc='center', loc='center', colColours=['lightblue'] * num_columns, 
                     bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(num_columns)))  # Adjust column widths
    plt.title('Most Frequent Values')
 
    plt.tight_layout()  # Ensure tight layout to remove extra whitespace
    plt.show()

def plot_repair_status(vehicledetails_df):
    plt.figure(figsize=(6, 6),num="Repair Status")

    ax = sns.countplot(x='repair_needed', data=vehicledetails_df)

    ax.bar_label(ax.containers[0])

    plt.title('Repair Status')
    plt.xlabel('Status (Y: Repair Needed, N: No Repair Needed)')
    plt.ylabel('Count')
    plt.show()

def plot_charge_status(vehicledetails_df):

    plt.figure(figsize=(6, 6),num="Charge Status")
    ax = sns.countplot(x='charge_status', data=vehicledetails_df)
    ax.bar_label(ax.containers[0])
    plt.title('Charge Status')
    plt.xlabel('Status (Y: Battery Full, N: Battery Not Full)')
    plt.ylabel('Count')
    plt.show()