from flask import Flask, render_template, request, jsonify, send_file
import os
import pandas as pd
from optimization import optimize_layout
from visualization import visualize_layout_with_labels  # ✅ Import visualization

app = Flask(__name__)

optimized_layout_df = None  # ✅ Global variable for storing optimized layout

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_files():
    global optimized_layout_df  # ✅ Ensure correct variable scope

    try:
        if "layout" not in request.files or "orders" not in request.files or "products" not in request.files:
            return jsonify({"error": "Missing one or more CSV files"}), 400

        layout_file = request.files["layout"]
        orders_file = request.files["orders"]
        products_file = request.files["products"]

        # ✅ Ensure upload directory exists
        os.makedirs("uploads", exist_ok=True)
        layout_path = "uploads/layout.csv"
        orders_path = "uploads/orders.csv"
        products_path = "uploads/products.csv"

        layout_file.save(layout_path)
        orders_file.save(orders_path)
        products_file.save(products_path)

        # ✅ Run optimization
        optimized_layout_df = optimize_layout(layout_path, orders_path, products_path)

        # ✅ Debugging Output
        print("✅ Optimization Completed Successfully")
        return jsonify({"message": "Files uploaded and optimization complete!"})

    except Exception as e:
        print(f"❌ Upload Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/get_layouts", methods=["GET"])
def get_layouts():
    try:
        return jsonify({
            "original": "/static/warehouse_original.png",
            "optimized": "/static/warehouse_optimized.png"
        })
    except Exception as e:
        print(f"❌ Layouts Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/download_optimized")
def download_optimized():
    file_path = "optimized_layout.csv"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

@app.route("/get_optimized_layout", methods=["GET"])
def get_optimized_layout():
    global optimized_layout_df  # ✅ Ensure we reference the correct global variable

    if optimized_layout_df is None:
        return jsonify({"error": "No data available. Upload first!"}), 400

    # ✅ Convert DataFrame to JSON
    return jsonify(optimized_layout_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
