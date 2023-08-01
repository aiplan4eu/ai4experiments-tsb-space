import os
import requests
import logging
import xml.etree.ElementTree as ET

from parser import parse_fromstring, parse_atlmodel
from planning import get_activity_name, get_available_resources, is_valid, encode_result
from typing import Tuple
from utils import Activity
from generate_model import generate_planning_model, convert_to_non_temporal_model
from up_grafene_engine.engine import  GrafeneEngine

from unified_planning.shortcuts import *
import unified_planning as up
import unified_planning.engines
import unified_planning.model
import unified_planning.model.metrics

get_environment().credits_stream = None

curr_dir = os.path.dirname(os.path.abspath(__file__))
tsb_space_src_dir = os.path.join(curr_dir, '..', 'tsb-space', 'src')
models_dir = os.path.join(tsb_space_src_dir, '..', 'models')

# import sys
# print("added path = ",tsb_space_src_dir)
# sys.path.append(tsb_space_src_dir)


def planning(request, engine: GrafeneEngine):
    logging.info("Generating planning problem...")

    with open(os.path.join(models_dir, 'atlmodel.xml')) as f:
        atlmodel = f.read()

    use_rehearsal_to_validate = os.environ.get('USE_REHEARSAL_TO_VALIDATE') == 'TRUE'

    _, _, _, template_activities = parse_atlmodel(atlmodel, False)
    problem, activity_params_mapping, tobj_to_val, extra_params = generate_planning_model(atlmodel, request)
    nt_problem = convert_to_non_temporal_model(problem)
    with Compiler(problem_kind=nt_problem.kind, compilation_kind="USERTYPE_FLUENTS_REMOVING") as compiler:
        nt_problem = compiler.compile(nt_problem).problem

    # print(nt_problem)

    logging.info("Planning...")

    activity_plan = None
    goals = list(nt_problem.goals)
    while activity_plan is None and len(goals) > 0:
        new_problem = nt_problem.clone()
        new_problem.add_quality_metric(up.model.metrics.MinimizeSequentialPlanLength())
        simulator = up.engines.UPSequentialSimulator(new_problem)
        activity_plan = []
        for i, g in enumerate(goals):
            new_problem.clear_goals()
            new_problem.add_goal(g)
            res = engine.solve(new_problem, "solved_optimally")
            plan = res.plan
            if plan is not None:
                state = simulator.get_initial_state()
                for ai in plan.actions:
                    action = ai.action
                    params = ai.actual_parameters
                    n = get_activity_name(action)
                    act_params = []
                    ta = template_activities[n]
                    _, obj_to_val = activity_params_mapping[n]
                    params_names = [p.name for p in action.parameters]
                    for p in ta.parameters:
                        k = p.name
                        if k in params_names:
                            i = params_names.index(k)
                            v = params[i].object().name
                            if (k, v) in obj_to_val:
                                v = obj_to_val[(k, v)]
                            else:
                                v = tobj_to_val[v]
                            act_params.append((k, str(v)))
                        elif action.name in extra_params and k in extra_params[action.name]:
                            act_params.append((k, extra_params[action.name][k]))
                        else:
                            act_params.append((k, str(p.default)))
                    activity_plan.append(Activity("", n, act_params))
                    state = simulator.apply(state, action, params)
                for k in new_problem.initial_values.keys():
                    new_problem.set_initial_value(k, state.get_value(k))
            else:
                activity_plan = None
                break

        if activity_plan is None:
            break
        elif use_rehearsal_to_validate:
            logging.info("Found a plan. Validating it using RAAS...")
            is_val, missing_resources = is_valid(request, activity_plan, len(goals))
            if is_val:
                break
            elif missing_resources:
                goals = goals[:-1]
                activity_plan = None
                logging.info("Not able to find an activity plan with the given resources! Planning again removing last goal activity...")
                if len(goals) == 0:
                    logging.info("No goal activities left!")
            else:
                break
        else:
            break

    if activity_plan is None:
        logging.info("No activity plan found!")
    else:
        logging.info("Activity plan found!")

    return activity_plan, len(goals)
