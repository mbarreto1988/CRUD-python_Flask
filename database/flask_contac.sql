create flaskContact;

use flaskContact;

create table contact(
id int auto_increment not null,
nombre varchar(50),
apellido varchar(50),
email nvarchar(50),
telefono int,
primary key(id)
);