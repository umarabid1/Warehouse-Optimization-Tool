import pandas as pd
from scipy.optimize import linear_sum_assignment
import numpy as np

def optimize_layout(layout_file, orders_file, products_file):
    layout_df = pd.read_csv(layout_file)
    orders_df = pd.read_csv(orders_file)
    products_df = pd.read_csv(products_file)

    # 🚀 Ensure the correct columns exist
    print("📊 Layout Columns:", layout_df.columns.tolist())
    print("📦 Orders Columns:", orders_df.columns.tolist())

    if "Aisle" not in layout_df.columns or "Shelf" not in layout_df.columns:
        raise KeyError("❌ 'Aisle' or 'Shelf' column is missing in Layout CSV!")

    if "Product_ID" not in layout_df.columns:
        raise KeyError("❌ 'Product_ID' column missing in Layout CSV!")

    demand = orders_df.groupby("Product_ID")["Quantity"].sum()
    layout_df["Demand"] = layout_df["Product_ID"].map(demand).fillna(0)

    layout_df = layout_df.sort_values(by="Demand", ascending=False)

    # ✅ Send full data structure to avoid undefined issues
    optimized_layout = layout_df[["Product_ID", "Product_Name", "Aisle", "Shelf"]]
    
    print("🚀 Optimized Layout Generated:", optimized_layout.to_dict(orient="records"))

    return optimized_layout
