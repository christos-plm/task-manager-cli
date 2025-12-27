# Pandas Learning Notes

## Key Concepts

**DataFrame**: A table of data (rows and columns)
**Series**: A single column from a DataFrame

## Common Operations

### Loading Data
```python
df = pd.read_csv('file.csv')

### Viewing Data
∙ df.head() - First rows
∙ df.tail() - Last rows
∙ df.info() - Column info
∙ df.describe() - Statistics

### Filtering
df[df['column'] == value]
df[(df['col1'] > 5) & (df['col2'] == 'text')]

### Sorting
df.sort_values('column', ascending=False)

### Grouping
df.groupby('column')['other_column'].mean()


---

### Creating Columns
- Simple calculation: `df['new'] = df['old'] * 2`
- Conditional: `np.where(condition, value_if_true, value_if_false)`
- Categories: `pd.cut(df['col'], bins=[...], labels=[...])`
- From dates: `(today - df['date']).dt.days`

### Modifying Data
- Update column: `df['col'] = df['col'].str.upper()`
- Apply function: `df['col'].apply(my_function)`
- Lambda: `df['col'].apply(lambda x: x * 2)`

### Handling Missing Data
- Check: `df.isnull().sum()`
- Fill: `df['col'].fillna(value)`
- Drop: `df.dropna()`

### Merging DataFrames
- Inner join: `df1.merge(df2, on='key', how='inner')`
- Left join: `df1.merge(df2, on='key', how='left')`

### Key Functions
- `np.where()` - conditional logic
- `.apply()` - apply function to column
- `.str` methods - string operations
- `.merge()` - join DataFrames
