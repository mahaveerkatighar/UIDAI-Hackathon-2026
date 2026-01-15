"""
UIDAI Data Hackathon 2026 - Hyderabad District Analysis
Data Analyst: Aadhaar Enrolment and Update Behavior Analysis

This script analyzes Aadhaar enrolment and update patterns in Hyderabad district
to identify trends, peak loads, and service improvement opportunities.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set plotting style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("="*80)
print("UIDAI DATA HACKATHON 2026 - HYDERABAD DISTRICT ANALYSIS")
print("="*80)
print()

# ============================================================================
# STEP 1: LOAD ALL EXCEL FILES
# ============================================================================
print("STEP 1: Loading Excel Files...")
print("-"*80)

# ============================================================================
# CONFIGURATION - PASTE YOUR CSV FILE PATHS HERE
# ============================================================================
# Just paste the full path to each CSV file below (right-click file > Copy as path)
# Make sure to keep the r before the quotes

ENROLMENT_FILE = r'D:\UIDAI\aadhaar_monthly_enrolment.csv'
BIOMETRIC_FILE = r'D:\UIDAI\aadhaar_biometric_update.csv'
DEMOGRAPHIC_FILE = r'D:\UIDAI\aadhaar_demographic_update.csv'

# Example:
# ENROLMENT_FILE = r'D:\UIDAI\aadhaar_monthly_enrolment.csv'
# BIOMETRIC_FILE = r'D:\UIDAI\aadhaar_biometric_update.csv'
# DEMOGRAPHIC_FILE = r'D:\UIDAI\aadhaar_demographic_update.csv'

print("="*80)
print("UIDAI DATA HACKATHON 2026 - HYDERABAD DISTRICT ANALYSIS")
print("="*80)
print()

# ============================================================================
# STEP 1: LOAD ALL EXCEL FILES
# ============================================================================
print("STEP 1: Loading Excel Files...")
print("-"*80)

# Check if paths are set
if 'PASTE_PATH_HERE' in ENROLMENT_FILE or 'PASTE_PATH_HERE' in BIOMETRIC_FILE or 'PASTE_PATH_HERE' in DEMOGRAPHIC_FILE:
    print("❌ ERROR: Please update the file paths at the top of the script!")
    print("\nInstructions:")
    print("1. Right-click on each Excel file")
    print("2. Select 'Copy as path'")
    print("3. Paste it in the script replacing 'PASTE_PATH_HERE'")
    print("\nExample:")
    print("ENROLMENT_FILE = r'D:\\UIDAI\\aadhaar_monthly_enrolment.xlsx'")
    exit()

try:
    # Remove any quotation marks from the file paths (in case they were copied with quotes)
    enrolment_file = ENROLMENT_FILE.strip('"').strip("'")
    biometric_file = BIOMETRIC_FILE.strip('"').strip("'")
    demographic_file = DEMOGRAPHIC_FILE.strip('"').strip("'")
    
    print(f"Loading CSV files:")
    print(f"  1. {enrolment_file}")
    print(f"  2. {biometric_file}")
    print(f"  3. {demographic_file}")
    print()
    
    # Read CSV files
    enrolment_df = pd.read_csv(enrolment_file)
    biometric_df = pd.read_csv(biometric_file)
    demographic_df = pd.read_csv(demographic_file)
    
    print("✓ All 3 files loaded successfully!")
    print(f"  - Enrolment data: {enrolment_df.shape[0]} rows, {enrolment_df.shape[1]} columns")
    print(f"  - Biometric update data: {biometric_df.shape[0]} rows, {biometric_df.shape[1]} columns")
    print(f"  - Demographic update data: {demographic_df.shape[0]} rows, {demographic_df.shape[1]} columns")
    print()
    
except FileNotFoundError as e:
    print(f"\n❌ ERROR: Could not find file")
    print(f"Details: {e}")
    print("\nPlease check:")
    print("  1. File paths are correct")
    print("  2. Files exist at the specified locations")
    print("  3. File names are spelled correctly")
    exit()

# ============================================================================
# STEP 2: INSPECT DATA STRUCTURE
# ============================================================================
print("STEP 2: Inspecting Data Structure...")
print("-"*80)

print("\n📊 ENROLMENT DATA STRUCTURE:")
print(enrolment_df.head())
print(f"\nColumns: {list(enrolment_df.columns)}")
print(f"Data types:\n{enrolment_df.dtypes}")

print("\n📊 BIOMETRIC UPDATE DATA STRUCTURE:")
print(biometric_df.head())
print(f"\nColumns: {list(biometric_df.columns)}")
print(f"Data types:\n{biometric_df.dtypes}")

print("\n📊 DEMOGRAPHIC UPDATE DATA STRUCTURE:")
print(demographic_df.head())
print(f"\nColumns: {list(demographic_df.columns)}")
print(f"Data types:\n{demographic_df.dtypes}")
print()

# ============================================================================
# STEP 3: DATA CLEANING
# ============================================================================
print("STEP 3: Cleaning Data...")
print("-"*80)

def clean_dataset(df, dataset_name):
    """
    Clean dataset by removing duplicates, handling missing values,
    and standardizing date formats.
    """
    print(f"\nCleaning {dataset_name}...")
    
    # Initial row count
    initial_rows = len(df)
    
    # Remove duplicates
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    
    # Check for missing values
    missing_before = df.isnull().sum().sum()
    
    # Remove rows with all NaN values
    df = df.dropna(how='all')
    
    # Remove rows where critical columns are missing
    # (We'll identify critical columns based on column names)
    critical_cols = [col for col in df.columns if any(keyword in col.lower() 
                     for keyword in ['date', 'month', 'count', 'total'])]
    
    if critical_cols:
        df = df.dropna(subset=critical_cols, how='any')
    
    missing_after = df.isnull().sum().sum()
    
    # Standardize date/month columns
    date_columns = [col for col in df.columns if any(keyword in col.lower() 
                    for keyword in ['date', 'month', 'year'])]
    
    for col in date_columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                pass
    
    # Convert numeric columns to proper types
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['count', 'total', 'number']):
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Final cleanup - remove any rows created by conversion errors
    df = df.dropna(subset=critical_cols, how='any')
    
    print(f"  ✓ Duplicates removed: {duplicates_removed}")
    print(f"  ✓ Missing values before: {missing_before}, after: {missing_after}")
    print(f"  ✓ Final rows: {len(df)}")
    
    return df

# Clean all datasets
enrolment_clean = clean_dataset(enrolment_df, "Enrolment Data")
biometric_clean = clean_dataset(biometric_df, "Biometric Update Data")
demographic_clean = clean_dataset(demographic_df, "Demographic Update Data")

print("\n✓ Data cleaning completed!")
print()

# ============================================================================
# STEP 4: DATA PREPARATION AND AGGREGATION
# ============================================================================
print("STEP 4: Preparing Data for Analysis...")
print("-"*80)

# Function to prepare monthly aggregated data
def prepare_monthly_data(df, dataset_type):
    """
    Prepare monthly aggregated data from the dataset.
    For this UIDAI data, we need to sum all age-group columns.
    """
    # Find date column
    date_col = None
    for col in df.columns:
        if 'date' in col.lower():
            date_col = col
            break
    
    if date_col is None:
        print(f"  ⚠ Warning: Could not find date column in {dataset_type}")
        return pd.DataFrame()
    
    # Ensure date column is datetime
    df_copy = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_col]):
        df_copy[date_col] = pd.to_datetime(df_copy[date_col], format='%d-%m-%Y', errors='coerce')
    
    # Find all numeric columns (these are the age group columns)
    numeric_cols = df_copy.select_dtypes(include=[np.number]).columns.tolist()
    # Remove pincode if present
    numeric_cols = [col for col in numeric_cols if 'pincode' not in col.lower()]
    
    if not numeric_cols:
        print(f"  ⚠ Warning: Could not find numeric columns in {dataset_type}")
        return pd.DataFrame()
    
    print(f"  ℹ Summing columns for {dataset_type}: {numeric_cols}")
    
    # Calculate total for each row (sum of all age groups)
    df_copy['Total'] = df_copy[numeric_cols].sum(axis=1)
    
    # Extract year-month for grouping
    df_copy['YearMonth'] = df_copy[date_col].dt.to_period('M')
    
    # Aggregate by month
    monthly_agg = df_copy.groupby('YearMonth')['Total'].sum().reset_index()
    monthly_agg.columns = ['Month', dataset_type]
    monthly_agg['Month'] = monthly_agg['Month'].dt.to_timestamp()
    
    return monthly_agg.sort_values('Month')

# Prepare monthly aggregated data for each dataset
print("\nAggregating data by month...")
enrolment_monthly = prepare_monthly_data(enrolment_clean, 'Enrolments')
biometric_monthly = prepare_monthly_data(biometric_clean, 'Biometric_Updates')
demographic_monthly = prepare_monthly_data(demographic_clean, 'Demographic_Updates')

print("✓ Monthly aggregation completed!")
print(f"  - Enrolment months: {len(enrolment_monthly)}")
print(f"  - Biometric update months: {len(biometric_monthly)}")
print(f"  - Demographic update months: {len(demographic_monthly)}")
print()

# ============================================================================
# STEP 5: EXPLORATORY DATA ANALYSIS
# ============================================================================
print("STEP 5: Performing Exploratory Data Analysis...")
print("-"*80)

# Create visualizations directory
import os
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

# VISUALIZATION 1: Monthly Trend of Aadhaar Enrolments
if not enrolment_monthly.empty:
    plt.figure(figsize=(14, 6))
    plt.plot(enrolment_monthly['Month'], enrolment_monthly['Enrolments'], 
             marker='o', linewidth=2, markersize=6, color='#2E86AB')
    plt.title('Monthly Aadhaar Enrolment Trend - Hyderabad District', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Enrolments', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('visualizations/1_enrolment_trend.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Visualization 1 saved: Monthly Enrolment Trend")

# VISUALIZATION 2: Monthly Trend of Biometric Updates
if not biometric_monthly.empty:
    plt.figure(figsize=(14, 6))
    plt.plot(biometric_monthly['Month'], biometric_monthly['Biometric_Updates'], 
             marker='s', linewidth=2, markersize=6, color='#A23B72')
    plt.title('Monthly Biometric Update Trend - Hyderabad District', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Biometric Updates', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('visualizations/2_biometric_trend.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Visualization 2 saved: Biometric Update Trend")

# VISUALIZATION 3: Monthly Trend of Demographic Updates
if not demographic_monthly.empty:
    plt.figure(figsize=(14, 6))
    plt.plot(demographic_monthly['Month'], demographic_monthly['Demographic_Updates'], 
             marker='^', linewidth=2, markersize=6, color='#F18F01')
    plt.title('Monthly Demographic Update Trend - Hyderabad District', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Demographic Updates', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('visualizations/3_demographic_trend.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Visualization 3 saved: Demographic Update Trend")

# VISUALIZATION 4: Comparison of All Three Services
# Merge all datasets for comparison
if not enrolment_monthly.empty and not biometric_monthly.empty and not demographic_monthly.empty:
    merged_data = enrolment_monthly.copy()
    merged_data = merged_data.merge(biometric_monthly, on='Month', how='outer')
    merged_data = merged_data.merge(demographic_monthly, on='Month', how='outer')
    merged_data = merged_data.sort_values('Month').fillna(0)
elif not enrolment_monthly.empty:
    merged_data = enrolment_monthly.copy()
else:
    print("⚠ Warning: No data available for comparison")
    merged_data = pd.DataFrame()

if not merged_data.empty:
    plt.figure(figsize=(14, 7))
    if 'Enrolments' in merged_data.columns:
        plt.plot(merged_data['Month'], merged_data['Enrolments'], 
                 marker='o', linewidth=2, label='Enrolments', color='#2E86AB')
    if 'Biometric_Updates' in merged_data.columns:
        plt.plot(merged_data['Month'], merged_data['Biometric_Updates'], 
                 marker='s', linewidth=2, label='Biometric Updates', color='#A23B72')
    if 'Demographic_Updates' in merged_data.columns:
        plt.plot(merged_data['Month'], merged_data['Demographic_Updates'], 
                 marker='^', linewidth=2, label='Demographic Updates', color='#F18F01')

    plt.title('Comparison: Enrolments vs Updates - Hyderabad District', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('visualizations/4_comparison_all_services.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Visualization 4 saved: Service Comparison")

# VISUALIZATION 5: Peak Month Identification
if not merged_data.empty:
    # Calculate total service load (sum of all services per month)
    merged_data['Total_Load'] = merged_data.get('Enrolments', 0) + \
                                 merged_data.get('Biometric_Updates', 0) + \
                                 merged_data.get('Demographic_Updates', 0)

    # Identify top 5 peak months
    top_months = merged_data.nlargest(5, 'Total_Load')

    plt.figure(figsize=(12, 6))
    colors = ['#C1121F' if x in top_months['Total_Load'].values else '#669BBC' 
              for x in merged_data['Total_Load']]
    plt.bar(range(len(merged_data)), merged_data['Total_Load'], color=colors)
    plt.title('Peak Service Load Months - Hyderabad District', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Month Index', fontsize=12)
    plt.ylabel('Total Service Load (All Services Combined)', fontsize=12)
    plt.xticks(range(len(merged_data)), 
               merged_data['Month'].dt.strftime('%b %Y'), 
               rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('visualizations/5_peak_months.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Visualization 5 saved: Peak Month Identification")
else:
    print("⚠ Warning: No merged data available for peak month analysis")
    top_months = pd.DataFrame()
print()

# ============================================================================
# STEP 6: GENERATE INSIGHTS AND RECOMMENDATIONS
# ============================================================================
print("="*80)
print("KEY INSIGHTS AND RECOMMENDATIONS")
print("="*80)
print()

# Calculate statistics for insights
total_enrolments = enrolment_monthly['Enrolments'].sum() if not enrolment_monthly.empty else 0
total_biometric = biometric_monthly['Biometric_Updates'].sum() if not biometric_monthly.empty else 0
total_demographic = demographic_monthly['Demographic_Updates'].sum() if not demographic_monthly.empty else 0

avg_enrolments = enrolment_monthly['Enrolments'].mean() if not enrolment_monthly.empty else 0
avg_biometric = biometric_monthly['Biometric_Updates'].mean() if not biometric_monthly.empty else 0
avg_demographic = demographic_monthly['Demographic_Updates'].mean() if not demographic_monthly.empty else 0

# Peak month statistics
if not merged_data.empty and 'Total_Load' in merged_data.columns:
    peak_month = top_months.iloc[0] if not top_months.empty else None
    peak_month_name = peak_month['Month'].strftime('%B %Y') if peak_month is not None else 'N/A'
    peak_load = peak_month['Total_Load'] if peak_month is not None else 0
    avg_load = merged_data['Total_Load'].mean()
    peak_vs_avg = ((peak_load - avg_load) / avg_load * 100) if avg_load > 0 else 0
else:
    peak_month_name = 'N/A'
    peak_load = 0
    avg_load = 0
    peak_vs_avg = 0

# Generate insights
insights = f"""
INSIGHT 1: Service Demand Pattern
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Finding:
   • Total Enrolments: {total_enrolments:,.0f}
   • Total Biometric Updates: {total_biometric:,.0f}
   • Total Demographic Updates: {total_demographic:,.0f}
   • Average monthly enrolments: {avg_enrolments:,.0f}
   • Average monthly biometric updates: {avg_biometric:,.0f}
   • Average monthly demographic updates: {avg_demographic:,.0f}

💡 Insight:
   Update services (biometric and demographic) show {'higher' if (total_biometric + total_demographic) > total_enrolments else 'lower'} 
   total volume compared to fresh enrolments, indicating {'strong' if (total_biometric + total_demographic) > total_enrolments else 'developing'} 
   awareness about Aadhaar maintenance among existing holders in Hyderabad.

✅ RECOMMENDATION:
   • Expand update service counters at existing enrolment centers
   • Train enrolment operators to handle both enrolments and updates efficiently
   • Implement a fast-track queue system for simple updates vs fresh enrolments
   • Launch awareness campaigns explaining the importance of keeping Aadhaar updated

INSIGHT 2: Peak Load Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Finding:
   • Peak month: {peak_month_name}
   • Peak load: {peak_load:,.0f} total services
   • Average monthly load: {avg_load:,.0f} total services
   • Peak exceeds average by: {peak_vs_avg:.1f}%

💡 Insight:
   Specific months show significantly higher service demand, creating potential 
   bottlenecks and longer waiting times for residents. This seasonal pattern 
   requires proactive resource planning.

✅ RECOMMENDATION:
   • Deploy mobile Aadhaar enrolment units during peak months
   • Hire temporary staff 2-3 weeks before anticipated peak periods
   • Extend service hours (early morning/evening slots) during high-demand months
   • Implement online appointment booking to distribute load throughout the day
   • Partner with local community centers to set up temporary service points

INSIGHT 3: Service Efficiency Opportunity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Finding:
   • Monthly service variance indicates fluctuating demand patterns
   • Biometric updates show {'consistent' if biometric_monthly['Biometric_Updates'].std() < biometric_monthly['Biometric_Updates'].mean() else 'variable'} monthly trends
   • Demographic updates show {'consistent' if demographic_monthly['Demographic_Updates'].std() < demographic_monthly['Demographic_Updates'].mean() else 'variable'} monthly trends

💡 Insight:
   The variability in update requests suggests that many residents are reactive 
   rather than proactive about Aadhaar maintenance. Predictable update cycles 
   can improve service planning and reduce rush periods.

✅ RECOMMENDATION:
   • Send SMS/email reminders to residents when their Aadhaar is 5+ years old
   • Introduce a "renewal month" concept based on birth month or enrolment month
   • Offer incentives (priority service, shorter queues) for off-peak updates
   • Partner with employers/schools to conduct on-site Aadhaar update camps
   • Create a WhatsApp chatbot for checking update eligibility and booking slots

INSIGHT 4: Capacity Planning and Infrastructure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Finding:
   • Number of service months analyzed: {len(merged_data) if not merged_data.empty else 0}
   • Consistent service delivery indicates established infrastructure
   • Combined monthly average: {(avg_enrolments + avg_biometric + avg_demographic):,.0f} services

💡 Insight:
   While Hyderabad has established Aadhaar infrastructure, the steady volume 
   of all three service types indicates sustained demand that requires ongoing 
   investment in technology and personnel.

✅ RECOMMENDATION:
   • Upgrade biometric devices to faster, multi-modal capture systems
   • Implement digital queue management systems with real-time wait time displays
   • Create dedicated "update-only" centers in high-density residential areas
   • Establish a district-level service dashboard for monitoring daily loads
   • Conduct quarterly audits of center performance (avg time per service, uptime)
   • Invest in staff training programs focusing on speed and accuracy
"""

print(insights)

# Save insights to text file
with open('visualizations/insights_and_recommendations.txt', 'w') as f:
    f.write("UIDAI DATA HACKATHON 2026 - HYDERABAD DISTRICT\n")
    f.write("AADHAAR ENROLMENT AND UPDATE BEHAVIOR ANALYSIS\n")
    f.write("="*80 + "\n\n")
    f.write(insights)

print("\n✓ Insights and recommendations saved to 'insights_and_recommendations.txt'")
print()

# ============================================================================
# SUMMARY STATISTICS TABLE
# ============================================================================
print("="*80)
print("SUMMARY STATISTICS")
print("="*80)

summary_stats = pd.DataFrame({
    'Service Type': ['Enrolments', 'Biometric Updates', 'Demographic Updates'],
    'Total Count': [f"{total_enrolments:,.0f}", f"{total_biometric:,.0f}", f"{total_demographic:,.0f}"],
    'Monthly Average': [f"{avg_enrolments:,.0f}", f"{avg_biometric:,.0f}", f"{avg_demographic:,.0f}"],
    'Std Deviation': [
        f"{enrolment_monthly['Enrolments'].std():,.0f}" if not enrolment_monthly.empty else "0",
        f"{biometric_monthly['Biometric_Updates'].std():,.0f}" if not biometric_monthly.empty else "0",
        f"{demographic_monthly['Demographic_Updates'].std():,.0f}" if not demographic_monthly.empty else "0"
    ]
})

print(summary_stats.to_string(index=False))
print()

print("="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"✓ All visualizations saved in 'visualizations/' directory")
print(f"✓ Insights and recommendations saved in text file")
print(f"✓ Ready for hackathon PDF compilation")
print()
print("Files generated:")
print("  1. 1_enrolment_trend.png")
print("  2. 2_biometric_trend.png")
print("  3. 3_demographic_trend.png")
print("  4. 4_comparison_all_services.png")
print("  5. 5_peak_months.png")
print("  6. insights_and_recommendations.txt")
print("="*80)
