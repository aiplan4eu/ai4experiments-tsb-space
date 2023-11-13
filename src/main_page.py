from functools import partial
from generate_request import all_activities, activity_description_map

import justpy as jp

from gui import Gui, activity_add_click, activity_str, ACTION_DETAILS_TEXT_CLASS, ACTION_DETAILS_TEXT_STYLE, activity_info_click


# Scaling factor for downscaling by 10%
SCALE_FACTOR = 0.9

LEFT_MARGIN, RIGHT_MARGIN = " margin-left: 9px; ", " margin-right: 18px; "

TITLE_DIV_CLASS = "grid justify-between gap-2 grid-cols-3"
TITLE_DIV_STYLE = f"grid-template-columns: auto auto auto; margin-top: 13.5px;{LEFT_MARGIN}{RIGHT_MARGIN}"

TITLE_TEXT_DIV_STYLE = "font-size: 72px; text-align: center; font-weight: bold;"

DESCRIPTION_STYLE = f"margin-top: 13.5px; font-size: 18px;{LEFT_MARGIN}{RIGHT_MARGIN}"
DESCRIPTION_TEXT = """
This is the integration of the tsb-space in the ai4experiments platform.
It works by specifying a series of high-level activities that must be performed in the specified order.
After the activity plan is defined, the planner decomposes each high-level activity into smaller actions that the robot performs to fulfill the plan.

- Press ADD to start adding activities.
- Press INFO to get information about a specific activity.
"""
SINGLE_DESCRIPTION_STYLE = f"{LEFT_MARGIN}{RIGHT_MARGIN}"

MAIN_BODY_DIV_CLASS = "grid justify-between grid-cols-3 gap-7"
MAIN_BODY_DIV_STYLE = f"grid-template-columns: max-content max-content 9px 0.9fr; width: 90vw; margin-top: 13.5px;{LEFT_MARGIN}{RIGHT_MARGIN}"

ACTIVITY_DETAILS_DIV_CLASS = "grid"
ACTIVITY_DETAILS_DIV_STYLE = f"grid-template-columns: max-content auto; font-size: 27px; font-weight: semibold; height: 0px;{LEFT_MARGIN}{RIGHT_MARGIN}"

ACTIONS_DIV_CLASS = "grid"
ACTIONS_DIV_STYLE = f"grid-template-columns: auto auto auto; font-size: 27px; font-weight: semibold; height: 0px; column-gap: 3px; row-gap: 2px;"

SINGLE_ACTION_P_CLASS = ""
SINGLE_ACTION_P_STYLE = f"font-weight: normal; font-size: 18px; margin-top: 13.5px;"

BUTTON_FONT_SIZE = int(18*SCALE_FACTOR)
ADD_BUTTON_CLASS = "bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-1.8 px-3.6 border border-blue-500 hover:border-transparent rounded m-1.8"
ADD_BUTTON_STYLE = f"font-weight: semibold; font-size: {BUTTON_FONT_SIZE}px; width: 80px;"

GOALS_DIV_CLASS = ""
GOALS_DIV_STYLE = "font-size: 27px; font-weight: semibold;"

min_goal_box_height = int(len(all_activities) * 56.7)
GOALS_CONTAINER_DIV_CLASS = ""
GOALS_CONTAINER_DIV_STYLE = f"border: 0.9px solid #000; min-height: {min_goal_box_height}px; font-weight: normal; font-size: 18px;\
 background-color:  #e1eff7; right-margin: 45px; width: 315px;"

CLEAR_SOLVE_BUTTONS_DIV_CLASS = "flex grid-cols-2"
CLEAR_SOLVE_BUTTONS_DIV_STYLE = "margin-top: 4px; column-gap: 3px;"

CLEAR_SOLVE_BUTTONS_CLASS = ADD_BUTTON_CLASS
CLEAR_SOLVE_BUTTONS_STYLE = f"font-weight: semibold; font-size: {BUTTON_FONT_SIZE}px;"

PLAN_DIV_CLASS = ""
PLAN_DIV_STYLE = f"font-size: 27px; font-weight: semibold;"

PLAN_PART_P_CLASS = ""
PLAN_PART_P_STYLE = f"font-weight: normal; font-size: 18px;"

CLEAR_PLAN_BUTTON_CLASS = ADD_BUTTON_CLASS
CLEAR_PLAN_BUTTON_STYLE = f"font-weight: semibold; font-size: {BUTTON_FONT_SIZE}px;"


def main_page(gui: Gui):
    wp = jp.WebPage(delete_flag=False)
    wp.page_type = 'main'
    title_div = jp.Div(
        a=wp,
        classes=TITLE_DIV_CLASS,
        style=TITLE_DIV_STYLE,
    )
    fbk_logo_div = jp.Div(
        a=title_div,
        style="height: 144px;",
    )
    fbk_logo = jp.Img(
        src="/static/logos/fbk.png",
        a=fbk_logo_div,
        classes="w3-image",
    )
    title_text_div = jp.Div(
        a=title_div,
        text="TSB-SPACE",
        style=TITLE_TEXT_DIV_STYLE,
    )
    trasys_logo_div = jp.Div(
        a=title_div,
        style="height: 144px;",
    )
    trasys = jp.Img(
        src="/static/logos/trasys.png",
        a=trasys_logo_div,
        classes="w3-image",
    )

    description_div = jp.Div(
        a=wp,
        style=DESCRIPTION_STYLE,
    )
    for single_desc in DESCRIPTION_TEXT.split("\n"):
        description_paragraph = jp.P(
            a=description_div,
            style=SINGLE_DESCRIPTION_STYLE,
            text=single_desc,
        )

    main_body_div = jp.Div(
        a=wp,
        classes=MAIN_BODY_DIV_CLASS,
        style=MAIN_BODY_DIV_STYLE,
    )

    # Create a separate div to display action details at the bottom of the page
    activity_details_div = jp.Div(
        a=wp,
        classes=ACTIVITY_DETAILS_DIV_CLASS,
        style=ACTIVITY_DETAILS_DIV_STYLE,
    )
    gui.activity_details_div = activity_details_div

    actions_div = jp.Div(
        a=main_body_div,
        text="ACTIVITIES:",
        classes=ACTIONS_DIV_CLASS,
        style=ACTIONS_DIV_STYLE,
    )

    _ = jp.P(
        a=actions_div,
        text="",
    )
    _ = jp.P(
        a=actions_div,
        text="",
    )

    for act in all_activities.keys():

        act_name = jp.P(
            a=actions_div,
            text=act,
            classes=SINGLE_ACTION_P_CLASS,
            style=SINGLE_ACTION_P_STYLE,
        )

        act_button = jp.Input(
            a=actions_div,
            value="ADD",
            type="submit",
            classes=ADD_BUTTON_CLASS,
            style=ADD_BUTTON_STYLE,
        )
        act_button.on('click', partial(activity_add_click, act, gui))

        info_button = jp.Input(
            a=actions_div,
            value="INFO",
            type="submit",
            classes=ADD_BUTTON_CLASS,
            style=ADD_BUTTON_STYLE,
        )
        info_click = partial(activity_info_click, act, gui)
        info_button.on('click', info_click)
        if gui.activity_info == act:
            info_click(None, None)

    goals_div = jp.Div(
        a=main_body_div,
        text="GOALS:",
        classes=GOALS_DIV_CLASS,
        style=GOALS_DIV_STYLE,
    )

    goals_container_div = jp.Div(
        a=goals_div,
        classes=GOALS_CONTAINER_DIV_CLASS,
        style=GOALS_CONTAINER_DIV_STYLE,
    )
    gui.goals_container_div = goals_container_div

    gui.update_chosen_activities()

    clear_solve_buttons_div = jp.Div(
        a=goals_div,
        classes=CLEAR_SOLVE_BUTTONS_DIV_CLASS,
        style=CLEAR_SOLVE_BUTTONS_DIV_STYLE,
    )

    clear = jp.Input(
        a=clear_solve_buttons_div,
        value="CLEAR",
        type="submit",
        classes=CLEAR_SOLVE_BUTTONS_CLASS,
        style=CLEAR_SOLVE_BUTTONS_STYLE,
    )
    clear.on('click', gui.clear_activities_click)
    solve = jp.Input(
        a=clear_solve_buttons_div,
        value="SOLVE",
        type="submit",
        classes=CLEAR_SOLVE_BUTTONS_CLASS,
        style=CLEAR_SOLVE_BUTTONS_STYLE,
    )
    solve.on('click', gui.generate_problem_click)

    _ = jp.Div(
        a=main_body_div,
        classes="",
        style="",
    )

    plan_div = jp.Div(
        a=main_body_div,
        text="PLAN:",
        classes=PLAN_DIV_CLASS,
        style=PLAN_DIV_STYLE,
    )
    gui.plan_div = plan_div

    gui.update_planning_execution()

    return wp
