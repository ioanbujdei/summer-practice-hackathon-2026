import reflex as rx
from typing import TypedDict
import random
from showup2move.states.user_state import UserState, SportPreference

UPLOAD_ID = "profile_upload"


class RegistrationState(rx.State):
    current_step: int = 1
    name: str = ""
    email: str = ""
    location: str = ""
    bio: str = ""
    selected_sports: list[SportPreference] = [
        {
            "name": "Football",
            "icon": "ball-football",
            "level": "Beginner",
            "selected": False,
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
            "level": "Beginner",
            "selected": False,
        },
        {
            "name": "Running",
            "icon": "run",
            "level": "Beginner",
            "selected": False,
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
            "level": "Beginner",
            "selected": False,
        },
        {
            "name": "Cycling",
            "icon": "bike",
            "level": "Beginner",
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
            "level": "Beginner",
            "selected": False,
        },
    ]
    uploaded_photo: str = ""
    TIME_SLOTS: list[str] = [
        "6-9 AM",
        "9-12 PM",
        "12-3 PM",
        "3-6 PM",
        "6-9 PM",
        "9-12 AM",
    ]
    DAYS: list[str] = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekly_availability: dict[str, list[str]] = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": [],
    }
    is_registered: bool = False

    @rx.var
    def step_one_valid(self) -> bool:
        return (self.name.strip() != "") & (self.email.strip() != "")

    @rx.var
    def any_sport_selected(self) -> bool:
        return any((s["selected"] for s in self.selected_sports))

    @rx.event
    def next_step(self):
        if self.current_step == 1:
            if not self.step_one_valid:
                return rx.toast("Please provide name and email.")
        elif self.current_step == 2:
            if not self.any_sport_selected:
                return rx.toast("Select at least one sport.")
        if self.current_step < 3:
            self.current_step += 1

    @rx.event
    def prev_step(self):
        if self.current_step > 1:
            self.current_step -= 1

    @rx.event
    def toggle_sport(self, sport_name: str):
        for sport in self.selected_sports:
            if sport["name"] == sport_name:
                sport["selected"] = not sport["selected"]
                break

    @rx.event
    def update_sport_level(self, sport_name: str, level: str):
        for sport in self.selected_sports:
            if sport["name"] == sport_name:
                sport["level"] = level
                break

    @rx.event
    def toggle_time_slot(self, day: str, slot: str):
        if slot in self.weekly_availability[day]:
            self.weekly_availability[day].remove(slot)
        else:
            self.weekly_availability[day].append(slot)

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            unique_name = f"{random.randint(1000, 9999)}_{file.name}"
            file_path = upload_dir / unique_name
            with file_path.open("wb") as f:
                f.write(upload_data)
            self.uploaded_photo = unique_name

    @rx.event
    async def complete_registration(self):
        if not self.step_one_valid or not self.any_sport_selected:
            yield rx.toast("Please ensure all steps are filled out correctly.")
            return
        user_state = await self.get_state(UserState)
        user_state.name = self.name
        user_state.email = self.email
        user_state.location = self.location
        user_state.bio = self.bio
        user_state.sports_list = self.selected_sports
        if self.uploaded_photo:
            user_state.avatar_url = self.uploaded_photo
        else:
            user_state.avatar_url = (
                f"https://api.dicebear.com/9.x/notionists/svg?seed={self.name}"
            )
        self.is_registered = True
        yield rx.toast("Welcome to ShowUp2Move! Redirecting...", duration=2000)
        yield rx.redirect("/")

    @rx.event
    def set_name(self, val: str):
        self.name = val

    @rx.event
    def set_email(self, val: str):
        self.name = val

    @rx.event
    def set_location(self, val: str):
        self.name = val

    @rx.event
    def set_bio(self, val: str):
        self.name = val