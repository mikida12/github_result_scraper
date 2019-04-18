CREATE DATABASE results;
use results;

CREATE TABLE github_search_results (
  id INT AUTO_INCREMENT,
  title VARCHAR(100),
  link VARCHAR(100),
  description VARCHAR(500),
  tags VARCHAR(200),
  datetime VARCHAR(20),
  language VARCHAR(50),
  stars VARCHAR(50),
  PRIMARY KEY (id)
);
