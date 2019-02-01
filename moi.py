from flask import Flask, render_template
#from forms import RegistrationForm

app = Flask(__name__)

#app.config(['SECRET_KEY'] = '9aca375bbf55de13ecab2a02c26ea51b'

@app.route('/')
def register():
 #   form = RegistrationForm()
 #   return render_template('register.html', title='Register',
#      form = 'form')
    return 'test'
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000)

