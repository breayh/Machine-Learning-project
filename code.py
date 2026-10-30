```python
import numpy as np
import pandas as pd
import wbgapi as wb
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#import languages database
languages_df = pd.read_csv("data.csv")
#country column
country_col = [c for c in languages_df.columns if 'country codes' in c.
↪lower()][0]
#degree of endangerment column
target_col = [c for c in languages_df.columns if 'degree' in c.lower() or␣
↪
'endangerment' in c.lower()][0]
#speakers count column
speaker_col = [c for c in languages_df.columns if 'speakers' in c.lower()][0]
# Primary country ISO code extraction
languages_df["primary_country"] = (languages_df[country_col].astype(str).str.
↪split("
,
").str[0].str.strip().str.upper())

#world bank socio-economic data
indicators = {
'NY.GDP.PCAP.CD': 'gdp_per_capita'
,
'IT.NET.USER.ZS': 'internet_usage_pct'
'SP.RUR.TOTL.ZS': 'rural_pop_pct'
,
,
}
#fetch only 2010
wb_df = wb.data.DataFrame(list(indicators.keys()), time=2010).reset_index()
wb_df = wb_df.rename(columns=indicators)
wb_df = wb_df.rename(columns={'index': 'primary_country'})#AI generated tests
print("\n=== MISSING VALUES SUMMARY (World Bank) ===")
wb_missing = wb_df[list(indicators.values())].isna().sum()
wb_pct = (wb_missing / len(wb_df)) * 100
missing_summary = pd.DataFrame({'Missing Count': wb_missing, 'Missing %':␣
↪wb_pct.round(2)})
print(missing_summary)# Merge Datasets
merged_df0 = pd.merge(
languages_df,
wb_df,
on='primary_country'
how='left'
,
)
#drop rows missing target vals
merged_df0 = merged_df0.dropna(subset=['degree_number']).copy()
#stabilize GDP per capita, so it's not out of bounds
merged_df0['log_gdp_per_capita'] = np.log1p(merged_df0['gdp_per_capita'].
↪clip(lower=0))
#fill missing values with 0
merged_df0[speaker_col] = merged_df0[speaker_col].fillna(0)
#log-transform for easier values (same as GDP per capita)
merged_df0['log_speakers'] = np.log1p(merged_df0[speaker_col])
#introduce new feature
merged_df0['speakers_per_country'] = 

# Merge Datasets
merged_df0 = pd.merge(
languages_df,
wb_df,
on='primary_country'
how='left'
,
)
#drop rows missing target vals
merged_df0 = merged_df0.dropna(subset=['degree_number']).copy()
#stabilize GDP per capita, so it's not out of bounds
merged_df0['log_gdp_per_capita'] = np.log1p(merged_df0['gdp_per_capita'].
↪clip(lower=0))
#fill missing values with 0
merged_df0[speaker_col] = merged_df0[speaker_col].fillna(0)
#log-transform for easier values (same as GDP per capita)
merged_df0['log_speakers'] = np.log1p(merged_df0[speaker_col])
#introduce new feature
merged_df0['speakers_per_country'] = 

# to vvoid division by zero/missing number_of_countries
if 'number_of_countries' not in merged_df0.columns:
merged_df0['number_of_countries'] = 1
merged_df0['speakers_per_country'] = (
merged_df0['log_speakers'] / merged_df0['number_of_countries'].replace(0, 1)
)

#AI generated tests
print("=== MERGE DIAGNOSTICS ===")
print(f"Original Languages Count : {len(languages_df)}")
print(f"Merged Dataset Count : {len(merged_df0)}")
print(f"Successful Merge Rate : {(1 - merged_df0['gdp_per_capita'].isna().
↪mean()) * 100:.2f}%\n")
print("=== MISSING VALUE COUNTS IN MERGED DATA ===")
wb_features = ['log_gdp_per_capita'
,
'internet_usage_pct'
print(merged_df0[wb_features].isna().sum())

# X - features
feature_cols = [
'log_speakers'
,
'number_of_countries'
,
'speakers_per_country'
'log_gdp_per_capita'
'internet_usage_pct'
,
,
,
]
clean_df = merged_df0[feature_cols + ["degree_number"]].dropna()
X = clean_df[feature_cols]
y = clean_df["degree_number"]

X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.25, random_state=42)

#first model - linear regression
model1 = LinearRegression()
model1.fit(X_train, y_train)
y_train_pred1 = model1.predict(X_train)
y_test_pred1 = model1.predict(X_test)

print("Linear Regression Results:")
print(f" Training MSE: {mean_squared_error(y_train, y_train_pred1):.4f} |␣
↪Training R²: {r2_score(y_train, y_train_pred1):.4f}")
print(f" Test MSE: {mean_squared_error(y_test, y_test_pred1):.4f} | Test␣
↪R²: {r2_score(y_test, y_test_pred1):.4f}")
print(f" Test MAE: {mean_absolute_error(y_test, y_test_pred1):.4f}\n")

plt.figure(figsize=(8, 6))
plt.scatter(
X_test['log_speakers'],
y_test,
color='b'
,
alpha=0.3,
s=10,
label='Test Languages'
)
log_spk_range = np.linspace(X_test['log_speakers'].min(),␣
↪X_test['log_speakers'].max(), 200)
dummy_X = pd.DataFrame({col: X_test[col].mean() for col in feature_cols},␣
↪index=range(200))
dummy_X['log_speakers'] = log_spk_range
dummy_X = dummy_X[feature_cols] # Enforce original column order to avoid␣
↪sklearn warnings
dummy_pred = model1.predict(dummy_X)
plt.plot(
log_spk_range,
dummy_pred,
color='r'
,
linewidth=2.5,
label='h(x) prediction'
)
plt.xlabel('log_speakers', size=12)
plt.ylabel('degree_number (endangerment level)', size=12)
plt.title('Linear Regression: log_speakers vs. endangerment (Test Set)'
↪size=14)
plt.legend(loc='best', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#second model - random forest regressor
model2 = RandomForestRegressor(n_estimators=100, random_state=42)
model2.fit(X_train, y_train)
y_train_pred2 = model2.predict(X_train)
y_test_pred2 = model2.predict(X_test)

print("Random Forest Regressor Results:")
print(f" Training MSE: {mean_squared_error(y_train, y_train_pred2):.4f} |␣
↪Training R²: {r2_score(y_train, y_train_pred2):.4f}")
print(f" Test MSE: {mean_squared_error(y_test, y_test_pred2):.4f} | Test␣
↪R²: {r2_score(y_test, y_test_pred2):.4f}")
print(f" Test MAE: {mean_absolute_error(y_test, y_test_pred2):.4f}\n")

plt.figure(figsize=(8, 5))
np.random.seed(42)
y_test_jittered = y_test + np.random.normal(0, 0.06, size=len(y_test))
plt.scatter(
y_test_jittered,
y_test_pred2,
alpha=0.35,
color='#2a9d8f'
,
s=20,
label='Model Predictions'
)
plt.plot(
[0, 4],
[0, 4],
color='#e76f51'
,
linestyle='--'
,
linewidth=2,
label=r'Ideal Fit ($y = \hat{y}$)'
)
plt.xlabel('Actual Endangerment Tier', fontsize=11)
plt.ylabel('Predicted Endangerment Tier (All 5 Features)', fontsize=11)
plt.title('Random Forest Accuracy Using All 5 Features', fontsize=12,␣
↪fontweight='bold')
plt.xticks([0, 1, 2, 3, 4], ['0','1','2','3','4'])
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
```
