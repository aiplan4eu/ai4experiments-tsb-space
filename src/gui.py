import asyncio
from concurrent import futures
from enum import Enum, auto
from functools import partial

import logging
import os
import grpc
import queue
import justpy as jp

import grpc_io.tsb_space_pb2 as op_pb2
import grpc_io.tsb_space_pb2_grpc as op_pb2_grpc

import unified_planning as up
from unified_planning.shortcuts import *

from generate_request import all_activities

DEBUG = False
BUTTON_CLASS = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2'
# BUTTON_CLASS = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
ACTIVITY_DIV_STYLE = "color:blue;"
PLAN_DIV_STYLE = "color:blue;"


DIV_CLASS = "margin: auto; width: 50%;"
class Mode(Enum):
    GENERATING_PROBLEM = auto()
    OPERATING = auto()


curr_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(curr_dir, 'models')


def my_click(activity, gui, component, msg):
    gui.logger.info("Clicked activity: " + activity + f"with mode: {gui.mode}")
    # gui.display_debug("Clicked activity: " + activity + f"with mode: {gui.mode}")
    assert activity in all_activities.keys()
    if gui.mode == Mode.GENERATING_PROBLEM:
        gui.activities.append(activity)
        gui.update_activity_div()


class Gui():
    def __init__(self):
        self.problems_queue = queue.Queue()
        self.plans_queue = queue.Queue()
        # a queue where the interface waits the start
        self.start_queue = queue.Queue()

        self.text_div  = jp.Div(
            text='Plan will be displayed here',
            classes='',
            style= PLAN_DIV_STYLE,
        )
        self.debug_div  = jp.Div(
            text='Debug will be displayed here',
            classes='',
        )
        self.activity_div = jp.Div(
            text='Chosen activities will be displayed here',
            classes=DIV_CLASS,
            style = ACTIVITY_DIV_STYLE,
        )
        self.mode = Mode.GENERATING_PROBLEM
        self.activities = []

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger.setLevel(logging.INFO)

    def update_activity_div(self):
        if self.activities:
            activity_text = "Chosen activities:"
        else:
            activity_text = f'Chosen activities will be displayed here'
        self.activity_div.text = activity_text

        self.activity_div.delete_components()
        for i, a in enumerate(self.activities):
            d = jp.Div(
                text=f" {i+1}) {a}",
                classes='',
                a=self.activity_div,
                style=ACTIVITY_DIV_STYLE,
            )
        self.activity_div.update()

    def clear_activities_click(self, msg):

        self.logger.info("Clearing")
        if self.mode == Mode.GENERATING_PROBLEM:
            self.activities = []
            self.update_activity_div()

    def clear_plan_click(self, msg):

        self.logger.info("Clearing plan")
        if self.mode == Mode.GENERATING_PROBLEM:
            self.text_div.delete_components()
            self.text_div.update()

    def show_gui_thread(self):
        @jp.SetRoute("/")
        def get_main_page():
            return main_page(self)
        jp.justpy(get_main_page)

    def generate_problem_click(self, msg):
        self.logger.info("Generating")
        if self.mode == Mode.GENERATING_PROBLEM:
            self.mode = Mode.OPERATING
            # unlock the planing method with the problem correctly generated
            self.start_queue.put(None)
            self.display_text("Started planning... wait till finish")

    def display_text(self, text: str):
        actions = text.split("\n")
        self.text_div.delete_components()
        for action in actions:
            d = jp.Div(
                text=f"{action}",
                classes='',
                a=self.text_div,
                style=PLAN_DIV_STYLE,
            )
        self.text_div.update()

    def display_debug(self, text):
        logging.debug(text)
        self.logger.debug(text)
        if DEBUG:
            self.debug_div.text = text
            self.debug_div.update()

def main_page(gui):
    wp = jp.WebPage(delete_flag = False)
    wp.page_type = 'main'
    assert isinstance(gui, Gui), f"{gui}"


    gui.text_div.add_page(wp)

    wp.add(gui.text_div)

    handle_buttons_div  = jp.Div(
        text='',
        classes='',
        a=wp,
    )

    submit_button = jp.Input(
        value='Submit Problem',
        type='submit',
        a=handle_buttons_div,
        classes=BUTTON_CLASS
    )
    submit_button.on('click', gui.generate_problem_click)

    clear_activities_button = jp.Input(
        value='Clear Activities',
        type='submit',
        a=handle_buttons_div,
        classes=BUTTON_CLASS
    )
    clear_activities_button.on('click', gui.clear_activities_click)

    clear_plan_button = jp.Input(
        value='Clear Plan',
        type='submit',
        a=handle_buttons_div,
        classes=BUTTON_CLASS
    )
    clear_plan_button.on('click', gui.clear_plan_click)


    activities_buttons_div  = jp.Div(
        text='Possible activities. Click one to add it.',
        classes='',
        a=wp,
    )
    for i, activity in enumerate(all_activities.keys()):
        if i % 3 == 0:
            activities_buttons_div  = jp.Div(
                text='',
                classes='',
                a=wp,
            )
        activity_button = jp.Input(
            value=activity,
            type='submit',
            a=activities_buttons_div,
            classes=BUTTON_CLASS
        )
        activity_button.on('click', partial(my_click, activity, gui))

    gui.activity_div.add_page(wp)
    wp.add(gui.activity_div)

    if DEBUG:
        gui.debug_div.add_page(wp)
        wp.add(gui.debug_div)

    return wp


async def reload_page():
    for page in jp.WebPage.instances.values():
        if page.page_type == 'main':
            await page.reload()


def activity_str(activity) -> str:
    ret = ["-"]
    if activity.ID:
        ret.append(f"ID: {activity.ID};")
    ret.append(f"{activity.name}")
    if activity.parameters:
        ret.append("(")
        for k, v in activity.parameters:
            ret.append(f"{k}={v},")
        ret.append(")")
    return "".join(ret)
