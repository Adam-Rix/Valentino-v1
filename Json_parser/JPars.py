# JPars.py
# v1.0.0
import asyncio
import json
import httpx
import os

from Valentino_v1.Json_parser.parser_itself import parse_collection
from Valentino_v1.request_sender.requester import send_request

class JParser:
    def __init__(self, collection_path):
        self.collection_path = collection_path

    async def Gettig_Json(self):

        files = []
        if os.path.isdir(self.collection_path):
            files = [
                os.path.join(self.collection_path, f)
                for f in os.listdir(self.collection_path)
                if f.endswith(".json")
            ]
        elif os.path.isfile(self.collection_path):
            files = [self.collection_path]
        else:
            print(f"\n smth went wrong with: {self.collection_path}")

        for file in files:
            print(f"\n🧪 Processing collection: {file}")
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Parse each request and example of response
            items = parse_collection(data)

            #  create async client
            async with httpx.AsyncClient(timeout=15) as client:
                # create coroutine (list of async tasks)
                tasks = [send_request(client, item) for item in items]
                responses = await asyncio.gather(*tasks) #wait while all will be ended

            # sorting through pairs
            for item, response in zip(items, responses):
                url = item.get("url")
                print(f"\n[🔍] Validating structure for: {url}")

                if response is None:
                    print("[❌] No response received.")
                    continue

                expected_response = next(iter(item.get("example_responses", [])), None)

                if not expected_response:
                    print("[ℹ️] No example response found for validation.")
                    continue

                # Method validation
                expected_method = expected_response.get("originalRequest", {}).get("method")
                actual_method = response.request.method.upper()
                if expected_method != actual_method:
                    print(f"❌ Method mismatch: expected {expected_method}, got {actual_method}")
                else:
                    print(f"✅ Matched request method: {actual_method}")


                # Status code validation
                expected_code = expected_response.get("code")
                actual_code = response.status_code
                if expected_code != actual_code:
                    print(f"❌ Status code mismatch: expected {expected_code}, got {actual_code}")
                    continue
                else:
                    print(f"✅ Matched status code: {actual_code}")

                try:
                    actual_json = response.json()
                except Exception:
                    print(f"[⚠️] Non-JSON response from {url} ({response.status_code}):\n⚠️⚠️⚠️SKIPPED⚠️⚠️⚠️")
                    continue

                try:
                    expected_json = json.loads(expected_response.get("body", "{}"))
                    validate_structure(expected_json, actual_json)

                    '''Debugging prints with expected and actual responses'''
                    # print("Expected (parsed from collection):", json.dumps(expected_json, indent=2, ensure_ascii=False))
                    # print("Actual (from response):", json.dumps(actual_json, indent=2, ensure_ascii=False))
                except json.JSONDecodeError:
                    print("[⚠️] Example body in collection is not valid JSON.")
                except Exception as e:
                    print(f"[⚠️] Unexpected error during validation: {e}")

# matching dicts and lists in memory
def validate_structure(expected, actual, path=""):

    if isinstance(expected, dict):

        if not isinstance(actual, dict):
            print(f"❌ Type mismatch at {path or 'root'}: expected object")
            return False

        for key in expected:
            if key not in actual:
                print(f"❌ Missing key at {path or 'root'}: {key}")
                continue

            # comparing types before recursion
            if not isinstance(actual[key], type(expected[key])):
                print(
                    f"⚠️ Type mismatch at {path + '.' + key}: expected {type(expected[key]).__name__}, got {type(actual[key]).__name__}")
            else:
                print(f"✅ Matched type for key at {path or 'root'}: {key} ({type(actual[key]).__name__})")

            # recursive nesting check
            validate_structure(expected[key], actual[key], path + f".{key}")


    elif isinstance(expected, list) and isinstance(actual, list):
        for i, (exp, act) in enumerate(zip(expected, actual)):
            validate_structure(exp, act, path + f"[{i}]")

    elif type(expected) != type(actual):
        print(f"⚠️ Type mismatch at {path}: expected {type(expected).__name__}, got {type(actual).__name__}")

    return True