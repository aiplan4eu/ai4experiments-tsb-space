import os

# curr_dir = os.path.dirname(os.path.abspath(__file__))
# tsb_space_src_dir = os.path.join(curr_dir, '..', 'tsb-space', 'src')
# models_dir = os.path.join(tsb_space_src_dir, '..', 'models')

# import sys
# print("added path = ",tsb_space_src_dir)
# sys.path.append(tsb_space_src_dir)


import asyncio
from functools import partial
import sys
import logging
import justpy as jp

from up_grafene_engine.engine import GrafeneEngine


from gui import Gui, main_page, Mode, reload_page
from generate_request import generate_request_str
from modified_planning import planning
from threading import Thread



def main():

    engine = GrafeneEngine(port=8061)

    gui = Gui(engine)

    gui_thread = Thread(target=gui.show_gui_thread)
    gui_thread.start()

    while True:
        # wait for the user input to start planning
        gui.start_queue.get(block=True)
        request = generate_request_str(gui.activities)
        activity_plan, n_goals = planning(request, gui)

        if activity_plan:
            ap_str = "\n".join(map(activity_str, activity_plan))
        else:
            ap_str = "No activity plan found"

        gui.update_plan(activity_plan, n_goals)

        gui.logger.info(ap_str)
        # gui.display_text(f"The activity plan is:\n {ap_str}\n \nIt reaches {n_goals} goals")
        gui.mode = Mode.GENERATING_PROBLEM
        asyncio.run(reload_page())


    server.wait_for_termination()

    gui_thread.join()

if __name__ == "__main__":
    # asyncio.run(main())
    main()
