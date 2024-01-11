# Language-Tutoring-Chatbot
In this project, we’re interested in building a demo of a social bot intended to help language learners practice their grammar and conversational skills. We will be focusing on the English-French language pair specifically for this demo.

We intend to produce an agent that is useful to second-language learners of French (with fluency in English). The goal of this tool is to help language learners with immersion, ie. conversing only in French. When the user makes mistakes, the agent will suggest corrections for those mistakes before proceeding with the conversation.

See the **Chatbot_Project_Report.pdf** file in this repo for the complete write-up of this project -- including motivation, design, experimentation, and results.

## Grammar Error Correction

We use a grammar error correction (GEC) model to integrate into the RASA framework. To do so, we finetune a pre-trained LM model, in our case, the mT5[1], on the Multilingual GEC dataset[2]. 

We were further interested in comparing the performance of mT5 finetuned for GEC against GPT-3.5 zero-shot evaluated on this task. We use the gpt-3.5-turbo model from OpenAI in conjunction with the LangChain API to zero-shot and few-shot prompt GPT. After analyzing the performance of both approaches, we found that the finetuned mT5 model slightly outperformed the prompted GPT model, even when using few-shot prompting. However, error analysis revealed that while mT5 outperforms based on the Multilingual GEC dataset, it is a much weaker language model than GPT-3.5 and fails to capture the broader semantic context of a sentence, producing confusing outputs for difficult inputs as a result. With this in mind, we use few-shot prompting on GPT-3.5 in the backend of our RASA chatbot. 

## Citations

[1] mT5. (n.d.). https://github.com/google-research/multilingual-t5 \
[2] Multilingual GEC Dataset. (n.d.). https://huggingface.co/datasets/juancavallotti/multilingual-gec.
