import reflex as rx
from showup2move.states.user_state import UserState


def sport_interest_card(sport: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    sport["icon"],
                    class_name=rx.cond(
                        sport["selected"],
                        "h-6 w-6 text-white",
                        "h-6 w-6 text-gray-400",
                    ),
                ),
                class_name=rx.cond(
                    sport["selected"],
                    "p-3 bg-emerald-500 rounded-xl",
                    "p-3 bg-gray-100 rounded-xl",
                ),
            ),
            rx.el.div(
                rx.el.p(sport["name"], class_name="font-bold text-gray-900"),
                rx.el.select(
                    rx.el.option("Beginner", value="Beginner"),
                    rx.el.option("Intermediate", value="Intermediate"),
                    rx.el.option("Advanced", value="Advanced"),
                    value=sport["level"],
                    on_change=lambda val: UserState.update_skill(
                        sport["name"], val
                    ),
                    class_name="text-xs text-gray-500 bg-transparent border-none p-0 focus:ring-0 cursor-pointer appearance-none",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-4",
        ),
        on_click=lambda: UserState.toggle_sport(sport["name"]),
        class_name=rx.cond(
            sport["selected"],
            "p-4 rounded-2xl border-2 border-emerald-500 bg-emerald-50 cursor-pointer transition-all",
            "p-4 rounded-2xl border border-gray-100 bg-white hover:border-emerald-200 cursor-pointer transition-all",
        ),
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src=UserState.avatar_url,
                        class_name="size-24 rounded-full border-4 border-white shadow-lg",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            UserState.name, class_name="text-3xl font-black"
                        ),
                        rx.el.p(UserState.location, class_name="text-gray-500"),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-6",
                ),
                rx.el.div(
                    rx.el.p(
                        f"Profile {UserState.profile_completeness}% Complete",
                        class_name="text-sm font-bold text-gray-900 mb-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            class_name="h-full bg-emerald-500 rounded-full",
                            style={
                                "width": f"{UserState.profile_completeness}%"
                            },
                        ),
                        class_name="w-48 h-2 bg-gray-200 rounded-full",
                    ),
                    class_name="flex flex-col items-end",
                ),
                class_name="flex justify-between items-center mb-10",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Display Name",
                            class_name="text-sm font-bold text-gray-700 mb-2 block",
                        ),
                        rx.el.input(
                            name="name",
                            default_value=UserState.name,
                            class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:border-emerald-500 outline-none",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Location",
                            class_name="text-sm font-bold text-gray-700 mb-2 block",
                        ),
                        rx.el.input(
                            name="location",
                            default_value=UserState.location,
                            class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:border-emerald-500 outline-none",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Bio / Description",
                        class_name="text-sm font-bold text-gray-700 mb-2 block",
                    ),
                    rx.el.textarea(
                        name="bio",
                        default_value=UserState.bio,
                        class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:border-emerald-500 outline-none h-32",
                    ),
                    class_name="mb-10",
                ),
                rx.el.h3(
                    "Sports Interests & Skill Levels",
                    class_name="text-xl font-bold mb-6",
                ),
                rx.el.div(
                    rx.foreach(UserState.sports_list, sport_interest_card),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-10",
                ),
                rx.el.button(
                    "Save Profile Changes",
                    type="submit",
                    class_name="px-8 py-4 bg-gray-900 text-white font-bold rounded-2xl hover:bg-emerald-600 shadow-xl transition-all",
                ),
                on_submit=UserState.save_profile,
            ),
            class_name="bg-white p-10 rounded-3xl border border-gray-100 shadow-sm",
        )
    )