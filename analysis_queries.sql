CREATE TABLE job_acceptance (
    age_years INT,
    gender VARCHAR(10),
    degree_specialization VARCHAR(50),
    technical_score FLOAT,
    aptitude_score FLOAT,
    communication_score FLOAT,
    status INT
);
SELECT status, COUNT(*) AS total_candidates
FROM job_acceptance
GROUP BY status;
SELECT status,
       AVG(technical_score) AS avg_technical,
       AVG(aptitude_score) AS avg_aptitude,
       AVG(communication_score) AS avg_communication
FROM job_acceptance
GROUP BY status;
SELECT 
    (SUM(status) * 100.0 / COUNT(*)) AS placement_rate
FROM job_acceptance;
