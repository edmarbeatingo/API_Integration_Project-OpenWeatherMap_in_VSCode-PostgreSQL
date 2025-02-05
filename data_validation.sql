SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 5;
SELECT version();
SELECT datname FROM pg_database WHERE datname = 'weather_analysis';
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'weather_data';
SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 5;
