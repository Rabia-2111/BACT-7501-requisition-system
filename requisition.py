requisition_counter = 10000


class Requisitionsystem:
    """Manages staff requisitions, approvals, reference numbers, and statistics."""

    def __init__(self):
        self.requisitions_list = []
        self.total_submitted = 0
        self.total_approved = 0
        self.total_pending = 0
        self.total_not_approved = 0

    def _generate_approval_ref(self, staff_id, req_id):
        """Generate approval reference code such as FN19001 from staff ID and requisition ID."""
        suffix = str(req_id)[-3:].zfill(3)
        return f"{staff_id}{suffix}"

    def add_requisition(self, date, staff_id, staff_name, items_data):
        """Add a new requisition, calculate total cost, and apply auto-approval under $500."""
        global requisition_counter
        requisition_counter += 1
        req_id = requisition_counter

        total = sum(item["cost"] for item in items_data)
        self.total_submitted += 1

        if total < 500:
            status = "Approved"
            approval_ref = self._generate_approval_ref(staff_id, req_id)
            self.total_approved += 1
        else:
            status = "Pending"
            approval_ref = "Not available"
            self.total_pending += 1

        requisition = {
            "date": date,
            "requisition_id": req_id,
            "staff_id": staff_id,
            "staff_name": staff_name,
            "items": items_data,
            "total": total,
            "status": status,
            "approval_reference": approval_ref,
            "rejection_reason": None
        }

        self.requisitions_list.append(requisition)
        print(f"Requisition ID {req_id} successfully added! Status: {status}")
        return req_id

    def respond_to_requisition(self, req_id, decision, reason=""):
        """Update a pending requisition to Approved or Not Approved and adjust counters."""
        for req in self.requisitions_list:
            if req["requisition_id"] == req_id:
                if req["status"] == "Pending":
                    decision_clean = decision.strip().lower()

                    if decision_clean == "approved":
                        req["status"] = "Approved"
                        req["approval_reference"] = self._generate_approval_ref(
                            req["staff_id"], req["requisition_id"]
                        )
                        self.total_pending -= 1
                        self.total_approved += 1
                        print(f"Requisition ID {req_id} has been Approved.")
                        return True

                    if decision_clean in ["not approved", "not_approved", "rejected"]:
                        req["status"] = "Not Approved"
                        req["approval_reference"] = "Not available"
                        req["rejection_reason"] = reason
                        self.total_pending -= 1
                        self.total_not_approved += 1
                        print(f"Requisition ID {req_id} has been Not Approved.")
                        return True

                    print("Invalid decision! Use 'Approved' or 'Not Approved'.")
                    return False

                print(f"Requisition ID {req_id} is not Pending.")
                return False

        print(f"Requisition ID {req_id} not found.")
        return False

    def display_requisitions(self):
        """Display formatted details for all stored requisitions."""
        if not self.requisitions_list:
            print("No requisitions found.")
            return

        print("\nDisplaying Requisitions:")
        for req in self.requisitions_list:
            print(f"Date: {req['date']}")
            print(f"Requisition ID: {req['requisition_id']}")
            print(f"Staff ID: {req['staff_id']}")
            print(f"Staff Name: {req['staff_name']}")
            print(f"Total: ${req['total']}")
            print(f"Status: {req['status']}")
            print(f"Approval Reference Number: {req['approval_reference']}")
            if req["status"] == "Not Approved" and req["rejection_reason"]:
                print(f"Rejection Reason: {req['rejection_reason']}")
            print()

    def display_statistics(self):
        """Display counts for submitted, approved, pending, and not approved requisitions."""
        print("\nStatistics:")
        print("Displaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {self.total_submitted}")
        print(f"The total number of approved requisitions: {self.total_approved}")
        print(f"The total number of pending requisitions: {self.total_pending}")
        print(f"The total number of not approved requisitions: {self.total_not_approved}")
        #commit 3 update