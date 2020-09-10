CREATE DATABASE imdbload;
GO

USE imdbload;
GO

CREATE TABLE aka_name (
    id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    name varchar(255),
    imdb_index varchar(3),
    name_pcode_cf varchar(11),
    name_pcode_nf varchar(11),
    surname_pcode varchar(11),
    md5sum varchar(65)
);
 
CREATE TABLE aka_title (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    title varchar(600),
    imdb_index varchar(4),
    kind_id integer NOT NULL,
    production_year integer,
    phonetic_code varchar(5),
    episode_of_id integer,
    season_nr integer,
    episode_nr integer,
    note varchar(72),
    md5sum varchar(33)
);
 
CREATE TABLE cast_info (
    id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    movie_id integer NOT NULL,
    person_role_id integer,
    note varchar(1000),
    nr_order integer,
    role_id integer NOT NULL
);
 
CREATE TABLE char_name (
    id integer NOT NULL PRIMARY KEY,
    name varchar(500) NOT NULL,
    imdb_index varchar(2),
    imdb_id integer,
    name_pcode_nf varchar(5),
    surname_pcode varchar(5),
    md5sum varchar(33)
);
 
CREATE TABLE comp_cast_type (
    id integer NOT NULL PRIMARY KEY,
    kind varchar(32) NOT NULL
);
 
CREATE TABLE company_name (
    id integer NOT NULL PRIMARY KEY,
    name varchar(255) NOT NULL,
    country_code varchar(6),
    imdb_id integer,
    name_pcode_nf varchar(5),
    name_pcode_sf varchar(5),
    md5sum varchar(33)
);
 
CREATE TABLE company_type (
    id integer NOT NULL PRIMARY KEY,
    kind varchar(32)
);
 
CREATE TABLE complete_cast (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer,
    subject_id integer NOT NULL,
    status_id integer NOT NULL
);
 
CREATE TABLE info_type (
    id integer NOT NULL PRIMARY KEY,
    info varchar(32) NOT NULL
);
 
CREATE TABLE keyword (
    id integer NOT NULL PRIMARY KEY,
    keyword varchar(100) NOT NULL,
    phonetic_code varchar(6)
);
 
CREATE TABLE kind_type (
    id integer NOT NULL PRIMARY KEY,
    kind varchar(15)
);
 
CREATE TABLE link_type (
    id integer NOT NULL PRIMARY KEY,
    link varchar(32) NOT NULL
);
 
CREATE TABLE movie_companies (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    company_id integer NOT NULL,
    company_type_id integer NOT NULL,
    note varchar(255)
);
 
CREATE TABLE movie_info (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info varchar(MAX) NOT NULL,
    note varchar(500)
);
 
CREATE TABLE movie_info_idx (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info varchar(10) NOT NULL,
    note varchar(1)
);
 
CREATE TABLE movie_keyword (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    keyword_id integer NOT NULL
);
 
CREATE TABLE movie_link (
    id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    linked_movie_id integer NOT NULL,
    link_type_id integer NOT NULL
);
 
CREATE TABLE name (
    id integer NOT NULL PRIMARY KEY,
    name varchar(125) NOT NULL,
    imdb_index varchar(9),
    imdb_id integer,
    gender varchar(1),
    name_pcode_cf varchar(5),
    name_pcode_nf varchar(5),
    surname_pcode varchar(5),
    md5sum varchar(33)
);
 
CREATE TABLE person_info (
    id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    info_type_id integer NOT NULL,
    info varchar(MAX) NOT NULL,
    note varchar(500)
);
 
CREATE TABLE role_type (
    id integer NOT NULL PRIMARY KEY,
    role varchar(32) NOT NULL
);
 
CREATE TABLE title (
    id integer NOT NULL PRIMARY KEY,
    title varchar(350) NOT NULL,
    imdb_index varchar(5),
    kind_id integer NOT NULL,
    production_year integer,
    imdb_id integer,
    phonetic_code varchar(5),
    episode_of_id integer,
    season_nr integer,
    episode_nr integer,
    series_years varchar(49),
    md5sum varchar(33)
);
GO


BULK INSERT aka_name FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/aka_name.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT aka_title FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/aka_title.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT cast_info FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/cast_info.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT char_name FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/char_name.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT comp_cast_type FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/comp_cast_type.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT company_name FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/company_name.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT company_type FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/company_type.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT complete_cast FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/complete_cast.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT info_type FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/info_type.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT keyword FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/keyword.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT kind_type FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/kind_type.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT link_type FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/link_type.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT movie_companies FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/movie_companies.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT movie_info FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/movie_info.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT movie_info_idx FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/movie_info_idx.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT movie_keyword FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/movie_keyword.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT movie_link FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/movie_link.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT name FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/name.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT person_info FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/person_info.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT role_type FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/role_type.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)
BULK INSERT title FROM '/home/nghia/Desktop/imdbload_cleaned/preprocessed/title.csv' WITH (FORMAT='CSV', FIELDTERMINATOR='\t', KEEPNULLS)

