import unittest
import torch
from pytorch_metric_learning.reducers import DivisorReducer

class TestDivisorReducer(unittest.TestCase):
    def test_divisor_reducer(self):
        reducer = DivisorReducer()
        batch_size = 100
        embedding_size = 64
        embeddings = torch.randn(batch_size, embedding_size)
        labels = torch.randint(0,10,(batch_size,))
        pair_indices = (torch.randint(0,batch_size,(batch_size,)), torch.randint(0,batch_size,(batch_size,)))
        triplet_indices = pair_indices + (torch.randint(0,batch_size,(batch_size,)),)
        losses = torch.randn(batch_size)

        for indices, reduction_type in [(torch.arange(batch_size), "element"),
                                        (pair_indices, "pos_pair"),
                                        (pair_indices, "neg_pair"),
                                        (triplet_indices, "triplet"),
                                        (None, "already_reduced")]:
            for partA, partB in [(0,0), (32,15)]:
                if reduction_type == "already_reduced":
                    L = losses[0]
                else:
                    L = losses
                loss_dict = {"loss": {"losses": L, "indices": indices, "reduction_type": reduction_type, "divisor_summands": {"partA": partA, "partB": partB}}}
                output = reducer(loss_dict, embeddings, labels)
                if partA+partB == 0:
                    correct_output = torch.sum(L)*0
                else:
                    correct_output = torch.sum(L) / (32+15)
                self.assertTrue(output == correct_output)

        
        loss_dict = {"loss": {"losses": losses[0], "indices": None, "reduction_type": "already_reduced"}}
        output = reducer(loss_dict, embeddings, labels)
        correct_output = losses[0]
        self.assertTrue(output == correct_output)
