import reflex as rx
from typing import TypedDict
from faker import Faker

fake = Faker()


class GroupMember(TypedDict):
    name: str
    avatar_url: str
    is_captain: bool


class Group(TypedDict):
    id: str
    name: str
    sport: str
    icon: str
    members: list[GroupMember]
    status: str
    created_at: str


class Event(TypedDict):
    id: str
    sport: str
    date: str
    time: str
    location: str
    participants: int
    max_participants: int
    creator: str


class Activity(TypedDict):
    id: str
    user: str
    action: str
    target: str
    time: str
    icon: str


class AppState(rx.State):
    upcoming_events: list[Event] = [
        {
            "id": "1",
            "sport": "Football",
            "date": "Today",
            "time": "6:00 PM",
            "location": "Mission Bay Park",
            "participants": 8,
            "max_participants": 14,
            "creator": "Mark S.",
        },
        {
            "id": "2",
            "sport": "Basketball",
            "date": "Tomorrow",
            "time": "5:30 PM",
            "location": "Dolores Park Courts",
            "participants": 5,
            "max_participants": 10,
            "creator": "Sarah L.",
        },
        {
            "id": "3",
            "sport": "Tennis",
            "date": "Sat, Oct 26",
            "time": "10:00 AM",
            "location": "Golden Gate Courts",
            "participants": 2,
            "max_participants": 4,
            "creator": "David W.",
        },
    ]
    activities: list[Activity] = [
        {
            "id": "1",
            "user": "Elena R.",
            "action": "joined the",
            "target": "Football Match",
            "time": "10m ago",
            "icon": "user-plus",
        },
        {
            "id": "2",
            "user": "You",
            "action": "confirmed",
            "target": "Yoga Session",
            "time": "2h ago",
            "icon": "check-circle",
        },
        {
            "id": "3",
            "user": "Chris P.",
            "action": "created",
            "target": "Morning Run",
            "time": "5h ago",
            "icon": "plus-circle",
        },
    ]
    groups: list[Group] = []
    active_groups_count: int = 0
    is_creating_event: bool = False
    event_sport_filter: str = "All"

    @rx.event
    def toggle_create_modal(self):
        self.is_creating_event = not self.is_creating_event

    @rx.event
    async def create_event(self, form_data: dict):
        new_event: Event = {
            "id": str(len(self.upcoming_events) + 1),
            "sport": form_data.get("sport", "General"),
            "date": form_data.get("date", "TBD"),
            "time": form_data.get("time", "TBD"),
            "location": form_data.get("location", "TBD"),
            "participants": 1,
            "max_participants": int(form_data.get("max_players", 10)),
            "creator": "You",
        }
        self.upcoming_events.append(new_event)
        self.is_creating_event = False
        self.activities.insert(
            0,
            {
                "id": str(len(self.activities) + 1),
                "user": "You",
                "action": "created",
                "target": f"{new_event['sport']} Match",
                "time": "Just now",
                "icon": "calendar-plus",
            },
        )
        from showup2move.states.notification_state import NotificationState

        notif_state = await self.get_state(NotificationState)
        notif_state.add_notification(
            "event", f"You created a new {new_event['sport']} match."
        )
        yield rx.toast(
            "Event created! Others can now see and join.", duration=3000
        )