import reflex as rx


def stat_card(
    label: str, value: str, icon: str, trend: str = None
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-emerald-600"),
            class_name="p-2 bg-emerald-50 rounded-lg w-fit mb-4",
        ),
        rx.el.p(label, class_name="text-sm font-medium text-gray-500 mb-1"),
        rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
        rx.cond(
            trend,
            rx.el.p(
                trend, class_name="text-xs font-medium text-emerald-600 mt-2"
            ),
            None,
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-all flex-1",
    )


def event_card(event: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(event["sport"], class_name="font-bold text-gray-900"),
                rx.el.p(
                    f"By {event['creator']}", class_name="text-xs text-gray-500"
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
                rx.el.span(event["date"], class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2 mb-2",
            ),
            rx.el.div(
                rx.icon("clock", class_name="h-4 w-4 text-gray-400"),
                rx.el.span(event["time"], class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2 mb-2",
            ),
            rx.el.div(
                rx.icon("map-pin", class_name="h-4 w-4 text-gray-400"),
                rx.el.span(
                    event["location"],
                    class_name="text-sm text-gray-600 truncate",
                ),
                class_name="flex items-center gap-2",
            ),
        ),
        rx.el.button(
            "Join Match",
            class_name="w-full mt-6 py-2 bg-gray-900 text-white text-sm font-bold rounded-xl hover:bg-emerald-600 transition-colors",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm hover:border-emerald-200 transition-all",
    )