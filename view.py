from flask import render_template, request, redirect, flash, session
from sqlalchemy.orm import aliased
from sqlalchemy import desc, asc
import database
import datetime
import models

# ///////////////////////////////Main Page, About Page Methods/////////////////////////


def start_page():
    """
    :return: Main Page.
    """
    if not session.get("Email") and not session.get("Password") and not session.get("ID"):
        return redirect("user/sign_in")
    return render_template('index.html')


def about():
    """
    :return: About Page.
    """
    return render_template('about.html')


# ///////////////////////////////The END///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////Cart Methods//////////////////////////////////////////

def cart():  # db alchemy done
    """
    Shows all dishes in cart.
    :return: data of all dishes in cart.
    """
    user_id = session['ID']
    order_status = 0
    order = database.db_session.query(models.Orders).filter(models.Orders.User == user_id,
                                                            models.Orders.Status == order_status).first()
    query = False
    try:
        ordered_dishes = aliased(models.OrderedDishes)
        dishes_ = aliased(models.Dishes)

        query = database.db_session.query(ordered_dishes, dishes_). \
            join(dishes_, ordered_dishes.dish == dishes_.ID). \
            filter(ordered_dishes.order_id == order.ID).all()

    except Exception as e:
        print("Помилка:", e)

    if request.method == 'POST':
        del_order = request.form.to_dict()
        if del_order:
            try:
                ord_id = database.db_session.query(models.Orders). \
                    filter(models.Orders.Status == 0,
                           models.Orders.User == int(session.get('ID'))).first()

                remove_order = database.db_session.query(models.OrderedDishes). \
                    filter(models.OrderedDishes.dish == int(del_order["dish"]),
                           models.OrderedDishes.order_id == ord_id.ID).first()
                database.db_session.delete(remove_order)
                database.db_session.commit()

            except Exception as e:
                print("Помилка:", e)
        return redirect('/cart')

    return render_template('cart.html',
                           result=query)


def cart_order():  # db alchemy done
    """
    :return: order_data for paying.
    """
    if request.method == 'POST':
        try:
            ord_id = database.db_session.query(models.Orders).filter(models.Orders.Status == 0,
                                                                     models.Orders.User == int(
                                                                         session.get('ID'))).first()
            ord_id.Status = 1
            database.db_session.commit()
            database.db_session.refresh(ord_id)
        except Exception as e:
            print("Помилка:", e)
        return redirect('/cart')
    if request.method == 'GET':
        try:
            result = database.db_session.query(models.Orders).filter(models.Orders.User == int(session.get('ID')),
                                                                     models.Orders.Status == 0).first()

            ordered_dishes = aliased(models.OrderedDishes)
            dishes_ = aliased(models.Dishes)

            dish_data = database.db_session.query(ordered_dishes, dishes_). \
                join(dishes_, ordered_dishes.dish == dishes_.ID). \
                filter(ordered_dishes.order_id == result.ID).all()
            return render_template('cart_order.html', result=result, dish_data=dish_data)
        except Exception as e:
            print("Помилка:", e)
        return render_template('cart_order.html')


def cart_add():  # db alchemy done
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'POST':
        # ordered_dishes_data = dict from html post method
        # ordered_dishes_data = {'dish': post_data(int), 'order_id': post_data(int), 'count': post_data(int)}
        ordered_dishes_data = request.form.to_dict()
        res = database.db_session.query(models.Orders).filter(models.Orders.User == int(session.get('ID')),
                                                              models.Orders.Status == 0).first()

        current_datetime = datetime.datetime.now()
        if res is not None:  # If Orders is not empty
            if res.User == int(session['ID']) and res.Status == 0:
                add_to_cart = models.OrderedDishes(dish=ordered_dishes_data['dish'],
                                                   count=ordered_dishes_data['count'],
                                                   order_id=res.ID)
                database.db_session.add(add_to_cart)
                database.db_session.commit()
                return redirect('/menu')
            elif res.User != int(session['ID']):
                #  get address
                address_id = database.db_session.query(models.Address). \
                             filter(models.Address.User == int(session.get('ID'))).first()
                try:
                    create_order = models.Orders(
                        User=int(session.get('ID')),
                        Address=int(address_id.ID),
                        Order_date=current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                        Status=0
                    )
                    database.db_session.add(create_order)
                    database.db_session.commit()
                    add_to_cart = models.OrderedDishes(dish=ordered_dishes_data['dish'],
                                                       count=ordered_dishes_data['count'],
                                                       order_id=res.ID)
                    database.db_session.add(add_to_cart)
                    database.db_session.commit()
                except Exception as e:
                    print("Помилка:", e)
        else:  # if Orders is empty
            # address id
            address_id = database.db_session.query(models.Address). \
                         filter(models.Address.User == int(session.get('ID'))).first()

            try:  # so creating data in Orders
                create_order = models.Orders(
                    User=int(session.get('ID')),
                    Address=int(address_id.ID),
                    Order_date=current_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    Status=0
                )
                database.db_session.add(create_order)
                database.db_session.commit()
                # taking data  from Orders
                res = database.db_session.query(models.Orders).filter(models.Orders.User == int(session.get('ID')),
                                                                      models.Orders.Status == 0).first()

                if res.User == int(session.get('ID')) and res.Status == 0:
                    add_to_cart = models.OrderedDishes(dish=ordered_dishes_data['dish'],
                                                       count=ordered_dishes_data['count'],
                                                       order_id=res.ID)
                    database.db_session.add(add_to_cart)
                    database.db_session.commit()
            except Exception as e:
                print("Помилка:", e)
            return redirect('/')
    return render_template('index.html')
# ///////////////////////////////The END///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////User Methods//////////////////////////////////////////


def user():  # db alchemy done
    """
    Different actions with user.
    methods=['GET', 'POST', 'PUT', 'DELETE']
    :return: user_data.
    """
    database.init_db()
    if session.get('ID') is None:
        return redirect('/user/sign_in')

    if request.method == 'GET' and session['ID'] is not None:
        user_info = database.db_session.query(models.User).where(models.User.ID == session.get('ID')).first()
        return render_template('user.html', result=user_info)


def user_update():  # db alchemy done
    database.init_db()
    if session.get('ID') is None:
        return redirect('/user/sign_in')

    if request.method == 'POST' and session['ID'] is not None:
        data = request.form.to_dict()

        current_user = database.db_session.query(models.User).filter(models.User.ID == session.get('ID')).first()

        current_user.Telephone = data['Telephone']
        current_user.Email = data['Email']
        current_user.Tg = data['Tg']
        current_user.Type = data['Type']

        database.db_session.commit()
        database.db_session.refresh(current_user)

        return redirect('/')
    return render_template('user_update.html')


def user_register():  # db alchemy done
    database.init_db()
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        try:
            register_user = models.User(Telephone=int(data['Telephone']),
                                        Password=data['Password'],
                                        Email=data['Email'],
                                        Tg=data['Tg'],
                                        Type=data['Type'])
            database.db_session.add(register_user)
            database.db_session.commit()
            return redirect('/user/sign_in')
        except Exception as e:
            print("Помилка:", e)
    return render_template('register.html')


def user_sign_in():  # db alchemy done
    """
    methods = [POST]
    :return:
    """
    database.init_db()
    if request.method == 'POST':
        data = request.form.to_dict()
        current_user = database.db_session.query(models.User).filter(models.User.Password == data['Password'],
                                                                     models.User.Email == data['Email']).first()

        if current_user is not None:
            flash('You logged in')
            session['ID'] = current_user.ID
            session['Telephone'] = current_user.Telephone
            session['Email'] = current_user.Email
            session['Password'] = current_user.Password
            session['Tg'] = current_user.Tg
            session['Type'] = current_user.Type
            return redirect('/')
        else:
            return '<p>Invalid data</p>'
    return render_template('sign_in.html')


def user_logout():  # db alchemy done
    """
    methods=['POST', 'GET']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    database.db_session.close()
    session['ID'] = None
    session['Email'] = None
    session['Password'] = None
    session['Type'] = None
    return redirect("/")


def user_restore():  # db alchemy done
    """
    methods=['POST']
    :return:
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            current_user = database.db_session.query(models.User).filter(models.User.Email == data['Email']).first()
            if current_user is not None:
                current_user.Password = data['Password']
                database.db_session.commit()
                return redirect('/user/sign_in')
        except Exception as e:
            print("Помилка:", e)
    return render_template('password_restore.html')


def user_orders_history():  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'GET':
        orders = database.db_session.query(models.Orders).filter(models.Orders.User == int(session.get('ID'))).all()
        return render_template('user_orders.html',
                               result=orders)


def user_order(order_id: int):  # db alchemy done
    """
    Shows user order
    methods=['GET']
    :return:
    """
    print(order_id)
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'GET':
        try:
            ordered_dishes = aliased(models.OrderedDishes)
            dishes_ = aliased(models.Dishes)

            query = database.db_session.query(ordered_dishes, dishes_). \
                join(dishes_, ordered_dishes.dish == dishes_.ID). \
                filter(ordered_dishes.order_id == int(order_id)).all()

            return render_template('user_order.html',
                                   result=query
                                   )
        except Exception as e:
            print("Помилка:", e)


def user_address_list():  # db alchemy done
    """
    methods=['GET', 'POST']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'GET':
        addresses = database.db_session.query(models.Address). \
            filter(models.Address.User == int(session.get('ID'))).all()

        return render_template('user_addresses.html', result=addresses)


def user_address_add():  # db alchemy done
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'POST':
        data = request.form.to_dict()
        address_post = models.Address(
            Town=data['Town'],
            Street=data['Street'],
            House=data['House'],
            Apt=data['Apt'],
            Block=data['Block'],
            Floor=data['Floor'],
            User=int(data['User'])
        )
        database.db_session.add(address_post)
        database.db_session.commit()
        database.db_session.refresh(address_post)
        return redirect('/user/addresses')
    return render_template('address_add.html', result=int(session.get('ID')))


def user_address(address_id: int):  # db alchemy done
    """
    methods=['GET', 'POST']
    :return:
    """
    print(address_id)
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'GET':
        data = database.db_session.query(models.Address).filter(models.Address.ID == int(address_id)).first()
        return render_template('user_address_edit.html', result=data)
    elif request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        address_edit = database.db_session.query(models.Address).filter(models.Address.ID == int(address_id)).first()
        address_edit.Town = data['Town']
        address_edit.Street = data['Street']
        address_edit.House = data['House']
        address_edit.Apt = data['Apt']
        address_edit.Block = data['Block']
        address_edit.Floor = data['Floor']
        address_edit.User = int(session.get('ID'))
        database.db_session.commit()
        database.db_session.refresh(address_edit)
        return redirect('/user/addresses')
    return render_template('user_addresses.html')


# ///////////////////////////////The END///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////Menu ,Category , Dish Methods/////////////////////////
def menu():  # db alchemy done
    if request.method == 'GET':
        return render_template('menu.html')


def categories():  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    if request.method == "GET":
        category_data = database.db_session.query(models.Category).all()
        return render_template('categories.html',
                               result=category_data)


def category_dishes(cat_id):  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    if request.method == "GET":
        dish_category = database.db_session.query(models.Dishes).filter(models.Dishes.Category == int(cat_id)).all()
        return render_template('category_dishes.html',
                               result=dish_category
                               )


def category_sort(cat_id, order_by, asc_desc_val):
    """
    methods=['GET']
    :return:
    """
    par = request.args
    print(par)
    if request.method == "GET":
        try:
            res = database.db_session.query(models.Dishes).order_by(desc(order_by)).all()
            return render_template('category_dishes.html',
                                   result=res
                                   )
        except Exception as e:
            print("Помилка:", e)


def dishes():  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    dish_data = database.db_session.query(models.Dishes).all()
    return render_template('category_dishes.html', result=dish_data
                           )


def dish(cat_id: int, dish_id: int):  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    admin_dish_edit(dish_id)
    if request.method == 'GET':
        dish_data = database.db_session.query(models.Dishes).filter(models.Dishes.ID == int(dish_id)).first()
        return render_template('dish.html',
                               result=dish_data)


def search():  # db alchemy done
    """
    methods=['GET', 'POST']
    :return:
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        dish_data_search = database.db_session.query(models.Dishes).filter(models.Dishes.Dish_name == data['search']).first()
        return render_template('dish.html',
                               result=dish_data_search
                               )
    return render_template('search.html')


def dish_sort(order_by_var, asc_desc_val):
    """
    methods=['GET', 'POST']
    :return:
    """

    if request.method == 'GET':
        print('order_by_var: ', order_by_var)
        if asc_desc_val == asc:
            res = database.db_session.query(models.Dishes).order_by(asc(order_by_var)).all()
            return render_template('category_dishes.html',
                                   result=res)
        else:
            res = database.db_session.query(models.Dishes).order_by(desc(order_by_var)).all()
            return render_template('category_dishes.html',
                                   result=res)


# ///////////////////////////////The END///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////Admin Methods/////////////////////////////////////////
def admin_dishes():  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'GET':
        if session['Type'] == 'Admin':
            dish_data = database.db_session.query(models.Dishes).all()
            return render_template('category_dishes.html', result=dish_data)


def admin_dish():  # db alchemy done
    """
    methods=['GET', 'POST']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'POST':
        data = request.form.to_dict()
        new_dish = models.Dishes(
            Dish_name=data['Dish_name'],
            Price=float(data['Price']),
            Description=data['Description'],
            Available=float(data['Available']),
            Category=float(data['Category']),
            Photo=data['Photo'],
            Ccal=float(data['Ccal']),
            Protein=float(data['Protein']),
            Fat=float(data['Fat']),
            Carb=float(data['Carb'])
        )
        database.db_session.add(new_dish)
        database.db_session.commit()
        return redirect('/admin/dishes')
    category_data = database.db_session.query(models.Category).all()
    return render_template('add_dish.html', cat_data=category_data)


def admin_dish_edit(dish_id):  # db alchemy done
    print(request.method)
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    dish_edit_data = database.db_session.query(models.Dishes).filter(models.Dishes.ID == dish_id).first()
    category_data = database.db_session.query(models.Category).all()
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            result = database.db_session.query(models.Dishes).filter(models.Dishes.ID == dish_id).first()
            result.Dish_name = data['Dish_name']
            result.Price = float(data['Price'])
            result.Description = data['Description']
            result.Available = int(data['Available'])
            result.Category = int(data['Category'])
            result.Photo = data['Photo']
            result.Ccal = float(data['Ccal'])
            result.Protein = float(data['Protein'])
            result.Fat = float(data['Fat'])
            result.Carb = float(data['Carb'])
            database.db_session.commit()
            if result:
                return redirect('/admin/dishes')
        except Exception as e:
            print("Помилка:", e)
    return render_template('dish_edit.html', result=dish_edit_data, cat_data=category_data)


def delete_dish(dish_id):  # db alchemy done
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            del_data = database.db_session.query(models.Dishes).where(models.Dishes.ID == int(data['ID'])).first()
            database.db_session.delete(del_data)
            database.db_session.commit()
        except Exception as e:
            print("Помилка:", e)
    return redirect('/admin/dishes')


def admin_orders():  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'GET':
        in_progress_orders = database.db_session.query(models.Orders).where(models.Orders.Status == 1).all()
        done_orders = database.db_session.query(models.Orders).where(models.Orders.Status == 2).all()
        return render_template('orders.html',
                               progress=in_progress_orders,
                               done=done_orders
                               )


def admin_order(order_id: int):  # db alchemy done
    """
    methods=['GET', 'POST']
    :return:
    """
    print(request.method)
    print(order_id)
    if session.get('ID') is None:
        return redirect('/user/sign_in')

    ordered_dishes = aliased(models.OrderedDishes)
    dishes_ = aliased(models.Dishes)

    ordered_dishes = database.db_session.query(ordered_dishes, dishes_). \
        join(dishes_, ordered_dishes.dish == dishes_.ID). \
        filter(ordered_dishes.order_id == int(order_id)).all()
    order_data = database.db_session.query(models.Orders).where(models.Orders.ID == order_id)
    if request.method == "POST":
        try:
            status_update = database.db_session.query(models.Orders).where(models.Orders.ID == order_id).first()
            status_update.Status = 2
            database.db_session.commit()
        except Exception as e:
            print("Помилка:", e)
        return redirect('/admin/orders')

    return render_template('order.html',
                           result=order_data,
                           dish_data=ordered_dishes
                           )


def admin_sort_order_status():
    """
    methods=['GET']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    return


def admin_set_order_status():
    """
    methods=['POST']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    return


def admin_show_categories():  # db alchemy done
    """
    methods=['GET']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == "GET":
        category_data = database.db_session.query(models.Category).all()
        return render_template('categories.html',
                               result=category_data)


def admin_category_edit():  # db alchemy done
    """
    methods=['POST', 'DELETE']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')
    if request.method == 'POST':
        data = request.form.to_dict()
        add_category = models.Category(
            Name=data['Name']
        )
        database.db_session.add(add_category)
        database.db_session.commit()
        return redirect('/admin/categories')
    return render_template('admin_categories.html')


def admin_search():  # working with regular user search in template
    """
    methods=['GET']
    :return:
    """
    if session.get('ID') is None:
        return redirect('/user/sign_in')

# ///////////////////////////////The END///////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////
