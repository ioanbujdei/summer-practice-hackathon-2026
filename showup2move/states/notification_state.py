import reflex as rx
from typing import TypedDict


class Notification(TypedDict):
    id: str
    type: str
    message: str
    timestamp: str
    read: bool


class NotificationState(rx.State):
    notifications: list[Notification] = [
        {
            "id": "1",
            "type": "group",
            "message": "New group formed: Sunday Football Squad",
            "timestamp": "10m ago",
            "read": False,
        },
        {
            "id": "2",
            "type": "event",
            "message": "Match starting in 1 hour at Mission Bay Park",
            "timestamp": "1h ago",
            "read": False,
        },
        {
            "id": "3",
            "type": "poll",
            "message": "Poll created: Which venue do you prefer?",
            "timestamp": "2h ago",
            "read": True,
        },
    ]
    show_dropdown: bool = False

    @rx.event
    def toggle_dropdown(self):
        self.show_dropdown = not self.show_dropdown

    @rx.event
    def mark_as_read(self, notif_id: str):
        for n in self.notifications:
            if n["id"] == notif_id:
                n["read"] = True
                break

    @rx.event
    def add_notification(self, type: str, message: str):
        self.notifications.insert(
            0,
            {
                "id": str(len(self.notifications) + 1),
                "type": type,
                "message": message,
                "timestamp": "Just now",
                "read": False,
            },
        )

    @rx.var
    def unread_count(self) -> int:
        return sum((1 for n in self.notifications if not n["read"]))


def render_notification(notif: Notification) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.match(
                notif["type"],
                (
                    "group",
                    rx.icon("users", class_name="h-4 w-4 text-emerald-600"),
                ),
                (
                    "event",
                    rx.icon("calendar", class_name="h-4 w-4 text-blue-600"),
                ),
                (
                    "poll",
                    rx.icon("bar-chart", class_name="h-4 w-4 text-purple-600"),
                ),
                rx.icon("bell", class_name="h-4 w-4 text-gray-600"),
            ),
            class_name="p-2 bg-gray-50 rounded-full shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                notif["message"],
                class_name=rx.cond(
                    notif["read"],
                    "text-sm text-gray-600",
                    "text-sm font-bold text-gray-900",
                ),
            ),
            rx.el.p(
                notif["timestamp"], class_name="text-xs text-gray-400 mt-1"
            ),
            class_name="flex-1",
        ),
        on_click=lambda: NotificationState.mark_as_read(notif["id"]),
        class_name=rx.cond(
            notif["read"],
            "flex gap-3 p-4 border-b border-gray-50 hover:bg-gray-50 cursor-pointer transition-colors opacity-70",
            "flex gap-3 p-4 border-b border-gray-50 bg-emerald-50/30 hover:bg-emerald-50/50 cursor-pointer transition-colors",
        ),
    )