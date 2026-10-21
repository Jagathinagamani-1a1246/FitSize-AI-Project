from flask import Flask, render_template, request, redirect, url_for, flash
from src.database import init_db, get_products, get_product, save_feedback, get_feedback_summary
from src.recommender import recommend_sizes

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-before-deployment"

init_db()


@app.route("/", methods=["GET"])
def index():
    categories = ["T-shirt", "Shirt", "Jeans", "Dress", "Jacket"]
    products = get_products()
    return render_template("index.html", products=products, categories=categories)


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        product_id = int(request.form.get("product_id", ""))
        product = get_product(product_id)
        if not product:
            flash("Please select a valid product.", "error")
            return redirect(url_for("index"))

        unit = request.form.get("unit", "cm")
        factor = 2.54 if unit == "in" else 1.0
        body = {
            "chest": float(request.form.get("chest", "")) * factor,
            "waist": float(request.form.get("waist", "")) * factor,
            "hip": float(request.form.get("hip", "")) * factor,
        }
        preference = request.form.get("fit_preference", "regular")
        if preference not in {"snug", "regular", "loose"}:
            preference = "regular"
        if any(v <= 0 or v > 250 for v in body.values()):
            raise ValueError("Measurements must be positive and within a reasonable range.")

        results = recommend_sizes(product, body, preference)
        if not results:
            flash("This product has no size-chart entries yet.", "error")
            return redirect(url_for("index"))

        return render_template(
            "result.html",
            product=product,
            body=body,
            preference=preference,
            results=results,
            unit_label="cm",
        )
    except (ValueError, TypeError):
        flash("Enter valid numeric measurements for chest, waist, and hip.", "error")
        return redirect(url_for("index"))


@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        product_id = int(request.form["product_id"])
        size_label = request.form["size_label"].strip()
        fit_label = request.form["fit_label"].strip()
        if fit_label not in {"small", "fit", "large"}:
            raise ValueError
        save_feedback(product_id, size_label, fit_label)
        flash("Thank you! Your feedback has been saved.", "success")
    except (KeyError, ValueError, TypeError):
        flash("Feedback could not be saved. Please try again.", "error")
    return redirect(url_for("index"))


@app.route("/about")
def about():
    summary = get_feedback_summary()
    return render_template("about.html", summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
