#Valentino_v1_0.py
#v1.0.0
from Valentino_v1.Json_parser.JPars import JParser
from dotenv import load_dotenv

import os
import pytest
import asyncio


'''Use path to your .env file'''
dotenv_path = r"path/to/your/.env"
load_dotenv(dotenv_path, override=True)

'''Debug print from .env'''
#print(os.getenv("PATH_TO_COLLECTION"))

'''Place here a path which lead u to the dir with collections.'''
@pytest.mark.parametrize("collection_path",
                         [os.path.dirname(os.path.abspath(__file__))]
                         )
def test_Correlator(collection_path):
    print(f"\n🧪 Starting test for: {collection_path}")

    processed = False
    for filename in os.listdir(collection_path):
        full_path = os.path.join(collection_path, filename)

        if filename.endswith(".json") and os.path.isfile(full_path):
            processed = True
            jparser = JParser(collection_path)
            asyncio.run(jparser.Gettig_Json())
        else:
            print(f"⛔ Skipped: {filename}")
    if not processed:
        pytest.fail("❌ No valid .json files found to process.")