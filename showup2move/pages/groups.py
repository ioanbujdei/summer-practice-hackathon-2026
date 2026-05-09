import reflex as rx
from showup2move.states.app_state import AppState, Group, GroupMember
from showup2move.states.matching_state import MatchingState


def group_member_avatar(member: GroupMember) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=member["avatar_url"],
            class_name="size-10 rounded-full border-2 border-white bg-gray-100",
            alt=member["name"],
        ),
        rx.cond(
            member["is_captain"],
            rx.el.div(
                rx.icon("crown", class_name="h-3 w-3 text-white"),
                class_name="absolute -top-1 -right-1 bg-yellow-400 rounded-full p-0.5 shadow-sm",
            ),
            None,
        ),
        title=rx.cond(
            member["is_captain"], f"{member['name']} (Captain)", member["name"]
        ),
        class_name="relative -ml-3 first:ml-0 transition-transform hover:z-10 hover:scale-110",
    )


def group_card(group: Group) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        group["icon"], class_name="h-5 w-5 text-emerald-600"
                    ),
                    class_name="p-2 bg-emerald-50 rounded-xl",
                ),
                rx.el.div(
                    rx.el.h3(
                        group["name"],
                        class_name="text-lg font-bold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        group["sport"],
                        class_name="text-sm text-gray-500 font-medium",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.match(
                group["status"],
                (
                    "forming",
                    rx.el.span(
                        "Forming",
                        class_name="px-3 py-1 bg-yellow-50 text-yellow-700 text-xs font-bold rounded-full border border-yellow-200",
                    ),
                ),
                (
                    "confirmed",
                    rx.el.span(
                        "Confirmed",
                        class_name="px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-full border border-emerald-200",
                    ),
                ),
                (
                    "playing",
                    rx.el.span(
                        "Playing Now",
                        class_name="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-bold rounded-full border border-blue-200",
                    ),
                ),
                rx.el.span(
                    group["status"],
                    class_name="px-3 py-1 bg-gray-50 text-gray-700 text-xs font-bold rounded-full border border-gray-200",
                ),
            ),
            class_name="flex justify-between items-start mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Roster",
                    class_name="text-xs font-bold uppercase text-gray-400 mb-2",
                ),
                rx.el.div(
                    rx.foreach(group["members"], group_member_avatar),
                    class_name="flex",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.p(
                    "Players",
                    class_name="text-xs font-bold uppercase text-gray-400 mb-2 text-right",
                ),
                rx.el.p(
                    f"{group['members'].length()} ready",
                    class_name="text-sm font-bold text-gray-900 text-right",
                ),
                class_name="shrink-0",
            ),
            class_name="flex justify-between items-end mb-8",
        ),
        rx.el.button(
            rx.icon("message-circle", class_name="h-4 w-4 mr-2"),
            "Open Chat",
            class_name="w-full flex items-center justify-center py-3 bg-gray-50 hover:bg-gray-100 text-gray-900 font-bold rounded-xl transition-colors border border-gray-200",
        ),
        class_name="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md hover:border-emerald-200 transition-all",
    )


def groups_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Your Groups", class_name="text-3xl font-black mb-2"),
                rx.el.p(
                    f"You are part of {AppState.active_groups_count} active groups",
                    class_name="text-gray-500 font-medium",
                ),
                class_name="flex flex-col",
            ),
            rx.el.button(
                rx.icon(
                    rx.cond(MatchingState.is_matching, "loader", "zap"),
                    class_name=rx.cond(
                        MatchingState.is_matching,
                        "mr-2 h-5 w-5 animate-spin",
                        "mr-2 h-5 w-5",
                    ),
                ),
                rx.cond(
                    MatchingState.is_matching,
                    "Finding Matches...",
                    "Find Match",
                ),
                on_click=MatchingState.run_matching,
                disabled=MatchingState.is_matching,
                class_name="flex items-center px-6 py-3 bg-emerald-600 text-white font-bold rounded-2xl shadow-lg shadow-emerald-200 hover:bg-emerald-700 transition-all disabled:opacity-75",
            ),
            class_name="flex justify-between items-center mb-10",
        ),
        rx.cond(
            AppState.groups.length() > 0,
            rx.el.div(
                rx.foreach(AppState.groups, group_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.icon("users", class_name="h-12 w-12 text-gray-300 mb-4"),
                rx.el.h3(
                    "No active groups yet",
                    class_name="text-xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Declare your availability on the dashboard to be matched into a group automatically!",
                    class_name="text-gray-500 text-center max-w-sm mb-6",
                ),
                rx.el.button(
                    "Find Match Now",
                    on_click=MatchingState.run_matching,
                    disabled=MatchingState.is_matching,
                    class_name="px-6 py-3 bg-gray-900 text-white font-bold rounded-xl",
                ),
                class_name="flex flex-col items-center justify-center p-20 bg-white rounded-3xl border-2 border-dashed border-gray-200",
            ),
        ),
    )