# Key-free implementation status

- Local registry and source-record change queue committed.
- Bounded OpenFEC adapter committed, awaiting API key and live test.
- Fictional side-by-side issue comparison prototype: open demo.html locally.
- Registry and adapter unit tests are committed, not yet executed in repository CI.
- Never publish demo candidates as actual candidates. Do not present FEC registration as confirmed ballot access.

## Remaining work
1. Run unit tests and fix failures; add CI workflow.
2. Obtain FEC_API_KEY and CONGRESS_API_KEY through official registration, stored in deployment secrets.
3. Build state/county election connectors and district/address matching with official ballot verification.
4. Replace fictional data with verified records and attach evidence per policy claim.
5. Connect approved data to public UI; keep corrections and provenance visible.
