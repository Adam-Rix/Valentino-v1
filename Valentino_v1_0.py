#Valentino_v1_0.py
#v1.0.0
from Valentino_v1.Json_parser.JPars import JParser
from dotenv import load_dotenv

import os
import pytest
import asyncio

# Getting envs
dotenv_path = r"D:\ProjectsPyY\Newideas\Valentino_v1\Envs\.env"
load_dotenv(dotenv_path, override=True)

'''Debug print from .env'''
#print(os.getenv("PATH_TO_DYNAMIC_STAND"))

'''Place here a path which lead u to the dir with collections.'''
@pytest.mark.parametrize("collection_path",
                         [os.getenv("PATH_TO_DYNAMIC_STAND")]
                         )
def test_Correlator(collection_path):
    print(f"🧪 Starting test for: {collection_path}")

    jparser = JParser(collection_path)
    asyncio.run(jparser.Gettig_Json())