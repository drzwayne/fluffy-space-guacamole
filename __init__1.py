from flask import Flask, render_template, request, redirect, url_for, flash
from Forms import CreateUserForm, CreateCustomerForm
from Cart import Order
import shelve, User, Customer

from SimpleWebApplication import Cart1

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/cart')
def cart():
    db = shelve.open('cart.db', 'c')
    try:
        cart_dict = db['Cart']

    except:
        cart = Cart1.Order()



        return render_template('cart.html')
    return render_template('cart.html')

@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')
        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")
        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.gender.data, create_user_form.email.data, create_user_form.birthday.data, create_user_form.address.data, create_user_form.payment_method.data, create_user_form.credit_number.data, create_user_form.exp_number.data, create_user_form.remarks.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        db.close()
        return redirect(url_for('retrieve_users'))
    return render_template('createUser.html', form=create_user_form)
@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')
        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")
        customer = Customer.Customer(create_customer_form.first_name.data,create_customer_form.last_name.data, create_customer_form.gender.data, create_customer_form.membership.data, create_customer_form.remarks.data, create_customer_form.email.data, create_customer_form.date_joined.data, create_customer_form.address.data)
        customers_dict[customer.get_user_id()] = customer
        db['Customers'] = customers_dict
        db.close()
        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)
@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)
@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()
    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)
@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']
        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_email(update_user_form.email.data)
        user.set_birthday(update_user_form.birthday.data)
        user.set_address(update_user_form.address.data)
        user.set_payment_method(update_user_form.payment_method.data)
        user.set_credit_number(update_user_form.credit_number.data)
        user.set_exp_number(update_user_form.exp_number.data)
        user.set_remarks(update_user_form.remarks.data)
        db['Users'] = users_dict
        db.close()
        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()
        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.email.data = user.get_email()
        update_user_form.birthday.data = user.get_birthday()
        update_user_form.address.data = user.get_address()
        update_user_form.payment_method.data = user.get_payment_method()
        update_user_form.credit_number.data = user.get_credit_number()
        update_user_form.exp_number.data = user.get_exp_number()
        update_user_form.remarks.data = user.get_remarks()
        return render_template('updateUser.html', form=update_user_form)
@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']
    users_dict.pop(id)
    db['Users'] = users_dict
    db.close()
    return redirect(url_for('retrieve_users'))
@app.route('/deleteOrder/<int:id>', methods=['POST'])
def delete_order(id):
    orders_dict = {}
    db = shelve.open('order.db', 'w')
    orders_dict = db['Orders']
    orders_dict.pop(id)
    db['Orders'] = orders_dict
    db.close()
    return redirect(url_for('cart'))
if __name__ == '__main__':
    app.run()
