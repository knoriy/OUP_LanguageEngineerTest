from typing import Dict, Optional
from pydantic import BaseModel, Field, constr, field_validator
from collections import defaultdict
import json

class Token(BaseModel):
    text: str
    lemma: constr(strip_whitespace=True) 
    pos: str
    feats: Optional[str]

    @field_validator('pos')
    def validate_pos(cls, value):
        valid_pos_tags = {'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X'}
        if value not in valid_pos_tags:
            raise ValueError('pos must be a valid part of speech')
        return value
    
    @field_validator('lemma', 'text')
    def must_not_be_empty(cls, value, field):
        if not value:
            raise ValueError(f"{field.field_name} cannot be empty")
        return value

class Lemma(BaseModel):
    lemma: str
    pos: str
    feats: Optional[str]  # Optional because feats can be None
    count: int = 1
    word_forms: Dict[str, int] = Field(default_factory=lambda: defaultdict(int))

    def add_occurrence(self, form: str):
        self.count += 1
        self.word_forms[form] += 1


def load_corpus_data(corpus_path: str):
    with open(corpus_path, encoding='utf-8') as f:
        corpus_data = json.load(f)
    return corpus_data

def get_lemmas(corpus_data: Dict):
    lemmas_dict: Dict[str, Lemma] = defaultdict(lambda: None)
    for sentence in corpus_data["sentences"]:
        for token_data in sentence['tokens']:
            token = Token(**token_data)
            if lemmas_dict[token.lemma]:
                lemmas_dict[token.lemma].add_occurrence(token.text)
            else:
                lemma = Lemma(lemma=token.lemma, pos=token.pos, feats=token.feats)
                lemma.word_forms[token.text] += 1
                lemmas_dict[token.lemma] = lemma

    return lemmas_dict


def main():
    corpus_data = load_corpus_data('sample_parsed_sentences.json')
    lemmas_dict = get_lemmas(corpus_data)

    output_data = [lemma.model_dump() for lemma in lemmas_dict.values()]

    # # dump to file
    # with open('sample_lemmas.json', 'w', encoding='utf-8') as f:
    #     json.dump(output_data, f, ensure_ascii=False, indent=2)

    json_output = json.dumps(output_data, ensure_ascii=False, indent=2)
    print(json_output)

if __name__ == '__main__':
    main()