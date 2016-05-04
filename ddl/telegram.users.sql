drop table if exists telegram.users;
create table telegram.users (
    user_id     bigint,
    telegram_id bigint,
    added       timestamp default current_timestamp
);

create index users_index on telegram.users using btree(telegram_id);