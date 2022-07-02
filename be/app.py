from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import datetime
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Initiation
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
load_dotenv()

# Initiates connection to DB
dbClient = MongoClient(os.getenv("CONNECTION_STRING"))
barangDijual = dbClient['kantinKejujuran']['barangDijual']
saldoSekarang = dbClient['kantinKejujuran']['saldoSekarang']

# Home
@app.route("/")
@cross_origin()
def home():
    return "BE is running"

@app.route("/barang-dijual", methods=["GET"])
@cross_origin()
def daftar_barang():
    item_details = barangDijual.find()
    items = []
    for item in item_details:
        item["_id"] = str(item["_id"])
        items.append(item)
    return jsonify(items), 200

@app.route("/hapus-barang", methods=["POST"])
@cross_origin()
def hapus_barang():
    if request.form.get("id") == None:
        return jsonify({"status": "invalid_body", "return_code": 0}), 200
    try:
        objId = ObjectId(request.form.get("id"))
        barangDijual.delete_one({"_id": objId})
    except:
        return jsonify({"status": "error", "return_code": 0}), 200
    else:
        return jsonify({"status": "success", "return_code": 1}), 200

@app.route("/tambah-barang", methods=["POST"])
@cross_origin()
def tambah_barang():
    if request.form.get("nama") == None or request.form.get("harga") == None:
        return jsonify({"status": "invalid_body", "return_code":0}), 200
    deskripsi = request.form.get("deskripsi") 
    if  deskripsi == None:
        deskripsi = "Tidak ada deskripsi untuk produk ini"
    link_gambar = request.form.get("link_gambar")
    if link_gambar == None:
        link_gambar = "https://media.discordapp.net/attachments/893484082275708980/992667550162886706/unknown.png"
    new_item = {
        "nama": request.form.get("nama"),
        "link_gambar": link_gambar,
       "deskripsi": deskripsi,
        "harga": request.form.get("harga"),
        "tanggal": datetime.datetime.utcnow(),
    }
    barangDijual.insert_one(new_item)
    return jsonify({"status": "success", "return_code": 1}), 200

@app.route("/cek-saldo", methods=["GET"])
@cross_origin()
def cek_saldo():
    saldoDetails = saldoSekarang.find({"_id": ObjectId(os.getenv("SALDO_ID"))}).limit(1)
    saldo = -1
    for detail in saldoDetails:
        saldo = detail["saldo"]
    if saldo == -1:
        return jsonify({"status": "error", "return_code": 0}), 200
    return jsonify({"status": "success", "return_code": 1, "saldo": saldo}), 200

@app.route("/ubah-saldo", methods=["POST"])
@cross_origin()
def ubah_saldo():
    if request.form.get("saldo_terbarukan") == None:
        return jsonify({"status": "invalid_body", "return_code": 0}), 200
    newBal = int(request.form.get("saldo_terbarukan"))
    if newBal < 0:
        return jsonify({"status": "error", "return_code": 0}), 200
    saldoSekarang.update_one(
        {"_id": ObjectId(os.getenv("SALDO_ID"))},
        { "$set" : {"saldo": newBal}},
    )
    return jsonify({"status": "success", "return_code": 1}), 200