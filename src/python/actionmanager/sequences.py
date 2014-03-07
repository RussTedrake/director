import actions
from actions import *
from collections import OrderedDict

#Create a list of all sequences
primitivesDict = OrderedDict([])
sequenceDict = OrderedDict([])

for name, value in actions.__dict__.iteritems():

    if hasattr(value, '__bases__') and Action in value.__bases__:
        if name == 'Goal' or name == 'Fail':
            continue
        argDict = {}
        for arg in value.inputs:
            argDict[arg] = 'USER'
        primitivesDict[name] = [{name : [value, 'goal', 'fail', argDict]}, name, 'Primitive']


#Create new sequences below and add each to the list.
# Format for adding is: (name, sequence_definition_dictionary, start_state, 'Sequence')

simple_reach_seq    = {'wait_for_scan1': [WaitForScan,    'pose_search',   'fail',      {} ],
                       'pose_search'   : [PoseSearch,     'reach_plan',    'walk_plan', {'Affordance': 'USER', 'Hand': 'USER', 'Constraints': 'USER'} ],
                       'walk_plan'     : [WalkPlan,       'walk',          'fail',      {'WalkTarget': 'pose_search'} ],
                       'walk'          : [Walk,           'wait_for_scan2','fail',      {'WalkPlan': 'walk_plan'} ],
                       'wait_for_scan2': [WaitForScan,    'fit',           'fail',      {} ],
                       'fit'           : [Fit,            'reach_plan',    'fail',      {'Affordance': 'USER'} ],
                       'reach_plan'    : [ReachPlan,      'reach',         'fail',      {'TargetPose': 'pose_search', 'Hand': 'pose_search', 'Constraints': 'USER'} ],
                       'reach'         : [Reach,          'grip',          'fail',      {'JointPlan': 'reach_plan'} ],
                       'grip'          : [Grip,           'retract_plan1', 'fail',      {'Hand': 'pose_search'} ],
                       'retract_plan1' : [JointMovePlan,  'retract_move1', 'fail',      {'PoseName': '1 walking with hose', 'Group': 'hose', 'Hand': 'USER'} ],
                       'retract_move1' : [JointMove,      'goal',          'fail',      {'JointPlan': 'retract_plan1'} ]}

#sequenceDict['PlannedReach'] = [simple_reach_seq, 'wait_for_scan1', 'Sequence']

simple_reach_seq = {'walk_plan'    : [WalkPlan,      'walk',          'fail',      {'WalkTarget': 'USER'} ],
                    'walk'         : [Walk,          'wait_for_scan', 'fail',      {'WalkPlan': 'walk_plan'} ],
                    'wait_for_scan': [WaitForScan,   'fit',           'fail',      {} ],
                    'fit'          : [Fit,           'reach_plan',    'fail',      {'Affordance': 'USER'} ],
                    'reach_plan'   : [ReachPlan,     'reach',         'walk_plan', {'TargetFrame': 'USER', 'Hand': 'USER', 'Constraints': 'USER'} ],
                    'reach'        : [Reach,         'grip',          'fail',      {'JointPlan': 'reach_plan'} ],
                    'grip'         : [Grip,          'retract_plan',  'fail',      {'Hand': 'pose_search'} ],
                    'retract_plan' : [JointMovePlan, 'retract_move',  'fail',      {'PoseName': '1 walking with hose', 'Group': 'hose', 'Hand': 'USER'} ],
                    'retract_move' : [JointMove,     'goal',          'fail',      {'JointPlan': 'retract_plan'} ]}

sequenceDict['SimpleReach'] = [simple_reach_seq, 'wait_for_scan', 'Sequence']

drill_reach_seq = {'pose_search'   : [PoseSearch,    'reach_plan',    'fail',      {'Affordance': 'drill', 'Hand' : 'right'} ],
                   'walk_plan'     : [WalkPlan,      'walk',          'fail',      {'WalkTarget': 'pose_search'} ],
                   'walk'          : [Walk,          'wait_for_scan', 'fail',      {'WalkPlan': 'walk_plan'} ],
                   'wait_for_scan' : [WaitForScan,   'fit',           'fail',      {} ],
                   'fit'           : [Fit,           'pose_search',   'fail',      {'Affordance': 'drill'} ],
                   'reach_plan'    : [ReachPlan,     'pregrasp_plan', 'walk_plan', {'TargetFrame': 'pose_search', 'Hand': 'pose_search', 'Constraints': 'none'} ],
                   'pregrasp_plan' : [JointMovePlan, 'pregrasp_move', 'fail',      {'PoseName': '1 walking with hose', 'Group': 'hose', 'Hand': 'right'} ],
                   'pregrasp_move' : [JointMove,     'reach_plan2',   'fail',      {'JointPlan': 'retract_plan'} ],
                   'reach_plan2'   : [ReachPlan,     'reach',         'fail',      {'TargetFrame': 'pose_search', 'Hand': 'pose_search', 'Constraints': 'none'} ],
                   'reach'         : [Reach,         'grip',          'fail',      {'JointPlan': 'reach_plan'} ],
                   'grip'          : [Grip,          'retract_plan',  'fail',      {'Hand': 'pose_search'} ],
                   'retract_plan'  : [JointMovePlan, 'retract_move',  'fail',      {'PoseName': '1 walking with hose', 'Group': 'hose', 'Hand': 'right'} ],
                   'retract_move'  : [JointMove,     'goal',          'fail',      {'JointPlan': 'retract_plan'} ]}

sequenceDict['DrillReachR'] = [drill_reach_seq, 'wait_for_scan', 'Sequence']

named_pose_seq = {'manip_mode' : [ChangeMode,    'joint_plan', 'fail', {'NewMode' : 'manip'} ],
                  'joint_plan' : [JointMovePlan, 'joint_move', 'fail', {'PoseName': '1 walking with hose', 'Group': 'hose', 'Hand': 'USER'} ],
                  'joint_move' : [JointMove,     'goal',       'fail', {'JointPlan': 'joint_plan'} ]}

sequenceDict['NamedPose'] = [named_pose_seq, 'manip_mode', 'Sequence']

simple_walk_seq = {'step_mode' : [ChangeMode,    'walk_plan', 'fail', {'NewMode'   : 'stand'} ],
                   'walk_plan' : [WalkPlan,      'walk',      'fail', {'WalkTarget': 'USER'} ],
                   'walk'      : [Walk,          'goal',      'fail', {'WalkPlan'  : 'walk_plan'} ]}

sequenceDict['SimpleWalk'] = [simple_walk_seq, 'step_mode', 'Sequence']

#Make a list out of the sequence ditionary, don't touch this line, just add to the dictionary
sequenceList = [[key]+sequenceDict[key] for key in sequenceDict.keys()]
