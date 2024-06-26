from models.transactions import TransactionModel
from models.users_credentials import UserModel
from models.users_events import EventModel
from models.users_profiles import UserProfileModel
from utilities.common import CommonUtils


class EventService:

    @staticmethod
    def is_existed_by_name(email: str, name: str):
        result = EventModel.find_by_email_name(email, name)
        return False if len(result) == 0 else True

    @staticmethod
    def create(email: str, name: str, budget: float):
        EventModel.create(email, name, budget)

    @staticmethod
    def get_list(email: str):
        login_id = UserModel.find_by_email(email)["id"]
        result = EventModel.find_all(login_id)
        events = []
        for item in result:
            events.append({
                "id": item[0],
                "name": item[1],
                "budget": item[2]
            })
        return events

    @staticmethod
    def get_budget_percentage(email: str, event_id: int, budget: int):
        login_id = UserModel.find_by_email(email)["id"]
        event_spent = EventModel.total_spent(login_id, event_id)
        return CommonUtils.calculate_budget_percentage(event_spent, budget)

    @staticmethod
    def is_existed_by_id(email: str, event_id: int):
        result = EventService.get(email, event_id)
        return False if len(result) == 0 else True

    @staticmethod
    def get(email: str, event_id: int) -> list[dict]:
        login_id = UserModel.find_by_email(email)["id"]
        result = EventModel.find_by_email_id(login_id, event_id)
        data = []
        for item in result:
            data.append({
                "id": item[0],
                "name": item[1],
                "budget": item[2],
                "spent": EventModel.total_spent(login_id, event_id)
            })
        return data


    @staticmethod
    def update(event_id: int, name: str, budget: float):
        EventModel.update(event_id, name, budget)

    @staticmethod
    def delete(id: int, email: str):
        EventModel.delete(id)

    @staticmethod
    def get_transactions(event_id: int) -> list[dict]:
        result = TransactionModel.get_by_event(event_id)
        data = []
        for item in result:
            data.append({
                "id": item[0],
                "transaction": item[1],
                "mode": item[2],
                "datestamp": item[3],
                "category": item[4],
                "note": item[5]
            })
        return data