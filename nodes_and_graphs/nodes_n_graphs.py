# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from dataclasses import dataclass, field
from os import getcwd, path

from prompt_toolkit.validation import ValidationError, Validator
from PyInquirer import prompt

GLOBAL_NODE_LIST: list = []


@dataclass
class Node:
    conn: list[list]
    t_p: float
    t_d: float

    def calc_t(self) -> float:
        return self.t_p + self.t_d


@dataclass
class Graph:
    node_dict: dict = field(default_factory=dict)

    def get_nodes_from_file(self, filename: str):
        __location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
        with open(path.join(__location__, filename), encoding="utf8") as file:
            for line in file:
                line = line.strip()
                unpack = line.split("|")
                # print(unpack)
                self.create_node(unpack[0], unpack[1].split(","), float(unpack[2]))

    def create_node(
        self, name: str, conns: list, t_p: float = 0.0, t_d: float = 0.0
    ) -> None:
        if name not in self.node_dict:
            self.node_dict[name] = Node([[], conns], t_p=t_p, t_d=t_d)
        else:
            self.node_dict[name].conn[1] = conns
            self.node_dict[name].t_p = t_p
            self.node_dict[name].t_d = t_d
        for i in conns:
            if i in self.node_dict:
                self.node_dict[i].conn[0].append(name)
            else:
                self.node_dict[i] = Node([[name], []], t_p=t_p, t_d=t_d)

    def get_stream(self, node: str, stream_num: int) -> list:
        stream: list = []
        if self.node_dict[node].conn[stream_num] != []:
            for i in self.node_dict[node].conn[stream_num]:
                stream = stream + self.get_stream(i, stream_num)
        stream.append(node)
        return stream

    def dependents(self, stream: str, node: str) -> list:
        stream_list: list = []
        if stream.lower() == "downstream":
            stream_list = self.get_stream(node, 1)[:-1]
        if stream.lower() == "upstream":
            stream_list = self.get_stream(node, 0)[:-1]
        return list(set(stream_list))

    def time_it(self, stream: str, node: str) -> str:
        total = self.node_dict[node].calc_t()
        for i in self.dependents(stream=stream, node=node):
            total += self.node_dict[i].calc_t()
        return format(total, ".1f")


class InputNodeValidator(Validator):
    def validate(self, document):
        if document.text not in GLOBAL_NODE_LIST:
            raise ValidationError(
                message="Incorrect node selected", cursor_position=len(document.text)
            )


@dataclass
class UserInputs:
    action: str
    stream: str
    node: str


def user_input(actions: list, streams: list) -> UserInputs:
    question_action = [
        {
            "type": "list",
            "name": "Action",
            "message": "What do you want to find?",
            "choices": actions,
        }
    ]
    question_stream = [
        {
            "type": "list",
            "name": "Stream",
            "message": "Select stream",
            "choices": streams,
        }
    ]

    question_node = [
        {
            "type": "input",
            "name": "Node",
            "message": "Which node? ",
            "validate": InputNodeValidator,
        }
    ]

    user_selection = UserInputs(
        prompt(question_action)["Action"],
        prompt(question_stream)["Stream"],
        prompt(question_node)["Node"],
    )

    return user_selection


def main():

    graph_node: Graph = Graph()
    graph_node.get_nodes_from_file("nodes.txt")

    global GLOBAL_NODE_LIST
    GLOBAL_NODE_LIST = graph_node.node_dict.keys()
    actions: dict = {
        "Find streams": graph_node.dependents,
        "Processing time": graph_node.time_it,
    }
    dependents: list = ["Downstream", "Upstream"]
    inputs: UserInputs = user_input(actions=actions.keys(), streams=dependents)
    if inputs.action == "Processing time" and inputs.stream == "Downstream":
        print(
            "Nonsensical! Processing time only makes sense for upstream (looking backwards in the graph)"
        )
    else:
        print(actions[inputs.action](inputs.stream, inputs.node))


if __name__ == "__main__":
    main()
