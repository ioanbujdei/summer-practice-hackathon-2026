import reflex as rx
from showup2move.states.chat_state import ChatState, ChatMessage, Poll, PollOption
from showup2move.states.app_state import AppState, Group
from showup2move.states.user_state import UserState


def group_chat_item(group: Group) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(group["icon"], class_name="h-5 w-5 text-emerald-600"),
            class_name="p-3 bg-emerald-50 rounded-xl shrink-0",
        ),
        rx.el.div(
            rx.el.h4(
                group["name"], class_name="font-bold text-gray-900 truncate"
            ),
            rx.el.p(
                f"{group['members'].length()} members",
                class_name="text-xs text-gray-500",
            ),
            class_name="flex flex-col flex-1 min-w-0",
        ),
        on_click=lambda: ChatState.set_active_group(group["id"]),
        class_name=rx.cond(
            ChatState.active_group_id == group["id"],
            "flex items-center gap-3 p-4 bg-gray-50 border-l-4 border-emerald-500 cursor-pointer transition-colors",
            "flex items-center gap-3 p-4 hover:bg-gray-50 border-l-4 border-transparent cursor-pointer transition-colors",
        ),
    )


def message_bubble(msg: ChatMessage) -> rx.Component:
    is_own = msg["sender_name"] == UserState.name
    return rx.cond(
        msg["is_system"],
        rx.el.div(
            rx.el.span(
                msg["content"],
                class_name="px-4 py-1.5 bg-gray-100 text-gray-500 text-xs font-bold rounded-full",
            ),
            class_name="flex justify-center my-6",
        ),
        rx.el.div(
            rx.cond(
                ~is_own,
                rx.image(
                    src=msg["avatar_url"],
                    class_name="size-8 rounded-full mt-auto shrink-0 bg-gray-100",
                ),
                None,
            ),
            rx.el.div(
                rx.cond(
                    ~is_own,
                    rx.el.span(
                        msg["sender_name"],
                        class_name="text-[10px] font-bold text-gray-400 mb-1 ml-1",
                    ),
                    None,
                ),
                rx.el.div(
                    rx.el.p(msg["content"], class_name="text-sm"),
                    class_name=rx.cond(
                        is_own,
                        "px-4 py-3 bg-emerald-500 text-white rounded-2xl rounded-br-sm shadow-sm",
                        "px-4 py-3 bg-white text-gray-900 rounded-2xl rounded-bl-sm shadow-sm border border-gray-100",
                    ),
                ),
                rx.el.span(
                    msg["timestamp"],
                    class_name=rx.cond(
                        is_own,
                        "text-[10px] text-gray-400 mt-1 mr-1 text-right",
                        "text-[10px] text-gray-400 mt-1 ml-1",
                    ),
                ),
                class_name=rx.cond(
                    is_own,
                    "flex flex-col items-end",
                    "flex flex-col items-start",
                ),
            ),
            class_name=rx.cond(
                is_own,
                "flex justify-end mb-4",
                "flex gap-2 justify-start mb-4 max-w-[85%]",
            ),
        ),
    )


def poll_option_view(
    poll_id: str, option: PollOption, total_votes: int
) -> rx.Component:
    percentage = rx.cond(
        total_votes > 0, (option["votes"] / total_votes * 100).to(int), 0
    )
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                option["text"],
                class_name="text-sm font-bold text-gray-800 relative z-10",
            ),
            rx.el.span(
                f"{option['votes']} votes",
                class_name="text-xs text-gray-500 relative z-10",
            ),
            class_name="flex justify-between items-center mb-1",
        ),
        rx.el.div(
            rx.el.div(
                class_name="absolute top-0 left-0 h-full bg-emerald-100 rounded-lg transition-all",
                style={"width": f"{percentage}%"},
            ),
            rx.el.button(
                "Vote",
                on_click=lambda: ChatState.vote_poll(poll_id, option["id"]),
                class_name="absolute right-2 top-1/2 -translate-y-1/2 px-3 py-1 bg-white border border-gray-200 text-xs font-bold rounded-lg shadow-sm hover:bg-gray-50 z-20 transition-all opacity-0 group-hover:opacity-100",
            ),
            class_name="relative h-10 bg-gray-50 rounded-lg border border-gray-100 flex items-center px-3 group overflow-hidden cursor-pointer",
        ),
        class_name="mb-3",
    )


def poll_card(poll: Poll) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("bar-chart-2", class_name="h-4 w-4 text-emerald-600"),
            rx.el.span(
                "Group Poll",
                class_name="text-xs font-bold text-emerald-700 uppercase tracking-wider",
            ),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.h4(
            poll["question"],
            class_name="text-base font-bold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.foreach(
                poll["options"],
                lambda opt: poll_option_view(
                    poll["id"], opt, poll["total_votes"]
                ),
            )
        ),
        rx.el.p(
            f"Total votes: {poll['total_votes']}",
            class_name="text-xs text-gray-400 mt-2 text-right",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm mb-6 w-full max-w-sm mx-auto",
    )


def create_poll_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Create Poll", class_name="text-2xl font-black mb-2"),
                rx.el.button(
                    rx.icon("x"),
                    on_click=ChatState.toggle_poll_modal,
                    class_name="absolute top-6 right-6 text-gray-400 hover:text-gray-900",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Question",
                    class_name="text-xs font-bold uppercase text-gray-400 mb-1 block",
                ),
                rx.el.input(
                    placeholder="e.g. What time works best?",
                    on_change=ChatState.set_poll_question_input,
                    class_name="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl mb-4 focus:border-emerald-500 focus:outline-none",
                    default_value=ChatState.poll_question_input,
                ),
                rx.el.label(
                    "Options (comma separated)",
                    class_name="text-xs font-bold uppercase text-gray-400 mb-1 block",
                ),
                rx.el.input(
                    placeholder="e.g. 6 PM, 7 PM, Tomorrow",
                    on_change=ChatState.set_poll_options_input,
                    class_name="w-full p-3 bg-gray-50 border border-gray-100 rounded-xl mb-6 focus:border-emerald-500 focus:outline-none",
                    default_value=ChatState.poll_options_input,
                ),
                rx.el.button(
                    "Create Poll",
                    on_click=ChatState.create_poll,
                    class_name="w-full py-3 bg-emerald-600 text-white font-bold rounded-xl shadow-lg shadow-emerald-200",
                ),
            ),
            class_name="bg-white p-8 rounded-3xl w-full max-w-md relative",
        ),
        class_name=rx.cond(
            ChatState.show_poll_modal,
            "fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4",
            "hidden",
        ),
    )


def chat_page() -> rx.Component:
    return rx.el.div(
        create_poll_modal(),
        rx.el.div(
            rx.el.h2("Messages", class_name="text-3xl font-black mb-6"),
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        AppState.groups.length() > 0,
                        rx.el.div(
                            rx.foreach(AppState.groups, group_chat_item),
                            class_name="divide-y divide-gray-100",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Join a group to start chatting",
                                class_name="text-gray-500 text-center py-10",
                            )
                        ),
                    ),
                    class_name="w-full md:w-80 bg-white border-r border-gray-100 flex flex-col shrink-0 rounded-l-3xl overflow-hidden",
                ),
                rx.el.div(
                    rx.cond(
                        ChatState.active_group_id != "",
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Group Chat",
                                    class_name="font-bold text-gray-900",
                                ),
                                rx.el.button(
                                    rx.icon(
                                        "bar-chart-2", class_name="h-4 w-4 mr-2"
                                    ),
                                    "Create Poll",
                                    on_click=ChatState.toggle_poll_modal,
                                    class_name="flex items-center px-3 py-1.5 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-lg border border-emerald-100 hover:bg-emerald-100 transition-colors",
                                ),
                                class_name="px-6 py-4 border-b border-gray-100 bg-white flex justify-between items-center",
                            ),
                            rx.el.div(
                                rx.foreach(ChatState.active_polls, poll_card),
                                rx.foreach(
                                    ChatState.active_messages, message_bubble
                                ),
                                class_name="flex-1 p-6 overflow-y-auto bg-gray-50/50",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    placeholder="Type your message...",
                                    on_change=ChatState.set_message_input,
                                    class_name="flex-1 px-4 py-3 bg-gray-100 border-none rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none",
                                    default_value=ChatState.message_input,
                                ),
                                rx.el.button(
                                    rx.icon("send", class_name="h-5 w-5"),
                                    on_click=ChatState.send_message,
                                    class_name="p-3 bg-emerald-600 text-white rounded-xl shadow-md hover:bg-emerald-700 transition-colors",
                                ),
                                class_name="p-4 bg-white border-t border-gray-100 flex gap-3 items-center",
                            ),
                            class_name="flex flex-col flex-1 h-full",
                        ),
                        rx.el.div(
                            rx.icon(
                                "message-square",
                                class_name="h-16 w-16 text-gray-200 mb-4",
                            ),
                            rx.el.h3(
                                "Select a conversation",
                                class_name="text-xl font-bold text-gray-900 mb-2",
                            ),
                            rx.el.p(
                                "Choose a group from the left to start chatting.",
                                class_name="text-gray-500 text-center",
                            ),
                            class_name="flex flex-col items-center justify-center flex-1 bg-gray-50",
                        ),
                    ),
                    class_name="flex-1 flex flex-col min-w-0 bg-white rounded-r-3xl",
                ),
                class_name="flex flex-col md:flex-row h-[70vh] bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden",
            ),
        ),
    )