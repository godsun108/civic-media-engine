# Official source connectors

Run `FEC_API_KEY=... python ballot_atlas/adapters/fec.py` to fetch Florida federal candidate filing records into `incoming.json`, then `python ballot_atlas/engine.py` to reconcile.

FEC filing **does not establish ballot qualification**, and the candidate list is not a complete personal ballot. The adapter is intentionally bounded to ten pages by default; inspect pagination before claiming comprehensive coverage. `source_updated_at` is collection time, not a filing date.

Congress.gov API is a separate legislative-record source requiring its own API key; votes, sponsorship and statements must not be treated as interchangeable evidence. Florida state/county candidate connectors and district-specific ballot matching remain pending. Do not publish inferred policy positions.
