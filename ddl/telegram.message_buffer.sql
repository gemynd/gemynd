drop table if exists telegram.message_buffer;
create table telegram.message_buffer (
    update_id bigint,
    id        bigint,
    chat_id   bigint,
    user_name varchar,
    message   varchar
);

create index message_buffer_index on telegram.message_buffer using btree(update_id);