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