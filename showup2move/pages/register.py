import reflex as rx
from showup2move.states.registration_state import RegistrationState, UPLOAD_ID


def progress_step(num: int, label: str, current: int) -> rx.Component:
    is_active = current == num
    is_completed = current > num
    return rx.el.div(
        rx.el.div(
            rx.cond(
                is_completed,
                rx.icon("check", class_name="h-4 w-4 text-white"),
                rx.el.span(
                    num,
                    class_name=rx.cond(
                        is_active,
                        "text-white font-bold",
                        "text-gray-400 font-bold",
                    ),
                ),
            ),
            class_name=rx.cond(
                is_completed | is_active,
                "size-8 rounded-full bg-emerald-500 flex items-center justify-center",
                "size-8 rounded-full bg-gray-100 flex items-center justify-center",
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                is_active,
                "text-xs font-bold text-gray-900 mt-2",
                "text-xs font-medium text-gray-400 mt-2",
            ),
        ),
        class_name="flex flex-col items-center",
    )


def step_one() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Basic Information", class_name="text-2xl font-black mb-6"),
        rx.el.div(
            rx.el.label(
                "Full Name",
                class_name="text-sm font-bold text-gray-700 mb-2 block",
            ),
            rx.el.input(
                placeholder="e.g. John Doe",
                on_change=RegistrationState.set_name,
                default_value=RegistrationState.name,
                class_name="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl mb-4",
            ),
            rx.el.label(
                "Email", class_name="text-sm font-bold text-gray-700 mb-2 block"
            ),
            rx.el.input(
                placeholder="john@example.com",
                on_change=RegistrationState.set_email,
                default_value=RegistrationState.email,
                class_name="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl mb-4",
            ),
            rx.el.label(
                "City", class_name="text-sm font-bold text-gray-700 mb-2 block"
            ),
            rx.el.input(
                placeholder="San Francisco",
                on_change=RegistrationState.set_location,
                default_value=RegistrationState.location,
                class_name="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl mb-4",
            ),
            rx.el.label(
                "Bio", class_name="text-sm font-bold text-gray-700 mb-2 block"
            ),
            rx.el.textarea(
                placeholder="Tell us about your sports level and interests...",
                on_change=RegistrationState.set_bio,
                default_value=RegistrationState.bio,
                class_name="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl h-32",
            ),
            class_name="mb-8",
        ),
        rx.el.button(
            "Continue",
            on_click=RegistrationState.next_step,
            disabled=~RegistrationState.step_one_valid,
            class_name="w-full py-4 bg-emerald-600 text-white font-bold rounded-2xl shadow-lg disabled:opacity-50",
        ),
    )


def sport_selection_card(sport: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                sport["icon"],
                class_name=rx.cond(
                    sport["selected"], "text-white", "text-gray-400"
                ),
            ),
            class_name=rx.cond(
                sport["selected"],
                "p-3 bg-emerald-500 rounded-xl",
                "p-3 bg-gray-100 rounded-xl",
            ),
        ),
        rx.el.div(
            rx.el.p(sport["name"], class_name="font-bold text-sm"),
            rx.cond(
                sport["selected"],
                rx.el.select(
                    rx.el.option("Beginner", value="Beginner"),
                    rx.el.option("Intermediate", value="Intermediate"),
                    rx.el.option("Advanced", value="Advanced"),
                    on_change=lambda val: RegistrationState.update_sport_level(
                        sport["name"], val
                    ),
                    class_name="text-[10px] text-emerald-700 bg-transparent font-bold border-none p-0 outline-none appearance-none",
                ),
                None,
            ),
            class_name="flex flex-col ml-3",
        ),
        on_click=lambda: RegistrationState.toggle_sport(sport["name"]),
        class_name=rx.cond(
            sport["selected"],
            "p-3 rounded-2xl bg-emerald-50 border-2 border-emerald-500 flex items-center cursor-pointer transition-all",
            "p-3 rounded-2xl bg-white border border-gray-100 flex items-center cursor-pointer hover:border-emerald-200 transition-all",
        ),
    )


def step_two() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Sports Interests", class_name="text-2xl font-black mb-2"),
        rx.el.p(
            "Select at least one sport you enjoy.",
            class_name="text-gray-500 text-sm mb-6",
        ),
        rx.el.div(
            rx.foreach(RegistrationState.selected_sports, sport_selection_card),
            class_name="grid grid-cols-2 gap-3 mb-8",
        ),
        rx.el.div(
            rx.el.button(
                "Back",
                on_click=RegistrationState.prev_step,
                class_name="px-6 py-4 text-gray-500 font-bold",
            ),
            rx.el.button(
                "Continue",
                on_click=RegistrationState.next_step,
                disabled=~RegistrationState.any_sport_selected,
                class_name="flex-1 py-4 bg-emerald-600 text-white font-bold rounded-2xl shadow-lg disabled:opacity-50",
            ),
            class_name="flex gap-4 items-center",
        ),
    )


def availability_slot(day: str, slot: str) -> rx.Component:
    return rx.el.button(
        on_click=lambda: RegistrationState.toggle_time_slot(day, slot),
        class_name=rx.cond(
            RegistrationState.weekly_availability[day].contains(slot),
            "flex-1 py-3 bg-emerald-500 text-white text-[10px] font-bold border-r border-emerald-400 last:border-r-0 first:rounded-l-lg last:rounded-r-lg transition-all shadow-inner",
            "flex-1 py-3 bg-gray-50 text-gray-400 text-[10px] font-bold border-r border-gray-200 last:border-r-0 first:rounded-l-lg last:rounded-r-lg hover:bg-emerald-50 transition-all",
        ),
    )


def availability_row(day: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            day, class_name="w-20 text-sm font-bold text-gray-700 shrink-0"
        ),
        rx.el.div(
            rx.foreach(
                RegistrationState.TIME_SLOTS,
                lambda slot: availability_slot(day, slot),
            ),
            class_name="flex flex-1 rounded-lg border border-gray-200 overflow-hidden",
        ),
        class_name="flex items-center gap-4 mb-3",
    )


def step_three() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Final Touches", class_name="text-2xl font-black mb-6"),
        rx.el.label(
            "Profile Photo",
            class_name="text-sm font-bold text-gray-700 mb-4 block",
        ),
        rx.el.div(
            rx.upload.root(
                rx.el.div(
                    rx.cond(
                        RegistrationState.uploaded_photo != "",
                        rx.image(
                            src=rx.get_upload_url(
                                RegistrationState.uploaded_photo
                            ),
                            class_name="size-24 rounded-full object-cover",
                        ),
                        rx.image(
                            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={RegistrationState.name}",
                            class_name="size-24 rounded-full bg-gray-100",
                        ),
                    ),
                    rx.el.p(
                        "Click or drag to change",
                        class_name="text-[10px] text-gray-400 mt-2",
                    ),
                    class_name="flex flex-col items-center justify-center",
                ),
                id=UPLOAD_ID,
                multiple=False,
                accept={"image/*": [".png", ".jpg", ".jpeg", ".svg"]},
                on_drop=RegistrationState.handle_upload(
                    rx.upload_files(upload_id=UPLOAD_ID)
                ),
                class_name="mx-auto border-2 border-dashed border-gray-100 rounded-full p-4 w-fit cursor-pointer hover:border-emerald-300 transition-all",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Weekly Availability",
                class_name="text-lg font-bold text-gray-900 mb-1",
            ),
            rx.el.p(
                "Tap time slots when you're typically available to play",
                class_name="text-xs text-gray-500 mb-6",
            ),
            rx.el.div(
                rx.el.div(class_name="w-20 shrink-0"),
                rx.el.div(
                    rx.foreach(
                        RegistrationState.TIME_SLOTS,
                        lambda slot: rx.el.span(
                            slot,
                            class_name="flex-1 text-[10px] font-black text-gray-400 text-center uppercase tracking-tighter",
                        ),
                    ),
                    class_name="flex flex-1",
                ),
                class_name="flex gap-4 mb-2",
            ),
            rx.foreach(RegistrationState.DAYS, availability_row),
            class_name="p-6 bg-white rounded-3xl border border-gray-100 shadow-sm mb-10",
        ),
        rx.el.div(
            rx.el.button(
                "Back",
                on_click=RegistrationState.prev_step,
                class_name="px-6 py-4 text-gray-500 font-bold",
            ),
            rx.el.button(
                "Complete Registration",
                on_click=RegistrationState.complete_registration,
                class_name="flex-1 py-4 bg-emerald-600 text-white font-bold rounded-2xl shadow-lg",
            ),
            class_name="flex gap-4 items-center",
        ),
    )


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("zap", class_name="h-5 w-5 text-white"),
                    class_name="bg-emerald-500 p-2 rounded-lg",
                ),
                rx.el.span("ShowUp2Move", class_name="text-xl font-black"),
                class_name="flex items-center gap-3 mb-10 justify-center",
            ),
            rx.el.div(
                progress_step(1, "Info", RegistrationState.current_step),
                rx.el.div(class_name="h-px bg-gray-100 w-12 mt-4"),
                progress_step(2, "Sports", RegistrationState.current_step),
                rx.el.div(class_name="h-px bg-gray-100 w-12 mt-4"),
                progress_step(3, "Finish", RegistrationState.current_step),
                class_name="flex justify-center mb-10",
            ),
            rx.match(
                RegistrationState.current_step,
                (1, step_one()),
                (2, step_two()),
                (3, step_three()),
                step_one(),
            ),
            class_name="w-full max-w-xl bg-white p-10 rounded-[2.5rem] shadow-xl",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-50 p-6 font-['Inter']",
    )