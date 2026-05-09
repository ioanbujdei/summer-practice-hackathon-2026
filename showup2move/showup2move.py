import reflex as rx
from showup2move.components.layout import layout_wrapper
from showup2move.pages.dashboard import dashboard_page
from showup2move.pages.profile import profile_page
from showup2move.pages.events import events_page
from showup2move.pages.groups import groups_page
from showup2move.pages.chat import chat_page
from showup2move.pages.welcome import welcome_page
from showup2move.pages.register import register_page
from showup2move.pages.login import login_page


def index() -> rx.Component:
    return layout_wrapper(dashboard_page(), "dashboard")


def profile() -> rx.Component:
    return layout_wrapper(profile_page(), "profile")


def events() -> rx.Component:
    return layout_wrapper(events_page(), "events")


def groups() -> rx.Component:
    return layout_wrapper(groups_page(), "groups")


def chat() -> rx.Component:
    return layout_wrapper(chat_page(), "chat")


def welcome() -> rx.Component:
    return welcome_page()


def register() -> rx.Component:
    return register_page()


def login() -> rx.Component:
    return login_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(profile, route="/profile")
app.add_page(events, route="/events")
app.add_page(groups, route="/groups")
app.add_page(chat, route="/chat")
app.add_page(welcome, route="/welcome")
app.add_page(register, route="/register")
app.add_page(login, route="/login")