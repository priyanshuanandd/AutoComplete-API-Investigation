# AutoComplete API Investigation
## Part1: Problem Statement
### Problem Statement

Extract all possible names from an undocumented autocomplete API at `http://35.200.185.69:8000` by discovering its behavior through testing, while handling constraints like rate limiting.

---

## Part2 : Installation 
### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/priyanshuanandd/AutoComplete-API-Investigation
   cd AutoComplete-API-Investigation-master
   ```
2. **Set Up Python Environment**:
   *Ensure Python 3.x is installed :*
   ```bash
   python3 -- version
   ```
3. **Install Dependencies**
 *Install from requirements.txt*
   ```bash
   pip3 install -r requirements.txt
   ```
4. **Run the Solution:(Offer Multi-Platform Support)**
   *Execute all the scripts in one go:*

   ```bash
   python3 run_all.py
   


   *Execute Only v1:*
   ```bash
   python3 extractv1.py #same goes for v2 and v3
   ```
   ![Screenshot (10)](https://github.com/user-attachments/assets/a1d720f7-d560-47cb-9bd0-6802b36b53ee)


---

## Part 3: Solution Approach - API Discovery


## Solution Approach

### API Discovery
Through testing, I found three endpoints:
- **`v1/autocomplete?query=<string>`**: Returns strings with lowercase letters (a-z).
- **`v2/autocomplete?query=<string>`**: Returns strings with digits (0-9) and letters (a-z).
- **`v3/autocomplete?query=<string>`**: Returns strings with letters (a-z), digits (0-9), and additional symbols (e.g., punctuation).

No other parameters beyond `query` were identified. Each endpoint:
- Returns JSON: `{"version": "vX", "count": ≤Y, "results": [strings]}`.
- Y is 10 ,12 and 15 for v1,v2 and v3 respectively.
- Has a max of 10 results per query.
- Limits strings to 10 characters.

## Part 4: Solution Approach - Algorithm and Optimization

### Algorithm and Optimization
I implemented a *Depth-First Search (DFS) algorithm with backtracking and optimization*.

#### Algorithm Details
### DFS Tree Example

Below is a visual representation of the DFS traversal for the `v1` endpoint, showing how prefixes are explored:

<div align="center">
  <img src="https://github.com/user-attachments/assets/18af377e-e1ac-44d6-a39d-808e9296d8da" alt="Graph" />
</div>

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

1. **Initialization**:
   - Start with an empty query (`""`) to fetch initial results.
   - Use a queue of `(prefix, parent)` pairs to track exploration and backtracking.

2. **Recursive Exploration**:
   - **If 10 Results**: Extend the last result’s substring (e.g., "aa" → "aak") to explore deeper.
   - **Same-Length Traversal**:
     - For a prefix like "aak", increment the last character (e.g., "aak" → "aal" → "aam" … → "aaz").
     - Each step queries the API and moves to the next letter until 'z'.
   - **Backtracking**: If results < 10 or at 'z' (e.g., "aaz"), return to the parent ("aa") and move to the next sibling ("ab").

3. **Character Sets**:
   - `v1`: a-z (26 characters).
   - `v2`: 0-9, a-z (36 characters).
   - `v3`: a-z, 0-9, symbols (inferred dynamically).

4. **Optimizations**:
   - **Substring Jumping**: Skip intermediate prefixes when 10 results are returned.
   - **Early Termination**: Stop exploring when results < 10.
   - **Unique Storage**: Use a `set` for O(1) lookup and duplicate filtering.

Each version (`v1`, `v2`, `v3`) implements these principles, adapting to their respective character sets.


## Part 5: Solution Approach - Rate Limiting Handling

### Rate Limiting Handling
Each endpoint has a different rate limit, addressed with tailored delays:
- **`v1`**: 100 requests/minute → 0.6 seconds/request (60/100 = 0.6s).
- **`v2`**: 50 requests/minute → 1.2 seconds/request (60/50 = 1.2s).
- **`v3`**: 80 requests/minute → 0.75 seconds/request (60/80 = 0.75s).

These delays were implemented in `extractv1.py`, `extractv2.py`, and `extractv3.py` respectively, ensuring compliance while maximizing throughput.



## Part 6 : Results

### Results

- **v1**:
  - Total API Calls: 10820
  - Strings Found: 18632
- **v2**:
  - Total API Calls: 3106
  - Strings Found: 13730
- **v3**:
  - Total API Calls: 3231
  - Strings Found: 12517


## Part 7 : Conclusion 

### Conclusion

The DFS solution with substring jumps and backtracking efficiently extracts names from `v1` (a-z), `v2` (0-z), and `v3` (symbols). The "aak" to "aaz" traversal increments the last character systematically, ensuring all same-length prefixes are covered. Rate limiting is handled with precise delays (0.6s, 1.2s, 0.75s), and the `set` ensures efficient storage.
```
