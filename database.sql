-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.cars
(
    car_id integer NOT NULL,
    agent character varying(40) NOT NULL,
    capacity integer NOT NULL,
    merk character varying(40) NOT NULL,
    fasilitas character varying(300),
    PRIMARY KEY (car_id)
);

CREATE TABLE IF NOT EXISTS public.orders
(
    schedule_id integer NOT NULL,
    user_id integer NOT NULL,
    tanggal date NOT NULL,
    seat integer NOT NULL,
    available_seat integer NOT NULL,
    PRIMARY KEY (schedule_id, user_id, tanggal)
);

CREATE TABLE IF NOT EXISTS public.schedule
(
    schedule_id integer NOT NULL,
    dari character varying(40) NOT NULL,
    menuju character varying(40) NOT NULL,
    harga money NOT NULL,
    car_id integer NOT NULL,
    days integer[],
    berangkat time without time zone,
    sampai time without time zone,
    PRIMARY KEY (schedule_id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    user_id integer NOT NULL,
    noktp character varying(16) NOT NULL,
    nama character varying(40) NOT NULL,
    jenkel character varying(15) NOT NULL,
    is_admin boolean NOT NULL,
    email character varying(40) NOT NULL,
    password character varying(128) NOT NULL,
    PRIMARY KEY (user_id)
);

ALTER TABLE public.orders
    ADD FOREIGN KEY (schedule_id)
    REFERENCES public.schedule (schedule_id)
    NOT VALID;


ALTER TABLE public.orders
    ADD FOREIGN KEY (user_id)
    REFERENCES public.users (user_id)
    NOT VALID;


ALTER TABLE public.schedule
    ADD FOREIGN KEY (car_id)
    REFERENCES public.cars (car_id)
    NOT VALID;

END;