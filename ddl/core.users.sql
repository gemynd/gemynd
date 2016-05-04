drop table if exists core.users;
create table core.users (
    id    serial primary key,
    name  varchar,
    added timestamp default current_timestamp
);

create index users_index on core.users using btree(name);