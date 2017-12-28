create table seller
(
	seller_id int auto_increment
		primary key,
	user_id int not null,
	first_name varchar(55) null,
	last_name varchar(55) null,
	email varchar(50) null
)
;

create index user_id
	on seller (user_id)
;

create table toy
(
	toy_id int auto_increment
		primary key,
	seller_id int not null,
	name varchar(55) null,
	list_date datetime null,
	toy_image varchar(55) null,
	constraint toy_ibfk_1
		foreign key (seller_id) references seller (seller_id)
)
;

create index seller_id
	on toy (seller_id)
;

create table user
(
	user_id int auto_increment
		primary key,
	first_name varchar(55) null,
	last_name varchar(55) null,
	email varchar(50) null,
	password varchar(50) null
)
;

alter table seller
	add constraint seller_ibfk_1
		foreign key (user_id) references user (user_id)
;

