
import asyncio
from enum import Enum, auto
from functools import partial

import logging
import os
import queue
import justpy as jp
# FOR FUTURE PROJECTS: check out the justpy.react functionality: https://justpy.io/blog/reactivity/


import unified_planning as up
from unified_planning.shortcuts import *

from generate_request import all_activities, activity_description_map


DEBUG = False
BUTTON_CLASS = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2'
# BUTTON_CLASS = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
ACTIVITY_DIV_STYLE = "color:blue;"
PLAN_DIV_STYLE = "color:blue;"

DIV_CLASS = "margin: auto; width: 50%;"

ACTION_DETAILS_TEXT_CLASS = ""
ACTION_DETAILS_TEXT_STYLE = f"margin-left: 0px; font-size: 18px; text-align: left;"


class Mode(Enum):
    GENERATING_PROBLEM = auto()
    OPERATING = auto()


curr_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(curr_dir, 'models')



class Gui():
    def __init__(self):
        # a queue where the interface waits the start
        self.start_queue = queue.Queue()

        self.mode = Mode.GENERATING_PROBLEM
        self.activities = []
        self.plan = None
        self.reached_goals = 0
        self.activity_info: Optional[str] = None

        self.goals_container_div: Optional[jp.Div] = None
        self.plan_div: Optional[jp.Div] = None
        self.activity_details_div: Optional[jp.Div] = None

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger.setLevel(logging.INFO)
        self.total_planning_goals = -1
        self.reached_planning_goals = -1

    def reset_execution(self):
        self.mode = Mode.GENERATING_PROBLEM
        self.total_planning_goals = -1
        self.reached_planning_goals = -1

    def update_chosen_activities(self):
        if self.goals_container_div is not None:
            self.goals_container_div.delete_components()
            for i, g in enumerate(self.activities):
                single_goal_p = jp.P(
                    a=self.goals_container_div,
                    text=f"{i+1}) {g}"
                )

    def update_activity_info(self):
        self.activity_details_div.delete_components()
        if self.activity_info is not None:

            self.activity_details_div.text = "Activity info:"
            image_path = f"/static/logos/activities/{self.activity_info.lower()}.png"
            _ = jp.P(
                a=self.activity_details_div,
                text="",
            )
            action_details_img = jp.Img(
                style="width: 130px; height: 130px;",
                a=self.activity_details_div,
                src=image_path,
                classes="w3-image",
            )
            action_details_text = jp.P(
                a=self.activity_details_div,
                text=activity_description_map.get(self.activity_info, "Error: no text found for the action"),
                classes=ACTION_DETAILS_TEXT_CLASS,
                style=ACTION_DETAILS_TEXT_STYLE,
                )
        else:
            self.activity_details_div.text = ""

    def update_planning_execution(self):
        from main_page import PLAN_PART_P_CLASS, PLAN_PART_P_STYLE
        if self.plan_div is not None:
            self.plan_div.delete_components()
            if self.plan is None and self.mode == Mode.GENERATING_PROBLEM:
                single_p = jp.P(
                    a=self.plan_div,
                    text="Choose some activities and press SOLVE.",
                    classes=PLAN_PART_P_CLASS,
                    style=PLAN_PART_P_STYLE,
                )
            elif self.plan is None and self.mode == Mode.OPERATING:
                single_p = jp.P(
                    a=self.plan_div,
                    text="Wait for planning to finish!",
                    classes=PLAN_PART_P_CLASS,
                    style=PLAN_PART_P_STYLE,
                )
                if self.reached_planning_goals != -1:
                    single_p = jp.P(
                        a=self.plan_div,
                        text=f"Reached {self.reached_planning_goals}/{self.total_planning_goals} goals.",
                        classes=PLAN_PART_P_CLASS,
                        style=PLAN_PART_P_STYLE,
                    )
            else:
                assert self.plan is not None
                for plan_activity in self.plan:
                    text = activity_str(plan_activity)
                    single_p = jp.P(
                        a=self.plan_div,
                        text=text,
                        classes=PLAN_PART_P_CLASS,
                        style=PLAN_PART_P_STYLE,
                    )
                single_p = jp.P(
                    a=self.plan_div,
                    text=f"It reaches {self.reached_goals} goals.",
                    classes=PLAN_PART_P_CLASS,
                    style=PLAN_PART_P_STYLE,
                )
            try:
                asyncio.run(self.plan_div.update())
            except RuntimeError:
                self.plan_div.update()

    def clear_activities_click(self, msg):

        self.logger.info("Clearing")
        if self.mode == Mode.GENERATING_PROBLEM:
            self.activities = []
            self.plan = None
            self.reached_goals = 0
            self.activity_info = None
            self.update_chosen_activities()
            self.update_planning_execution()
            self.update_activity_info()


    def clear_plan_click(self, msg):

        #TODO create the button that does this
        self.logger.info("Clearing plan")
        if self.mode == Mode.GENERATING_PROBLEM:
            self.plan = None

    def update_plan(self, activity_plan, reached_goals):
        self.plan = activity_plan
        self.reached_goals = reached_goals

    def show_gui_thread(self):
        from main_page import main_page
        @jp.SetRoute("/")
        def get_main_page():
            return main_page(self)
        jp.justpy(get_main_page)

    def generate_problem_click(self, msg):
        self.logger.info("Generating")
        if self.mode == Mode.GENERATING_PROBLEM:
            self.mode = Mode.OPERATING
            self.plan = None
            self.update_planning_execution()
            # unlock the planing method with the problem correctly generated
            self.start_queue.put(None)


def activity_info_click(name, gui: Gui, component, msg):
    gui.logger.info("Clicked info: " + name + f"with mode: {gui.mode}")
    assert name in all_activities.keys()
    gui.activity_info = name
    gui.update_activity_info()


def activity_add_click(activity, gui: Gui, component, msg):
    gui.logger.info("Clicked activity: " + activity + f"with mode: {gui.mode}")
    assert activity in all_activities.keys()
    if gui.mode == Mode.GENERATING_PROBLEM:
        gui.activities.append(activity)
        gui.update_chosen_activities()

async def reload_page():
    for page in jp.WebPage.instances.values():
        if page.page_type == 'main':
            await page.reload()


def activity_str(activity) -> str:
    ret = ["- "]
    if activity.ID:
        ret.append(f"ID: {activity.ID};")
    ret.append(f"{activity.name}")
    if activity.parameters:
        ret.append("(")
        print_params_names = len(activity.parameters) < 6
        params = []
        for k, v in activity.parameters:
            if print_params_names:
                params.append(f"{k}={v}")
            else:
                params.append(f"{v}")
        ret.append(", ".join(params))
        ret.append(")")
    return "".join(ret)
