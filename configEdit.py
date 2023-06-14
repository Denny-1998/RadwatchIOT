from flask import Flask, render_template, request

app = Flask(__name__)

class ConfigEdit:
    
    def __init__(self, config_file):
        print("starting api for conf_edit")
        self.config_file = config_file

    def update_config(self, url, logger_name, user_name, password, serial_number):
        with open(self.config_file, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith('url ='):
                lines[i] = f'url = {url}\n'
            elif line.startswith('loggerName ='):
                lines[i] = f'loggerName = {logger_name}\n'
            elif line.startswith('userName ='):
                lines[i] = f'userName = {user_name}\n'
            elif line.startswith('password ='):
                lines[i] = f'password = {password}\n'
            elif line.startswith('serialNumber ='):
                lines[i] = f'serialNumber = {serial_number}\n'

        with open(self.config_file, 'w') as file:
            file.writelines(lines)

@app.route('/', methods=['GET', 'POST'])
def edit_config():
    if request.method == 'POST':
        url = request.form['url']
        logger_name = request.form['logger_name']
        user_name = request.form['user_name']
        password = request.form['password']
        serial_number = request.form['serial_number']

        conf_editor = ConfigEdit('logger.conf')
        conf_editor.update_config(url, logger_name, user_name, password, serial_number)
        print("config changed")
    return render_template('edit_config.html')

if __name__ == '__main__':
    app.run()
