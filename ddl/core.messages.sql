drop table if exists core.messages;
create table core.messages (
    source_id         bigint,
    source_message_id bigint,
    direction         char,
    chat_id           bigint,
    message           varchar,
    added             timestamp default current_timestamp
);