drop table if exists telegram.updates;
create table telegram.updates (
    id          serial,
    update_id   bigint,
    updated     timestamp default current_timestamp
);

create index updates_index on telegram.updates using btree(id);