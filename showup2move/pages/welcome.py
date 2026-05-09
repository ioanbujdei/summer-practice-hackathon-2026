import reflex as rx


def feature_card(icon: str, title: str, desc: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-emerald-600"),
            class_name="p-3 bg-emerald-50 rounded-xl mb-4 w-fit",
        ),
        rx.el.h3(title, class_name="text-lg font-bold mb-2"),
        rx.el.p(desc, class_name="text-sm text-gray-500 font-medium"),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm",
    )


def welcome_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("zap", class_name="h-8 w-8 text-white"),
                    class_name="bg-emerald-500 p-3 rounded-2xl mb-8 mx-auto w-fit shadow-lg shadow-emerald-200",
                ),
                rx.el.h1(
                    "Show Up. Get Matched. Play.",
                    class_name="text-5xl md:text-7xl font-black tracking-tight text-gray-900 mb-6",
                ),
                rx.el.p(
                    "The smartest way to find teammates for spontaneous sports activities and level up your game.",
                    class_name="text-xl text-gray-500 max-w-2xl mx-auto mb-10",
                ),
                rx.el.div(
                    rx.el.a(
                        "Get Started Now",
                        href="/register",
                        class_name="px-8 py-4 bg-emerald-600 text-white font-bold rounded-2xl shadow-xl shadow-emerald-200 hover:bg-emerald-700 transition-all",
                    ),
                    rx.el.a(
                        "Sign In",
                        href="/login",
                        class_name="px-8 py-4 bg-white text-gray-900 font-bold rounded-2xl border border-gray-200 hover:bg-gray-50 transition-all",
                    ),
                    class_name="flex flex-col sm:flex-row gap-4 justify-center",
                ),
                class_name="text-center max-w-4xl mx-auto",
            ),
            class_name="pt-20 pb-16 px-6",
        ),
        rx.el.div(
            rx.el.div(
                feature_card(
                    "zap",
                    "Smart Matching",
                    "Our algorithm finds the perfect partners based on your skill level and availability.",
                ),
                feature_card(
                    "message-circle",
                    "Instant Group Chat",
                    "Coordinate effortlessly with your new squad through built-in group messaging.",
                ),
                feature_card(
                    "calendar",
                    "Easy Coordination",
                    "Propose venues, vote on times, and confirm attendance with a single tap.",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
            ),
            class_name="max-w-6xl mx-auto px-6 pb-20",
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
    )