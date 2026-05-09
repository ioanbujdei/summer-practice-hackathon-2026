import reflex as rx
from typing import TypedDict


class SportPreference(TypedDict):
    name: str
    icon: str
    level: str
    selected: bool


class UserState(rx.State):
    name: str = "Alex Johnson"
    email: str = "alex@showup2move.com"
    bio: str = "Love outdoor sports and meeting new teammates! Usually free weekday evenings."
    location: str = "San Francisco, CA"
    avatar_url: str = "https://api.dicebear.com/9.x/notionists/svg?seed=Alex"
    availability_today: str = "undecided"
    show_up_streak: int = 12
    sports_played: int = 4
    sports_list: list[SportPreference] = [
        {
            "name": "Football",
            "icon": "ball-football",
            "level": "Intermediate",
            "selected": True,
        },
        {
            "name": "Tennis",
            "icon": "armchair",
            "level": "Beginner",
            "selected": False,
        },
        {
            "name": "Basketball",
            "icon": "basketball",
            "level": "Advanced",
            "selected": True,
        },
        {
            "name": "Running",
            "icon": "run",
            "level": "Intermediate",
            "selected": True,
        },
        {
            "name": "Volleyball",
            "icon": "volleyball",
            "level": "Beginner",
            "selected": False,
        },
        {
            "name": "Swimming",
            "icon": "waves",
            "level": "Intermediate",
            "selected": False,
        },
        {
            "name": "Cycling",
            "icon": "bike",
            "level": "Intermediate",
            "selected": False,
        },
        {
            "name": "Badminton",
            "icon": "shuttlecock",
            "level": "Beginner",
            "selected": False,
        },
        {
            "name": "Yoga",
            "icon": "lotus",
            "level": "Intermediate",
            "selected": True,
        },
    ]

    @rx.event
    def set_availability(self, status: str):
        self.availability_today = status
        if status == "yes":
            self.show_up_streak += 1
            from showup2move.states.matching_state import MatchingState

            yield rx.toast(
                "Awesome! We're looking for matches for you today...",
                duration=3000,
            )
            yield MatchingState.run_matching
        elif status == "no":
            yield rx.toast(
                "Got it! Rest up and we'll catch you next time.", duration=3000
            )

    @rx.event
    def toggle_sport(self, sport_name: str):
        for sport in self.sports_list:
            if sport["name"] == sport_name:
                sport["selected"] = not sport["selected"]
                break

    @rx.event
    def update_skill(self, sport_name: str, new_level: str):
        for sport in self.sports_list:
            if sport["name"] == sport_name:
                sport["level"] = new_level
                break

    @rx.event
    def save_profile(self, form_data: dict):
        self.name = form_data.get("name", self.name)
        self.bio = form_data.get("bio", self.bio)
        self.location = form_data.get("location", self.location)
        yield rx.toast("Profile saved successfully!", duration=2000)

    @rx.var
    def active_sports_count(self) -> int:
        return sum((1 for s in self.sports_list if s["selected"]))

    @rx.var
    def profile_completeness(self) -> int:
        score = 0
        if self.name:
            score += 25
        if self.bio:
            score += 25
        if self.location:
            score += 25
        if self.active_sports_count > 0:
            score += 25
        return score