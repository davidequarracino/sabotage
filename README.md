# sabotage

Automated OSINT pipeline for ransomware leak tracking. This tool synchronizes public intelligence feeds with a managed PostgreSQL instance, ensuring data persistence and idempotency.

## Architecture
Built with Python 3.10 and executed via GitHub Actions. Data is ingested from the `ransomware.live` API and stored in a Supabase (PostgreSQL) cluster. The pipeline is triggered automatically via cron every 12 hours or manually via workflow dispatch.

## Core Logic
Resilient data fetching is handled through `urllib3` with exponential backoff to manage API rate limits. The system implements in-memory deduplication and utilizes PostgreSQL `ON CONFLICT` logic to perform atomic upserts, preventing duplicate records.

## Setup

### Environment Variables
Configure the following secrets in the GitHub repository:
* `SUPABASE_URL`: Target project API endpoint.
* `SUPABASE_KEY`: Service_role or anon key.

### Database Schema
```sql
CREATE TABLE public.cyber_leaks (
    id bigint primary key generated always as identity,
    company_name text,
    leak_date text,
    threat_group text,
    website_url text unique,
    created_at timestamp with time zone default now()
);
