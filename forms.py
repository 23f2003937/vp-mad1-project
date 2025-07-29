from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from models import User, ParkingLot

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)], 
                          render_kw={"placeholder": "Enter your username", "class": "form-control", "autocomplete": "username"})
    password = PasswordField('Password', validators=[DataRequired()],
                           render_kw={"placeholder": "Enter your password", "class": "form-control", "autocomplete": "current-password"})

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)],
                          render_kw={"placeholder": "Choose a unique username", "class": "form-control", "pattern": "[a-zA-Z0-9_]{3,80}", "title": "Username must be 3-80 characters, letters, numbers, and underscores only"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "Enter your email address", "class": "form-control", "type": "email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)],
                           render_kw={"placeholder": "Create a strong password (6+ characters)", "class": "form-control", "autocomplete": "new-password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()],
                                   render_kw={"placeholder": "Confirm your password", "class": "form-control", "autocomplete": "new-password"})
    
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
    prime_location_name = StringField('Location Name', validators=[DataRequired(), Length(min=3, max=200)],
                                     render_kw={"placeholder": "e.g., Downtown Mall", "class": "form-control", "maxlength": "200"})
    price = FloatField('Price per Unit Time', validators=[DataRequired(), NumberRange(min=0.01, max=100.00)],
                      render_kw={"placeholder": "e.g., 2.50", "class": "form-control", "step": "0.01", "min": "0.01", "max": "100.00"})
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=500)],
                           render_kw={"placeholder": "Enter complete address", "class": "form-control", "rows": "3", "maxlength": "500"})
    pin_code = StringField('Pin Code', validators=[DataRequired(), Length(min=5, max=10)],
                          render_kw={"placeholder": "e.g., 12345", "class": "form-control", "pattern": "[0-9]{5,10}", "title": "Pin code must be 5-10 digits"})
    maximum_number_of_spots = IntegerField('Maximum Number of Spots', validators=[DataRequired(), NumberRange(min=1, max=1000)],
                                          render_kw={"placeholder": "e.g., 50", "class": "form-control", "min": "1", "max": "1000"})

class BookParkingForm(FlaskForm):
    lot_id = SelectField('Parking Lot', coerce=int, validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(BookParkingForm, self).__init__(*args, **kwargs)
        # Populate choices with available parking lots
        lots = ParkingLot.query.all()
        self.lot_id.choices = [(lot.id, f"{lot.prime_location_name} - ${lot.price}/hr ({lot.available_spots_count} spots available)") for lot in lots if lot.available_spots_count > 0]
