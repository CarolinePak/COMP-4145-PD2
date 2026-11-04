import copy
import json
import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from modules.recommendation_logic import *

class RecommendationTests(unittest.TestCase):
 def setUp(self):
  self.catalogue=load_catalogue()
  self.output={'analysis_summary':'Visible dryness.','products':[{'product_id':'P08','why':'Hydration matches visible dryness.','selection_note':'An optional hydration option.'}], 'routine':{'morning':[{'instruction':'Moisturize as directed.','product_id':None}], 'evening':[{'instruction':'Follow label directions.','product_id':'P08'}]},'tips':['Introduce products individually.'],'limitations':'Image observations are uncertain.'}
 def test_catalogue(self):
  self.assertGreaterEqual(len(self.catalogue),20)
  for p in self.catalogue:
   self.assertTrue(p['source_url'].startswith('https://'))
   self.assertTrue(p['benefits'])
 def test_validation(self):
  validate_response(json.dumps(self.output),self.catalogue)
  for change in ('unknown','duplicate','routine','missing'):
   d=copy.deepcopy(self.output)
   if change=='unknown':d['products'][0]['product_id']='INVENTED'
   if change=='duplicate':d['products']*=2
   if change=='routine':d['routine']['morning'][0]['product_id']='P20'
   if change=='missing':del d['limitations']
   with self.assertRaises(ValueError):validate_response(json.dumps(d),self.catalogue)
 def test_minimized_context(self):
  a={'concerns':['dryness'],'skin_condition_description':'Dry appearance','age_estimate':30,'image_name':'private.jpg'}
  self.assertEqual(set(analysis_context(a)),{'concerns','skin_condition_description'})
  self.assertNotEqual(request_signature(a,self.catalogue),request_signature({'concerns':['oil']},self.catalogue))
 def test_app_empty_and_mock_api(self):
  app=AppTest.from_file('app.py').run()
  self.assertFalse(app.exception)
  app.sidebar.radio[0].set_value('💄 Recommendations').run()
  self.assertTrue(any('Complete a Skin Analysis' in i.value for i in app.info))
  app.session_state.current_analysis={'concerns':['Dryness'],'skin_condition_description':'Visible dry texture.'}
  app.session_state.api_key='test-only-not-a-real-key'
  app.run()
  with patch('config.config.API_KEY', 'test-only-not-a-real-key'), patch('modules.api_client.LLMClient.call_llm',return_value={'success':True,'response':json.dumps(self.output)}):
   next(b for b in app.button if b.label=='Generate Recommendations').click().run()
  self.assertFalse(app.exception)
  self.assertTrue(any('Hyaluronic Acid' in s.value for s in app.subheader))
  app.session_state.current_analysis={'concerns':['Oil'],'skin_condition_description':'Visible shine.'}
  app.run()
  self.assertIsNone(app.session_state.recommendations)

if __name__=='__main__':unittest.main()
