import reflex as rx
from showup2move.states.app_state import AppState
from showup2move.components.cards import event_card
from showup2move.states.event_detail_state import EventDetailState


def create_event_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Create New Match", class_name="text-2xl font-black mb-2"
                ),
                rx.el.p(
                    "Organize a sport and find teammates near you.",
                    class_name="text-gray-500",
                ),
                rx.el.button(
                    rx.icon("x"),
                    on_click=AppState.toggle_create_modal,
                    class_name="absolute top-6 right-6",
                ),
                class_name="mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Sport",
                            class_name="text-xs font-bold uppercase text-gray-400 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Football"),
                            rx.el.option("Basketball"),
                            rx.el.option("Tennis"),
                            rx.el.option("Running"),
                            name="sport",
                            class_name="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl appearance-none",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Max Players",
                            class_name="text-xs font-bold uppercase text-gray-400 mb-1",
                        ),
                        rx.el.input(
                            name="max_players",
                            type="number",
                            placeholder="10",
                            class_name="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Date",
                            class_name="text-xs font-bold uppercase text-gray-400 mb-1",
                        ),
                        rx.el.input(
                            name="date",
                            type="date",
                            class_name="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Time",
                            class_name="text-xs font-bold uppercase text-gray-400 mb-1",
                        ),
                        rx.el.input(
                            name="time",
                            type="time",
                            class_name="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex gap-4 mb-4",
                ),
                rx.el.label(
                    "Location Name",
                    class_name="text-xs font-bold uppercase text-gray-400 mb-1",
                ),
                rx.el.input(
                    name="location",
                    placeholder="e.g. Golden Gate Park",
                    class_name="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl mb-6",
                ),
                rx.el.button(
                    "Launch Event",
                    type="submit",
                    class_name="w-full py-4 bg-emerald-600 text-white font-bold rounded-2xl shadow-lg shadow-emerald-200",
                ),
                on_submit=AppState.create_event,
            ),
            class_name="bg-white p-8 rounded-3xl w-full max-w-lg relative",
        ),
        class_name=rx.cond(
            AppState.is_creating_event,
            "fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4",
            "hidden",
        ),
    )


def venue_card(
    name: str, address: str, price: str, rating: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h5(name, class_name="font-bold text-gray-900 text-sm"),
            rx.el.p(address, class_name="text-xs text-gray-500"),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.span(
                price,
                class_name="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md",
            ),
            rx.el.span(
                rx.icon(
                    "star", class_name="h-3 w-3 inline mr-1 text-yellow-400"
                ),
                rating,
                class_name="text-xs font-bold text-gray-700 ml-2",
            ),
            class_name="flex items-center",
        ),
        class_name="flex justify-between items-center p-3 border border-gray-100 rounded-xl mb-2 hover:border-emerald-200 transition-colors",
    )


def event_card_with_details(event: dict) -> rx.Component:
    is_expanded = EventDetailState.selected_event_id == event["id"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        event["sport"],
                        class_name="font-bold text-gray-900 text-lg",
                    ),
                    rx.el.p(
                        f"By {event['creator']}",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.span(
                        f"{event['participants']}/{event['max_participants']}",
                        class_name="text-xs font-bold text-emerald-700",
                    ),
                    class_name="px-2 py-1 bg-emerald-100 rounded-full",
                ),
                class_name="flex justify-between items-start mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("calendar", class_name="h-4 w-4 text-gray-400"),
                    rx.el.span(
                        event["date"],
                        class_name="text-sm text-gray-600 font-medium",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="h-4 w-4 text-gray-400"),
                    rx.el.span(
                        event["time"],
                        class_name="text-sm text-gray-600 font-medium",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.div(
                    rx.icon("map-pin", class_name="h-4 w-4 text-gray-400"),
                    rx.el.span(
                        event["location"],
                        class_name="text-sm text-gray-600 font-medium truncate",
                    ),
                    class_name="flex items-center gap-2",
                ),
            ),
            rx.el.button(
                rx.cond(is_expanded, "Hide Details", "View Details & Join"),
                on_click=lambda: EventDetailState.select_event(event["id"]),
                class_name=rx.cond(
                    is_expanded,
                    "w-full mt-6 py-2 bg-gray-100 text-gray-700 text-sm font-bold rounded-xl hover:bg-gray-200 transition-colors",
                    "w-full mt-6 py-2 bg-gray-900 text-white text-sm font-bold rounded-xl hover:bg-emerald-600 transition-colors",
                ),
            ),
            class_name="p-6",
        ),
        rx.cond(
            is_expanded,
            rx.el.div(
                rx.el.div(class_name="h-px w-full bg-gray-100 mb-6"),
                rx.el.div(
                    rx.el.h5(
                        "Participants",
                        class_name="text-xs font-bold uppercase text-gray-400 mb-3",
                    ),
                    rx.el.div(
                        rx.image(
                            src="https://api.dicebear.com/9.x/notionists/svg?seed=Alex",
                            class_name="size-8 rounded-full border-2 border-white bg-gray-100 -ml-2 first:ml-0 relative z-10",
                        ),
                        rx.image(
                            src="https://api.dicebear.com/9.x/notionists/svg?seed=Sarah",
                            class_name="size-8 rounded-full border-2 border-white bg-gray-100 -ml-2 relative z-20",
                        ),
                        rx.el.div(
                            "+2",
                            class_name="size-8 rounded-full border-2 border-white bg-gray-100 -ml-2 relative z-30 flex items-center justify-center text-[10px] font-bold text-gray-600",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.h5(
                        "Venue Suggestions",
                        class_name="text-xs font-bold uppercase text-gray-400 mb-3",
                    ),
                    venue_card(
                        "Central Park Courts", "123 Park Ave", "$0", "4.8"
                    ),
                    venue_card(
                        "City Sports Arena", "45 Downtown Blvd", "$15/hr", "4.5"
                    ),
                    venue_card(
                        "Community Center", "789 Local St", "$5/hr", "4.2"
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "map-pin", class_name="h-6 w-6 text-red-500 mb-2"
                        ),
                        rx.el.span(
                            f"Map View: {event['location']}",
                            class_name="text-xs font-bold text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center h-32 bg-gray-100 rounded-xl border border-gray-200",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    rx.icon("check", class_name="h-5 w-5 mr-2"),
                    "Confirm Attendance",
                    class_name="w-full py-3 bg-emerald-600 text-white font-bold rounded-xl shadow-lg shadow-emerald-200 hover:bg-emerald-700 transition-colors flex items-center justify-center",
                ),
                class_name="px-6 pb-6",
            ),
            None,
        ),
        class_name="bg-white rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-all overflow-hidden",
    )


def events_page() -> rx.Component:
    return rx.el.div(
        create_event_modal(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Upcoming Events", class_name="text-3xl font-black"
                    ),
                    rx.el.p(
                        "Find a match that fits your schedule.",
                        class_name="text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2"),
                    "Create Event",
                    on_click=AppState.toggle_create_modal,
                    class_name="px-6 py-3 bg-emerald-600 text-white font-bold rounded-2xl shadow-lg shadow-emerald-100 flex items-center",
                ),
                class_name="flex justify-between items-center mb-10",
            ),
            rx.el.div(
                rx.el.button(
                    "All Sports",
                    class_name="px-4 py-2 bg-gray-900 text-white text-sm font-bold rounded-full",
                ),
                rx.el.button(
                    "Football",
                    class_name="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-sm font-bold rounded-full hover:bg-emerald-50",
                ),
                rx.el.button(
                    "Basketball",
                    class_name="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-sm font-bold rounded-full hover:bg-emerald-50",
                ),
                rx.el.button(
                    "Tennis",
                    class_name="px-4 py-2 bg-white border border-gray-100 text-gray-600 text-sm font-bold rounded-full hover:bg-emerald-50",
                ),
                class_name="flex gap-2 mb-8 overflow-x-auto pb-2",
            ),
            rx.el.div(
                rx.foreach(AppState.upcoming_events, event_card_with_details),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start",
            ),
            class_name="p-2",
        ),
    )