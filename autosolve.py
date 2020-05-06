from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import json

class Learn:
    def __init__(self):
        self.questionAnswers, self.iterations = self.getTerms()
        
        
    def getTerms(self):
        terms = []
        data = driver.execute_script("return Quizlet.assistantModeData.terms")
        iterations = driver.execute_script("return Quizlet.assistantModeData.terms.length")
        for i in range(0, iterations):
            terms.append({"term": data[i]["word"], "definition": data[i]["definition"]})
                
        return terms, iterations

    def solve(self):
        mode = self.getMode()
        if mode == 'choice':
            buttons = driver.find_elements_by_class_name('MultipleChoiceQuestionPrompt-termOption')
            buttonsText = driver.find_element_by_class_name('MultipleChoiceQuestionPrompt-termOptions').find_elements_by_class_name("FormattedTextWithImage")
            questionText = driver.find_element_by_class_name("MultipleChoiceQuestionPrompt-prompt").find_element_by_class_name("PromptTextWithImage").find_element_by_class_name("FormattedTextWithImage").text
            answer = "ERROR: Answer could not be found over {} searches".format(self.iterations)
            for i in range(0, self.iterations):
                #print(f"{i}:\n  Question Text: {questionText}\n  Term: {questionAnswers[i]['term']}\n  Definition: {questionAnswers[i]['definition']}")
                if questionText == self.questionAnswers[i]['term']:
                    answer = self.questionAnswers[i]['definition']
                elif questionText == self.questionAnswers[i]['definition']:
                    answer = self.questionAnswers[i]['term']
            if answer == buttonsText[0].text:
                buttons[0].click()
            elif answer == buttonsText[1].text:
                buttons[1].click()
            elif answer == buttonsText[2].text:
                buttons[2].click()
            elif answer == buttonsText[3].text:
                buttons[3].click()
            else:
                print(answer)
        elif mode == 'written':
            questionText = driver.find_element_by_class_name("FixedQuestionLayout-content").find_element_by_class_name("PromptTextWithImage").find_element_by_class_name("FormattedTextWithImage").text
            for i in range(0, self.iterations):
                #print(f"{i}:\n  Question Text: {questionText}\n  Term: {questionAnswers[i]['term']}\n  Definition: {questionAnswers[i]['definition']}")
                if questionText == self.questionAnswers[i]['term']:
                    answer = self.questionAnswers[i]['definition']
                elif questionText == self.questionAnswers[i]['definition']:
                    answer = self.questionAnswers[i]['term']
            driver.find_element_by_class_name('AutoExpandTextarea-textarea').send_keys(answer)
            driver.find_element_by_class_name('AutoExpandTextarea-textarea').send_keys(Keys.ENTER)
        elif mode == 'flashcards':
            driver.find_element_by_class_name('FlippableFlashcard').click()
            time.sleep(0.2)
            driver.find_element_by_class_name('FlashcardQuestionView-action').find_element_by_class_name('UIButtonWithKeyboardHint').click()
    def resume(self):
        driver.find_element_by_class_name('FixedContinueButton').click()
        print('On continue screen, resuming...')

    def getMode(self):
        try:
            driver.find_element_by_class_name('MultipleChoiceQuestionPrompt-termOptions')
            return 'choice'
        except:
            try:
                driver.find_element_by_class_name('AutoExpandTextarea-textarea')
                return 'written'
            except:
                try:
                    driver.find_element_by_class_name('FlippableFlashcard') 
                    return 'flashcards'
                except:
                    raise Exception('There was an error determining the mode of the learn question.')
quizletURL = input("Please enter the quizlet URL: ")

if 'quizlet.com' not in quizletURL:
    while 'quizlet.com' not in quizletURL:
        quizletURL = input("Please enter a valid quizlet URL: ")

if 'https://' not in quizletURL:
    quizletURL = 'https://' + quizletURL


service = Service('/chromedriver')
service.start()

driver = webdriver.Remote(service.service_url)
driver.get(quizletURL)
splicedURL = quizletURL.split('/')
mode = ''
modes = ['learn', 'write', 'spell', 'test', 'match', 'gravity']
for m in modes:
    if m in splicedURL[4]:
        mode = splicedURL[4]

time.sleep(1)
driver.find_element_by_xpath('//*[@id="AssistantModeTarget"]/div/div/div/div[2]/div/span[1]/div/div/div[2]/div/button').click()

learn = Learn()
while True:
    time.sleep(0.1)
    try:
        learn.solve()
    except Exception as e:
        #print(e)
        try:
            learn.resume()
        except: 
            pass
    time.sleep(0.8)

