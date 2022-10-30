import networkx as nx

from classes.workload.layer_node import LayerNode, InputLayerNode
from typing import Dict, Any
from networkx import DiGraph


class DNNWorkload(DiGraph):

    def __init__(self, workload: Dict[Any, Dict], **attr):
        """
        Collect all the algorithmic workload information here.
        :param workload: user-defined workload file (py).

        :return (self): Directed Graph with nodes the layers and edges the connections between layers.
        """
        super().__init__(**attr)

        layer_id_to_obj = {}  # Lookup dict for id to LayerNode object translation
        #self.layer_node_list = []

        for layer_id, layer in workload.items():
            # TODO Support other type of layers, such as concatenation, max pooling, BN, etc.
            #  What is special about max pooling?
            # elif type(layer_id) == str and layer_id[0:6] == 'concat':
            #     continue
            '''For each item in the dict generate the LayerNode and add it to the dnn graph G'''

            if layer['equation'] == 'input':
                layer_node = InputLayerNode(layer_id, **layer)
                self.add_node(layer_node)
                layer_id_to_obj[layer_id] = layer_node
                #self.layer_node_list.append(layer_node)
            else:
                layer_node = LayerNode(layer_id, layer)
                '''Save this layer_id and LayerNode pair in the layer_id_to_obj dict'''
                layer_id_to_obj[layer_id] = layer_node
                # self.add_node(layer_id, info=layer_node)
                self.add_node(layer_node)
                #self.layer_node_list.append(layer_node)
                '''Find all of its operand sources and add edges accordingly'''
                edges = []
                for (op, parent_list) in layer.get('operand_source', {}).items():
                    for parent_id in parent_list:
                        parent_layer = layer_id_to_obj[parent_id]
                        edges.append((parent_layer, layer_node))
                        layer_node.input_operand_source[op] = parent_layer
                self.add_edges_from(edges)

    def topological_sort(self):
        return nx.topological_sort(self)

    def get_node_with_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        raise ValueError("DNNWorkload instance does not have a node with the requested id")

if __name__ == "__main__":
    from inputs.WL.Meta_prototype.workload_fsrcnn import workload
    # from inputs.ASPLOS.WL.Meta_prototype.workload_dmcnnvd import workload
    # from inputs.ASPLOS.WL.Meta_prototype.workload_mccnn import workload
    # from inputs.ASPLOS.WL.Meta_prototype.workload_mobilenetv1 import workload
    # from inputs.ASPLOS.WL.Meta_prototype.workload_resnet18 import workload

    ml_workload = DNNWorkload(workload)

    # print layer size
    weight_size = 0
    activation_size = 0
    I_size_list = []
    O_size_list = []
    MAC_count = 0
    for idx, layer in enumerate(ml_workload.nodes):
        print ()
        if isinstance(layer, InputLayerNode):
            continue
        try:
            weight_size += layer.operand_size_elem['W'] * layer.operand_precision['W'] / 8 / 1024
            activation_size += layer.operand_size_elem['I'] * layer.operand_precision['I'] / 8 / 1024
            I_size_list.append(layer.operand_size_elem['I'] * layer.operand_precision['I'] / 8 / 1024)
            O_size_list.append(layer.operand_size_elem['O'] * layer.operand_precision['O_final'] / 8 / 1024)
            MAC_count += layer.total_MAC_count
        except:
            weight_size += 0
        for operand in layer.operand_list:
            if operand == 'O':
                operand1 = 'O_final'
            else:
                operand1 = operand
            print('layer', idx,
                  ' operand', operand,
                  ' size (kB): ', layer.operand_size_elem[operand] * layer.operand_precision[operand1] / 8 / 1024)

    activation_size += layer.operand_size_elem['O'] * layer.operand_precision['O_final'] / 8 / 1024
    print('\nTotal weight size (kB): ', weight_size)
    print('\nTotal activation size (kB): ', activation_size)
    print('\nInput size (kB): ', I_size_list)
    print('Output size (kB): ', O_size_list)
    print('\nAverage Input size (kB): ', sum(I_size_list)/len(I_size_list))
    print('Average Output size (kB): ', sum(O_size_list)/len(O_size_list))
    print('\nMax Input size (kB): ', max(I_size_list))
    print('Max Output size (kB): ', max(O_size_list))

    print('\nTotal MAC count: ', MAC_count)
    G = ml_workload
    # visualize_dnn_graph(G)


