import state
import orderedcollections
import sys

class DFA:
    def __init__(self, classes, states, startStateId):
        self.classes = classes
        self.states = states
        self.startStateId = startStateId
class MinimalDFA:
    def __init__(self):
        self.classes = orderedcollections.OrderedMap()
        self.states = orderedcollections.OrderedMap()
        self.numStates = 0

    def buildFromDFA(self, dfa):
        def newState():
            aState = state.State(self.numStates)
            self.states[self.numStates] = aState
            self.numStates += 1
            return self.numStates - 1
        def transToMinPartition(fromDFAStateId, onClass):
            goesTo = dfa.states[fromDFAStateId].onClassGoTo(onClass)
            return self.dfa2min[goesTo]
        def onClasses(minStateId):
            transitionsOn = orderedcollections.OrderedSet()
            for stateID in self.min2dfa[minStateId]:
                for classCh in self.classes:
                    if self.states[stateID].hasTransition(classCh):
                        transitionsOn.add(classCh)

            return transitionsOn

        def finer(minStateId):
            distinguishedStates = orderedcollections.OrderedSet()
            try:
                firstStateID = self.min2dfa[minStateId].pop()
            except Exception:
                return False
            madeAChange = False
            for onClass in dfa.states[firstStateID].getTransitions():
                firstGoesTo = transToMinPartition(firstStateID, onClass)
                for secondaryStateID in self.min2dfa[minStateId]:
                    secondGoesTo = transToMinPartition(
                        secondaryStateID, onClass)
                    if firstGoesTo != secondGoesTo:
                        distinguishedStates.add(secondaryStateID)
                        madeAChange = True
            self.min2dfa[minStateId].add(firstStateID)
            if len(distinguishedStates) == 0:
                return False
            for stateID in distinguishedStates:
                self.min2dfa[minStateId].remove(stateID)
            newStateForM2DFA = newState()
            self.min2dfa[newStateForM2DFA] = distinguishedStates
            for stateID in distinguishedStates:
                self.dfa2min[stateID] = newStateForM2DFA
            return madeAChange
        def constructMinStateTransitions():
            for minStateId in self.states:
                minState = self.states[minStateId]
                dfaStateIds = list(self.min2dfa[minStateId])
                dfaStateIds.sort()
                dfaStateId = dfaStateIds[0]

                if dfa.states[dfaStateId].isAccepting():
                    minState.setAccepting(
                        dfa.states[dfaStateId].getAcceptsTokenId())
                minState.transitions = {}

                trans = dfa.states[dfaStateId].getTransitions()
                for onClass in trans:
                    toDFAStateId = trans[onClass]
                    dfaState = dfa.states[toDFAStateId]
                    toStateId = self.dfa2min[toDFAStateId]
                    minState.addTransition(onClass, toStateId)

            self.startStateId = self.dfa2min[dfa.startStateId]

        self.classes = dfa.classes

        startStateId = newState()
        self.min2dfa = orderedcollections.OrderedMap()
        self.dfa2min = orderedcollections.OrderedMap()
        self.dfa2min[-1] = -1

        self.min2dfa[startStateId] = orderedcollections.OrderedSet()
        for stateId in dfa.states:
            dfaState = dfa.states[stateId]

            if not dfaState.isAccepting():
                self.min2dfa[startStateId].add(stateId)
                self.dfa2min[stateId] = startStateId
            else:
                found = False

                for minStateId in self.states:
                    minState = self.states[minStateId]
                    if minState.getAcceptsTokenId() == dfaState.getAcceptsTokenId():
                        self.min2dfa[minStateId].add(stateId)
                        self.dfa2min[stateId] = minStateId
                        found = True

                if not found:
                    finalStateId = newState()
                    self.min2dfa[finalStateId] = orderedcollections.OrderedSet([
                                                                               stateId])
                    self.dfa2min[stateId] = finalStateId
                    self.states[finalStateId].setAccepting(
                        dfaState.getAcceptsTokenId())

        self.startStateId = self.dfa2min[dfa.startStateId]
        while changed:
            changed = False
            for stateID in range(self.numStates):
                change = finer(stateID)
                if change:
                    changed = True
        constructMinStateTransitions()
    def writeListing(self, outStream):
        outStream.write("DFA TOI THIEU DUOC XAY DUNG LA:\n\n")
        outStream.write("Trang thai bat dau la: " +
                        str(self.startStateId) + "\n\n")
        outStream.write("Trang thai     ON CLASS     GO TO     ACCEPTS\n")
        outStream.write("-----     --------     -----     -------\n")

        for stateId in range(self.numStates):
            if self.states[stateId].isAccepting():
                acceptsId = self.states[stateId].getAcceptsTokenId()
                tokenName = "yes"
            else:
                tokenName = ""

            outStream.write("%5d %34s\n" % (stateId, tokenName))

            trans = self.states[stateId].getTransitions()
            for onClass in trans:
                outStream.write("%18s     %5d\n" % (onClass, trans[onClass]))

            outStream.write("\n")


def main():

    classes = {"a": frozenset(['a']), "b": frozenset(['b'])}

    q0 = state.State(0)
    q1 = state.State(1)
    q2 = state.State(2)
    q3 = state.State(3)
    q4 = state.State(4, 1)
    q5 = state.State(5)
    q6 = state.State(6)

    q0.addTransition("a", 1)
    q1.addTransition("b", 2)
    q2.addTransition("b", 3)
    q3.addTransition("a", 4)
    q4.addTransition("a", 5)
    q5.addTransition("b", 6)
    q6.addTransition("b", 3)

    states = {0: q0, 1: q1, 2: q2, 3: q3, 4: q4, 5: q5, 6: q6}

    dfa = DFA(classes, states, 0)

    mindfa = MinimalDFA()
    mindfa.buildFromDFA(dfa)
    mindfa.writeListing(sys.stdout)


if __name__ == "__main__":
    main()


# In[ ]:




