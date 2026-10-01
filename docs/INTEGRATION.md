# Integration contracts

## Inbound from Civic Ledger: evidence_packet.v1
Fields: id, title, summary, jurisdiction, source_urls[], retrieved_at, claims[], limitations[], revision.
Evidence is immutable per revision. CME links claims to evidence packet IDs.

## Inbound from VHE: talent_profile.v1
Fields: id, display_name, synthetic_disclosure, allowed_formats[], voice_profile_ref, brand_rules_ref, revision.

## Outbound from CME: publication_event.v1
Fields: id, outlet_id, editorial_class, evidence_packet_ids[], host_ids[], published_at, canonical_url, disclosures[], revision, correction_of.

Adapters must validate schemas, authenticate senders, be idempotent, and log failures. Never automatically publish an inbound record without editorial gates.
