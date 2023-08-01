from generate_request import all_activities

import justpy as jp

LEFT_MARGIN, RIGHT_MARGIN = " margin-left: 10px; ", " margin-right: 20px; "

TITLE_DIV_CLASS = "grid justify-between gap-2 grid-cols-3"
TITLE_DIV_STYLE = "grid-template-columns: auto auto auto; margin-top: 15px;" + LEFT_MARGIN + RIGHT_MARGIN

TITLE_TEXT_DIV_STYLE = "font-size: 80px; text-align: center; text-weight: bold;"

DESCRIPTION_STYLE = "margin-top: 15px; font-size: 20px;" + LEFT_MARGIN + RIGHT_MARGIN
DESCRIPTION_TEXT = """
This is the description of the tsb-space and how it works.
bla bla bla
new line bla bla
new line bla
"""
SINGLE_DESCRIPTION_STYLE = LEFT_MARGIN + RIGHT_MARGIN


MAIN_BODY_DIV_CLASS = "grid justify-between grid-cols-3 gap-7"
MAIN_BODY_DIV_STYLE = "grid-template-columns: minmax(max-content, 25%) minmax(max-content, 25%) 10px minmax(max-content, 33%); width: 100vw; margin-top: 15px;" + LEFT_MARGIN + RIGHT_MARGIN

ACTIONS_DIV_CLASS = "grid"
# Setting height to 0 it'sa trick to solve the problem of the goal div changing size
ACTIONS_DIV_STYLE = f"grid-template-columns: auto auto; font-size: 30px; font-weight: semibold; height: 0px;"

SINGLE_ACTION_P_CLASS = ""
SINGLE_ACTION_P_STYLE = "font-weight: normal; font-size: 20px; margin-top: 15px;"

ADD_BUTTON_CLASS = "bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2"
ADD_BUTTON_STYLE = "font-weight: semibold; font-size: 20px; width: 100px;"

GOALS_DIV_CLASS = ""
GOALS_DIV_STYLE = "font-size: 30px; font-weight: semibold;"

min_goal_box_height = len(all_activities) * 63
GOALS_CONTAINER_DIV_CLASS = ""
GOALS_CONTAINER_DIV_STYLE = f"border: 1px solid #000; min-height: {min_goal_box_height}px; font-weight: normal; font-size: 20px;\
 background-color:  #e1eff7; right-margin: 50px;"

CLEAR_SOLVE_BUTTONS_DIV_CLASS = "flex grid-cols-2"
CLEAR_SOLVE_BUTTONS_DIV_STYLE = ""

CLEAR_SOLVE_BUTTONS_CLASS = ADD_BUTTON_CLASS
CLEAR_SOLVE_BUTTONS_STYLE = "font-weight: semibold; font-size: 20px;"

PLAN_DIV_CLASS = ""
PLAN_DIV_STYLE = "font-size: 30px; font-weight: semibold;"

PLAN_PART_P_CLASS = ""
PLAN_PART_P_STYLE = "font-weight: normal; font-size: 20px;"

CLEAR_PLAN_BUTTON_CLASS = ADD_BUTTON_CLASS
CLEAR_PLAN_BUTTON_STYLE = "font-weight: semibold; font-size: 20px;"


chosen_activities = ["AAAAAA", "BBBBBB", "AAAAA", "CCCCC"]
# chosen_activities = []

chosen_plan = chosen_activities

@jp.SetRoute("/")
def main_page():
    wp = jp.WebPage(delete_flag = False)
    wp.page_type = 'main'
    title_div = jp.Div(
        a=wp,
        classes=TITLE_DIV_CLASS,
        style=TITLE_DIV_STYLE,
    )
    fbk_logo_div = jp.Div(
        a=title_div,
        # text="FBK LOGO",
        # style="font-size: 30px;",
        style="height: 160px;",
    )
    fbk_logo = jp.Img(
        # src="/static/logos/fbk.webp",
        src="/static/logos/fbk.png",
        a=fbk_logo_div,
        classes="w3-image",
        # style="height: 100%; length: auto;",
    )
    title_text_div = jp.Div(
        a=title_div,
        text="TSB-SPACE",
        style=TITLE_TEXT_DIV_STYLE,
    )
    trasys_logo_div = jp.Div(
        a=title_div,
        # text="TRASYS LOGO",
        style="height: 160px;",
    )
    trasys = jp.Img(
        src="/static/logos/trasys.png",
        a=trasys_logo_div,
        classes="w3-image",
        # style="height: 10px; length: 10px;"
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

    actions_div = jp.Div(
        a=main_body_div,
        text="ACTIONS:",
        classes=ACTIONS_DIV_CLASS,
        style=ACTIONS_DIV_STYLE,
    )

    # Useless paragprah, added just as a place-holder
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
    for i, g in enumerate(chosen_activities):
        single_goal_p = jp.P(
            a=goals_container_div,
            text=f"{i+1}) {g}"
        )
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
    solve = jp.Input(
        a=clear_solve_buttons_div,
        value="SOLVE",
        type="submit",
        classes=CLEAR_SOLVE_BUTTONS_CLASS,
        style=CLEAR_SOLVE_BUTTONS_STYLE,
    )

    # Useless div, added just as a place-holder
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

    for p in chosen_plan:
        single_p = jp.P(
            a=plan_div,
            text=f"- {p}",
            classes=PLAN_PART_P_CLASS,
            style=PLAN_PART_P_STYLE,
        )





    return wp

jp.justpy(main_page)
