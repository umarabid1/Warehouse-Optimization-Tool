import matplotlib
matplotlib.use('Agg')  # ✅ Prevent GUI errors
import matplotlib.pyplot as plt
import pandas as pd
import os

def visualize_layout_with_labels(original_layout_file, optimized_layout_df, products_file):
    original_layout_df = pd.read_csv(original_layout_file)
    products_df = pd.read_csv(products_file)

    static_dir = "static"
    os.makedirs(static_dir, exist_ok=True)

    def create_layout(layout_df, title, filename, color, label_text):
        plt.figure(figsize=(8, 4))
        plt.scatter(layout_df['Aisle'], layout_df['Shelf'], color=color, s=200, label=label_text, edgecolors='black')

        for _, row in layout_df.iterrows():
            product_name = products_df.loc[products_df['Product_ID'] == row['Product_ID'], 'Product_Name'].values
            if len(product_name) > 0:
                plt.text(row['Aisle'], row['Shelf'] + 0.2, product_name[0], fontsize=8, ha='center', va='bottom',
                         color='white', bbox=dict(facecolor='black', alpha=0.7, boxstyle="round,pad=0.2"))

        plt.legend()
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.title(title)
        plt.savefig(os.path.join(static_dir, filename), bbox_inches='tight', pad_inches=0.3, dpi=100)
        plt.close()

    # ✅ Create Original Layout
    create_layout(original_layout_df, "Original Warehouse Layout", "warehouse_original.png", 'blue', "Original Layout")

    # ✅ Create Optimized Layout
    create_layout(optimized_layout_df, "Optimized Warehouse Layout", "warehouse_optimized.png", 'green', "Optimized Layout")
