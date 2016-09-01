create table monitor_info
(
    monitor_key varchar(200) primary key not null,
    monitor_name varchar(200) default '' not null,
    monitor_type varchar(100) default '',
    monitor_type_name varchar(100) default '',
    system_name varchar(200) default '',
    asset_id varchar(40) not null,
    server_name varchar(200) default '',
    ip_address varchar(100) default ''
);

create table monitor_realtime_log
(
    create_time bigint(20) not null,
    monitor_key varchar(100) not null,
    monitor_type varchar(100) default '' not null,
    success varchar(10) default '' not null,
    xml longblob not null
);
create index monitor_realtime_log_create_time_index on monitor_realtime_log (create_time);

create table cpu_log
(
    create_time bigint(20) default '0' not null,
    monitor_key varchar(200) default '' not null,
    cpu_usage decimal(5,2) default '0.00'
);

create table memory_log
(
    create_time bigint(20) default '0' not null,
    monitor_key varchar(100) default '' not null,
    total_phys decimal(20,2) default '0.00',
    avail_phys decimal(20,2) default '0.00',
    used_phys decimal(20,2) default '0.00',
    total_page_file decimal(20,2) default '0.00',
    avail_page_file decimal(20,2) default '0.00',
    used_page_file decimal(20,2) default '0.00',
    memory_used_rate decimal(10,2) default '0.00',
    memory_load decimal(20,2) default '0.00',
    page_file_used_rate decimal(10,2) default '0.00'
);

create table storage_log
(
    create_time bigint(20) default '0' not null,
    monitor_key varchar(100) default '' not null,
    drive varchar(50) default '',
    total_bytes bigint(30) default '0',
    total_free_bytes bigint(30) default '0',
    free_bytes_available bigint(30) default '0',
    drive_type varchar(50) default '',
    hit_info varchar(50) default '',
    used_rate decimal(10,2) default '0.00'
);