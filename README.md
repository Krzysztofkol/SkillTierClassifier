# Skill Tier Classifier

Simple web app to help you classify your skills into relevant skill proficiency tiers.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Adding Skills](#adding-skills)
5. [Using the Application](#using-the-application)
6. [Understanding Tier Classification](#understanding-tier-classification)

## Project Overview

The Skill Tier Classifier is a tool designed to help you assess and categorize your skills based on proficiency levels. It uses a series of questions to determine the appropriate tier (E, D, C, B, A, or S) for each skill you evaluate. This application is perfect for personal development, career planning, or team skill assessment.

Key features:
- Simple web interface for easy skill assessment
- Tier-based classification system (E to S)
- Ability to add custom skills for evaluation

### Project file structure:
```
SkillTierClassifier/
├backend/
│├──app.py
│├──classifier.py
│└──skill_tierlist.csv
├frontend/
│├──index.html
│├──styles.css
│└──app.js
└─ README.md
```

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher:
	- Flask
	- flask_cors
- Node.js and npm (for running the frontend)
- A modern web browser (Chrome, Firefox, Safari, or Edge)

## Installation

Follow these steps to set up the Skill Tier Classifier on your local machine:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/skill-tier-classifier.git
   cd skill-tier-classifier
   ```

2. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd ../frontend
   npm install
   ```

4. Start the backend server:
   ```
   cd ../backend
   python app.py
   ```

5. In a new terminal, start the frontend:
   ```
   cd ../frontend
   npm start
   ```

6. The port is `2139`. Open your web browser and navigate to `http://localhost:2139` to use the application.

## Adding Skills

To add new skills for classification:

1. Open the `backend/skill_tierlist.csv` file in a text editor.
2. Add a new line for each skill you want to classify, using the format:
   ```
   tier|skill
   ```
   For example:
   ```
   |programming
   |public speaking
   |data analysis
   ```
   Leave the tier blank for new skills.

3. Save the file.

4. Restart the backend server for changes to take effect.

## Using the Application

1. Open the application in your web browser.
2. You'll see a skill name and a question related to that skill.
3. Answer the question by clicking either "Yes" or "No".
4. Continue answering questions until the skill is classified or all questions are answered.
5. The application will move on to the next unclassified skill automatically.
6. Repeat the process for all skills in your list.

## Understanding Tier Classification

The Skill Tier Classifier uses the following tier system:

- E: Novice
- D: Basic
- C: Competent
- B: Proficient
- A: Advanced
- S: Mastery

Each tier represents a different level of proficiency, with E being the lowest and S being the highest. The application asks a series of questions to determine the appropriate tier for each skill. The questions become progressively more challenging as you move up the tiers.

## Additional details

Sometimes it might be unobvious how to break skill familiarity levels down into specific tiers. You can use LLMs for guidance. Example prompt:

```GPT-4o
There are 6 skill proficiency tiers: S (Mastery), A (Advanced), B (Proficient), C (Competent), D (Basic), and E (Novice).
SKILL:="___".
Outline skill proficiency levels for SKILL.
```