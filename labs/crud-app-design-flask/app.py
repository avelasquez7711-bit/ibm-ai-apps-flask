# import libraries
from flask import Flask, request, url_for, redirect, render_template

# instantiate Flask functionality
app = Flask(__name__)

# sample data
transactions = [
    {"id": 1, "date": "2023-06-01", "amount": 100},
    {"id": 2, "date": "2023-06-02", "amount": -200},
    {"id": 3, "date": "2023-06-03", "amount": 300},
]


# route to list all transactions
@app.route("/", methods=["GET"])
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# route to handle transaction creation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # check if request method is POST (form submission)
    if request.method == "POST":
        # create new transaction object using form field values
        transaction = {
            "id": len(transactions)
            + 1,  # generate new ID based on current len transactions list
            "date": request.form["date"],  # get 'date' field value from form
            "amount": float(
                request.form["amount"]
            ),  # get 'amount' field value from form and convert to a float
        }
        # append new transaction to transactions list
        transactions.append(transaction)

        # redirect to transactions list page after adding new transaction
        return redirect(url_for("get_transactions"))

    # if request method is GET, render form template to display the add transaction form
    return render_template("form.html")


# route to handle transaction editing
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # check if request method is POST (form submission)
    if request.method == "POST":
        # get updated values from form fields
        date = request.form["date"]
        amount = float(request.form["amount"])

        # find transaction with matching ID and update values
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = date
                transaction["amount"] = amount
                break  # exit loop if transaction found and updated

        # redirect to transaction list page after update
        return redirect(url_for("get_transactions"))

    # if request method if GET, find transaction with matching ID and render edit form
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            # render edit form template and pass transaction to be edited
            return render_template("edit.html", transaction=transaction)

    # if transaction not found return JSON message and 404 code
    return {"message": "Transaction not found"}, 404


# route to handle transaction deletion
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # find transaction with matchig ID and remove from list
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            break

    # redirect to transactions list page
    return redirect(url_for("get_transactions"))


# route to handle transaction search
@app.route("/search", methods=["GET", "POST"])
def search_transaction():
    if request.method == "POST":
        min_amount = float(request.form["min_amount"])
        max_amount = float(request.form["max_amount"])

        filtered_transaction = []

        for transaction in transactions:
            transaction_amount = transaction["amount"]
            if transaction_amount >= min_amount and transaction_amount <= max_amount:
                filtered_transaction.append(transaction)

        return render_template("transactions.html", transactions=filtered_transaction)

    return render_template("search.html")


# run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
