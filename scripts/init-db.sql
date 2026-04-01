-- Initialize PostgreSQL database for DApp Voting System

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create database if not exists (this runs in docker-entrypoint-initdb.d)
-- The database is already created by POSTGRES_DB env var

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE voting_dapp TO voting_user;

-- Set timezone
SET timezone = 'UTC';

-- Create custom types
DO $$ BEGIN
    CREATE TYPE election_state AS ENUM (
        'start',
        'validate_voter',
        'vote',
        'count',
        'declare_winner',
        'done',
        'paused'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE blockchain_mode AS ENUM (
        'permissionless',
        'permissioned'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE voting_type AS ENUM (
        'simple',
        'ranked',
        'quadratic'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM (
        'voter',
        'election_admin',
        'auditor',
        'super_admin'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
END $$;
