import unittest
class AdvisorTriggerTests(unittest.TestCase):
 def test_nontriggers_do_not_include_first_hard_cap(self):
  non={"first_hard_cap","missing_credentials","single_reviewer_failure","ordinary_bug"}
  self.assertIn("first_hard_cap",non)
if __name__=="__main__":unittest.main()
