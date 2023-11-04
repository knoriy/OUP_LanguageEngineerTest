from typing import Dict, Optional
from pydantic import BaseModel, Field, constr, field_validator
from collections import defaultdict
import json
import tqdm

class Token(BaseModel):
    '''
    A model representing a token with attributes for text, lemma, part of speech, and features.
    
    Attributes:
        text (str): The actual text of the token.
        lemma (constr): The base or dictionary form of the word, with leading and trailing whitespace stripped.
        pos (str): The part of speech tag, validated against a set of valid universal POS tags.
        feats (Optional[str]): An optional string of morphological features.
    '''
    text: str
    lemma: constr(strip_whitespace=True) 
    pos: str
    feats: Optional[str]

    @field_validator('pos')
    def validate_pos(cls, value):
        '''
        Validates that the part of speech is one of the values from the universal POS tags set: https://www.sketchengine.eu/tagsets/universal-pos-tags/
        
        Raises:
            ValueError: If the part of speech is not in the set of valid POS tags.
        '''
        valid_pos_tags = {'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X'}
        if value not in valid_pos_tags:
            raise ValueError('pos must be a valid part of speech')
        return value
    
    @field_validator('lemma', 'text')
    def must_not_be_empty(cls, value, field):
        """
        Validates that the field is not empty.
        
        Args:
            value (str): The field value to validate.
            field: The model field.
        
        Returns:
            str: The validated field value.
        
        Raises:
            ValueError: If the field value is empty.
        """
        if not value:
            raise ValueError(f"{field.field_name} cannot be empty")
        return value

class Lemma(BaseModel):
    """
    A model representing a lemma with attributes for the base form, part of speech, features, count, and word forms.
    
    Attributes:
        lemma (str): The base or dictionary form of the word.
        pos (str): The part of speech tag.
        feats (Optional[str]): An optional string of morphological features.
        count (int): The frequency count of the lemma in the corpus, initialized to 1.
        word_forms (Dict[str, int]): A mapping of word forms to their respective frequency counts.
    """
    lemma: str
    pos: str
    feats: Optional[str]  # Optional because feats can be None
    count: int = 1
    word_forms: Dict[str, int] = Field(default_factory=lambda: defaultdict(int))

    def add_occurrence(self, form: str):
        """
        Increments the count of the lemma and updates the word form frequency.
        
        Args:
            form (str): The word form to increment in the frequency count.
        """
        self.count += 1
        self.word_forms[form] += 1


def load_corpus_data(corpus_path: str):
    """
    Loads a corpus from a JSON file.
    
    Args:
        corpus_path (str): The file path to the corpus JSON file.
    
    Returns:
        dict: The loaded corpus data.
    """
    with open(corpus_path, encoding='utf-8') as f:
        corpus_data = json.load(f)
    return corpus_data

def get_lemmas(corpus_data: Dict):
    """
    Processes a corpus to construct a dictionary of lemmas.
    
    Args:
        corpus_data (dict): The corpus data with sentences and tokens.
    
    Returns:
        Dict[str, Lemma]: A dictionary mapping lemmas to their respective Lemma model instances.
    """
    lemmas_dict: Dict[str, Lemma] = defaultdict(lambda: None)
    for sentence in tqdm.tqdm(corpus_data["sentences"], desc="Processing sentences"):
        for token_data in sentence['tokens']:
            token = Token(**token_data)
            if lemmas_dict[token.lemma]:
                lemmas_dict[token.lemma].add_occurrence(token.text)
            else:
                lemma = Lemma(lemma=token.lemma, pos=token.pos, feats=token.feats)
                lemma.word_forms[token.text] += 1
                lemmas_dict[token.lemma] = lemma

    return lemmas_dict


def main(args):
    corpus_data = load_corpus_data(args.corpus_path)
    lemmas_dict = get_lemmas(corpus_data)

    output_data = [lemma.model_dump() for lemma in lemmas_dict.values()]

    # dump to file
    with open(args.output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # json_output = json.dumps(output_data, ensure_ascii=False, indent=2)
    # print(json_output)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process a corpus to extract lemmas.')
    parser.add_argument('corpus_path', type=str, help='The file path to the corpus JSON file.')
    parser.add_argument('-o', '--output_path', type=str, default='output.json', help='The file path to the output JSON file.')
    args = parser.parse_args()
    
    main(args)