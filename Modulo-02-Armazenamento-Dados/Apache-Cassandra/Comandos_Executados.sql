# Comandos básicos - Cassandra


### Keyspace

CREATE KEYSPACE db_cassandra
WITH
REPLICATION = { 
	'class': 'SimpleStrategy',
	'replication_factor': 1
};


### DESC Keyspace

DESC KEYSPACE db_cassandra;


### USE Keyspace

USE db_cassandra;


### CREATE TABLE

CREATE TABLE posts(
	tag varchar,
	name varchar,
	author varchar,
	description text,
	likes int,
	PRIMARY KEY (tag, name)
);


### DESC TABLE

DESC TABLE posts;


### INSERT | UPDATE | DELETE | SELECT

#### INSERT

INSERT INTO db_cassandra.posts (tag, name, author, description, likes)
VALUES
('apache-cassandra', 'Cassandra post', 'Thomaz', 'post do cassandra', 0);

INSERT INTO db_cassandra.posts (tag, name, author, description, likes)
VALUES
('apache-cassandra', 'Cassandra post1', 'Antonio', 'post do cassandra', 1);

INSERT INTO db_cassandra.posts (tag, name, author, description, likes)
VALUES
('apache-cassandra', 'Cassandra post2', 'Jose', 'post do cassandra', 2);

INSERT INTO db_cassandra.posts (tag, name, author, description, likes)
VALUES
('apache-cassandra', 'Cassandra post3', 'Pietro', 'post do cassandra', 3);

INSERT INTO db_cassandra.posts (tag, name, author, description, likes)
VALUES
('apache-cassandra', 'Cassandra post4', 'Rossito', 'post do cassandra', 6);

INSERT INTO db_cassandra.posts (tag, name, author, description, likes)
VALUES
('apache-cassandra', 'Cassandra post5', 'Caio', 'post do cassandra', 10);


#### SELECT 

SELECT * FROM posts


### INSERT | IF NOT EXISTS

INSERT INTO db_cassandra.posts (tag, name, author, description, likes)
VALUES
('apache-cassandra', 'Cassandra post', 'Thomaz', 'post do cassandra', 0)
IF NOT EXISTS;


### UPDATE

SELECT * 
FROM posts
WHERE tag = 'apache-cassandra' 
  AND name = 'Cassandra post4';

UPDATE posts
SET likes = 2
WHERE tag = 'apache-cassandra'
  AND name = 'Cassandra post4';


### ERROR SELECT 

-- Erro:

SELECT *
FROM posts
WHERE likes = 2;  

InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"

-- Correto:

SELECT *
FROM posts
WHERE likes = 2
ALLOW FILTERING;


### DELETE

-- False: tag/name não existem:

DELETE FROM db_cassandra.posts
WHERE tag = 'teste' 
  AND name = 'teste'
IF EXISTS;  

-- Existe

DELETE FROM db_cassandra.posts
WHERE tag = 'apache-cassandra' 
  AND name = 'Cassandra post5'
IF EXISTS;  

-- IN

DELETE FROM db_cassandra.posts
WHERE tag = 'apache-cassandra'
  AND name IN ('Cassandra post4', 'Cassandra post2');  


### VIEW MATERIALIZED

CREATE MATERIALIZED VIEW posts_por_likes AS
SELECT  tag, name, author, description, likes
FROM posts
WHERE tag IS NOT NULL
  AND name IS NOT NULL
  AND likes IS NOT NULL
PRIMARY KEY (likes, tag, name);  


SELECT * FROM posts_por_likes WHERE likes = 3;


-- DROP

DROP MATERIALIZED VIEW posts_por_likes