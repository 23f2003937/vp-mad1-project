from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from models import User, ParkingLot

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')
    
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords do not match.')

class ParkingLotForm(FlaskForm):
    prime_location_name = StringField('Location Name', validators=[DataRequired(), Length(min=3, max=200)])
    price_per_hour = FloatField('Price per Hour', validators=[DataRequired(), NumberRange(min=0.01)])
    address = TextAreaField('Address', validators=[DataRequired()])
    pin_code = StringField('Pin Code', validators=[DataRequired(), Length(min=5, max=10)])
    maximum_number_of_spots = IntegerField('Maximum Number of Spots', validators=[DataRequired(), NumberRange(min=1, max=1000)])

class BookParkingForm(FlaskForm):
    lot_id = SelectField('Parking Lot', coerce=int, validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(BookParkingForm, self).__init__(*args, **kwargs)
        # Populate choices with available parking lots
        lots = ParkingLot.query.all()
        self.lot_id.choices = [(lot.id, f"{lot.prime_location_name} - ${lot.price_per_hour}/hr ({lot.available_spots_count} spots available)") for lot in lots if lot.available_spots_count > 0]
