import reflex as rx


def nav_item(label: str, icon: str, href: str, active: bool) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon,
            class_name=rx.cond(
                active, "h-5 w-5 text-emerald-600", "h-5 w-5 text-gray-500"
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                active,
                "font-semibold text-emerald-700",
                "font-medium text-gray-600",
            ),
        ),
        href=href,
        class_name=rx.cond(
            active,
            "flex items-center gap-3 px-4 py-3 rounded-xl bg-emerald-50 border border-emerald-100 transition-all",
            "flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-gray-50 text-gray-600 transition-all",
        ),
    )


def sidebar(current_page: str) -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("zap", class_name="h-6 w-6 text-white"),
                    class_name="bg-emerald-500 p-2 rounded-lg",
                ),
                rx.el.span(
                    "ShowUp2Move",
                    class_name="text-xl font-bold tracking-tight text-gray-900",
                ),
                class_name="flex items-center gap-3 mb-10 px-2",
            ),
            rx.el.nav(
                nav_item(
                    "Dashboard",
                    "layout-dashboard",
                    "/",
                    current_page == "dashboard",
                ),
                nav_item(
                    "Events", "calendar", "/events", current_page == "events"
                ),
                nav_item(
                    "Groups", "users", "/groups", current_page == "groups"
                ),
                nav_item(
                    "Chat", "message-circle", "/chat", current_page == "chat"
                ),
                nav_item(
                    "Profile", "user", "/profile", current_page == "profile"
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=Alex",
                    class_name="size-10 rounded-full bg-gray-100",
                ),
                rx.el.div(
                    rx.el.p(
                        "Alex Johnson",
                        class_name="text-sm font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Pro Player",
                        class_name="text-xs text-emerald-600 font-medium",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3 p-3 bg-gray-50 rounded-2xl border border-gray-100",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                "Sign Out",
                on_click=rx.redirect("/welcome"),
                class_name="w-full mt-4 flex items-center justify-center py-3 text-red-500 font-bold hover:bg-red-50 rounded-xl transition-all",
            ),
            class_name="mt-auto pt-6 border-t",
        ),
        class_name="w-72 h-screen bg-white border-r border-gray-200 p-6 flex flex-col sticky top-0 shrink-0 shadow-sm hidden md:flex",
    )