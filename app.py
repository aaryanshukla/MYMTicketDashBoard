import subprocess

# Install necessary packages
subprocess.check_call(['pip', 'install', 'requests'])
subprocess.check_call(['pip', 'install', 'matplotlib'])

# Rest of your code
import os
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st
import matplotlib.pyplot as plt
import math


st.set_page_config(layout="wide")

# Set page background color
st.markdown(
    """
    <style>
    body {
        background-color: #F5F5F5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# JIRA API details
jira_url = "https://mattyoungmedia.atlassian.net"
api_username = "aaryan4@illinois.edu"
api_token = os.environ.get('JIRA_API_TOKEN')


def get_all_tickets():
    jql_query = 'project = MOP'
    api_url = f"{jira_url}/rest/api/3/search?jql={jql_query}"
    response = requests.get(api_url, auth=HTTPBasicAuth(api_username, api_token))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_completed_tickets():
    jql_query = 'project = MOP AND status = Done AND resolved >= -7d'
    api_url = f"{jira_url}/rest/api/3/search?jql={jql_query}"
    response = requests.get(api_url, auth=HTTPBasicAuth(api_username, api_token))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_tickets_by_story_points(min_points, max_points=None):
    if max_points is None:
        jql_query = f'project = MOP AND "Story point estimate" >= {min_points}'
    else:
        jql_query = f'project = MOP AND "Story point estimate" >= {min_points} AND "Story point estimate" <= {max_points}'
    
    api_url = f"{jira_url}/rest/api/3/search?jql={jql_query}"
    response = requests.get(api_url, auth=HTTPBasicAuth(api_username, api_token))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# Retrieve all tickets
all_tickets = get_all_tickets()

if all_tickets:
    num_tickets = all_tickets["total"]

completed_tickets = get_completed_tickets()

if completed_tickets:
    num_tickets_completed = completed_tickets["total"]

    frontend_tickets = 0
    backend_tickets = 0
    fullstack_tickets = 0
    other_tickets = 0

    for issue in all_tickets["issues"]:
        labels = issue["fields"]["labels"]
        if "frontend" in labels:
            frontend_tickets += 1
        elif "backend" in labels:
            backend_tickets += 1
        elif "fullstack" in labels:
            fullstack_tickets += 1
        else:
            other_tickets += 1

    frontend_percentage = math.floor((frontend_tickets / num_tickets) * 100)
    backend_percentage = math.floor((backend_tickets / num_tickets) * 100)
    fullstack_percentage = math.floor((fullstack_tickets / num_tickets) * 100)
    other_percentage = math.floor((other_tickets / num_tickets) * 100)

    # Query tickets with different story point estimates
    story_points_2 = get_tickets_by_story_points(2)
    story_points_3 = get_tickets_by_story_points(3)
    story_points_4 = get_tickets_by_story_points(4)
    story_points_5 = get_tickets_by_story_points(5, max_points=8)

    if story_points_2:
        num_tickets_sp2 = story_points_2["total"]
    
    if story_points_3:
        num_tickets_sp3 = story_points_3["total"]
    
    if story_points_4:
        num_tickets_sp4 = story_points_4["total"]
    
    if story_points_5:
        num_tickets_sp5 = story_points_5["total"]

    # Bar graph for ticket types
    ticket_types = ['Frontend', 'Fullstack', 'Backend', 'Other']
    ticket_percentages = [frontend_percentage, fullstack_percentage, backend_percentage, other_percentage]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.subplots_adjust(wspace=0.5)

    colors = ['#FF6F61', '#FFCC5C', '#8B8B8B', '#5D9CEC']  # Set custom colors

    ax1.bar(ticket_types, ticket_percentages, color=colors)
    ax1.set_xlabel('Ticket Types', fontsize=12)
    ax1.set_ylabel('Percentage', fontsize=12)
    ax1.set_title('Ticket Types', fontsize=12, pad=10)
    ax1.grid(True)

    ax1.tick_params(axis='x', labelsize=10)  # Increase the font size of x-axis tick labels
    ax1.tick_params(axis='y', labelsize=10)  # Increase the font size of y-axis tick labels

    # Pie chart for number of tickets vs. tickets completed in the last 7 days
    labels = ['Tickets', 'Completed Last 7 Days']
    sizes = [num_tickets, num_tickets_completed]
    colors = ['#5D9CEC', '#FF6F61']  # Set custom colors
    explode = (0, 0.1)  # explode the second slice (completed tickets)

    ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax2.set_title('Number of Tickets vs. Completed Last 7 Days', fontsize=14, pad=10)

    ax2.legend(fontsize=10)  # Increase the font size of the legend

    # Streamlit app
    st.title("MYM Ticket Dashboard")

    # Set header background color
    st.markdown(
        """
        <style>
        h1 {
            background-color: #FFFFFF;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Set dashboard container background color
    st.markdown(
        """
        <style>
        .dashboard-container {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-gap: 20px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Set insights background color
    st.markdown(
        """
        <style>
        .insights {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            color: #333333;  /* Set text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown(
            '<div class="dashboard-container"><div class="insights"><h3>Tickets Completed Last 7 Days</h3><p>{}</p></div><div class="insights"><h3>Frontend Tickets Percentage</h3><p>{}</p></div><div class="insights"><h3>Backend Tickets Percentage</h3><p>{}</p></div><div class="insights"><h3>Fullstack Tickets Percentage</h3><p>{}</p></div><div class="insights"><h3>Other Tickets Percentage</h3><p>{}</p></div><div class="insights"><h3>Number of tickets with story point estimate greater than 2</h3><p>{}</p></div><div class="insights"><h3>Number of tickets with story point estimate greater than 3</h3><p>{}</p></div><div class="insights"><h3>Number of tickets with story point estimate greater than 4</h3><p>{}</p></div><div class="insights"><h3>Number of tickets with story point estimate greater than 5</h3><p>{}</p></div></div>'.format(
                num_tickets_completed, frontend_percentage, backend_percentage, fullstack_percentage, other_percentage, num_tickets_sp2, num_tickets_sp3, num_tickets_sp4, num_tickets_sp5),
            unsafe_allow_html=True
        )

    # Display the bar graph and pie chart
    st.pyplot(fig)
else:
    st.write("Failed to fetch ticket data.")
