drop table if exists users;
create table users (
  id integer primary key autoincrement,
  prenom text not null, nom text not null, company text not null, status text not null, picture text not null
);