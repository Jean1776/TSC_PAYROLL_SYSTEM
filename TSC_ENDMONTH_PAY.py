import pandas as pd

NEW_PAYROLL=pd.read_csv('NEW_PAYROLL_AFTER_PROMOTION.csv')

print(NEW_PAYROLL.head(20))

NEW_PAYROLL['GROSS INCOME']=(NEW_PAYROLL['BASIC_SALARY']+NEW_PAYROLL['Commuter_Allowance']+NEW_PAYROLL['House_Allowance'])

NEW_PAYROLL['NSSF Contribution']=(NEW_PAYROLL['BASIC_SALARY']*0.06).clip(upper=6480.00).round(2)

NEW_PAYROLL['Taxable Pay']=(NEW_PAYROLL['GROSS INCOME']-NEW_PAYROLL['NSSF Contribution']).round(2)


NEW_PAYROLL['GROSS PAYE']=NEW_PAYROLL['Taxable Pay'].apply(lambda x: (24000*0.10)+(8333*0.25)+((x-32333)*0.30) if x>32333 else ((24000*0.10)+((x-24000)*0.25) if x>24000 else x*0.10))

NEW_PAYROLL['Net PAYE']=(NEW_PAYROLL['GROSS PAYE']-2400.00).clip(lower=0).round(2)
NEW_PAYROLL['Housing Levy']=(NEW_PAYROLL['BASIC_SALARY']*0.015).round(2)

NEW_PAYROLL['SHIF']=(NEW_PAYROLL['BASIC_SALARY']*0.0275).round(2)

Total_deductions=NEW_PAYROLL['Housing Levy']+ NEW_PAYROLL['SHIF']+NEW_PAYROLL['NSSF Contribution']+NEW_PAYROLL['Net PAYE']

NEW_PAYROLL['Net Monthly Pay']=(NEW_PAYROLL['GROSS INCOME']-Total_deductions)

print(NEW_PAYROLL.head(20))

NEW_PAYROLL.to_excel("TSC_MASTER_PAYROLL.xlsx",index=False)
