import reflex as rx
from showup2move.components.sidebar import sidebar
from showup2move.states.notification_state import NotificationState, render_notification


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1("ShowUp2Move", class_name="md:hidden text-xl font-bold"),
            rx.el.div(class_name="flex-1"),
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", class_name="h-5 w-5 text-gray-600"),
                    rx.cond(
                        NotificationState.unread_count > 0,
                        rx.el.span(
                            NotificationState.unread_count.to_string(),
                            class_name="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white",
                        ),
                        None,
                    ),
                    on_click=NotificationState.toggle_dropdown,
                    class_name="relative p-2 bg-white rounded-full border border-gray-200 hover:bg-gray-50 transition-colors",
                ),
                rx.cond(
                    NotificationState.show_dropdown,
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Notifications",
                                class_name="font-bold text-gray-900",
                            ),
                            class_name="p-4 border-b border-gray-100",
                        ),
                        rx.el.div(
                            rx.foreach(
                                NotificationState.notifications,
                                render_notification,
                            ),
                            class_name="max-h-80 overflow-y-auto",
                        ),
                        class_name="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-gray-100 z-50 overflow-hidden",
                    ),
                    None,
                ),
                class_name="relative",
            ),
            class_name="flex items-center mb-8",
        )
    )


def layout_wrapper(content: rx.Component, page_id: str) -> rx.Component:
    return rx.el.div(
        sidebar(page_id),
        rx.el.main(
            rx.el.div(header(), content, class_name="max-w-6xl mx-auto"),
            class_name="flex-1 min-h-screen bg-gray-50 p-4 md:p-10 overflow-auto",
        ),
        class_name="flex min-h-screen font-['Inter'] text-gray-900",
    )