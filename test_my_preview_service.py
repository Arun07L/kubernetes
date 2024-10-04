from tests.test_preview_base import TestBase
from preview.server.services.preview_service import PreviewService


class TestMyPreviewService(TestBase):

    def test_my_update_item(self):
        self.session.set_user_by_email('arun@kissflow.com')
        ps = PreviewService(self.component)
        assert_dict = {"Name_1": "Arun", "Year": 2000, "Dept" : "Product"}
        item = ps.update_item("Preview_Model001","Preview_Model001","ActivityDef_001",assert_dict)
        self.assertIn("Name_1", item, "The Name not in Item Data")
        self.assertIn("Year", item, "The Year not in Item Data")
        self.assertIn("Age", item, "The Age not in Item Data")
        self.assertEqual(item.get("Age",0), 24, "Computed Value::Age is not equal to Expected Value")


    def test_my_get_item(self):
        ps = PreviewService(self.component)
        item = ps.get_item("Preview_Model001","Preview_Model001","ActivityDef_001")
        self.assertIn("_id",item,"The id not in Item Data")
        self.assertIn("Name", item, "The Name not in Item Data")
        self.assertIn("_created_by", item, "_created_by not in Item Data")
        self.assertIn("_modified_by", item, "_modified_by not in Item Data")
        self.assertIn("_created_at", item, "_created_at not in Item Data")
        self.assertIn("_modified_at", item, "_modified_at not in Item Data")
        self.assertIn("_flow_name", item, "_flow_name not in Item Data")
        self.assertIn("_flow_type", item, "_flow_type not in Item Data")
        self.assertIn("_status", item, "_flow_type not in Item Data")
        self.assertIn("_stage", item, "_flow_type not in Item Data")
        self.assertIn("_root_process_instance", item, "_flow_type not in Item Data")
        self.assertIn("_triggered_integrations", item, "_triggered_integrations not in Item Data")

    def test_my_approve_item(self):
        self.session.set_user_by_email('arun@kissflow.com')
        ps = PreviewService(self.component)
        item = ps.approve("Preview_Model001", "Preview_Model001", "ActivityDef_002")
        print(item)
        self.assertIn("_last_completed_step", item, "_last_completed_step not in Item")


    def test_my_get_progress(self):
        ps = PreviewService(self.component)
        item = ps.get_progress("Preview_Model001", "Preview_Model001")
        self.assertIn("_id", item, "The id not in Item Data")
        self.assertIn("ProcessId", item, "The ProcessId not in Item Data")
        self.assertIn("ProcessName", item, "The ProcessName not in Item Data")
        self.assertIn("ProcessName", item, "The ProcessName not in Item Data")
        self.assertIn("_status", item, "The _status not in Item Data")
        self.assertIn("_progress", item, "The _progress not in Item Data")
        self.assertIn("Steps", item, "The Steps not in Item Data")

    def test_my_reset_progress(self):
        self.session.set_user_by_email('arun@kissflow.com')
        ps = PreviewService(self.component)
        ps.reset_progress("Preview_Model001","Preview_Model001")
        item = self.session.get(self.session.get_model_by_id("Preview_Model001"),"Preview_Model001")._doc
        pi = item["ProcessInstance"][0]
        ai = item["ActivityInstance"][0]
        self.assertEqual(item["Age"], 0, "The data is not reset")
        self.assertEqual(pi["CurrentActivityInstance"], "ActivityDef_001", "The CurrentActivityInstance not in Item")
        self.assertEqual(pi["StartActivityInstance"], "ActivityDef_001", "The StartActivityInstance not in Item")
        self.assertEqual(ai["ScriptName"], "Start", "The ScriptName not in Item")
        self.assertEqual(ai["NodeType"], "StartEvent", "The NodeType not in Item")
        self.assertEqual(ai["_status"], "InProgress", "The _status not in Item")

    def test_my_create_item(self):
        self.session.set_user_by_email('arun@kissflow.com')
        ps = PreviewService(self.component)
        item = ps.create_item('Preview_Model001')
        self.assertEqual(item["Age"], 0, "Not created")



