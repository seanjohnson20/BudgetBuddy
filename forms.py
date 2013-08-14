from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, BooleanField, IntegerField, DecimalField, DateField, SelectField
from database import db_session
from models import User


class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
  confirm = PasswordField('Repeat Password')
  accept_eula = BooleanField('I accept the ', [validators.Required()])
  submit = SubmitField("Sign Up")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True
      

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = User.query.filter_by(email = self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
      

class TransactionForm(Form):  
    account = SelectField('Select Account',[validators.Required("Please select Account.")])
    category = SelectField('Select Category',[validators.Required("Please select Category.")])
    goal = SelectField('Optional: Apply Savings to Goal',[validators.Optional("Apply Savings to Goal.")])
    notes = TextField("Notes",  [validators.optional("Optional: add notes")])
    amount = DecimalField("Amount",  [validators.Required("Please enter Amount.")])
    submit = SubmitField("Submit/Update Transaction")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
    
class AccountForm(Form):  #form3
    name = TextField("Account",  [validators.Required("Please select Account")])
    submit = SubmitField("Add Account")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False    

    
class EditAcctForm(Form): 
    id = IntegerField("ID",)
    name = TextField("Account", )
    email = TextField("Email", )
    submit = SubmitField("Update Account")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False        
            
            
class CategoryForm(Form): 
    name = TextField("Category",  [validators.Required("Please select Category")])
    submit = SubmitField("Add Category")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False       

class EditCatForm(Form): 
    id = IntegerField("ID",)
    name = TextField("Category", )
    email = TextField("Email", )
    submit = SubmitField("Update Category")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False   
            

class GoalForm(Form):  
    category = SelectField('Select Category',[validators.Required("Please select Account.")])
    target = TextField("Target Date", [validators.optional("Enter Target Date")],id="datepicker")
    description = TextAreaField("Goal Description",  [validators.optional("Enter Amount")])
    amount = DecimalField("Goal Amount", [validators.Required("Enter Amount")])
    submit = SubmitField("Add Goal")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
            
            
class EditGoalForm(Form):  
    id = IntegerField("ID",)
    email = TextField("Email", )
    category = SelectField('Select Category',[validators.Required("Please select Account.")])
    target = TextField("Target Date",id="datepicker")
    description = TextAreaField("Goal Description",  [validators.optional("Enter Amount")])
    amount = DecimalField("Goal Amount", [validators.Required("Enter Amount")])
    submit = SubmitField("Update Goal")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False            
            
            

            
            
            
            