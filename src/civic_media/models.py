from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EditorialClass(str, Enum):
    news = "news"
    analysis = "analysis"
    opinion = "opinion"
    advocacy = "advocacy"
    sponsored = "sponsored"


class EvidenceReference(StrictModel):
    packet_id: str = Field(min_length=1)
    revision: int = Field(ge=1)
    schema_version: str = "evidence_packet.v1"


class EditorialBrief(StrictModel):
    id: str = Field(min_length=1)
    outlet_id: str = Field(min_length=1)
    headline: str = Field(min_length=1)
    editorial_class: EditorialClass
    evidence: list[EvidenceReference] = Field(default_factory=list)
    synthetic_host_ids: list[str] = Field(default_factory=list)
    disclosures: list[str] = Field(default_factory=list)
    status: str = "draft"

    @model_validator(mode="after")
    def editorial_gate(self):
        if self.status != "draft":
            raise ValueError("Intake only accepts draft briefs; publication requires a separate approval workflow")
        if self.editorial_class in (EditorialClass.news, EditorialClass.analysis) and not self.evidence:
            raise ValueError("News and analysis require evidence packet references")
        if self.editorial_class in (EditorialClass.advocacy, EditorialClass.sponsored) and not self.disclosures:
            raise ValueError("Advocacy and sponsored content require disclosures")
        if any(e.schema_version != "evidence_packet.v1" for e in self.evidence):
            raise ValueError("Unsupported evidence contract")
        return self


class PublicationEvent(StrictModel):
    schema_version: str = "publication_event.v1"
    id: str
    outlet_id: str
    editorial_class: EditorialClass
    evidence_packet_ids: list[str]
    host_ids: list[str]
    published_at: datetime
    canonical_url: HttpUrl
    disclosures: list[str]
    revision: int = Field(ge=1)
    correction_of: str | None = None
