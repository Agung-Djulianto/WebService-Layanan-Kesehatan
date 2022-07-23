# mengiport modul
import botogram, requests, json, time

#menentukan API dan deskripsi bot
bot = botogram.create("5252104681:AAHTel2qn2qF1WdJOdSnt3kYo2zLGBey_LM")
bot.about = "bot ini dalam masa pembuatan"
bot.after_help = ["Bot ini bertujuan untuk pencarian data rumah sakit di wilayah Kota Sidoarjo",]
bot.owner = "@Ancoent009"


# fungisi untuk membuat deskripsi pada menu start
@bot.command("start")
def start_command(chat, message):
    start = "Untuk Memulai"
    Cari = "- /Cari ==> untuk menampilkan semua rumah sakit yang berada di Sidoarjo"
    RumahSakit = "- /rumahsakit ==> pencarian rumah sakit berdasarkan nama rumah sakit contoh : /rumahsakit <sepasi> nama rumah sakit yang dituju"
    Poli = "- /Poli ==> untuk mecari poli berdasarkan nama poli. contoh : /Poli <spasi> nama poli yang dicari"
    Lokasi = "- /lokasi ==> untuk mecari rumah sakit berdasarkan lokasi yang diinginkan contoh : /alamat <spasi> Nama Lokasi"
    bantuan = "- /help ==> untuk informasi lebih lanjut" 
    chat.send("\n \n {} \n \n {} \n \n {} \n \n {} \n \n {} \n \n {}".format(start,Cari,RumahSakit,Poli,Lokasi,bantuan))

# fungsi untuk membuat tombol
@bot.command("Cari")
def search_command(chat, message, args):
    """Reply to a simple survey!"""
    btns = botogram.Buttons()
    btns[0].callback("Rumah Sakit", "rumahsakit")
    chat.send("Tekan 'Rumah Sakit' untuk memunculkan semua data rumah sakit", attach=btns)
    chat.send("waktu pencarian : {}".format(waktu))

# fungsi untuk query /rumahsakit
@bot.callback("rumahsakit")
def notify_callback(query, data, chat, message):
    url = 'http://127.0.0.1:5000/api/RumahSakit/' #url WebService
    waktu_awal = time.time()
    response_info = requests.get(url)
    response = response_info.json()
    waktu_akhir = time.time()
    waktu = waktu_akhir-waktu_awal
    data_j = response['data']

    for i in data_j:
        lis = []
        Nama_RS = i['Nama_RS']
        Alamat_RS= i['Alamat_RS']
        No_telp = i['No_telp']
        koordinat_maps = i['koordinat_maps']
        lis.append(i)
        chat.send("Nama Rumah Sakit : {} \n Alamat : {} \n Nomer Telpon: {} \n Lokasi : {} ".format(Nama_RS, Alamat_RS, No_telp, koordinat_maps))
    chat.send("waktu pencarian : {}".format(waktu))
    chat.send("Kembali Kepencarian Tekan ==> /start")

# fungsi untuk pencarian rumah sakit berdasarkan nama
@bot.command("rumahsakit")
def datars(chat, message, args ):
    url = 'http://127.0.0.1:5000/api/RumahSakit/'
    waktu_awal = time.time()
    PARAMS = {"Nama_RS": args}
    json_data = requests.get(url, params = PARAMS)
    response = json_data.json()
    waktu_akhir = time.time()
    waktu = waktu_akhir-waktu_awal
    data_j = response['data']

    for i in data_j:
        lis = []
        Nama_RS = i['Nama_RS']
        Alamat_RS= i['Alamat_RS']
        No_telp = i['No_telp']
        koordinat_maps = i['koordinat_maps']
        lis.append(i)
        chat.send("Nama Rumah Sakit : {} \n Alamat : {} \n Nomer Telpon: {} \n Lokasi : {}".format(Nama_RS, Alamat_RS, No_telp, koordinat_maps))
    chat.send("waktu pencarian : {}".format(waktu))
    chat.send("Kembali Kepencarian Tekan ==> /start")

# fungsi untuk mencari rumah skait bedasarkan lokasi
@bot.command("lokasi")
def datars(chat, message, args ):
    url = 'http://127.0.0.1:5000/api/RumahSakit/'
    waktu_awal = time.time()
    PARAMS = {"Alamat_RS": args}
    json_data = requests.get(url, params = PARAMS)
    response = json_data.json()
    waktu_akhir = time.time()
    waktu = waktu_akhir-waktu_awal
    data_j = response['data']

    for i in data_j:
        lis = []
        Nama_RS = i['Nama_RS']
        Alamat_RS= i['Alamat_RS']
        No_telp = i['No_telp']
        koordinat_maps = i['koordinat_maps']
        lis.append(i)
        chat.send("Nama Rumah Sakit : {} \n Alamat : {} \n Nomer Telpon: {} \n Lokasi : {}".format(Nama_RS, Alamat_RS, No_telp, koordinat_maps))
    chat.send("waktu pencarian : {}".format(waktu))
    chat.send("Kembali Kepencarian Tekan ==> /start")

#fungsi untuk pencarian poli
@bot.command("Poli")
def hello_command(chat, message, args):
    url = "http://127.0.0.1:5000/api/poli/"
    PARAMS = {"Nama_Poli": args}
    waktu_awal = time.time()
    json_data = requests.get(url, params = PARAMS)
    response = json_data.json()
    waktu_akhir = time.time()
    waktu = waktu_akhir-waktu_awal
    data_j = response['data']
    for i in data_j:
        lis = []
        Nama_RS = i['Nama_RS']
        Nama_Poli = i['Nama_Poli']
        Nama_dokter = i['Nama_dokter']
        Jam_Oprasional= i['Jam_Oprasional']
        Deskripsi_poli = i['Deskripsi_poli']
        lis.append(i)
        chat.send("Rumah Sakit : {} \n Nama Poli: {} \n Dokter : {} \n Oprasional {} \n Keterangan : {} \n ".format(Nama_RS, Nama_Poli, Nama_dokter, Jam_Oprasional, Deskripsi_poli))
    chat.send("waktu pencarian : {}".format(waktu))
    chat.send("Kembali Kepencarian Tekan ==> /start")
    # chat.send("Hello " + ", ".join(args))


if __name__ == "__main__":
    bot.run()