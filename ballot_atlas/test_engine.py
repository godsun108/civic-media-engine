import unittest
from engine import normalize,reconcile
class RegistryTests(unittest.TestCase):
 def setUp(self):
  self.row={'source_id':'fec:TEST','name':'Example','office':'U.S. House','jurisdiction':'FL','source_url':'https://example.org/evidence','source_updated_at':'2026-10-04T00:00:00Z'}
 def test_requires_source(self):
  with self.assertRaises(ValueError):normalize({})
 def test_new_candidate(self):
  state,events=reconcile([],[self.row]);self.assertEqual(len(state),1);self.assertEqual(events[0]['type'],'new_candidate')
 def test_no_change(self):
  state,events=reconcile([normalize(self.row)],[self.row]);self.assertEqual(events,[])
 def test_preserves_positions_on_source_change(self):
  old=normalize(self.row);old['positions']=[{'issue':'Water','reviewed':True}]
  changed=dict(self.row,name='Changed Name');state,events=reconcile([old],[changed]);self.assertEqual(state[0]['positions'],old['positions']);self.assertTrue(events[0]['review_required'])
if __name__=='__main__':unittest.main()
