from operator import itemgetter
from python_helper import ObjectHelper, RandomHelper, ReflectionHelper, log
from reinforcement_learning.framework.object import Object, Id, getId
from reinforcement_learning.framework import value as valueModule
from reinforcement_learning.framework.value import List, Dictionary
from reinforcement_learning.ai.history import History
from reinforcement_learning.ai.state import State
from reinforcement_learning.ai.action import Action
from reinforcement_learning.ai.reward import Reward
from reinforcement_learning.framework.exception import (
    MethodNotImplementedException
)


class AgentConstants:

    ID = '_id'
    ACTIONS = 'actions'
    ACTION = 'action'
    ACTION_VALUE = 'value'
    ACTION_VISITS = 'visits'

    ID_DB_KEY = ID
    STATE_HASH_DB_KEY = 'stateHash'
    ACTIONS_DB_KEY = ACTIONS
    ACTION_DB_KEY = ACTION
    ACTION_VALUE_DB_KEY = ACTION_VALUE
    ACTION_VISITS_DB_KEY = ACTION_VISITS


class Agent(Object):

    def __init__(
        self,
        key: str,
        actionTable: dict = None,
        exploration: float = 0.0,
        retention: float = 1.0,
        id: Id = None
    ):
        """
        'actionTable': {
            'stateHash': {
                '_id': MongoDbId('something'),
                'actions': [
                    {
                        'action': 'some action',
                        'value': float(),
                        'visits': int()
                    }
                ]
            }
        }
        """
        Object.__init__(self, id=id)
        self.key = key
        self.setActionTable({} if ObjectHelper.isEmpty(actionTable) else actionTable)
        self.exploration = exploration
        self.retention = retention
        self.activateAgentUpdate()

    def getCopy(self):
        raise Exception('Agents should not be copied')

    def getKey(self) -> str:
        return str(self.key)

    def setActionTable(self, actionTable: dict):
        # self.actionTable = {**actionTable}
        self.actionTable = actionTable

    def getActionTable(self):
        # return {**self.actionTable}
        return self.actionTable

    def getDefaultStateActions(self):
        raise MethodNotImplementedException()

    def getAction(self, state: State, possibleActions: List) -> tuple:
        raise MethodNotImplementedException()

    def byPassAgentUpdate(self):
        self.doUpdate: bool = False

    def activateAgentUpdate(self):
        self.doUpdate: bool = True

    def update(self, history: History, isFinalState: bool):
        if self.doUpdate:
            self._update(history, isFinalState)

    def _update(self, history: History, isFinalState: bool):
        raise MethodNotImplementedException()

    def access(self, givenStateHash: State) -> dict:
        for stateHash, visit in self.actionTable.items():
            if givenStateHash == stateHash:
                return visit
        return Dictionary()

    def accessByAction(self, stateHash: str, action: Action) -> dict:
        for v in self.access(stateHash).get(AgentConstants.ACTIONS, List()):
            if action.getHash() == v[AgentConstants.ACTION].getHash():
                return v
        # for stateHash, visit in self.actionTable.items():
        #     if givenStateHash == stateHash:
        #         for v in visit[AgentConstants.ACTIONS]:
        #             # print('===========================================================================================')
        #             # print(action)
        #             # print(action.getHash())
        #             # print(v[AgentConstants.ACTION])
        #             # print(v[AgentConstants.ACTION].getHash())
        #             if action.getHash() == v[AgentConstants.ACTION].getHash():
        #                 return v
        return Dictionary()

    def printActionTable(self):
        actionTable = self.getActionTable()
        log.prettyPython(self.printActionTable, 'actionTable', actionTable, logLevel=log.DEBUG)
        for k, v in actionTable.items():
            actionTable[k] = valueModule.sortedBy(v[AgentConstants.ACTIONS], AgentConstants.ACTION_VALUE)
        log.prettyPython(self.printActionTable, 'q(s,a)', actionTable, logLevel=log.DEBUG)
        log.debug(self.printActionTable, f'size: {len(self.actionTable)}')

    def __str__(self):
        return f'{ReflectionHelper.getClassName(self)}(id: {self.getId()})'

    def __repr__(self):
        return self.__str__()
