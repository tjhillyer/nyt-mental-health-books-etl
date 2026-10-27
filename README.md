# Mental Health in Book Coverage — NYT Data ETL Pipeline

A Python ETL (Extract, Transform, Load) pipeline that answers one question:
**which books did The New York Times cover in connection with "mental health" from 2000 to 2020, and how often was each one written about?**

Final project for Object-Oriented Programming (Python), Rutgers University, Spring 2022.

## How it works

| Stage | What happens |
|---|---|
| **Extract** | Queries the [NYT Article Search API](https://developer.nytimes.com/docs/articlesearch-product/1/overview) for articles in the *Books* section mentioning "mental health" (2000–2020), paging through results with a delay between requests to respect rate limits. Each page's keywords are cached to a pickle file. |
| **Transform** | Merges the cached keyword files into one list, then uses regular expressions to keep only book titles (keywords tagged `(Book)`) and strip extra characters. A `hit_counts()` function queries the API again to count articles referencing each title. |
| **Load** | Writes each title and its hit count to `book_results.csv`. |

## Results

The pipeline found **26 books**. Coverage was very uneven: most titles were referenced fewer than 100 times, while a few passed 1,000.

| Book | NYT hits |
|---|---|
| How We Are | 20,252 |
| Cover | 8,480 |
| George | 7,125 |
| What We See When We Read | 5,690 |
| A Fairly Good Time | 725 |

Full results: [`data/book_results.csv`](data/book_results.csv)

## Run it yourself

1. Get a free API key at <https://developer.nytimes.com>.
2. Install the dependency and set your key:
   ```bash
   pip install -r requirements.txt
   export NYT_API_KEY="your-key-here"     # Windows PowerShell: $env:NYT_API_KEY="your-key-here"
   ```
3. Run the pipeline (it takes several minutes because of the rate-limit delays):
   ```bash
   python nyt_books_etl.py
   ```

## Tools

Python · `requests` · `pickle` · `pathlib` · `re` · `csv` · NYT Article Search API

## Next idea

Track how often "mental health" appears in NYT coverage year by year to see whether the conversation has grown since 2000.
