drop table if exists core.sources;
create table core.sources (
    id     bigint  primary key,
    source varchar
);

insert into core.sources (id, source) values (1, 'telegram');