import reflex as rx
from showup2move.states.user_state import UserState
from showup2move.states.app_state import AppState
from showup2move.components.cards import stat_card, event_card
from showup2move.states.matching_state import MatchingState


def availability_prompt() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "ShowUpToday?",
                    class_name="text-2xl font-black text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Ready to burn some calories and meet new people?",
                    class_name="text-gray-600",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("check", class_name="mr-2 h-5 w-5"),
                    "Yes, Count me in",
                    on_click=lambda: UserState.set_availability("yes"),
                    disabled=MatchingState.is_matching,
                    class_name=rx.cond(
                        UserState.availability_today == "yes",
                        "flex items-center px-6 py-3 bg-emerald-600 text-white rounded-2xl font-bold shadow-lg shadow-emerald-200 disabled:opacity-75",
                        "flex items-center px-6 py-3 bg-emerald-50 text-emerald-600 rounded-2xl font-bold border border-emerald-100 hover:bg-emerald-600 hover:text-white transition-all disabled:opacity-50",
                    ),
                ),
                rx.el.button(
                    rx.icon("x", class_name="mr-2 h-5 w-5"),
                    "Not today",
                    on_click=lambda: UserState.set_availability("no"),
                    disabled=MatchingState.is_matching,
                    class_name=rx.cond(
                        UserState.availability_today == "no",
                        "flex items-center px-6 py-3 bg-red-500 text-white rounded-2xl font-bold shadow-lg shadow-red-200 disabled:opacity-75",
                        "flex items-center px-6 py-3 bg-red-50 text-red-600 rounded-2xl font-bold border border-red-100 hover:bg-red-500 hover:text-white transition-all disabled:opacity-50",
                    ),
                ),
                class_name="flex gap-4",
            ),
            class_name="flex flex-col md:flex-row items-center gap-6",
        ),
        class_name="bg-white p-8 rounded-3xl border-2 border-emerald-100 shadow-xl shadow-emerald-900/5 mb-10 relative overflow-hidden",
    )


def activity_item(activity: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(activity["icon"], class_name="h-4 w-4 text-emerald-600"),
            class_name="p-2 bg-emerald-50 rounded-full shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    activity["user"], class_name="font-bold text-gray-900"
                ),
                f" {activity['action']} ",
                rx.el.span(
                    activity["target"],
                    class_name="font-semibold text-emerald-600",
                ),
                class_name="text-sm text-gray-600",
            ),
            rx.el.p(activity["time"], class_name="text-xs text-gray-400 mt-1"),
            class_name="flex-1",
        ),
        class_name="flex gap-4 py-4 border-b border-gray-50 last:border-0",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        availability_prompt(),
        rx.el.div(
            stat_card(
                "Active Groups",
                AppState.active_groups_count.to_string(),
                "users",
            ),
            stat_card("Upcoming Events", "3", "calendar"),
            stat_card(
                "Sports Played", UserState.sports_played.to_string(), "trophy"
            ),
            stat_card(
                "Show-up Streak",
                f"{UserState.show_up_streak} Days",
                "flame",
                trend="+2 this week",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Upcoming Matches", class_name="text-xl font-bold"
                    ),
                    rx.el.button(
                        "See All",
                        class_name="text-sm font-semibold text-emerald-600 hover:underline",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.foreach(AppState.upcoming_events, event_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                ),
                class_name="lg:col-span-2",
            ),
            rx.el.div(
                rx.el.h3("Activity Feed", class_name="text-xl font-bold mb-6"),
                rx.el.div(
                    rx.foreach(AppState.activities, activity_item),
                    class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                ),
                class_name="lg:col-span-1",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-10",
        ),
    )