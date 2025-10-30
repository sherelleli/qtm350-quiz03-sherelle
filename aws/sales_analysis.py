import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Read the retail sales data
with open('retail_sales.txt', 'r') as f:
    lines = f.readlines()

# Skip the header comment and read the data
data_str = ''.join(lines[1:])
from io import StringIO
df = pd.read_csv(StringIO(data_str), sep=r'\s+')

# Convert date column to datetime objects
df['date'] = pd.to_datetime(df['date'])

# Print basic statistics
print("Retail Sales Analysis:")
print("======================")
print(f"Total days analysed: {len(df)}")
print(f"Total sales revenue: ${df['revenue'].sum():,.2f}")
print(f"Average daily revenue: ${df['revenue'].mean():,.2f}")
best_day_idx = df['revenue'].idxmax()
best_day_date_str = str(df.at[best_day_idx, 'date'])
print(f"Best sales day: {best_day_date_str} with ${df.at[best_day_idx, 'revenue']:,.2f}")
print(f"Average transaction value: ${df['avg_transaction'].mean():.2f}")

# Find best-selling category
category_totals = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
print(f"Best-selling category: {category_totals.index[0]} with ${category_totals.iloc[0]:,.2f}")

# Create a visualisation
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
sns.set_style("whitegrid")

# Plot 1: Daily revenue trend
ax1.plot(df['date'], df['revenue'], marker='o', color='dodgerblue', linewidth=2)
ax1.set_xlabel('Date')
ax1.set_ylabel('Revenue ($)', color='black')
ax1.set_title('Daily Sales Revenue Trend', fontsize=14, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='black')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)

# Plot 2: Category performance
category_sales = df.groupby('category')['revenue'].sum().sort_values()
bars = ax2.barh(category_sales.index, category_sales.values, color=sns.color_palette("viridis", len(category_sales)))
ax2.set_xlabel('Total Revenue ($)')
ax2.set_title('Revenue by Product Category', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

# Add value labels on bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width + max(category_sales) * 0.01, bar.get_y() + bar.get_height()/2, 
             f'${width:,.0f}', ha='left', va='center')

plt.tight_layout()
fig.suptitle('30-Day Retail Sales Performance Report', fontsize=18, fontweight='bold', y=1.02)

# Save the figure
plt.savefig('sales_analysis.png', bbox_inches='tight', dpi=300)
print("\nAnalysis complete. Results saved to 'sales_analysis.png'")