# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# GPT3 AS TUTOR MODEL 

import openai

from langchain.chat_models import ChatOpenAI

# initialize the models
gpt3 = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key="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"
)

# import dataset

from datasets import load_dataset
dataset = load_dataset('akufeldt/fr-gec-dataset')

# few shot

examples = []
for i in range(51,54):
  inp = dataset['test']['modified'][i][13:]
  ans = dataset['test']['sentence'][i]
  thing = 'Correct the errors in the following French text without telling me what you did: ' + inp + '\n'+ans
  examples.append(thing)
  
from langchain import PromptTemplate

gecprompt = PromptTemplate(
    input_variables=['sent'],
    template='\n\n'.join(examples)+'Correct the errors in the following French text without telling me what you did: {sent} \n',
)

from langchain.chains import LLMChain
gecchain = LLMChain(llm=gpt3, prompt=gecprompt)


# Continue conversation

gecprompt3 = PromptTemplate(
    input_variables=['sent'],
    template='Continue the conversation in French: {sent} \n',
)

from langchain.chains import LLMChain
gecchain3 = LLMChain(llm=gpt3, prompt=gecprompt3)

class GrammarCorrectionAction(Action):
    def name(self) -> Text:
        return "action_generate_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve user's message
        user_message = tracker.latest_message.get('text')
        
        # Get the generated response from the GPT3 API response
        generated_response = gecchain.run(user_message)

        if user_message in generated_response.lower() or 'no error' in generated_response.lower():
            res = "Good Job! That's correct.\n" + gecchain3.run(user_message)
        else:
            res = 'Say this: ' + generated_response
        # Send the generated response back to the chatbot
        dispatcher.utter_message(text=res)
        
        return [] 
    

# To answer vocab question

gecprompt2 = PromptTemplate(
    input_variables=['sent'],
    template='{sent} \n',
)

from langchain.chains import LLMChain
gecchain2 = LLMChain(llm=gpt3, prompt=gecprompt2)

class VocabQuestionAction(Action):
    def name(self) -> Text:
        return "action_answer_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve user's message
        user_message = tracker.latest_message.get('text')
        
        if 'in french' not in user_message:
            user_message+= 'in french'

        # Get the generated response from the GPT3 API response
        generated_response = gecchain2.run(user_message)

        # Send the generated response back to the chatbot
        dispatcher.utter_message(text=generated_response)
        
        return [] 
    
# class LanguageAction(Action):
#     def name(self) -> Text:
#         return "action_language"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         detected_language = tracker.latest_message['metadata']['language']
#         # Use the detected language for further processing or customization
#         if detected_language == 'fr':
#             dispatcher.utter_message(f"The detected language is: {detected_language}. Is this correct?")
#         return []
