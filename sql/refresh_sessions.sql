DELETE FROM T_SESSION
WHERE TIME_STAMP < now() - interval '1 minutes';
