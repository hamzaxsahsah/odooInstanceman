from odoo.tests import common
from datetime import datetime, timedelta
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestInstanceRequest(common.TransactionCase):
    
    
    @classmethod
    def test_create_instance_request(self):
        # Create a sample instance request with a future limit date
        future_limit_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        instance_request_data = {
            "name": "Test Instance",
            "limit_date": future_limit_date,
            # Add other required fields
        }

        instance_request = self.env["kzm.instance.request"].create(instance_request_data)

        # # Check if the instance request was created successfully
        # self.assertTrue(instance_request)
        # self.assertEqual(instance_request.state, "draft")

    # def test_create_instance_request_past_limit_date(self):
    #     # Try to create an instance request with a past limit date, should raise a validation error
    #     past_limit_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    #     instance_request_data = {
    #         "name": "Test Instance",
    #         "limit_date": past_limit_date,
    #         # Add other required fields
    #     }

    #     with self.assertRaises(exceptions.ValidationError):
    #         self.env["kzm.instance.request"].create(instance_request_data)

    # def test_unlink_draft_instance_request(self):
    #     # Create a sample instance request in draft state
    #     instance_request_data = {
    #         "name": "Draft Instance",
    #         "state": "draft",
    #         # Add other required fields
    #     }

    #     draft_instance_request = self.env["kzm.instance.request"].create(instance_request_data)

    #     # Try to unlink the draft instance request
    #     draft_instance_request.unlink()

    #     # Check if the instance request was unlinked successfully
    #     self.assertFalse(draft_instance_request.exists())

    # def test_unlink_processed_instance_request(self):
    #     # Try to unlink a processed instance request, should raise a validation error
    #     processed_instance_request_data = {
    #         "name": "Processed Instance",
    #         "state": "processed",
    #         # Add other required fields
    #     }

    #     processed_instance_request = self.env["kzm.instance.request"].create(processed_instance_request_data)

    #     with self.assertRaises(exceptions.ValidationError):
    #         processed_instance_request.unlink()

    # # Add more test cases as needed for other methods and scenarios
