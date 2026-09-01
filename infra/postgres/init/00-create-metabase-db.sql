-- Multi-database provisioning for Metabase BI isolation
SELECT 'CREATE DATABASE metabase'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'metabase')\gexec

GRANT ALL PRIVILEGES ON DATABASE metabase TO passporttwin;
