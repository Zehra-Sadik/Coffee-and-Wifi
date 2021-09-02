from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, TextField
from wtforms.validators import DataRequired, Length, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = TextField('Cafe name', validators=[DataRequired()])
    url = StringField('Location URL', validators=[DataRequired(), URL(require_tld=False, message="Invalid URL")])
    opentime = StringField('Open Time', validators=[DataRequired()])
    closingtime = StringField('Closing Time', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=[('✘'),('☕'), ('☕☕'), ('☕☕☕'), ('☕☕☕☕'), ('☕☕☕☕☕')])
    wifi = SelectField('Wifi Rating', choices=[('✘'),('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪'), ('💪💪💪💪💪')],)
    power = SelectField('Power Rating', choices=[('✘'),('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/templates/add.html', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
        with open('cafe-data.csv', 'a', encoding='utf-8-sig') as f:
            f.write(f"\n{form.cafe.data},{form.url.data},{form.opentime.data},{form.closingtime.data},{form.coffee.data},{form.wifi.data},{form.power.data}")
            f.close()
    return render_template('add.html', form=form)


@app.route('/templates/cafes.html')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8-sig') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
