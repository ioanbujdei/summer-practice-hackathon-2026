import reflex as rx
from typing import TypedDict
import datetime
import random
from showup2move.states.user_state import UserState


class ChatMessage(TypedDict):
    id: str
    group_id: str
    sender_name: str
    avatar_url: str
    content: str
    timestamp: str
    is_system: bool


class PollOption(TypedDict):
    id: str
    text: str
    votes: int


class Poll(TypedDict):
    id: str
    group_id: str
    question: str
    options: list[PollOption]
    voter_ids: list[str]
    total_votes: int


class ChatState(rx.State):
    active_group_id: str = ""
    messages: list[ChatMessage] = []
    polls: list[Poll] = []
    message_input: str = ""
    poll_question_input: str = ""
    poll_options_input: str = ""
    show_poll_modal: bool = False

    @rx.event
    def set_active_group(self, group_id: str):
        self.active_group_id = group_id

    @rx.event
    def set_message_input(self, value: str):
        self.message_input = value

    @rx.event
    def set_poll_question_input(self, value: str):
        self.poll_question_input = value

    @rx.event
    def set_poll_options_input(self, value: str):
        self.poll_options_input = value

    @rx.event
    def toggle_poll_modal(self):
        self.show_poll_modal = not self.show_poll_modal

    @rx.var
    def active_messages(self) -> list[ChatMessage]:
        if not self.active_group_id:
            return []
        return [
            m for m in self.messages if m["group_id"] == self.active_group_id
        ]

    @rx.var
    def active_polls(self) -> list[Poll]:
        if not self.active_group_id:
            return []
        return [p for p in self.polls if p["group_id"] == self.active_group_id]

    @rx.event
    async def send_message(self):
        if not self.message_input.strip() or not self.active_group_id:
            return
        user_state = await self.get_state(UserState)
        self.messages.append(
            {
                "id": str(random.randint(100000, 999999)),
                "group_id": self.active_group_id,
                "sender_name": user_state.name,
                "avatar_url": user_state.avatar_url,
                "content": self.message_input,
                "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                "is_system": False,
            }
        )
        self.message_input = ""

    @rx.event
    def create_poll(self):
        if (
            not self.poll_question_input.strip()
            or not self.poll_options_input.strip()
            or (not self.active_group_id)
        ):
            return
        options = [
            opt.strip()
            for opt in self.poll_options_input.split(",")
            if opt.strip()
        ]
        if not options:
            return
        poll_options = []
        for i, opt in enumerate(options):
            poll_options.append({"id": str(i), "text": opt, "votes": 0})
        self.polls.append(
            {
                "id": str(random.randint(100000, 999999)),
                "group_id": self.active_group_id,
                "question": self.poll_question_input,
                "options": poll_options,
                "voter_ids": [],
                "total_votes": 0,
            }
        )
        self.poll_question_input = ""
        self.poll_options_input = ""
        self.show_poll_modal = False
        self.messages.append(
            {
                "id": str(random.randint(100000, 999999)),
                "group_id": self.active_group_id,
                "sender_name": "System",
                "avatar_url": "",
                "content": f"A new poll was created: '{self.poll_question_input}'",
                "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                "is_system": True,
            }
        )

    @rx.event
    def vote_poll(self, poll_id: str, option_id: str):
        for p in self.polls:
            if p["id"] == poll_id:
                user_token = self.router.session.client_token
                if user_token in p["voter_ids"]:
                    return rx.toast("You already voted!", duration=2000)
                p["voter_ids"].append(user_token)
                for opt in p["options"]:
                    if opt["id"] == option_id:
                        opt["votes"] += 1
                        p["total_votes"] += 1
                break