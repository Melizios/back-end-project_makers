INSERT INTO public.order
                    (schedule_id, user_id, seat, available_seat, tanggal)
                    VALUES (1, 9, 3,(select c.capacity
                                    from cars as c
                                    inner join schedule as s
                                    on c.car_id=s.car_id
                                    where s.schedule_id=1)-3,'2021-11-30');

INSERT INTO public.orders(
	schedule_id, user_id, seat, available_seat, tanggal)
	VALUES (1, 9, 2,(select available_seat from public.orders where tanggal='2021-11-30' and schedule_id=1 order by available_seat desc limit 1)-4,'2021-11-30');
	
INSERT INTO public.order(
	schedule_id, user_id, seat, available_seat, tanggal)
	VALUES (1, 9, 2,(select available_seat from public.order where tanggal='2021-12-01' and schedule_id=1 order by available_seat limit 1)-4,'2021-12-01');
