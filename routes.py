# coding: utf-8
# u.t.f.-8  line included so Jinja templates can handle '%.02f' in them.
from flask import Flask, render_template, request, g, session, flash, \
     redirect, url_for, abort
from database import db_session, engine
from models import User, Accounts, Categories, Transactions, Goals
from flask import Flask
from flask.ext.mail import Message
from config import *
from forms import SignupForm, SigninForm, TransactionForm, AccountForm, CategoryForm, GoalForm, EditAcctForm, EditCatForm, EditGoalForm, EditTransForm
from functools import wraps
from sqlalchemy import func
from datetime import date, datetime

today = date.today()
 
app = Flask(__name__)
app.config.from_object('config')


## -----------------------No Login Required ------------------------------ ##

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if 'email' in session:
        return redirect(url_for('profile')) 
  
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db_session.add(newuser)
            db_session.commit()
            session['email'] = newuser.email
            flash('You have successfully signed up and you are logged in')
            print (str(session['email']),'has been successfully signed up and logged in')
            return redirect(url_for('home'))
    elif request.method == 'GET':
        print('Guest is on signup page.')
        return render_template('signup.html', form=form)

        
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
      
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            flash('You are logged in')
            print (str(session['email']),'is logged in') 
        return redirect(url_for('home'))
                
    elif request.method == 'GET':
        return render_template('signin.html', form=form)      
        
        
@app.route("/")
def index():
    if 'email' in session:
        print (str(session['email']),'is on Index')
    else:
        print('Guest is on Index')
        
    usrs = User.query.order_by(User.email)
    #usrs = db_session.query(User).order_by(User.firstname)
    return render_template('index.html', usrs=usrs)
    
    
@app.route("/eula/")
def eula():
    if 'email' in session:
        print (str(session['email']),'is on EULA')
    else:
        print('Guest is on EULA')
    return render_template('eula.html')
   
   
@app.route("/about/")
def about():
    if 'email' in session:
        print (str(session['email']),'is on About')
    else:
        print('Guest is on About')
    return render_template('about.html')
   
        
@app.route("/help/")
def help():
    if 'email' in session:
        print (str(session['email']),'is on Help')
    else:
        print('Guest is on Help')
    return render_template('help.html')        
    

## -----------------------Login Required ------------------------------ ##    
      
    
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'email' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            print('Guest: You need to login first')
            return redirect(url_for('signin'))
    return wrap

    
@app.route("/home/")
@login_required
def home():
    #goals by session user
    con=engine.connect()
    goals = con.execute("""select id, email, category, description, target, round(amount/((julianday(target)-julianday('now'))/30),2) as 'monthly', round((((julianday(target)-julianday(datetime('now')))/30)),1) as 'months',
round((julianday(target)-julianday(datetime('now'))),0) as 'days', round(goals.amount,0) as 'amount'
from goals
where email=:param
order by category""", {"param":session['email']} )
    
    progress = con.execute("""select goals.category, goals.description, ifnull(round(sum(transactions.amount),2), 0) as 'sum', round(((julianday(target)-julianday(datetime('now')))/30),1) as 'months', round((julianday(target)-julianday(datetime('now'))),0) as 'days',
round(goals.amount,2) as 'goal', ifnull((sum(transactions.amount)/goals.amount*100),0) as 'progress' 
from goals LEFT JOIN transactions on goals.category=transactions.category and goals.description=transactions.goal
and goals.email=transactions.email
where goals.email=:param 
and goals.amount is not null 
group by goals.category, goals.description
order by goals.category""", {"param":session['email']} )
   
    #transactions by session user
    transactions = con.execute("select * from transactions where email=:param order by trans_date desc", {"param":session['email']} )
    
    #accounts by session user
    accounts = con.execute("select accounts.id, accounts.name,  ifnull(round(sum(transactions.amount),2),0) as 'sum'  from  accounts left join transactions on accounts.name=transactions.account and accounts.email=transactions.email where accounts.email=:param group by accounts.name order by accounts.name", {"param":session['email']} )
    
    #categories by session user
    categories = con.execute("select categories.id, categories.name, ifnull(round(sum(transactions.amount),2),0) as 'sum' from categories left join transactions on categories.name=transactions.category and categories.email=transactions.email where categories.email=:param group by categories.name order by categories.name", {"param":session['email']} )
    
    print (str(session['email']),'is on Home')
    return render_template('home.html', accounts=accounts, transactions=transactions, categories=categories, goals=goals, progress=progress, today=today)   

    
@app.route("/add_goal/", methods=['GET', 'POST'])
@login_required
def add_goal():
    print (str(session['email']),'is on add_goal')
    email = session['email']
    form = GoalForm()
    form.category.choices = [(c.name,c.name) for c in Categories.query.filter_by(email=email)]
    if request.method == 'POST':
        if form.validate() == False:
            print ("validate failed: ",session['email'], form.category.data, form.target.data, form.description.data, form.amount.data)
            return render_template('addgoal.html', form=form)
        else:
            newgoal = Goals(str(session['email']), str(form.category.data), str(form.target.data), str(form.description.data), float(form.amount.data))
            print ("validated goal data: ",session['email'], form.category.data, form.target.data, form.description.data, form.amount.data)
            db_session.add(newgoal)
            db_session.commit()
            flash('You created a new goal.')
            print (str(session['email']),'has successfully added a new goal')
            return redirect('/home')
    print ("submit failed: ",session['email'], form.category.data, form.target.data, form.description.data, form.amount.data)
    return render_template('addgoal.html', form=form) 
    
"""
    For each of the following (Acct, Cat, Goal, Trans) I have an Add Route which is self-explanatory,
    an Edit Route, which I using expressly to pass an obj ID into a form, and a Mod Route, 
    which receives the populated form and updates the database on submit.
    
    This seems kludgy to me, but it's the only way I could find to pass the ID and object appropriately.

""" 
    
    
@app.route('/edit_goal/<int:id>/')
@login_required
def edit_goal(id):
    email = session['email']
    print 'Edit_goal says ID = ', id
    print (str(session['email']),'is on edit_goal')
    goal = Goals.query.get(id)
    form = EditGoalForm(obj=goal)
    form.category.choices = [(c.name,c.name) for c in Categories.query.filter_by(email=email)]
    return render_template('editgoal.html', form=form) 

    
@app.route("/mod_goal/", methods=['GET', 'POST'])
@login_required
def mod_goal():
    email = session['email']
    print (str(session['email']),'is on mod_goal')
    form = EditGoalForm()
    if request.method == 'POST':
        db_session.query(Goals).filter_by(id = form.id.data).\
    update({"category":form.category.data, "target":form.target.data, "description":form.description.data, "amount":form.amount.data}, synchronize_session=False)
        db_session.commit()
        flash('You modified a goal.')
        print (str(session['email']),'has successfully modified a goal')
        return redirect(url_for('home'))
    return render_template('editgoal.html', form=form)
    
    
@app.route("/add_trans/", methods=['GET', 'POST'])
@login_required
def add_trans():
    print (str(session['email']),'is on add_trans')
    email = session['email']
    form = TransactionForm()
    form.account.choices = [(a.name,a.name) for a in Accounts.query.filter_by(email=email).order_by(Accounts.name)]
    form.category.choices = [(c.name,c.name) for c in Categories.query.filter_by(email=email).order_by(Categories.name)]
    form.goal.choices = [(g.description,g.description) for g in Goals.query.filter_by(email=email).order_by(Goals.description)]
    if request.method == 'POST':
        if form.validate() == False:
            print ("validate failed: ",session['email'], form.account.data, form.category.data, form.notes.data, form.amount.data)
            return render_template('addtrans.html', form=form)
        else:
            newtrans = Transactions(str(session['email']), str(form.account.data), str(form.category.data), str(form.goal.data), today, str(form.notes.data), float(form.amount.data))
            print ("validated Transaction data: ", session['email'], form.account.data, form.category.data, str(today), form.notes.data, form.amount.data)
            db_session.add(newtrans)
            db_session.commit()
            flash('You created a new transaction.')
            print (str(session['email']),'has successfully added a new transaction')
            return redirect('/home')
    print ("submit failed: ",session['email'], form.account.data, form.category.data, today, form.notes.data, form.amount.data)
    return render_template('addtrans.html', form=form)


@app.route('/edit_trans/<int:id>/')
@login_required
def edit_trans(id):
    email = session['email']
    print 'Edit_Trans says ID = ', id
    print (str(session['email']),'is on edit_trans')
    acct = Transactions.query.get(id)
    form = EditTransForm(obj=acct)
    form.account.choices = [(a.name,a.name) for a in Accounts.query.filter_by(email=email).order_by(Accounts.name)]
    form.category.choices = [(c.name,c.name) for c in Categories.query.filter_by(email=email).order_by(Categories.name)]
    form.goal.choices = [(g.description,g.description) for g in Goals.query.filter_by(email=email).order_by(Goals.description)]
    return render_template('edittrans.html', form=form) 

    
@app.route("/mod_trans/", methods=['GET', 'POST'])
@login_required
def mod_trans():
    email = session['email']
    print (str(session['email']),'is on mod_trans')
    form = EditTransForm()
    if request.method == 'POST':
        db_session.query(Transactions).filter_by(id = form.id.data).\
    update({"account":form.account.data, "category":form.category.data, "goal":form.goal.data, "notes":form.notes.data, "amount":form.amount.data}, synchronize_session=False)
        db_session.commit()
        flash('You modified a transaction.')
        print (str(session['email']),'has successfully modified a transaction')
        return redirect(url_for('home'))
    return render_template('edittrans.html', form=form)
    

@app.route("/add_acct/", methods=['GET', 'POST'])
@login_required
def add_acct():
    print (str(session['email']),'is on add_acct')
    form = AccountForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('addacct.html', form=form)
        else:
            newacct = Accounts(form.name.data, session['email'])
            db_session.add(newacct)
            db_session.commit()
            flash('You created a new account.')
            print (str(session['email']),'has successfully added a new account')
            return redirect(url_for('home'))
    elif request.method == 'GET':
        print (str(session['email']),'is still on add_acct')
        return render_template('addacct.html', form=form)  
        
       
@app.route('/edit_acct/<int:id>/')
@login_required
def edit_acct(id):
    print 'Edit_Acct says ID = ', id
    print (str(session['email']),'is on edit_acct')
    acct = Accounts.query.get(id)
    form = EditAcctForm(obj=acct)
    return render_template('editacct.html', form=form) 

    
@app.route("/mod_acct/", methods=['GET', 'POST'])
@login_required
def mod_acct():
    print (str(session['email']),'is on mod_acct')
    form = EditAcctForm()
    if request.method == 'POST':
        db_session.query(Accounts).filter_by(id = form.id.data).\
    update({"name":form.name.data}, synchronize_session=False)
        db_session.commit()
        flash('You modified an account.')
        print (str(session['email']),'has successfully modified an account')
        return redirect(url_for('home'))
    return render_template('editacct.html', form=form) 
  
  
@app.route("/add_cat/", methods=['GET', 'POST'])
@login_required
def add_cat():
    print (str(session['email']),'is on add_cat')
    form = CategoryForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('addcat.html', form=form)
        else:
            newcat = Categories(form.name.data, session['email'])
            db_session.add(newcat)
            db_session.commit()
            flash('You created a new category.')
            print (str(session['email']),'has successfully<BR>added a new category')
            return redirect(url_for('home'))
    elif request.method == 'GET':
        print (str(session['email']),'is still on add_cat')
        return render_template('addcat.html', form=form)          



@app.route('/edit_cat/<int:id>/')
@login_required
def edit_cat(id):
    print 'Edit_Cat says ID = ', id
    print (str(session['email']),'is on edit_cat')
    cat = Categories.query.get(id)
    form = EditCatForm(obj=cat)
    return render_template('editcat.html', form=form) 

    
@app.route("/mod_cat/", methods=['GET', 'POST'])
@login_required
def mod_cat():
    print (str(session['email']),'is on mod_acct')
    form = EditAcctForm()
    if request.method == 'POST':
        db_session.query(Categories).filter_by(id = form.id.data).\
    update({"name":form.name.data}, synchronize_session=False)
        db_session.commit()
        flash('You modified a category.')
        print (str(session['email']),'has successfully modified a category')
        return redirect(url_for('home'))
    return render_template('editcat.html', form=form) 

        
# Delete transactions:
@app.route('/delete_trans/<int:id>/',)
@login_required
def delete_trans(id):
    con=engine.connect()
    con.execute('delete from transactions where id =:id', {"id":id} )
    flash('The transaction was deleted.')
    print (str(session['email']), 'deleted transaction ID: ', id)
    return redirect(url_for('home'))
    

    
# Delete account:
@app.route('/delete_acct/<int:id>/',)
@login_required
def delete_acct(id):
    con=engine.connect()
    con.execute('delete from accounts where id =:id', {"id":id} )
    flash('The account was deleted.')
    print (str(session['email']), 'deleted account ID: ', id)
    return redirect(url_for('home'))
    
# Delete category:
@app.route('/delete_cat/<int:id>/',)
@login_required
def delete_cat(id):
    con=engine.connect()
    con.execute('delete from categories where id =:id', {"id":id} )
    flash('The category was deleted.')
    print (str(session['email']), 'deleted category ID: ',id)
    return redirect(url_for('home'))   
    
# Delete goal:
@app.route('/delete_goal/<int:id>/',)
@login_required
def delete_goal(id):
    con=engine.connect()
    con.execute('delete from goals where id =:id', {"id":id} )
    flash('The goal was deleted.')
    print (str(session['email']), 'deleted goal ID: ',id)
    return redirect(url_for('home'))        
    
    
@app.route("/profile/")
@login_required
def profile():
    if 'email' in session:
        print (str(session['email']),'is on Profile')
    else:
        print('Guest is on Profile ... and this should never happen')
        
    usr = str(session['email'])
    #transactions by session user
    transactions = db_session.query(Transactions).filter(Transactions.email==usr).all()
    
    #accounts by session user
    accounts = db_session.query(Accounts).filter(Accounts.email==usr).all()
    
    #categories by session user
    categories = db_session.query(Categories).filter(Categories.email==usr).all()
    cat_cnt = db_session.query(func.count(Categories.id)).filter(Categories.email==usr)
  
    #progress by session user
    con=engine.connect()
    progress = con.execute("select transactions.category, sum(transactions.amount) as sum, goals.goal, ((sum(transactions.amount)/goals.goal )*100) as progress from transactions, goals where transactions.category=goals.category and transactions.email=:param group by transactions.category", {"param":session['email']} )
        
    return render_template('profile.html', progress=progress)
    
    
@app.route('/signout')
@login_required
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))
    flash('You have been logged out')
    print (str(session['email']),'has been logged out.')    
    session.pop('email', None)
    return redirect(url_for('index'))
    
if __name__ == "__main__":
    run.app()
