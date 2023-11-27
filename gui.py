# Importing required libraries
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from langdetect import detect
from googletrans import Translator

import requests
from bs4 import BeautifulSoup
from selenium import webdriver 
import time
from selenium.webdriver.chrome.service import Service
import json
from datetime import datetime

# Function to generate a pie chart
def generate_chart(data):
    # Processing the data for the graph
    languages = []
    counts = []

    for line in data:
        parts = line.strip().split(': ')
        language = parts[0]
        count = int(parts[1].split()[0])
        languages.append(language)
        counts.append(count)

    # Creating the data dictionary and obtaining the most used language
    data_dict = {languages[i]: counts[i] for i in range(len(languages))}
    most_used_language = max(data_dict, key=data_dict.get)
    max_count = data_dict[most_used_language]
    # Creation of the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=languages, autopct='%1.1f%%', startangle=140)
    plt.title('Programming Languages Used by the Candidate')
    # Show the most used language in the center of the graph
    plt.text(0, 0, f'{most_used_language}\n{max_count} projects', ha='center', va='center', fontsize=12, color='white')
    plt.axis('equal')
    plt.show()

# Function to move to the next field
def next_field(event):
    # Get the current field and move to the next
    focus = window.focus_get()
    if focus == profile_text:
        linkedin_entry.focus_set()
    elif focus == linkedin_entry:
        github_entry.focus_set()
    elif focus == github_entry:
        twitter_entry.focus_set()
    elif focus == twitter_entry:
        analyze_data() # Start analysis by pressing "Enter"

# Function to save information
def save_information():
    # Get the information entered in the profile and social links
    profile_required = profile_text.get("1.0", tk.END).strip()
    social_media = {
        "LinkedIn": linkedin_entry.get(),
        "GitHub": github_entry.get(),
        "Twitter": twitter_entry.get(),
    }
    # Save the information to a text file
    with open('profile_required.txt', 'w', encoding='utf-8') as file:
        file.write(profile_required)

  #Function to extract information--------------------------------------------------------------------------
def github(link, output_file):
    URL = link
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    
    elements = soup.find_all('span', itemprop='programmingLanguage')
    languages_count = {}
    # Extract text from each found element
    for element in elements:
        language = element.text
        if language in languages_count:
            languages_count[language] += 1
        else:
            languages_count[language] = 1
    
    result = ""
    for language, count in languages_count.items():
        result += f"{language}: {count} times\n"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(result)
def twitter(link, output_file):
    url = link
    print(url)
    service = Service()
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.headless = True 
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    
    time.sleep(8)
    
    html = driver.page_source
    
    soup = BeautifulSoup(html, "html.parser")
    spans = soup.find_all("div", {"data-testid": "tweetText"})
    
    texts = [span.find("span").text for span in spans]
    result = "\n".join(texts)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(result)
def linkedin(link, output_file):
    api_key = 'Lft06RYN092hZtzBITokYA'
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company'
    params = {
        'url': link,
        'resolve_numeric_id': 'true',
        'categories': 'include',
        'funding_data': 'include',
        'extra': 'include',
        'exit_data': 'include',
        'skills': 'include',
        'acquisitions': 'include',
        'use_cache': 'if-present',
    }
    response = requests.get(api_endpoint, params=params, headers=headers)
    formatted_data = json.dumps(response.json(), indent=4)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(formatted_data)

# Function to extract data from social media
def extract_social_media_data():
    
    github_link = github_entry.get()
    github_output_file = 'github_result.txt'
    github(github_link, github_output_file)
    
    linkedin_link = linkedin_entry.get()
    linkedin_output_file = 'linkedin_result.txt'
    #linkedin(linkedin_link, linkedin_output_file)
    
    twitter_link = twitter_entry.get()
    twitter_output_file = 'twitter_result.txt'
    #twitter(twitter_link, twitter_output_file)
    
    messagebox.showinfo("Data Extraction", "Data extracted from social media")
    #----------------------------------------------------------------------------------------------------------
def analyze_data():
    extract_social_media_data()
    save_information()
    
    # Twitter Data Analysis
    with open('twitter_result.txt', 'r', encoding='utf-8') as file:
        messages = file.readlines()

    def translate_to_english(message):
        translator = Translator()
        try:
            translation = translator.translate(message, src=detect(message), dest='en')
            return translation.text
        except:
            return message

    translated_messages = [translate_to_english(message) for message in messages]

    data = pd.DataFrame({'Text': translated_messages})
    data['Sentiment'] = data['Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)

    plt.figure(figsize=(10, 6))
    plt.hist(data['Sentiment'], bins=30, edgecolor='black')
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.show()

    # LinkedIn Data Analysis
    with open('linkedin_result.txt', 'r', encoding='utf-8') as file:
        json_data = file.read()

    data = json.loads(json_data)
    experiences = data.get('experiences', [])

    weights = {
        "Software Engineer Intern": 30,
        "Engineering Intern": 25,
        "Collaborator": 20,
        "Committee": 15,
        "Solutions Developer Engineer": 30
    }

    total_weight = 0
    total_score = 0

    for experience in experiences:
        title = experience.get('title')
        if title in weights:
            weight = weights[title]
            total_weight += weight

            starts_at = experience.get('starts_at', {})
            ends_at = experience.get('ends_at', {})
            
            duration = 0
            if ends_at is None:
                current_date = datetime.now()
                day = current_date.day
                month = current_date.month
                year = current_date.year
                duration = (year - starts_at.get('year', 0)) * 12 + (month - starts_at.get('month', 0))
            else:
                duration = (ends_at.get('year', 0) - starts_at.get('year', 0)) * 12 + (ends_at.get('month', 0) - starts_at.get('month', 0))

            score = min(duration / 12, 1) * weight
            total_score += score

    evaluation = (total_score / total_weight) * 100 if total_weight > 0 else 0

    labels = list(weights.keys())
    scores = [0] * len(labels)

    for experience in experiences:
        title = experience.get('title')
        if title in weights:
            index = labels.index(title)
            scores[index] = weights[title]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, scores, color='skyblue')
    plt.xlabel('Roles')
    plt.ylabel('Weight')
    plt.title('Role Evaluation in Work Experiences')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    print(f"Profile Evaluation: {evaluation:.2f}")

    # GitHub Data Analysis
    with open('github_result.txt', 'r') as file:
        data = file.readlines()

    generate_chart(data)
    messagebox.showinfo("Data Analysis", f"Candidate coincidence: {evaluation:.2f}" )
# Create the main window
window = tk.Tk()
window.title("Candidate Form")

# Create and place elements in the window
profile_label = tk.Label(window, text="Required Profile:")
profile_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

profile_text = tk.Text(window, height=5, width=40)
profile_text.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
profile_text.bind("<Return>", next_field)  # Bind Enter key to change fields

social_label = tk.Label(window, text="Social Media:")
social_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

linkedin_label = tk.Label(window, text="LinkedIn:")
linkedin_label.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
linkedin_entry = tk.Entry(window, width=30)
linkedin_entry.grid(row=2, column=2, padx=10, pady=5)
linkedin_entry.insert(0, "https://www.linkedin.com/in/maiky/")  # Set a default value or placeholder

github_label = tk.Label(window, text="GitHub:")
github_label.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
github_entry = tk.Entry(window, width=30)
github_entry.grid(row=3, column=2, padx=10, pady=5)
github_entry.insert(0, "https://github.com/axlRoman?tab=repositories")  # Set a default value or placeholder

twitter_label = tk.Label(window, text="Twitter:")
twitter_label.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
twitter_entry = tk.Entry(window, width=30)
twitter_entry.grid(row=4, column=2, padx=10, pady=5)
twitter_entry.insert(0, "https://twitter.com/JRon103")  # Set a default value or placeholder

analyze_button = tk.Button(window, text="Analyze Data", command=analyze_data)
analyze_button.grid(row=6, column=2, padx=10, pady=5)

# Start the main GUI loop
window.mainloop()
