from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime as dt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fghjtybnruvm10192837465'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash("You've changed your name!")
        if old_email is not None and old_email != form.email.data:
            flash("You've changed your email!")
            
        session['name'] = form.name.data
        session['email'] = form.email.data if utoronto_email(form.email.data) else None
        
        return redirect(url_for('index'))
    return render_template('index.html', current_time=dt.utcnow(), form=form, name=session.get('name'), email=session.get('email'))
    
    
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

def utoronto_email(email):
    if "utoronto" in email:
        return True
    return False


class HelloForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[Email()])
    submit = SubmitField('Submit')

        

if __name__ == '__main__':
    app.run(debug=True)
   
    