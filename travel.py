import base64
from datetime import datetime
from logging import log
from types import SimpleNamespace
from flask import Flask,request,jsonify,Response
from base64 import encode
import flask
import psycopg2
import time

app=Flask(__name__)
# select extract(isodow from date '2021-11-17')
def connect():
    return psycopg2.connect(user="postgres",
                                    password="candra",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="travelApp")

def login():
    try:
        username=request.authorization["username"].lower()
        password=request.authorization["password"]  
        connection=connect()
        cursor=connection.cursor()
        cursor.execute("select password from users where nama=%s or email=%s",(username,username,))
        passdb=cursor.fetchone()
        if base64.b64encode(password.encode("utf-8"))==passdb[0].encode("utf-8"):
            return True
        else:
            return False
    except (Exception, psycopg2.Error) as error:
        return False

def isadmin():
    try:
        username=request.authorization["username"].lower()
        connection=connect()
        cursor=connection.cursor()
        cursor.execute("select is_admin from users where nama=%s or email=%s",(username,username,))
        adminstat=cursor.fetchone()[0]
        return adminstat
    except:
        return False

@app.route('/')
def home():
    return f'Welcome to Trappel'

@app.route('/register',methods=["POST"])
def signup():
    body=request.get_json()
    try:
        name=body["name"].lower()
        ktp=body["ktp"]
        jenkel=body["jenkel"]
        is_admin=body["isadmin"]
        email=body["email"]
        password=body["password"]
        connection=connect()
        cursor=connection.cursor()
        sqlquery="insert into users \
            (nama,noktp,jenkel,is_admin,email,password) \
            values \
            (%s,%s,%s,%s,%s,encode(%s,'base64'))"
        cursor.execute(sqlquery,(name,ktp,jenkel,is_admin,email,password))
        connection.commit()
        return f'akun berhasil dibuat',200
    except (Exception, psycopg2.Error) as error:
        return f'email atau ktp sudah terpakai atau data yang dimasukkan kurang',400
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route('/login')
def signin():
    if login():
        return f'selamat datang {request.authorization["username"].lower()}'
    else:
        return f'Gagal login'

@app.route('/cekadmin')
def adm():
    if isadmin():
        return f'hi admin'
    else:
        return f'ure a pleb'

@app.route('/updateUser',methods=["PUT"])
def upduser():
    if login():
        connection=connect()
        cursor=connection.cursor()
        try:
            username=request.authorization["username"].lower()
            up=request.get_json()
            print(up)
            email=up["email"]
            nama=up["nama"]
            noktp=up["noktp"]
            jenkel=up["jenkel"]
            password=up["password"]
            cursor.execute("UPDATE users\
                            SET nama=%s, email=%s, password=encode(%s,'base64'), noktp=%s,jenkel=%s\
                            WHERE nama=%s or email=%s;",(nama,email,password,noktp,jenkel,username,username,))
            connection.commit()
            return f'User data updated',200
        except:
            return f'Mohon isi semua data, atau email/ktp sudah digunakan',400
    else:
        return f'Mohon login terlebih dahulu',401

@app.route('/addcar',methods=["POST"])
def addcar():
    if login():
        if isadmin():
            connection=connect()
            cursor=connection.cursor()
            try:
                body=request.get_json()
                agent=body["agent"]
                capacity=body["capacity"]
                merk=body["merk"]
                fasilitas=body["fasilitas"]
                sqlquery="insert into cars \
                    (agent,capacity,merk,fasilitas) \
                    values \
                    (%s,%s,%s,%s)"
                cursor.execute(sqlquery,(agent,capacity,merk,fasilitas,))
                connection.commit()
                return f'Data bus telah ditambahkan',200
            except (Exception, psycopg2.Error) as error:
                return f'data yang dimasukkan kurang',400
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
        else:
            return f'Anda bukan admin',401
    else:
        return f'Please Sign In!',401

@app.route('/updateCar',methods=["POST"])
def upcar():
    if login():
        if isadmin():
            connection=connect()
            cursor=connection.cursor()
            try:
                body=request.get_json()
                agent=body["agent"]
                capacity=body["capacity"]
                merk=body["merk"]
                fasilitas=body["fasilitas"]
                upagent=body["upagent"]
                upmerk=body["upmerk"]
                sqlquery="update cars \
                    set agent=%s,capacity=%s,merk=%s,fasilitas=%s \
                    where agent=%s and merk=%s"
                cursor.execute(sqlquery,(agent,capacity,merk,fasilitas,upagent,upmerk,))
                connection.commit()
                return f'Data bus telah diperbarui',200
            except (Exception, psycopg2.Error) as error:
                return f'data yang dimasukkan kurang',400
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
        else:
            return f'Anda bukan admin',401
    else:
        return f'Please Sign In!',401

# INSERT INTO public.schedule(
# 	dari, menuju, harga, car_id, days, berangkat,sampai)
# 	VALUES ('Bandung', 'Jakarta', 100000, 2, '{1,2,3,4,5}', '19:00','22:00');
@app.route('/addSchedule',methods=["POST"])
def addSchedule():
    if login():
        if isadmin():
            connection=connect()
            cursor=connection.cursor()
            try:
                body=request.get_json()
                dari=body["dari"]
                menuju=body["menuju"]
                harga=body["harga"]
                car_id=body["car_id"]
                hari=body["hari"]
                berangkat=body["berangkat"]
                sampai=body["sampai"]
                sqlquery="insert into schedule \
                    (dari,menuju,harga,car_id,days,berangkat,sampai) \
                    values \
                    (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sqlquery,(dari,menuju,harga,car_id,hari,berangkat,sampai,))
                connection.commit()
                return f'Jadwal telah ditambahkan',200
            except (Exception, psycopg2.Error) as error:
                return f'data yang dimasukkan kurang',400
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
        else:
            return f'Anda bukan admin',401
    else:
        return f'Please Sign In!',401

@app.route('/updateSchedule',methods=["PUT"])
def updateSchedule():
    if login():
        if isadmin():
            connection=connect()
            cursor=connection.cursor()
            try:
                body=request.get_json()
                upScheId=body["upScheId"]
                dari=body["dari"]
                menuju=body["menuju"]
                harga=body["harga"]
                car_id=body["car_id"]
                hari=body["hari"]
                berangkat=body["berangkat"]
                sampai=body["sampai"]
                sqlquery="UPDATE schedule \
                    SET dari=%s, menuju=%s, harga=%s, car_id=%s, days=%s, berangkat=%s, sampai=%s\
                    WHERE schedule_id=%s"
                cursor.execute(sqlquery,(dari,menuju,harga,car_id,hari,berangkat,sampai,upScheId,))
                connection.commit()
                return f'Jadwal telah diperbarui',200
            except (Exception, psycopg2.Error) as error:
                return f'data yang dimasukkan kurang',400
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
        else:
            return f'Anda bukan admin',401
    else:
        return f'Please Sign In!',401

@app.route('/deleteSchedule',methods=["DELETE"])
def deleteSchedule():
    if login():
        if isadmin():
            connection=connect()
            cursor=connection.cursor()
            try:
                body=request.get_json()
                ScheId=body["ScheId"]
                sqlquery="DELETE FROM public.schedule \
	                        WHERE schedule_id=%s"
                cursor.execute(sqlquery,(ScheId,))
                connection.commit()
                return f'Jadwal telah dihapus',200
            except (Exception, psycopg2.Error) as error:
                return f'data yang dimasukkan kurang',400
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
        else:
            return f'Anda bukan admin',401
    else:
        return f'Please Sign In!',401

def cek_seat(scheID,tanggal):
    connection=connect()
    cursor=connection.cursor()
    try:
        sqlquery2="select available_seat from orders where tanggal=%s and schedule_id=%s order by available_seat"
        cursor.execute(sqlquery2,(tanggal,scheID,))
        return cursor.fetchone()[0]
    except:
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/searchSchedule',methods=["GET"])
def searchSchedule():
    if login():
        connection=connect()
        cursor=connection.cursor()
        try:
            body=request.get_json()
            dari=body["dari"]
            menuju=body["menuju"]
            tanggal=body["tanggal"]
            # format tanggal => yyyy-mm-dd
            if tanggal>=str(datetime.now())[0:10]:
                sqlquery="select s.dari,s.menuju,s.harga,s.berangkat,s.sampai,c.agent,c.capacity,c.merk,c.fasilitas,s.schedule_id \
                    from schedule as s \
                    inner join cars as c \
                    on s.car_id=c.car_id \
                    where s.dari=%s and s.menuju=%s and \
                    (select extract(isodow from date %s)) \
                    =any(s.days) "
                if tanggal==str(datetime.now())[0:10]:
                    jam=str(datetime.now())[11:16]
                    sqlquery+=" and berangkat>%s"
                    cursor.execute(sqlquery,(dari,menuju,tanggal,jam,))
                else:
                    cursor.execute(sqlquery,(dari,menuju,tanggal,))
                mobile_records = cursor.fetchall()
                a=[]
                for row in mobile_records:
                    availseat=row[6]
                    if cek_seat(row[9],tanggal)!=None:
                        availseat=cek_seat(row[9],tanggal)
                    a.append({"Dari" : row[0],
                    "Menuju" : row[1],
                    "Harga" : row[2],
                    "Berangkat":str(row[3]),
                    "Sampai":str(row[4]),
                    "Travel Agent":row[5],
                    "Kapasitas":row[6],
                    "Kursi tersedia": availseat,
                    "Merk Bus":row[7],
                    "Fasilitas":row[8] })
                if a!=[]:
                    return jsonify(a)
                else:
                    return f'Tidak ditemukan', 404
            else:
                return f'Tidak dapat melihat jadwal yang telah berlalu',400
        except (Exception, psycopg2.Error) as error:
            return f'data yang dimasukkan kurang',400
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return f'Please Sign In!',401

def cek_order(schedule_id,tanggal):
    connection=connect()
    cursor=connection.cursor()
    sqlquery="select * from orders where schedule_id=%s and tanggal=%s"
    cursor.execute(sqlquery,(schedule_id,tanggal,))
    simpan=cursor.fetchone()
    print(simpan)
    if simpan!=None:
        return True
    else:
        return False

@app.route('/order',methods=["POST"])
def order():
    if login():
        if not isadmin():
            connection=connect()
            cursor=connection.cursor()
            try:
                username=request.authorization["username"]
                body=request.get_json()
                scheID=body["schedule_id"]
                seat=body["seat"]
                tanggal=body["tanggal"]
                if cek_order(scheID,tanggal):
                    try:
                        sqlquery="INSERT INTO public.orders \
                            (schedule_id, user_id, seat, available_seat, tanggal) VALUES \
                            (%s,\
                            (select user_id from users \
                                where nama=%s or email=%s)\
                            ,%s,\
                            (select available_seat from public.orders \
                                where tanggal=%s and schedule_id=%s \
                                order by available_seat limit 1)-%s,\
                            %s);"
                        cursor.execute(sqlquery,(scheID,username,username,seat,tanggal,scheID,seat,tanggal,))
                        connection.commit()
                        return f'Perjalanan telah dipesan',200
                    except (Exception, psycopg2.Error) as error:
                        return f'Kursi penuh',400
                else:
                    try:
                        cursor.close()
                        connection.close()
                        connection=connect()
                        cursor=connection.cursor()
                        sqlquery2="INSERT INTO public.orders \
                        (schedule_id, user_id, seat, available_seat, tanggal) VALUES \
                        (%s, \
                        (select user_id from users \
                            where nama=%s or email=%s)\
                        ,%s,(select c.capacity \
                            from cars as c \
                            inner join schedule as s \
                            on c.car_id=s.car_id \
                            where s.schedule_id=%s)-%s,\
                        %s);"
                        cursor.execute(sqlquery2,(scheID,username,username,seat,scheID,seat,tanggal,))
                        connection.commit()
                        return f'Perjalanan telah dipesan',200
                    except (Exception, psycopg2.Error) as error:
                        return f'data yang dimasukkan kurang',400
            except:
                return f'Terdapat kesalahan pada server',500
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
        else:
            return f'Hanya customer yang dapat memesan',401
    else:
        return f'Please Sign In!',401

@app.route('/toproute')
def toproute():
    connection=connect()
    cursor=connection.cursor()
    try:
        sqlquery="select s.dari,s.menuju,count(s.dari) from schedule as s \
                inner join orders as o \
                on s.schedule_id=o.schedule_id \
                group by s.dari,s.menuju \
                order by count(s.dari) desc limit 5 "
        cursor.execute(sqlquery)
        mobile_records = cursor.fetchall()
        a=[]
        print("Print each row and it's columns values")
        for row in mobile_records:
            a.append({"Dari" : row[0],
            "Menuju" : row[1],
            "Jumlah pesanan":row[2] })
        if a!=[]:
            return jsonify(a)
        else:
            return f'Tidak ditemukan', 404
    except (Exception, psycopg2.Error) as error:
        return f'Terdapat kesalahan pada server',500
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def daysconverter(x):
    match x:
        case 1:
            return "Senin"
        case 2:
            return "Selasa"
        case 3:
            return "Rabu"
        case 4:
            return "Kamis"
        case 5:
            return "Jumat"
        case 6:
            return "Sabtu"
        case 7:
            return "Minggu"
        case _:
            return "Error"

@app.route('/topschedule')
def topschedule():
    connection=connect()
    cursor=connection.cursor()
    try:
        sqlquery="select count(extract(isodow from tanggal)),extract(isodow from tanggal) as days from orders\
            group by extract(isodow from tanggal) \
            order by count(extract(isodow from tanggal))desc,extract(isodow from tanggal)"
        cursor.execute(sqlquery)
        mobile_records = cursor.fetchall()
        a=[]
        print("Print each row and it's columns values")
        for row in mobile_records:
            a.append({"Jumlah pesanan" : row[0],
            "Hari" : daysconverter(row[1]) })
        if a!=[]:
            return jsonify(a)
        else:
            return f'Tidak ditemukan', 404
    except (Exception, psycopg2.Error) as error:
        return f'Terdapat kesalahan pada server',500
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route('/topusers')
def topusers():
    connection=connect()
    cursor=connection.cursor()
    try:
        sqlquery="select u.nama,count(o.user_id) from users as u \
                inner join orders as o \
                on u.user_id=o.user_id \
                group by o.user_id,u.nama \
                order by count(o.user_id) desc limit 5;"
        cursor.execute(sqlquery)
        mobile_records = cursor.fetchall()
        a=[]
        print("Print each row and it's columns values")
        for row in mobile_records:
            a.append({"Nama" : row[0],
            "Jumlah pesanan" : row[1] })
        if a!=[]:
            return jsonify(a)
        else:
            return f'Tidak ditemukan', 404
    except (Exception, psycopg2.Error) as error:
        return f'Terdapat kesalahan pada server',500
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__==('__main__'):
    app.run(debug=True)