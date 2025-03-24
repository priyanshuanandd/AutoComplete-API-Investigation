# AutoComplete API Investigation

## Part1: Problem Statement

Extract all possible names from an undocumented autocomplete API at `http://35.200.185.69:8000` by discovering its behavior through testing, while handling constraints like rate limiting.

---

## Part2 : Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/priyanshuanandd/AutoComplete-API-Investigation
   cd AutoComplete-API-Investigation-master
2. **Set Up Python Environment**:
   *Ensure Python 3.x is installed :*
   ```bash
   python3 -- version

3. ***Install Dependencies***

 *Install from requirements.txt*
   ```bash
   pip3 install -r requirements.txt
   ```
 *Contents:*
   ```text
   requests
   ```
4. ***Run the Solution:***
*Execute all the scripts in one go:*
```bash
python3 run_all.py
```
*Execute Only v1:*
```bash
python3 extractv1.py #same goes for v2 and v3
```


---

### Part 3: Solution Approach - API Discovery

```markdown
## Solution Approach

### API Discovery
Through testing, I found three endpoints:
- **`v1/autocomplete?query=<string>`**: Returns strings with lowercase letters (a-z).
- **`v2/autocomplete?query=<string>`**: Returns strings with digits (0-9) and letters (a-z).
- **`v3/autocomplete?query=<string>`**: Returns strings with letters (a-z), digits (0-9), and additional symbols (e.g., punctuation).

No other parameters beyond `query` were identified. Each endpoint:
- Returns JSON: `{"version": "vX", "count": ≤10, "results": [strings]}`.
- Has a max of 10 results per query.
- Limits strings to 10 characters.
### Part 4: Solution Approach - Algorithm and Optimization

### Algorithm and Optimization
I implemented a **Depth-First Search (DFS)** algorithm with backtracking and optimization:

#### Algorithm Details
1. **Initialization**:
   - Start with an empty query (`""`) to fetch initial results.
   - Use a queue of `(prefix, parent)` pairs to track exploration and backtracking.

2. **Recursive Exploration**:
   - **If 10 Results**: Recurse deeper with the last result’s substring (length = current + 1). Example: "aa" → "aak".
   - **Same-Length Traversal**: 
     - For a prefix like "aak", traverse all same-length prefixes by incrementing the last character from 'k' to 'z' (for `v1`’s a-z alphabet).
     - Process: Query "aak", then "aal" (k → l), "aam" (l → m), ..., to "aaz" (y → z), using the alphabet "abcdefghijklmnopqrstuvwxyz".
     - Each step queries the API and moves to the next letter until 'z'.
   - **Backtracking**: When results < 10 and 'z' is reached (e.g., "aaz"), backtrack to the parent ("aa") and move to the next sibling ("ab").

3. **Character Sets**:
   - `v1`: a-z (26 characters).
   - `v2`: 0-9, a-z (36 characters).
   - `v3`: a-z, 0-9, symbols (broader set inferred from responses).

4. **Execution**:
   - `v1` in `autocomplete.py` uses "abcdefghijklmnopqrstuvwxyz".
   - `v2` and `v3` in `extractv2.py` and `extractv3.py` adjust the alphabet accordingly.

#### Optimization Techniques
- **Substring Jump**: Jump to the last result’s substring (e.g., "aa" → "aak") when 10 results are returned, skipping intermediate prefixes.
- **Early Termination**: Stop a branch when results < 10.
- **Unique Storage**: Use a `set` for O(1) lookup and no duplicates.


### Part 5: Solution Approach - Rate Limiting Handling

### Rate Limiting Handling
Each endpoint has a different rate limit, addressed with tailored delays:
- **`v1`**: 100 requests/minute → 0.6 seconds/request (60/100 = 0.6s).
- **`v2`**: 50 requests/minute → 1.2 seconds/request (60/50 = 1.2s).
- **`v3`**: 80 requests/minute → 0.75 seconds/request (60/80 = 0.75s).

These delays were implemented in `autocomplete.py`, `extractv2.py`, and `extractv3.py` respectively, ensuring compliance while maximizing throughput.

### Part 6 : Solution Approach - DFS Tree Example
```markdown
### DFS Tree Example

Below is a visual representation of the DFS traversal for the `v1` endpoint, showing how prefixes are explored:

```
```text

- **Flow Explained**:
  1. **`""`**: Initial query returns 10 results, recurse to "a".
  2. **`a`**: Returns 10 results, recurse to "aa".
  3. **`aa`**: Returns 10 results (e.g., "aa", ..., "aakfubvxv"), recurse to "aak" (substring of last result).
  4. **`aak`**: Returns 1 result ("aakfubvxv"), traverse to "aal" (k → l).
  5. **`aal`**: Returns 0 results, continue to "aaz" (l → m → ... → z).
  6. **`aaz`**: Returns 3 results ("aaza", "aazlhbqx", "aaztpk"), exhausted at 'z' with < 10 results.
  7. **Backtrack**: From "aaz" to parent "aa", then to next sibling "ab".
  8. **`ab`**: Continue exploration (e.g., 1 result "abagnc"), proceed to "ac".
```
### Part 7 : Results
```markdown
## Results

- **v1**:
  - Total API Calls: [TBD after full run]
  - Strings Found: [TBD after full run]
- **v2**:
  - Total API Calls: [TBD after full run]
  - Strings Found: [TBD after full run]
- **v3**:
  - Total API Calls: [TBD after full run]
  - Strings Found: [TBD after full run]
```

### Part 8 : Conclusion 
```markdown 
## Conclusion

The DFS solution with substring jumps and backtracking efficiently extracts names from `v1` (a-z), `v2` (0-z), and `v3` (symbols). The "aak" to "aaz" traversal increments the last character systematically, ensuring all same-length prefixes are covered. Rate limiting is handled with precise delays (0.6s, 1.2s, 0.75s), and the `set` ensures efficient storage.
```