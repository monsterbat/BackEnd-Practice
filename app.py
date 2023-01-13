from flask import *
from flask_cors import CORS
import requests
from MySQL_con import *
import datetime
# .env 
from dotenv import load_dotenv
import os
load_dotenv()
s3_url = os.getenv("s3_url")
cloudFront_url = os.getenv("cloudFront_url")

app=Flask(
	__name__,
	static_folder="static",
    static_url_path="/static"
)

CORS(app)
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/api/image", methods=["PUT","GET"])
def image():
    if request.method == "PUT":
        try:

            rawData = request.get_json()
            # print("rawData data type",type(rawData))
            current_time_code = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            image_type = rawData["image_type"]
            image_name = current_time_code+"."+image_type
            connent = rawData["connent"]
            image_raw = rawData["image_raw"]
            image_raw = bytes(image_raw)
            headers = {
                "Content-Type": f"image/{image_type}",
            }
            s3_upload_url = f"{s3_url}/{image_name}"
            print("C1",s3_upload_url)
            s3_upload = requests.put(s3_upload_url,headers=headers, data=image_raw, timeout=30)
            request_status = s3_upload.status_code
            if request_status == 200:
                # into MySQL
                sql_command = """
                INSERT INTO img_connent (connent, imagename)
                VALUES (%s,%s);
                """                
                value_input = (connent,image_name)
                insert_or_update_data(sql_command,value_input)
                # get data from MySQL
                sql_command="""
                SELECT connent, imagename
                FROM img_connent 
                ORDER BY id DESC LIMIT 1;
                """
                user_info = query_data_read(sql_command)
                image_name_get = user_info[0]["imagename"]
                connent_get = user_info[0]["connent"]
                cloudFront_download_url = f"{cloudFront_url}/{image_name_get}"

                data = {
                    "imageUrl":cloudFront_download_url,
                    "connent":connent_get
                }  
                return jsonify(data), 200
        except Exception as ex:
            return jsonify(error="true", message=f"{ex}"), 500
    if request.method == "GET":
        try:
            sql_command="""
            SELECT connent, imagename
            FROM img_connent 
            """
            user_info = query_data_read(sql_command)
            print("user_info",user_info)
            # len(user_info)
            dataSum = []
            for user_info_list in user_info:
                connent = user_info_list["connent"]
                imagename = user_info_list["imagename"]
                image_url = f"{cloudFront_url}/{imagename}"
                data = {
                    "connent":connent,
                    "imageUrl":image_url
                }
                print(data)
                dataSum.append(data)
            print("dataSum",dataSum)
            return dataSum
        except Exception as ex:
            return jsonify(error="true", message=f"{ex}"), 500


app.debug = True
app.run(host = "0.0.0.0",port=80)