import pytest
from app.matcher import FuzzyMatcher

ENTITIES = [
    "Büro AG",
    "Büro Offices Berlin GmbH & Co. KG",
    "Acme Corporation",
    "Test Entity GmbH"
]

def test_match_variants():
    matcher = FuzzyMatcher(ENTITIES)
    result = matcher.match("Buero AG")[0]
    assert result["entity"] == "Büro AG"
    assert result["confidence"] >= 0.85
    result2 = matcher.match("Buro Offices Berlin")[0]
    assert result2["confidence"] >= 0.7

def test_top_n():
    matcher = FuzzyMatcher(ENTITIES)
    results = matcher.match("Buro Offices Berlin", top_n=2)
    assert len(results) == 2
    assert results[0]["confidence"] >= results[1]["confidence"]
