CREATE TABLE t_session (
    uidpk           integer PRIMARY KEY,
    session_id      integer,
    email           varchar(40),
    time_stamp      timestamp
);