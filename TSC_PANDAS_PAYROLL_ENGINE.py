#data preparation
import pandas as pd
import pandasql as ps
from pandasql import sqldf
import io

#load lookup table
Salary_lookup=[
    {'Current_Group': 'B5', 'Salary_Scale': 34958.00, 'Commuter_Allowance': 4000.00, 'House_Allowance': 6000.00},
    {'Current_Group': 'C1', 'Salary_Scale': 43774.00, 'Commuter_Allowance': 5000.00, 'House_Allowance': 7000.00},
    {'Current_Group': 'C2', 'Salary_Scale': 53943.00, 'Commuter_Allowance': 6000.00, 'House_Allowance': 8000.00},
    {'Current_Group': 'C3', 'Salary_Scale': 65307.00, 'Commuter_Allowance': 7000.00, 'House_Allowance': 9000.00},
    {'Current_Group': 'C4', 'Salary_Scale': 77840.00, 'Commuter_Allowance': 8000.00, 'House_Allowance': 10000.00},
    {'Current_Group': 'C5', 'Salary_Scale': 93408.00, 'Commuter_Allowance': 9000.00, 'House_Allowance': 12000.00},
    {'Current_Group': 'D1', 'Salary_Scale': 108240.00, 'Commuter_Allowance': 10000.00, 'House_Allowance': 14000.00},
    {'Current_Group': 'D2', 'Salary_Scale': 118242.00, 'Commuter_Allowance': 11000.00, 'House_Allowance': 16000.00},
    {'Current_Group': 'D3', 'Salary_Scale': 141000.00, 'Commuter_Allowance': 12000.00, 'House_Allowance': 18000.00},
    {'Current_Group': 'D4', 'Salary_Scale': 156000.00, 'Commuter_Allowance': 13000.00, 'House_Allowance': 20000.00},
    {'Current_Group': 'D5', 'Salary_Scale': 172000.00, 'Commuter_Allowance': 14000.00, 'House_Allowance': 22000.00}
]

df_Salary_lookup=pd.DataFrame(Salary_lookup, columns=['Current_Group', 'Salary_Scale', 'Commuter_Allowance', 'House_Allowance'])

print("="*50)

print(df_Salary_lookup)

print("="*50)

df_Salary_lookup.to_csv("Salary_lookup.csv",index=False)

#ERRO handling remove double quotes from rows
with open ("tsc_teachers_practice_data.csv","r") as f:
    raw_lines=f.readlines()

processed_lines_for_csv=[]

for line in raw_lines:
    stripped_line=line.strip()
    if stripped_line.startswith('"') and stripped_line.endswith('"'):
        processed_lines_for_csv.append(stripped_line.strip('"'))
    else:
        processed_lines_for_csv.append(stripped_line)

file_content_cleaned='\n'.join(processed_lines_for_csv)

df_file_content_cleaned=pd.read_csv(io.StringIO(file_content_cleaned),sep=',',engine='python')
print("FILE CONTENT CLEANED:")
print("="*50)
print()
print(df_file_content_cleaned)
print("="*50)
print()

df_teachers=pd.read_csv(io.StringIO(file_content_cleaned),sep=',',engine='python')

print(df_teachers.head(20))

df_lookup=pd.read_csv("Salary_lookup.csv")

df_teachers.columns=df_teachers.columns.str.strip()

df_lookup.columns=df_lookup.columns.str.strip()

print("TEACHERS  TABLE COLUMNS:",df_teachers.columns.tolist())

print("LOOKUP TABLE COLUMNS:",df_lookup.columns.tolist())

#merge tables
pysqldf=lambda q:sqldf(q,env=globals())

query_1="""
SELECT 
    t."TSC Number",
    t."Teacher Name",
    t."Year of Birth",
    t."Year of Employment",
    t."Job Group",
    (2026-t."Year of Birth") AS AGE,
    CASE WHEN (2026-t."Year of Birth")>=60 THEN "RETIRED" ELSE "ACTIVE" END AS HR_STATUS,
    CASE WHEN (2026-t."Year of Birth")>=60 THEN 0.00 ELSE COALESCE(ref.Salary_Scale,0.00) END AS BASIC_SALARY,
    CASE WHEN (2026-t."Year of Birth")>=60 THEN 0.00 ELSE COALESCE(ref.Commuter_Allowance,0.00) END AS COMMUTER_ALLOWANCE,
    CASE WHEN (2026-t."Year of Birth")>=60 THEN 0.00 ELSE COALESCE(ref.House_Allowance,0.00) END AS HOUSE_ALLOWANCE
    
FROM 
    df_teachers t
LEFT JOIN 
    df_lookup ref
ON 
    TRIM(t."Job Group") = TRIM(ref.Current_Group);
"""

PAYROLL=pysqldf(query_1)

print(f"PAYROLL TABLE:\n{PAYROLL.head(10)}")

print(PAYROLL.columns.tolist())
#promotion logic


Current_year=2026

PAYROLL['Years of Service']=Current_year-PAYROLL['Year of Employment']

promotion_map={'B5':'C1','C1':'C2','C2':'C3','C3':'C4','C4':'C5','C5':'D1','D1':'D2','D2':'D3','D3':'D4','D4':'D5'}

eligible_for_promotion=(
                       (PAYROLL['Years of Service']>=3) &
                       (PAYROLL['HR_STATUS']=='ACTIVE')&
                       (PAYROLL['Job Group'].isin(promotion_map.keys())))

PAYROLL.loc[eligible_for_promotion,'New Job Group']=PAYROLL.loc[eligible_for_promotion,'Job Group'].map(promotion_map)

print(f"Eligible for promotion:\n{PAYROLL.loc[eligible_for_promotion]}")  

temp_df=PAYROLL.loc[eligible_for_promotion].merge(
     df_lookup,
     left_on='New Job Group',
     right_on='Current_Group',
     how='left'
)

if not temp_df.empty:
    PAYROLL.loc[eligible_for_promotion,'BASIC_SALARY']=temp_df['Salary_Scale'].values

    PAYROLL.loc[eligible_for_promotion,'COMMUTER_ALLOWANCE']=temp_df['Commuter_Allowance'].values

    PAYROLL.loc[eligible_for_promotion,'HOUSE-ALLOWANCE']=temp_df['House_Allowance'].values

NEW_PAYROLL_AFTER_PROMOTION=temp_df.filter(items=['TSC Number','Teacher Name',  'New Job Group','BASIC_SALARY','Commuter_Allowance','House_Allowance'])

print(f"After promotion:\n{NEW_PAYROLL_AFTER_PROMOTION.head(10)}")

print("="*50)

#convert to csv

print(NEW_PAYROLL_AFTER_PROMOTION.to_csv('NEW_PAYROLL_AFTER_PROMOTION.csv',index=False))











