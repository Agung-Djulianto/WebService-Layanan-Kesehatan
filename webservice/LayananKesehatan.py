from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource,reqparse
import json

# Database ORM
from peewee import *

# Generate Database
db = "LayananKesehatan.db"
database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database = database

class RumahSakit(BaseModel):
	id = AutoField(primary_key=True)
	Nama_RS = CharField(unique=True)
	Alamat_RS = TextField()
	No_telp = CharField()
	koordinat_maps = CharField()
	# Latitude = CharField()
	# Longitude = CharField()
	Foto_RS = TextField(null=True,default=None)

class Poli(BaseModel):
	id = AutoField(primary_key=True)
	id_RS = ForeignKeyField(RumahSakit)
	Nama_Poli = TextField()
	Nama_dokter = TextField()
	Jam_Oprasional = CharField()
	Deskripsi_poli = TextField()

# INSERT POLI SCRIPT manual 
# insert into poli (id,id_RS_id,Nama_Poli,Nama_dokter,Jam_Oprasional,Deskripsi_poli) values ("1","1","Talang","Bambang","07:00","Yah begitu");

def create_tables():
	with database:
		database.create_tables([RumahSakit, Poli])

app = Flask(__name__)
api = Api(app)

# Simple Read and Post RumahSakit
class read_Rumah_Sakit(Resource):
	def get(self):
		# mendapatkan data menggunakan quwery
		parser = reqparse.RequestParser()
		parser.add_argument("id",type=int,help="id, Must int, required")
		parser.add_argument("Nama_RS", type=str, help="Nama_RS, Must str, required")
		parser.add_argument("Alamat_RS",type=str,help="Alamat_RS, Must int, required")
		args = parser.parse_args()
		
		if args['id'] and args['Nama_RS']:
			return jsonify({"massage" : "PILIH SALAH SATU ID ATAU NAMA RUMAH SAKIT "})
		elif args['id']:
			get_rumahsakit = list(RumahSakit.select().where(RumahSakit.id == args['id']).dicts())
			return {'data': get_rumahsakit,"message":'Data Rumah Sakit Terambil'}
		elif args['Nama_RS']:
			get_rumahsakit = list(RumahSakit.select().where(RumahSakit.Nama_RS.contains(args['Nama_RS'])).dicts())
			return {'data': get_rumahsakit,"message":'Data Rumah Sakit Terambil'}
		elif args['Alamat_RS']:
			get_rumahsakit = list(RumahSakit.select().where(RumahSakit.Alamat_RS.contains(args['Alamat_RS'])).dicts())
			return {'data': get_rumahsakit,"message":'Data Rumah Sakit Terambil'}
		else:
			get_rumahsakit = list(RumahSakit.select().dicts())
			return{'data': get_rumahsakit,"massage":"Data Rumah Sakit Terambil"}
		return jsonify({"message":"Helloworld"})



	def post(self):
		# Menambah Data Rumah Sakit
		parser = reqparse.RequestParser()
		parser.add_argument("Nama_RS",location="form", type=str, required=True, help="Nama_RS, Must str, required")
		parser.add_argument("Alamat_RS",location="form", type=str, required=True, help="Alamat_RS, Must str, required")
		parser.add_argument("No_telp",location="form", type=str, required=True, help="No_telp, Must str, required")
		parser.add_argument("koordinat_maps",location="form", type=str, required=True, help="koordinat_maps, Must str, required")
		# parser.add_argument("Latitude",location="form", type=str, required=True, help="Latitude, Must str, required")
		# parser.add_argument("Longitude",location="form", type=str, required=True, help="rumahsakit, Must str, required")
		args = parser.parse_args()

		try:
			RumahSakit.create(Nama_RS=args['Nama_RS'], Alamat_RS=args['Alamat_RS'],No_telp=args['No_telp'], koordinat_maps=args['koordinat_maps'],Foto_RS=None)
			# RumahSakit.create(Nama_RS=args['Nama_RS'], Alamat_RS=args['Alamat_RS'], No_telp=args['No_telp'], koordinat_maps=args['koordinat_maps'])
			return jsonify({"hasil":"RS {} Created".format(args['Nama_RS']),"status":'000'})
		except IntegrityError:
			return jsonify({"hasil":"Data Rumah Sakit Sudah Ada",'status':'001'})
	
	def put(self):
		# Update Rumah Sakit
		parser = reqparse.RequestParser()
		parser.add_argument('id', location="form", type=int, required=True, help="id, Must int, required")
		parser.add_argument("Nama_RS",location="form", type=str, required=True, help="Nama_RS, Must str, required")
		parser.add_argument("Alamat_RS",location="form", type=str, required=True, help="Alamat_RS, Must str, required")
		parser.add_argument("No_telp",location="form", type=str, required=True, help="No_telp, Must str, required")
		parser.add_argument("koordinat_maps",location="form", type=str, required=True, help="koordinat_maps, Must str, required")
		# parser.add_argument("Latitude",location="form", type=str, required=True, help="Latitude, Must str, required")
		# parser.add_argument("Longitude",location="form", type=str, required=True, help="rumahsakit, Must str, required")
		args = parser.parse_args()
		cek_rumahsakit= RumahSakit.select().where(RumahSakit.id == args['id'])
		if cek_rumahsakit.exists():
			update_rumahsakit = RumahSakit.update(Nama_RS=args['Nama_RS'],Alamat_RS=args['Alamat_RS'], No_telp=args['No_telp'], koordinat_maps=args['koordinat_maps']).where(RumahSakit.id == args['id'])
			update_rumahsakit.execute()
			return jsonify({"message":"Data Rumah Sakit Diperbarui"})
		else:
			return jsonify({'message':'Data Rumah Sakit Tidak Ditemukan'})


	def delete(self):
		# Menghapus Rumah Sakit
		parser = reqparse.RequestParser()
		parser.add_argument('id', type=int, required=True, help="id, Must str, required")
		args = parser.parse_args()
		cek_rumahsakit = RumahSakit.select().where(RumahSakit.id == args['id'])
		if cek_rumahsakit.exists():
			delete_rumahsakit = RumahSakit.delete().where(RumahSakit.id == args['id'])
			delete_rumahsakit.execute()
			return jsonify({'message':"Data Rumah Sakit terhapus"})
		else:
			return jsonify({'message':'Data Rumah Sakit Tidak Ditemukan'})

 # Simple Read and Post poli
class read_Poli(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("id", type=int,help="Poli, Must int, required")
		parser.add_argument("id_RS", type=int,help="Poli, Must int, required")
		parser.add_argument('Nama_Poli', type=str, help='Nama_Poli, Must str, required')
		#parser.add_argument('Nama_RS', type=str, help='Nama_RS, Must str, required')
		
		args = parser.parse_args()

		if args['id'] and args['Nama_Poli']:
			return jsonify({"massage" : "PILIH SALAH SATU ID ATAU NAMA POLI"})
		elif args['id']:
			get_poli = list(Poli.select().where(Poli.id == args['id']).dicts())
			return {'data': get_poli,"message":'Data Poli Terambil'}
		elif args['Nama_Poli']:
			get_poli = list(Poli.select().where(Poli.Nama_Poli.contains(args['Nama_Poli'])).dicts())
			return {'data': get_poli,"message":'Data Poli Terambil'}
		elif args['id_RS']:
			get_poli = list(Poli.select().where(Poli.id_RS == args['id_RS']).dicts())
		else:
			get_poli = list(Poli.select().dicts())
			return{'data': get_poli,"massage":"Data Poli Terambil"}

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("id_RS", type=str, required=True, help="id_RS, Must str, required")
		parser.add_argument("Nama_Poli", type=str, required=True, help="Nama_Poli, Must str, required")
		parser.add_argument("Nama_dokter", type=str, required=True, help="Nama_dokter, Must str, required")
		parser.add_argument("Jam_Oprasional", type=str, required=True, help="Jam_Oprasional, Must str, required")
		parser.add_argument("Deskripsi_poli", type=str, required=True, help="Deskripsi_poli, Must str, required")
		args = parser.parse_args()

		try:
			Poli.create(id_RS=args['id_RS'], Nama_Poli=args['Nama_Poli'], Nama_dokter=args['Nama_dokter'], Jam_Oprasional=args['Jam_Oprasional'], Deskripsi_poli=args['Deskripsi_poli'])
			return jsonify({"hasil":"POLI {} Created".format(args['Nama_Poli']),"status":'000'})
		except IntegrityError:
			return jsonify({"hasil":"Data Poli Sudah Ada",'status':'001'})

	def put(self):
		# Update Poli
		parser = reqparse.RequestParser()
		parser.add_argument('id', location="form", type=int, required=True, help="id, Must int, required")
		parser.add_argument('id_RS', location="form", type=int, required=True, help="id_RS, Must int, required")
		parser.add_argument("Nama_Poli",location="form", type=str, required=True, help="Nama_RS, Must str, required")
		parser.add_argument("Nama_dokter",location="form", type=str, required=True, help="Alamat_RS, Must str, required")
		parser.add_argument("Jam_Oprasional",location="form", type=str, required=True, help="No_telp, Must str, required")
		parser.add_argument("Deskripsi_poli",location="form", type=str, required=True, help="Deskripsi_poli, Must str, required")
		args = parser.parse_args()
		cek_poli= Poli.select().where(Poli.id == args['id'])
		if cek_poli.exists():
			update_poli = Poli.update(id_RS=args['id_RS'], Nama_Poli=args['Nama_Poli'], Nama_dokter=args['Nama_dokter'], Jam_Oprasional=args['Jam_Oprasional'], Deskripsi_poli=args['Deskripsi_poli']).where(Poli.id == args['id'])
			update_poli.execute()
			return jsonify({"message":"Data Poli Diperbarui"})
		else:
			return jsonify({'message':'Data Poli Tidak Ditemukan'})
 
	def delete(self):
		# Menghapus Rumah Sakit
		parser = reqparse.RequestParser()
		parser.add_argument('id', type=int, required=True, help="id, Must str, required")
		args = parser.parse_args()
		cek_poli = Poli.select().where(Poli.id == args['id'])
		if cek_poli.exists():
			delete_poli = Poli.delete().where(Poli.id == args['id'])
			delete_poli.execute()
			return jsonify({'message':"Data Poli Terhapus"})
		else:
			return jsonify({'message':'Data Poli Tidak ditemukan'})

class poli(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("Nama_Poli",type=str, help="Nama_Poli, Must str")
		args = parser.parse_args()

		if args['Nama_Poli'] is None:
			Data_Poli= []
			query_Poli = Poli.select()
			if query_Poli.exists():
				for i in query_Poli:
					data = {}
					data['Nama_RS'] = i.id_RS.Nama_RS
					data['Nama_Poli'] = i.Nama_Poli
					data['Nama_dokter'] = i.Nama_dokter
					data['Jam_Oprasional'] = i.Jam_Oprasional
					data['Deskripsi_poli'] = i.Deskripsi_poli
					Data_Poli.append(data)
				return jsonify({"data":Data_Poli,'status':'000'})
			else:
				return jsonify({"data":Data_Poli,'status':'000'})
		else :
			Data_Poli= []
			query_Poli = Poli.select().where(Poli.Nama_Poli.contains(args['Nama_Poli']))
			if query_Poli.exists():
				for i in query_Poli:
					data = {}
					data['Nama_RS'] = i.id_RS.Nama_RS
					data['Nama_Poli'] = i.Nama_Poli
					data['Nama_dokter'] = i.Nama_dokter
					data['Jam_Oprasional'] = i.Jam_Oprasional
					data['Deskripsi_poli'] = i.Deskripsi_poli
					Data_Poli.append(data)
				return jsonify({"data":Data_Poli,'status':'000'})
			else:
				return jsonify({"data":Data_Poli,'status':'000'})

# class Resource_Coba(Resource):
# 	def get(self):
# 		datapoli = []
# 		selekpoli = Poli.select()
# 		for i in selekpoli:
# 			data = {
# 				'id_RS':int(str(i.id_RS)),
# 				'Nama_Poli':i.Nama_Poli,
# 				'Nama_dokter':i.Nama_dokter,
# 				'Jam_Oprasional':i.Jam_Oprasional,
# 				'Deskripsi_poli':i.Deskripsi_poli
# 			}
# 			datapoli.append(data)
# 		with open("data_poli.json","w") as outputfile:
# 			json.dump(datapoli,outputfile)

	# 	return 'oke'

	# def post(self):
	# 	f = open("data_poli.json")
	# 	data = json.load(f)
	# 	print(data)
	# 	for i in data:
	# 		Poli.create(
	# 			id_RS=i['id_RS'],
	# 			Nama_Poli=i['Nama_Poli'],
	# 			Nama_dokter=i['Nama_dokter'],
	# 			Jam_Oprasional=i['Jam_Oprasional'],
	# 			Deskripsi_poli=i['Deskripsi_poli']
	# 		)
	# 	return 'oke'

api.add_resource(read_Rumah_Sakit, "/api/RumahSakit/")
api.add_resource(poli, "/api/poli/")
api.add_resource(read_Poli, "/api/Poli/")
# api.add_resource(Resource_Coba, '/coba/')

if __name__ == "__main__":
	create_tables()
	app.run(debug=True)