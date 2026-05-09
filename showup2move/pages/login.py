import reflex as rx
from showup2move.states.registration_state import RegistrationState


class LoginState(rx.State):
    email: str = ""

    @rx.event
    async def handle_login(self):
        reg_state = await self.get_state(RegistrationState)
        if (
            self.email == reg_state.email
            or self.email == "demo@showup2move.com"
        ):
            yield rx.toast("Logging in...")
            yield rx.redirect("/")
        else:
            yield rx.toast("Email not found. Please register.")

    @rx.event
    def set_email(self, val: str):
        self.name = val


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("zap", class_name="h-6 w-6 text-white"),
                    class_name="bg-emerald-500 p-2 rounded-lg",
                ),
                rx.el.span(
                    "ShowUp2Move",
                    class_name="text-2xl font-black text-gray-900",
                ),
                class_name="flex items-center gap-3 mb-10 justify-center",
            ),
            rx.el.div(
                rx.el.h2(
                    "Welcome back!",
                    class_name="text-2xl font-bold mb-2 text-center",
                ),
                rx.el.p(
                    "Sign in to see your matches.",
                    class_name="text-gray-500 text-center mb-8 font-medium",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email Address",
                        class_name="text-sm font-bold text-gray-700 mb-2 block",
                    ),
                    rx.el.input(
                        placeholder="Enter your email",
                        on_change=LoginState.set_email,
                        class_name="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl focus:border-emerald-500 outline-none",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Sign In",
                    on_click=LoginState.handle_login,
                    class_name="w-full py-4 bg-emerald-600 text-white font-bold rounded-2xl shadow-lg shadow-emerald-100 mb-6",
                ),
                rx.el.div(
                    rx.el.span(
                        "Don't have an account? ",
                        class_name="text-gray-500 font-medium",
                    ),
                    rx.el.a(
                        "Register",
                        href="/register",
                        class_name="text-emerald-600 font-bold hover:underline",
                    ),
                    class_name="text-center text-sm",
                ),
            ),
            class_name="w-full max-w-md bg-white p-10 rounded-[2.5rem] shadow-xl",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-50 p-6",
    )