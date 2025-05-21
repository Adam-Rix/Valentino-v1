# Valentino  
Valentino is an asynchronous API contract validator that works with Postman collections.  
It compares real server responses to prepared in advance example responses and validates the entire structure of server's responses.

---

## Valentino_v1_0.py  
Main runner script:  

- Uses `pytest` with parameterized input for the collection path;  
- Loads `.env` variables using `python-dotenv`;  
- Entry point for executing all validation logic.

---

## JPars.py  
Core parser and validator:  

- Parses the collection and builds structured items;  
- Sends all requests asynchronously using `httpx`;  
- Matches real responses with `example_responses` from the collection;  
- Supports both strict and structural validation (key presence);  
- Skips non-JSON responses gracefully.

# 🧪 Example Postman Collections
You can find a sample Postman collection [here](https://github.com/Adam-Rix/Valentino-v1/tree/main/collections). \
**BUT DELETE IT BEFORE USING** \
**IT WILL WORK ONLY  WITH USABLE COLLECTIONS**

---

## parser_itself.py  
Parses Postman collections:

- Extracts method, URL, headers, body;  
- Converts local URLs to remote (e.g., replaces `localhost` to your domain with .env help);  
- Collects example responses (`code`, `body`) for future comparison;
- Prints parsing summary.

---

## requester.py  
Handles sending HTTP requests:

- Adds required headers, cookies, and token;  
- Ensures HTTPS is used even if collection uses HTTP;  
- Returns full HTTP response object;  
- Logs response body (or warns if non-JSON);  
- Handles failures with error logging.

---

## .env  
Holds environment configuration:
```env
#paths
PATH_TO_DYNAMIC_STAND=PATH/TO/YOUR/COLLECTION/FOLDER
PATH_TO_COOKIES=PATH/TO/YOUR/.JSON/COOKIES

#links
OLD_DOMAIN=YOUR/OLD/DOMAIN (OR THE SAME AS CURRENT)
NEW_DOMAIN=YOUR/CURRENT/DOMAIN

#headers
ACCEPT_ENCODING=IF/NEEDED
CONNECTION==IF/NEEDED

#Token
TOKEN=YOUR/TOKEN/IF/NEEDED (DONT FORGET USE IT IN requester.py)
```

---

## Example of Output
🧪 Starting test for: some.json; \
[🔍] Parsed item: GET https://.../filters — 1 example(s) \
[🔍] Validating structure for: https://.../filters

✅ Matched with Reference key at .data[0]: name (str) \
**OR** \
❌ Missing key at .data[3]: defaultValue (str)\
**FOR EACH RESPONSE**

---

## Tech Plan:

1. Improve `parser_itself.py` for: ☑️ \
   1.1 Collecting request bodies; ✅  
   1.2 Parsing example responses; ✅  
   1.3 Replacing non-JSON responses with response codes (200, 300, etc.). ✅  
---
2. Create async engine for request validation: ☑️  
   2.1 Use `httpx.AsyncClient` for concurrency; ✅  
   2.2 Parametrize collection paths via `.env`; ✅  
   2.3 Wrap logic in `async def Gettig_Json()`. ✅  
---
3. Validate response structure (not full match): ☑️  
   3.1 Match field presence only (via tree walk); ✅  
   3.2 Detect missing keys & type mismatches; ✅  
   3.3 Add exception handling & debug printing. ✅  
---
4. Enhance result output: ☑️  
   4.1 Color-coded validation results (✅/❌); ✅ \
   4.2 Export validation logs to file (JSON). ✅  
---
5. Finalize the EPIC: 🛠 \
   5.1 Add multiple collection reading; ✅ \
   5.2 Add datatype validation; ✅ \
   5.3 Cleanup structure & docstrings; 🛠  \
   5.4 Prepare for packaging as CLI tool. ⏳
---
6. Port all above on **php 8.3** . ⏳
