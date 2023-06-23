from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import openai
import re
openai.organization = "org-HY9eNlQ5xSMYsQ0QzZkx4iKO"
API_KEY= "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"
openai.api_key = API_KEY
Google_API_KEY ="AIzaSyBkfIa12KckrxJJhor6iMi0FY9-C8UlJOQ"    

def CreateQuiz(Content_text):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": Content_text}
      ]
    )

    text = completion.choices[0].message.content
    quest = re.compile(r'^\d+(?:\)|\.|\-)(.+\?$)')
    opt = re.compile(r'^[a-zA-Z](?:\)|\.|\-)(.+$)')
    ans= re.compile(r'Answer:\s[a-zA-Z](?:\)|\.|\-)(.+$)')
    questions = []
    options=[]
    sub =[]
    answers =[]
    for line in text.splitlines():
        if line == '':
            if sub:
                options.append(sub)
                sub=[]
        else:
            if quest.match(line):
                line_mod = line.strip()
                questions.append(line_mod)
            if opt.match(line):
                line_mod = line.strip()
                sub.append(line_mod)
            if ans.match(line):
                line_mod= line.strip()
                answers.append(line_mod)
    if sub:
        options.append(sub)
       
    print(len(questions))
    print(len(options))
    print(len(answers))



    #Create Quiz Form
    
    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": "Quiz form",
        }
    }
    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()
    # Request body to add a multiple-choice question
    # JSON to convert the form into a quiz
    update = {
        "requests": [
            {
                "updateSettings": {
                    "settings": {
                        "quizSettings": {
                            "isQuiz": True
                        }
                    },
                    "updateMask": "quizSettings.isQuiz"
                }
            }
        ]
    }
    # Converts the form into a quiz
    question_setting = form_service.forms().batchUpdate(formId=result["formId"],body=update).execute()
    for i in range(len(questions)): 
        NEW_QUESTION = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": questions[i],
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value":j} for j in options[i]],
                                    "shuffle": True
                                }
                            }
                        },
                    },
                    "location": {
                        "index": i
                    }
                }
            }]
        }
        question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

    get_result = form_service.forms().get(formId=result["formId"]).execute()
    return get_result['responderUri']