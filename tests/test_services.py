import pytest
from app.matcher import FuzzyMatcher
from app.services import MatchingService, FileProcessingService
from app.config import CANONICAL_ENTITIES, REQUIRED_CSV_COLUMN, REQUIRED_JSON_FIELD, ERROR_UNSUPPORTED_FILE_TYPE
from fastapi import UploadFile
import io
import pandas as pd
import json

ENTITIES = CANONICAL_ENTITIES

def test_match_single_entity_success():
    matcher = FuzzyMatcher(ENTITIES)
    service = MatchingService(matcher)
    result = service.match_single_entity("Buro AG")
    assert result["top_match"]["entity"] == "Büro AG"
    assert result["top_match"]["confidence"] > 0.8

def test_match_single_entity_empty():
    matcher = FuzzyMatcher(ENTITIES)
    service = MatchingService(matcher)
    with pytest.raises(ValueError):
        service.match_single_entity("")

def test_match_batch_entities_success():
    matcher = FuzzyMatcher(ENTITIES)
    service = MatchingService(matcher)
    names = ["Buro AG", "Buro Offices Berlin GmbH & Co. KG"]
    results = service.match_batch_entities(names)
    assert len(results) == 2
    assert results[0]["match"] is not None
    assert results[1]["match"] is not None

def test_match_batch_entities_empty():
    matcher = FuzzyMatcher(ENTITIES)
    service = MatchingService(matcher)
    with pytest.raises(ValueError):
        service.match_batch_entities([])

def make_upload_file(filename, content):
    return UploadFile(filename=filename, file=io.BytesIO(content))

def test_validate_file_type():
    assert FileProcessingService.validate_file_type("test.csv")
    assert FileProcessingService.validate_file_type("test.json")
    assert not FileProcessingService.validate_file_type("test.txt")

def test_extract_names_from_csv():
    df = pd.DataFrame({REQUIRED_CSV_COLUMN: ["Buro AG", "Buro GmbH"]})
    content = df.to_csv(index=False).encode()
    file = make_upload_file("test.csv", content)
    names = FileProcessingService.extract_names_from_file(file)
    assert names == ["Buro AG", "Buro GmbH"]

def test_extract_names_from_json():
    df = pd.DataFrame({REQUIRED_JSON_FIELD: ["Buro AG", "Buro GmbH"]})
    content = df.to_json().encode()
    file = make_upload_file("test.json", content)
    names = FileProcessingService.extract_names_from_file(file)
    assert names == ["Buro AG", "Buro GmbH"]

def test_extract_names_from_file_invalid_type():
    file = make_upload_file("test.txt", b"irrelevant")
    with pytest.raises(Exception):
        FileProcessingService.extract_names_from_file(file) 