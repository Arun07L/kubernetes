from server.services.process_service import ProcessService
from tests.test_base import TestBase, mock__publish_messages


class TestProcessService(TestBase):

    def test_pending_task_count_by_activity_with_query_params(self):
        self.session.set_user_by_email("neo@orangescape.com")
        ps = ProcessService(self.component)
        query_params = '123'
        res = ps.get_pending_task_count_by_activity(process_id="Model001", activity_id="ActivityDef002",
                                                    query_params=query_params)

        self.assertEqual(res["Count"], 3, msg="Pending task count is not correct.")
        self.assertIn("Count", res, msg="Count key is not found in the response.")

    def test_get_my_tasks_skip_aggregation_with_query_params(self):
        self.session.set_user_by_email('trinity@orangescape.com')
        ps = ProcessService(self.component)
        data = ps.get_pending_tasks('Model004', "ActivityDef021", skip_aggregation=True, query_params="Air India")

        self.assertEqual(len(data["Data"]), 3)
        self.assertEqual(data.get("Aggregation"), None)