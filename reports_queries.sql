select s.dari,s.menuju from schedule as s
inner join orders as o
on s.schedule_id=o.schedule_id
group by s.dari,s.menuju
order by count(s.dari) desc limit 5;

select count(extract(isodow from tanggal)),extract(isodow from tanggal) as days from orders
group by extract(isodow from tanggal)
order by count(extract(isodow from tanggal))desc,extract(isodow from tanggal);

select u.nama,count(o.user_id) from users as u
inner join orders as o
on u.user_id=o.user_id
group by o.user_id,u.nama
order by count(o.user_id) desc limit 5;
