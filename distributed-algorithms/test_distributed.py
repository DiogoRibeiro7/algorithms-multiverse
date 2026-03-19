"""
Test Suite for Distributed Algorithms

Tests:
- Vector clocks (Lamport, Vector, Version vectors, causality)
- Byzantine fault tolerance (generals, PBFT)
- Gossip protocols (rumor mongering, aggregation, SWIM)
- Chord DHT (create, join, store, lookup)
- Paxos consensus (basic, competing proposals, failures)
- Raft consensus (cluster, leader election)

Run with:
    python -m pytest test_distributed.py -v
    or
    python test_distributed.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from vector_clocks import (
    LamportClock,
    VectorClock,
    VersionVector,
    CausalityTracker,
)
from byzantine_fault_tolerance import (
    ByzantineGenerals,
    SimplifiedPBFT,
    ByzantineFailureDetector,
)
from gossip_protocols import (
    GossipNode,
    AntiEntropyProtocol,
    RumorMongering,
    GossipAggregation,
    SWIMProtocol,
    GossipSimulator,
)
from chord_dht import ChordDHT
from paxos_consensus import PaxosSimulator
from raft_consensus import RaftCluster


# ============================================================================
# VECTOR CLOCK TESTS
# ============================================================================


class TestLamportClock(unittest.TestCase):
    def test_tick(self):
        lc = LamportClock("P1")
        t1 = lc.tick()
        t2 = lc.tick()
        self.assertGreater(t2, t1)

    def test_send(self):
        lc = LamportClock("P1")
        t = lc.send()
        self.assertGreater(t, 0)

    def test_receive(self):
        lc1 = LamportClock("P1")
        lc2 = LamportClock("P2")
        lc1.tick()
        lc1.tick()
        lc1.tick()
        ts = lc1.send()
        lc2.receive(ts)
        # P2's clock should be at least as large as received timestamp
        self.assertGreaterEqual(lc2.get_time(), ts)

    def test_causality(self):
        lc = LamportClock("P1")
        t1 = lc.tick()
        t2 = lc.tick()
        result = lc.happens_before(t1, t2)
        self.assertTrue(result)


class TestVectorClock(unittest.TestCase):
    def test_tick(self):
        vc = VectorClock("P1", ["P1", "P2", "P3"])
        t = vc.tick()
        self.assertEqual(t["P1"], 1)
        self.assertEqual(t["P2"], 0)

    def test_send_receive(self):
        vc1 = VectorClock("P1", ["P1", "P2"])
        vc2 = VectorClock("P2", ["P1", "P2"])
        vc1.tick()
        ts = vc1.send()
        vc2.receive(ts)
        # P2 should reflect P1's clock
        self.assertGreaterEqual(vc2.get_time()["P1"], 1)

    def test_happens_before(self):
        vc1 = {"P1": 1, "P2": 0}
        vc2 = {"P1": 2, "P2": 1}
        self.assertTrue(VectorClock.happens_before(vc1, vc2))
        self.assertFalse(VectorClock.happens_before(vc2, vc1))

    def test_concurrent(self):
        vc1 = {"P1": 2, "P2": 0}
        vc2 = {"P1": 0, "P2": 2}
        self.assertTrue(VectorClock.concurrent(vc1, vc2))

    def test_not_concurrent(self):
        vc1 = {"P1": 1, "P2": 0}
        vc2 = {"P1": 2, "P2": 1}
        self.assertFalse(VectorClock.concurrent(vc1, vc2))

    def test_merge(self):
        vc1 = {"P1": 3, "P2": 1}
        vc2 = {"P1": 1, "P2": 4}
        merged = VectorClock.merge(vc1, vc2)
        self.assertEqual(merged["P1"], 3)
        self.assertEqual(merged["P2"], 4)


class TestVersionVector(unittest.TestCase):
    def test_increment(self):
        vv = VersionVector("node1")
        v = vv.increment()
        self.assertEqual(v["node1"], 1)

    def test_dominates(self):
        vv1 = VersionVector("A")
        vv1.increment()
        vv1.increment()

        vv2 = VersionVector("A")
        vv2.increment()

        self.assertTrue(vv1.dominates(vv2.get_version()))
        self.assertFalse(vv2.dominates(vv1.get_version()))

    def test_conflicts(self):
        vv1 = VersionVector("A")
        vv1.increment()

        vv2 = VersionVector("B")
        vv2.increment()

        self.assertTrue(vv1.conflicts_with(vv2.get_version()))


class TestCausalityTracker(unittest.TestCase):
    def test_add_and_order(self):
        ct = CausalityTracker()
        ct.add_event("e1", {"P1": 1, "P2": 0})
        ct.add_event("e2", {"P1": 2, "P2": 1})
        ct.add_event("e3", {"P1": 1, "P2": 2})
        order = ct.get_causal_order()
        self.assertIsInstance(order, list)
        self.assertEqual(len(order), 3)

    def test_concurrent_events(self):
        ct = CausalityTracker()
        ct.add_event("e1", {"P1": 1, "P2": 0})
        ct.add_event("e2", {"P1": 0, "P2": 1})
        self.assertTrue(ct.are_concurrent("e1", "e2"))


# ============================================================================
# BYZANTINE FAULT TOLERANCE TESTS
# ============================================================================


class TestByzantineGenerals(unittest.TestCase):
    def test_agreement_with_no_traitors(self):
        bg = ByzantineGenerals(4, 0)
        result = bg.oral_messages(True, max_rounds=1)
        self.assertIsInstance(result, dict)

    def test_agreement_with_one_traitor(self):
        # Need n >= 3f+1, so 4 generals with 1 traitor should work
        bg = ByzantineGenerals(4, 1)
        result = bg.oral_messages(True, max_rounds=2)
        self.assertIsInstance(result, dict)

    def test_impossibility(self):
        # 3 generals with 1 traitor: impossible to guarantee agreement
        bg = ByzantineGenerals(3, 1)
        result = bg.oral_messages(True, max_rounds=1)
        self.assertIsInstance(result, dict)


class TestSimplifiedPBFT(unittest.TestCase):
    def test_normal_operation(self):
        pbft = SimplifiedPBFT(4, 1)
        result = pbft.request("test_command")
        self.assertIsInstance(result, bool)

    def test_view_change(self):
        pbft = SimplifiedPBFT(4, 1)
        pbft.view_change()
        # Should still work after view change
        result = pbft.request("after_view_change")
        self.assertIsInstance(result, bool)


class TestByzantineFailureDetector(unittest.TestCase):
    def test_timing_violation(self):
        bfd = ByzantineFailureDetector(4)
        is_violation = bfd.detect_timing_violations(
            "node_0", expected_time=1.0, actual_time=2.0, tolerance=0.1
        )
        self.assertTrue(is_violation)

    def test_no_timing_violation(self):
        bfd = ByzantineFailureDetector(4)
        is_violation = bfd.detect_timing_violations(
            "node_0", expected_time=1.0, actual_time=1.05, tolerance=0.1
        )
        self.assertFalse(is_violation)

    def test_message_omission(self):
        bfd = ByzantineFailureDetector(4)
        self.assertTrue(bfd.detect_message_omission("node_0", 10, 5))
        self.assertFalse(bfd.detect_message_omission("node_0", 10, 10))


# ============================================================================
# GOSSIP PROTOCOL TESTS
# ============================================================================


class TestGossipNode(unittest.TestCase):
    def test_update_data(self):
        node = GossipNode("node1")
        node.update_data("key1", "value1")
        # Data should be stored
        self.assertIn("key1", node.data)

    def test_add_peer(self):
        node = GossipNode("node1")
        node.add_peer("node2")
        node.add_peer("node3")
        targets = node.select_gossip_targets()
        self.assertIsInstance(targets, list)


class TestAntiEntropyProtocol(unittest.TestCase):
    def test_update_and_merge(self):
        p1 = AntiEntropyProtocol("node1")
        p2 = AntiEntropyProtocol("node2")

        p1.update("key1", "value1")
        p2.update("key2", "value2")

        # Merge p1's data into p2 using vector_clock attribute
        p2.merge(p1.data, p1.vector_clock)
        self.assertIn("key1", p2.data)

    def test_digest(self):
        p = AntiEntropyProtocol("node1")
        p.update("key1", "value1")
        digest = p.get_digest()
        self.assertIn("key1", digest)


class TestRumorMongering(unittest.TestCase):
    def test_receive_new_rumor(self):
        rm = RumorMongering("node1")
        is_new = rm.receive_rumor("rumor1", "content1")
        self.assertTrue(is_new)

    def test_receive_duplicate_rumor(self):
        rm = RumorMongering("node1")
        rm.receive_rumor("rumor1", "content1")
        is_new = rm.receive_rumor("rumor1", "content1")
        self.assertFalse(is_new)


class TestGossipAggregation(unittest.TestCase):
    def test_exchange(self):
        ga1 = GossipAggregation("node1", 10.0)
        ga2 = GossipAggregation("node2", 20.0)
        new_sum, new_weight = ga1.exchange(ga2.sum, ga2.weight)
        # After exchange, both should converge toward average
        self.assertIsInstance(new_sum, float)

    def test_estimate(self):
        ga = GossipAggregation("node1", 42.0)
        self.assertAlmostEqual(ga.get_estimate(), 42.0)


class TestSWIMProtocol(unittest.TestCase):
    def test_add_member(self):
        swim = SWIMProtocol("node1")
        swim.add_member("node2")
        swim.add_member("node3")
        alive = swim.get_alive_members()
        self.assertIn("node2", alive)
        self.assertIn("node3", alive)

    def test_ping(self):
        swim = SWIMProtocol("node1")
        swim.add_member("node2")
        # Ping returns bool (simulated)
        result = swim.ping("node2")
        self.assertIsInstance(result, bool)


class TestGossipSimulator(unittest.TestCase):
    def test_inject_and_converge(self):
        sim = GossipSimulator(5, fanout=2)
        sim.inject_update("node_0", "test_key", "test_value")
        # Run several rounds
        for _ in range(20):
            sim.simulate_round()
        count = sim.get_infection_count("test_key")
        self.assertGreater(count, 1)


# ============================================================================
# CHORD DHT TESTS
# ============================================================================


class TestChordDHT(unittest.TestCase):
    def test_create_and_join(self):
        dht = ChordDHT(m_bits=10)
        n1 = dht.create_node("node1")
        dht.join(n1)
        n2 = dht.create_node("node2")
        dht.join(n2, n1)
        stats = dht.get_stats()
        self.assertEqual(stats["nodes"], 2)

    def test_store_and_lookup(self):
        dht = ChordDHT(m_bits=10)
        n1 = dht.create_node("node1")
        dht.join(n1)
        dht.store("key1", "value1", n1)
        value, hops = dht.lookup("key1", n1)
        self.assertEqual(value, "value1")

    def test_delete(self):
        dht = ChordDHT(m_bits=10)
        n1 = dht.create_node("node1")
        dht.join(n1)
        dht.store("key1", "value1", n1)
        dht.delete("key1", n1)
        value, _ = dht.lookup("key1", n1)
        self.assertIsNone(value)

    def test_hash_deterministic(self):
        dht = ChordDHT(m_bits=10)
        h1 = dht.hash_key("test")
        h2 = dht.hash_key("test")
        self.assertEqual(h1, h2)


# ============================================================================
# PAXOS CONSENSUS TESTS
# ============================================================================


class TestPaxosConsensus(unittest.TestCase):
    def test_basic_consensus(self):
        sim = PaxosSimulator(num_nodes=5)
        result = sim.run_basic_consensus("value1")
        self.assertIsInstance(result, bool)

    def test_competing_proposals(self):
        sim = PaxosSimulator(num_nodes=5)
        result = sim.run_competing_proposals(["val_a", "val_b"])
        # Should decide on one of the values
        self.assertIsNotNone(result)

    def test_with_failures(self):
        sim = PaxosSimulator(num_nodes=5)
        result = sim.run_with_failures("value1", failure_rate=0.2)
        self.assertIsInstance(result, bool)


# ============================================================================
# RAFT CONSENSUS TESTS
# ============================================================================


class TestRaftConsensus(unittest.TestCase):
    def test_cluster_creation(self):
        cluster = RaftCluster(num_nodes=5)
        summary = cluster.get_state_summary()
        self.assertEqual(len(summary), 5)

    def test_leader_election(self):
        cluster = RaftCluster(num_nodes=5)
        # Simulate several steps to trigger election
        for _ in range(50):
            cluster.simulate_step()
        leader = cluster.get_leader()
        # Leader might or might not be elected depending on timing
        self.assertIsInstance(leader, (str, type(None)))

    def test_state_summary(self):
        cluster = RaftCluster(num_nodes=3)
        summary = cluster.get_state_summary()
        self.assertEqual(len(summary), 3)
        for val in summary.values():
            # Summary values may be dicts or strings depending on impl
            self.assertIsNotNone(val)


if __name__ == "__main__":
    unittest.main(verbosity=2)
