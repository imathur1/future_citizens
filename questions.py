import pickle
import requests
from bs4 import BeautifulSoup

def get_questions(num):
    questions = []
    unique = set()
    url = 'https://my.uscis.gov/en/prep/test/civics/view'
    while len(unique) < num:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        arr = []
        question = soup.find('span', {'class': 'question-text'})
        if question.text.strip() not in unique:
            unique.add(question.text.strip())
            arr.append(question.text.strip())

            answers = []
            responses = soup.findAll('div', {'class': 'en'})
            correct = soup.findAll('div', {'class': 'answer-icon'})
            for i in range(len(responses)):
                answers.append(responses[i].text.strip())
                if correct[i].text.strip() == "Correct":
                    arr.append(responses[i].text.strip())
            arr.append(answers)

            explanation = soup.find('div', {'class': 'study-materials'}).findChildren("div", recursive=False)
            arr.append(explanation[-1].text.strip())

            questions.append(arr)

        print(len(questions))

    with open('questions', 'wb') as f:
        pickle.dump(questions, f)

# get_questions(95)