from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_menu():
    connection = sqlite3.connect("cafeteria.db")
    connection.row_factory = sqlite3.Row

    menu = connection.execute(
        "SELECT * FROM menu_items"
    ).fetchall()

    connection.close()

    return menu


@app.route("/")
def home():
    menu = get_menu()
    return render_template("menu.html", menu=menu)
    
@app.route("/admin")
def admin():
    menu = get_menu()

    connection = sqlite3.connect("cafeteria.db")
    connection.row_factory = sqlite3.Row

    orders = connection.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        menu=menu,
        orders=orders
    )
    
@app.route("/admin/add", methods=["POST"])
def add_food():
    name = request.form["name"]
    price = request.form["price"]

    connection = sqlite3.connect("cafeteria.db")

    connection.execute(
        "INSERT INTO menu_items (name, price, available) VALUES (?, ?, ?)",
        (name, price, 1)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")

@app.route("/admin/delete/<int:item_id>", methods=["POST"])
def delete_food(item_id):

    connection = sqlite3.connect("cafeteria.db")

    connection.execute(
        "DELETE FROM menu_items WHERE id = ?",
        (item_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")

@app.route("/admin/toggle/<int:item_id>", methods=["POST"])
def toggle_availability(item_id):

    connection = sqlite3.connect("cafeteria.db")

    connection.execute(
        """
        UPDATE menu_items
        SET available = CASE
            WHEN available = 1 THEN 0
            ELSE 1
        END
        WHERE id = ?
        """,
        (item_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")

@app.route("/admin/edit/<int:item_id>", methods=["GET", "POST"])
def edit_food(item_id):

    connection = sqlite3.connect("cafeteria.db")
    connection.row_factory = sqlite3.Row

    item = connection.execute(
        "SELECT * FROM menu_items WHERE id = ?",
        (item_id,)
    ).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        connection.execute(
            """
            UPDATE menu_items
            SET name = ?, price = ?, quantity = ?
            WHERE id = ?
            """,
            (name, price, quantity, item_id)
        )

        connection.commit()
        connection.close()

        return redirect("/admin")

    connection.close()

    return render_template("edit.html", item=item)

@app.route("/place-order", methods=["POST"])
def place_order():

    items = request.form["items"]
    total = request.form["total"]

    connection = sqlite3.connect("cafeteria.db")

    # Create the order first
    cursor = connection.execute(
        """
        INSERT INTO orders (order_number, items, total, status)
        VALUES (?, ?, ?, ?)
        """,
        ("TEMP", items, total, "Pending")
    )

    order_id = cursor.lastrowid

    # Create a proper order number
    order_number = f"ORD-{1000 + order_id}"

    # Update the order with the real order number
    connection.execute(
        """
        UPDATE orders
        SET order_number = ?
        WHERE id = ?
        """,
        (order_number, order_id)
    )

    connection.commit()

    status = "Pending"

    connection.close()

    return render_template(
        "order_confirmation.html",
        order_number=order_number,
        total=total,
        status=status
    )

@app.route("/admin/order/<int:order_id>/status", methods=["POST"])
def update_order_status(order_id):

    status = request.form["status"]

    connection = sqlite3.connect("cafeteria.db")

    connection.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE id = ?
        """,
        (status, order_id)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")

@app.route("/order-status/<order_number>")
def order_status(order_number):

    connection = sqlite3.connect("cafeteria.db")
    connection.row_factory = sqlite3.Row

    order = connection.execute(
        "SELECT * FROM orders WHERE order_number = ?",
        (order_number,)
    ).fetchone()

    connection.close()

    if not order:
        return "Order not found"

    return render_template(
        "order_status.html",
        order=order
    )

if __name__ == "__main__":
    app.run(debug=True)