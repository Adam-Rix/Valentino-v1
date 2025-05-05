#v0.0.1

from Valentino_v1.Json_parser.JPars import JParser

import pytest
import asyncio
import sys
import os

'''Place here a path which lead u to the dir with collections.'''
@pytest.mark.parametrize("collection_path",
                         [r"D:\ProjectsPyY\Newideas\Valentino_v1\collections\Шахматка дин цен два.postman_collection.json"])
def test_Correlator(collection_path):
    print(f"🧪 Starting test for: {collection_path}")

    jparser = JParser(collection_path)
    asyncio.run(jparser.Gettig_Json())