# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Version 1.00
import csv
import random
import functools
import helpers as help
import psychopy.visual
from psychopy import visual, event, core, gui


# get user data before setup, since Dlg does not work in fullscreen
title = 'SIP IAT'
questions = {'ID': '', 'Condition': ['A', 'B']}
info = help.getInput(title, questions) or core.quit()

# create all the basic objects (window, fixation-cross, feedback)
win = visual.Window(units='norm', color='black', fullscr=True)
fixCross = visual.TextStim(win, text='+', height=0.1)
negFeedback = visual.TextStim(win, text='X', color='red', height=0.1)
win.setMouseVisible(False)

# partially apply the helper functions to suite our needs
draw = functools.partial(help.draw, win)
show = functools.partial(help.showInstruction, win)
wrapdim = functools.partial(help.wrapdim, win, height=0.08)

# Response Mappings
# you can change the keybindings and allRes to fit your IAT constraints
keybindings = ['e', 'i']
allRes = ['Other', 'Self','Science', 'Liberal Arts']
allMappings = help.getResponseMappings(allRes, keybindings=keybindings)
negoposelfMap, selfnegopoMap = allMappings[-2:]
selfotherMap, otherselfMap, posnegMap, negposMap = allMappings[:4]

self, other, pos, neg = ['Other', 'Self', 'Science', 'Liberal Arts']
leftup, rightup = (-0.8, +0.8), (+0.8, +0.8)
leftdown, rightdown = (-0.8, +0.7), (+0.8, +0.7)

# this could be implemented better, naming is pretty hard
otherself = wrapdim({other: leftup, self: rightup})
negpos = wrapdim({neg: leftup, pos: rightup})
selfother = wrapdim({self: leftup, other: rightup})
selfnegopo = wrapdim({self: leftup, neg: leftdown,
                      other: rightup, pos: rightdown})
negopoself = wrapdim({neg: leftup, other: leftdown,
                      pos: rightup, self: rightdown})

experimentData = []
timer = core.Clock()
# you can easily change the stimuli by changing the csv
stimuli = help.getStimuli('stimuli.csv')

ISI = 0.150
TIMEOUT = 1.5
feedbackTime = 1


def block(anchors, responseMap, selection, trialName, trials=20):
    data = []
    help.autodraw(anchors)

    filteredStim = help.filterStimuli(stimuli, 'response', *selection)
    extendedStim = help.compensate(filteredStim, trials)
    randomStim = sorted(extendedStim, key=lambda x: random.random())[:trials]
    preparedStim = help.deneigh(randomStim)

    for stimulus in preparedStim:
        onTime = True
        content = stimulus['content']
        rightAnswer = responseMap[stimulus['response']]
        curStim = visual.TextStim(win, text=content, height=0.1)
        rightKeys = list(responseMap.values()) + ['escape']
        draw(curStim)
        timer.reset()
        userAnswer = event.waitKeys(keyList=rightKeys) or []
        choseWisely = help.equals(userAnswer, rightAnswer)
        if choseWisely:
            RT = timer.getTime()
        elif 'escape' in userAnswer:
            core.quit()
        else:
            RT = timer.getTime()
            onTime = False
            draw(negFeedback, feedbackTime)
            draw(curStim)
            event.waitKeys(keyList=[rightAnswer])
        data.append([ISI, content, int(onTime), RT, trialName])
        draw(fixCross, ISI)

    help.autodraw(anchors, draw=False)
    return data

def wrap(*args, **kwargs):
    return functools.partial(block, *args, **kwargs)


allBlocks = {
    1: wrap(otherself, otherselfMap, allRes[:2], 'SelfOther'),
    2: wrap(negpos, negposMap, allRes[2:], 'LibSci'),
    3: wrap(negopoself, negoposelfMap, allRes, 'LibSelfSciOther'),
    4: wrap(negopoself, negoposelfMap, allRes, 'LibSelfSciOther40', trials=40),
    5: wrap(selfother, selfotherMap, allRes[:2], 'OtherSelf'),
    6: wrap(selfnegopo, selfnegopoMap, allRes, 'OtherLibSelfSci'),
    7: wrap(selfnegopo, selfnegopoMap, allRes, 'OtherLibSelfSci40', trials=40)
}


def main():
    # Instruction Setup
    header = ['ISI', 'Content', 'corrAns', 'RT', 'trialName']
    mainInstruction = 'instructions/mainInstruction.png'
    instructions = {1: 'instructions/instr1.png',
                    2: 'instructions/instr2.png',
                    3: 'instructions/instr3.png',
                    4: 'instructions/instr4.png',
                    5: 'instructions/instr5.png',
                    6: 'instructions/instr6.png',
                    7: 'instructions/instr7.png'}
    endInstruction = 'instructions/endInstruction.png'

    show(image=mainInstruction)
    trialType = random.randint(0, 1)
    order = [1, 2, 3, 4, 5, 6, 7] if trialType else [5, 2, 6, 7, 1, 3, 4]


    # order the blocks and instruction according to the trialType
    blockOrder = [allBlocks[num] for num in order]
    instructionOrder = [instructions[num] for num in order]
    data = help.runExperiment(show, instructionOrder, blockOrder)

    ## Save Data to CSV
    experimentData.extend([info.values(), header])
    experimentData.extend(data)
    print(experimentData)
    file = '{0}_{1}.csv'.format(info['Condition'], trialType)
    help.saveData(file, experimentData)

    show(image=endInstruction)

main()
