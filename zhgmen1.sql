create database zhgmen;
use zhgmen;
create table authors
	(
		id int(4) not null PRIMARY KEY auto_increment,
		name varchar(10) not null,
		region varchar(20) not null default 'chinese',
		description varchar(2000)		
		);
create table books
	(
		id int(4) not null PRIMARY KEY auto_increment,
		name varchar(20) not null,
		author varchar(20) not null,
		link varchar(50) not null,
		description varchar(2000)
		);
create table short
	(
		id int(4) not null PRIMARY KEY auto_increment,
		name varchar(20) not null,
		author varchar(20) not null,
		content LONGTEXT not null,
		);