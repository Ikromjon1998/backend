import pytest
from app.preprocessor import normalize_text, standardize_legal_terms

def test_normalize_text():
    assert normalize_text("BÜRO AG") == "buro ag"
    assert normalize_text("G.M.B.H") == "g.m.b.h"
    assert normalize_text("Büro-Offices & Co.") == "buro-offices & co."
    assert normalize_text("  Büro   AG  ") == "buro ag"

def test_legal_terms():
    assert standardize_legal_terms("G.M.B.H") == "gmbh"
    assert standardize_legal_terms("Aktiengesellschaft") == "ag"
    assert standardize_legal_terms("und") == "and"
    assert standardize_legal_terms("Büro Offices GmbH & Co. KG") == "Büro Offices gmbh and Co. KG"
