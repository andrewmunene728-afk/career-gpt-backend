DROP TABLE IF EXISTS careers;

CREATE TABLE careers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  description TEXT,
  required_grade TEXT,
  field TEXT
);

INSERT INTO careers (title, description, required_grade, field)
VALUES
('Software Engineer', 'Builds and maintains software systems.', 'B', 'Technology'),
('Doctor', 'Treats patients and promotes health.', 'A', 'Health'),
('Teacher', 'Educates students in schools.', 'C', 'Education'),
('Nurse', 'Provides patient care in hospitals.', 'B', 'Health'),
('Civil Engineer', 'Designs and oversees construction projects.', 'B', 'Engineering');
