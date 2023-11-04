import os
import pytest
from .oup_le_task import Token, Lemma, load_corpus_data, get_lemmas

def test_token_creation():
    '''
    Test the creation of a Token instance with valid data.
    '''
    token = Token(text='2019', lemma='2019', pos='NUM', feats=None)
    assert token.text == '2019'
    assert token.lemma == '2019'
    assert token.pos == 'NUM'
    assert token.feats is None

def test_token_creation_with_whitespace():
    '''
    Test that leading and trailing whitespace is stripped from lemma.
    '''
    token = Token(text=' run ', lemma=' run ', pos='VERB', feats=None)
    assert token.lemma == 'run'

def test_token_invalid_pos():
    '''
    Test that an invalid pos value raises a ValueError.
    '''
    with pytest.raises(ValueError):
        Token(text='run', lemma='run', pos='INVALID_POS', feats=None)

def test_token_empty_text():
    '''
    Test that an empty text value raises a ValueError.
    '''
    with pytest.raises(ValueError):
        Token(text='', lemma='run', pos='VERB', feats=None)

def test_lemma_add_occurrence():
    '''
    Test the add_occurrence method of Lemma.
    '''
    lemma = Lemma(lemma='run', pos='VERB', feats=None)
    lemma.add_occurrence('ran')
    lemma.add_occurrence('running')
    assert lemma.count == 3
    assert lemma.word_forms == {'ran': 1, 'running': 1}

def test_lemma_add_occurrence_duplidate():
    '''
    Test the add_occurrence method of Lemma.
    '''
    lemma = Lemma(lemma='run', pos='VERB', feats=None)
    lemma.add_occurrence('running')
    lemma.add_occurrence('running')
    assert lemma.count == 3
    assert lemma.word_forms == {'running': 2}

def test_load_corpus_data():
    '''
    Test loading of corpus data from a JSON file.
    '''
    if not os.path.exists('path_to_test_corpus.json'):
        pytest.skip("Test corpus file not found")
    corpus_data = load_corpus_data('sample_parsed_sentences.json')

    assert 'sentences' in corpus_data
    assert isinstance(corpus_data['sentences'], list)

def test_get_lemmas():
    '''
    Test extraction of lemmas from corpus data.
    '''
    corpus_data = {
        "sentences": [
            {
                "tokens": [
                    {"text": "run", "lemma": "run", "pos": "VERB", "feats": "Tense=Past"},
                    {"text": "running", "lemma": "run", "pos": "VERB", "feats": "Tense=PresentParticiple"}
                ]
            }
        ]
    }
    lemmas = get_lemmas(corpus_data)
    assert 'run' in lemmas
    assert lemmas['run'].count == 2
    assert lemmas['run'].word_forms['running'] == 1

