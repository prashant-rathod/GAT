INSERT INTO t_account (uidpk, email, password_hash) VALUES
    (1, 'test@test.com', crypt('test_password', gen_salt('bf', 8)));

