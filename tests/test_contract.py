import pytest
from pydantic import ValidationError
from civic_media.models import EditorialBrief

BASE = dict(id="brief-1", outlet_id="science", headline="A documented event",
            editorial_class="news",
            evidence=[dict(packet_id="packet-1", revision=1)])

def test_news_requires_evidence():
    assert EditorialBrief(**BASE).status == "draft"
    with pytest.raises(ValidationError):
        EditorialBrief(**{**BASE, "evidence": []})

def test_sponsored_requires_disclosure():
    with pytest.raises(ValidationError):
        EditorialBrief(**{**BASE, "editorial_class": "sponsored", "disclosures": []})

def test_cannot_publish_through_intake():
    with pytest.raises(ValidationError):
        EditorialBrief(**{**BASE, "status": "published"})
