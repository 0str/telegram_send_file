from flask import request, Flask
from flask_restful import Api
import json,io,requests
# файл, в котором хранится токен от бота
import config

app = Flask(__name__)
api = Api(app)
# ссылка, по которой файл будет отправлен пользователю
tg_url = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendDocument'

# URL адрес, на который отправляются данные из формы на сайте
@app.route('/getfile', methods=['POST'])
def send_file_to_telegram():
    # проверяем был ли получен файл из формы
    if 'file' not in request.files:
        return 'No file', 400
    else:
        file = request.files['file']
        request_form = request.form
        # проверяем были ли переданы другие данные формы
        if request_form:
            try:
                caption = request_form['caption']
                tg_id = request_form['tg_id']
            except:
                return "not all data has been sent", 400
        else:
            return 'request.form is empty', 400
        if file.filename == '':
            return 'No filename', 400
        else:
            try:
                file_read = file.read()
                # создаем буфер, в который будет помещен файл
                buf = io.BytesIO()
                buf.write(file_read)
                # смещение буфера на 0 позицию
                buf.seek(0)
                buf_read = buf.read()
                files = {'document': (file.filename, buf_read)}
                r = requests.post(tg_url, data={'chat_id':tg_id,'caption':caption}, files=files)
                if r.status_code == 200:
                    json_string  = {
                        "is_success" : True
                    }
                    return json.dumps(json_string), 200
                else:
                    json_string  = {
                        "is_success" : False
                    }
                    return json.dumps(json_string), 400
            except Exception as ex:
                return ex, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')
