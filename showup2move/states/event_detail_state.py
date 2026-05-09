import reflex as rx


class EventDetailState(rx.State):
    selected_event_id: str = ""

    @rx.event
    def select_event(self, event_id: str):
        if self.selected_event_id == event_id:
            self.selected_event_id = ""
        else:
            self.selected_event_id = event_id