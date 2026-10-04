import os,unittest,json,io
from unittest.mock import patch
from fec import fetch
class Response(io.BytesIO):
 def __enter__(self):return self
 def __exit__(self,*args):self.close()
class Tests(unittest.TestCase):
 @patch.dict(os.environ,{"FEC_API_KEY":"test"})
 def test_mapping_and_ballot_caution(self):
  def opener(req,timeout):
   return Response(json.dumps({"results":[{"candidate_id":"H6FL00001","name":"TEST, A","office":"H","party":"IND"}],"pagination":{"pages":1}}).encode())
  records=fetch(opener=opener)
  self.assertEqual(len(records),1)
  self.assertEqual(records[0]["ballot_status"],"NOT_VERIFIED")
  self.assertEqual(records[0]["source_id"],"fec:H6FL00001")
 @patch.dict(os.environ,{},clear=True)
 def test_key_required(self):
  with self.assertRaises(RuntimeError):fetch()
if __name__=="__main__":unittest.main()
