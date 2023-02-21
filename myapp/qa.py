import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import spacy
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh import qparser
import os

nlp = spacy.load('en_core_web_sm')

tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

def answer_question(question, documents):
    # Preprocess the question
    question = nlp(question.lower())
    question = ' '.join([token.lemma_ for token in question if not token.is_stop])

    # Index the documents
    ix = open_dir(os.path.join(os.getcwd(), 'whoosh_index'))
    parser = QueryParser("content", schema=ix.schema)
    query = parser.parse(question)
    with ix.searcher() as searcher:
        results = searcher.search(query, limit=None)
        texts = [hit.fields()['content'] for hit in results]

    # Generate answers
    answers = []
    for text in texts:
        inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="pt")
        start_positions, end_positions = model(**inputs).values()

        start_index = torch.argmax(start_positions)
        end_index = torch.argmax(end_positions)
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_index:end_index+1]))
        answers.append(answer)

    return answers
