import reflex as rx
import asyncio
import random
import datetime
from faker import Faker
from showup2move.states.user_state import UserState
from showup2move.states.app_state import AppState, Group, GroupMember

fake = Faker()


class MatchingState(rx.State):
    is_matching: bool = False

    @rx.event(background=True)
    async def run_matching(self):
        async with self:
            if self.is_matching:
                return
            self.is_matching = True
        await asyncio.sleep(2)
        async with self:
            user_state = await self.get_state(UserState)
            app_state = await self.get_state(AppState)
            active_sports = [s for s in user_state.sports_list if s["selected"]]
            if not active_sports:
                self.is_matching = False
                return rx.toast(
                    "Please select at least one sport in your profile to be matched!",
                    duration=4000,
                )
            chosen_sport = random.choice(active_sports)
            sport_name = chosen_sport["name"]
            sport_icon = chosen_sport["icon"]
            size_rules = {
                "Football": (10, 14),
                "Tennis": (2, 4),
                "Basketball": (6, 10),
                "Running": (3, 8),
                "Volleyball": (8, 12),
            }
            min_size, max_size = size_rules.get(sport_name, (4, 8))
            group_size = random.randint(min_size, max_size)
            members: list[GroupMember] = []
            for _ in range(group_size - 1):
                members.append(
                    {
                        "name": fake.first_name(),
                        "avatar_url": f"https://api.dicebear.com/9.x/notionists/svg?seed={random.randint(1000, 9999)}",
                        "is_captain": False,
                    }
                )
            members.append(
                {
                    "name": user_state.name,
                    "avatar_url": user_state.avatar_url,
                    "is_captain": False,
                }
            )
            captain_idx = random.randint(0, len(members) - 1)
            members[captain_idx]["is_captain"] = True
            adjectives = [
                "Sunday",
                "Morning",
                "Sunset",
                "Lightning",
                "Thunder",
                "Urban",
                "Casual",
            ]
            nouns = ["Squad", "Duo", "Team", "Crew", "Club", "Maniacs"]
            group_name = f"{random.choice(adjectives)} {sport_name} {random.choice(nouns)}"
            new_group: Group = {
                "id": str(random.randint(10000, 99999)),
                "name": group_name,
                "sport": sport_name,
                "icon": sport_icon,
                "members": members,
                "status": "forming",
                "created_at": datetime.datetime.now().strftime("%I:%M %p"),
            }
            app_state.groups.append(new_group)
            app_state.active_groups_count = len(app_state.groups)
            app_state.activities.insert(
                0,
                {
                    "id": str(random.randint(10000, 99999)),
                    "user": "System",
                    "action": "formed a new group:",
                    "target": group_name,
                    "time": "Just now",
                    "icon": "users",
                },
            )
            from showup2move.states.chat_state import ChatState

            chat_state = await self.get_state(ChatState)
            chat_state.messages.append(
                {
                    "id": str(random.randint(100000, 999999)),
                    "group_id": new_group["id"],
                    "sender_name": "System",
                    "avatar_url": "",
                    "content": f"Welcome to {group_name}! Introduce yourselves and decide on a time/venue.",
                    "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                    "is_system": True,
                }
            )
            from showup2move.states.notification_state import NotificationState

            notif_state = await self.get_state(NotificationState)
            notif_state.add_notification(
                "group", f"New group formed: {group_name}"
            )
            self.is_matching = False
            return rx.toast(
                f"Match found! You were added to {group_name}.", duration=5000
            )