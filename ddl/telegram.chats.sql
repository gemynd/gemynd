drop table if exists telegram.chats;
create table telegram.chats (
    chat_id     bigint,
    telegram_id bigint,
    added       timestamp default current_timestamp
);

create index chats_index on telegram.chats using btree(telegram_id);