import pytest
import tkinter as tk
import main

@pytest.fixture
def headless_app(monkeypatch):
    def fake_askstring(title, prompt):
        return "Player A" if "Player A" in prompt else "Player B"
    monkeypatch.setattr(main.simpledialog, "askstring", fake_askstring)

    root = tk.Tk()
    app = main.App(root)
    root.withdraw()  # headless
    yield root, app
    root.destroy()


# from unittest.mock import patch
# import main
# import tkinter as tk
# import pytest

# @patch("main.simpledialog.askstring", side_effect=["Player A", "Player B"])
# def test_initial_focus_to_wide_1st_serve_dir(_mock):
#     """App starts with focus on the 1st direction listbox."""
#     root, refs = main.build_app()
#     root.update_idletasks()
#     root.update()
#     root.withdraw()
#     # TESTING
#     assert root.focus_get() == refs["listbox_1st_direction"]
#     # END TESTING
#     root.destroy()

# @patch("main.simpledialog.askstring", side_effect=["Player A", "Player B"])
# def test_initial_navigation_to_1st_serve_body(_mock):
#     """The App starts focused with 1st Wide, after one Down press
#     it should now be pointed at body. """
#     root, refs = main.build_app()
#     root.update_idletasks()
#     root.update()
#     root.withdraw()
#     # PROCEDURE
#     root.event_generate("<Down>")
#     # TESTING
#     assert root.focus_get() == refs["listbox_1st_direction"]
#     assert refs["listbox_1st_direction"].get(tk.ACTIVE) == "Body"
#     # END TESTING
#     root.destroy()

# @patch("main.simpledialog.askstring", side_effect=["Player A", "Player B"])
# def test_listbox_down_key_stops_at_last_item(_mock):
#     """Verify that when the Down arrow key is pressed on the last item of the listbox,
#     the selection remains on the last item instead of looping back to the first."""
#     root, refs = main.build_app()
#     root.update_idletasks()
#     root.update()

#     # PROCEDURE
#     root.event_generate("<Down>")
#     root.event_generate("<Down>")
#     root.event_generate("<Down>")
#     # TESTING
#     assert refs["listbox_1st_direction"].get(tk.ACTIVE) == "In Net"
#     root.event_generate("<Down>")
#     assert refs["listbox_1st_direction"].get(tk.ACTIVE) == "In Net"
#     # END TESTING
#     root.after(2000, root.destroy)
#     root.mainloop()

