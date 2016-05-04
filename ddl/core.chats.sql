drop table if exists core.chats;
create table core.chats (
    id          serial primary key,
    user_id     bigint,
    added       timestamp default current_timestamp
);