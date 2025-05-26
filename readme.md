## SAFE-APIOpt

Our approach aims to identify SaFE API pairs and determine the more efficient API within each pair through automatically generated performance evaluation cases. 

![method](image\method.png)

## Scripts

### 1. fetch_so_posts.py

**Usage**

```
python fetch_so_posts.py <keyword> <tag> [--pagesize N] [--max-pages M]
```

- `<keyword>`: Search term for title/content
- `<tag>`: Single tag to add (the script automatically prepends `python;`)
- `--pagesize`: Number of results per page (default: 50)
- `--max-pages`: Maximum number of pages to fetch (default: 2)

**Example**

```
python fetch_so_posts.py fast torch
```

→ Get links search with the keyword 'fast' for the torch library .And produces an Excel file named `python_torch_fast.xlsx`

------

### 2. so_answer_crawler.py

**Usage**

```
python so_answer_crawler.py <input_excel> [--output <output_excel>] [--delay SECONDS]
```

- `<input_excel>`: Path to Excel file (must contain `title` & `link` columns)
- `--output`: Output filename 
- `--delay`: Seconds to wait between requests (default: 0.5)

**Example**

```
python so_answer_crawler.py torch_fast.xlsx --output=torch_fast_answers.xlsx --delay=1.0
```

------

### 3. gpt.py

**Usage**

```
python gpt.py <input_excel> [--output <output_excel>]
```

- `<input_excel>`: Path to Excel 
- `--output`: Output filename (default: `generated_output.xlsx`)

**Example**

```
python gpt.py torch__fast_answers.xlsx --output=torch_potential_SaFE_API.xlsx
```

