#!/usr/bin/env python3
"""
Test Suite for Topic Matrix Expansion & Selection Engine
Validates:
1. Topic matrix structure (8 pillars, >= 25 topics each, >= 200 topics total).
2. Strict uniqueness (0 duplicate topics across pillars).
3. E-E-A-T quality standards (no banned generic prefixes like 'Introducción a...').
4. Thematic diversity & pairwise similarity check within the matrix.
5. Topic selection engine prioritizing fresh, uncovered topics.
6. Algorithmic fallback generator producing unique tridimensional topics.
"""

import unittest
import os
import sys
from difflib import SequenceMatcher

# Import live code from scripts
sys.path.insert(0, os.path.dirname(__file__))
from publish_daily_jekyll_post import (
    TOPIC_MATRIX,
    select_next_topic,
    generate_algorithmic_topic,
    is_topic_covered,
    scan_existing_posts
)


class TestTopicMatrixExpansion(unittest.TestCase):
    def test_total_pillars(self):
        """Matrix must have exactly 8 enterprise pillars."""
        self.assertEqual(len(TOPIC_MATRIX), 8)

    def test_minimum_topics_per_pillar(self):
        """Every pillar must have at least 25 enterprise topics."""
        for pillar, topics in TOPIC_MATRIX.items():
            self.assertGreaterEqual(
                len(topics), 25,
                f"Pillar '{pillar}' has only {len(topics)} topics, expected at least 25."
            )

    def test_total_topics_count(self):
        """Matrix must contain at least 200 total topics."""
        total = sum(len(topics) for topics in TOPIC_MATRIX.values())
        self.assertGreaterEqual(total, 200, f"Total topics: {total}, expected >= 200.")

    def test_zero_duplicate_topics(self):
        """Every topic string in the matrix must be globally unique."""
        seen = {}
        for pillar, topics in TOPIC_MATRIX.items():
            for t in topics:
                t_clean = t.strip().lower()
                self.assertNotIn(
                    t_clean, seen,
                    f"Duplicate topic found: '{t}' in '{pillar}' (already in '{seen.get(t_clean)}')"
                )
                seen[t_clean] = pillar

    def test_no_banned_generic_prefixes(self):
        """Topics must avoid repetitive, uninspired introductory prefixes."""
        banned_prefixes = [
            "introducción a", "qué es ", "conceptos básicos de", "aprende a",
            "primeros pasos con", "todo sobre ", "guía para principiantes"
        ]
        for pillar, topics in TOPIC_MATRIX.items():
            for t in topics:
                t_low = t.lower()
                for bp in banned_prefixes:
                    self.assertFalse(
                        t_low.startswith(bp),
                        f"Topic '{t}' in '{pillar}' starts with banned prefix '{bp}'"
                    )

    def test_pairwise_similarity_within_matrix(self):
        """No two topics in the matrix should have excessive textual similarity (> 75%)."""
        all_topics = []
        for pillar, topics in TOPIC_MATRIX.items():
            all_topics.extend(topics)

        for i in range(len(all_topics)):
            for j in range(i + 1, len(all_topics)):
                t1, t2 = all_topics[i], all_topics[j]
                ratio = SequenceMatcher(None, t1.lower(), t2.lower()).ratio()
                self.assertLess(
                    ratio, 0.75,
                    f"Excessive topic similarity ({ratio*100:.1f}%):\n  1: '{t1}'\n  2: '{t2}'"
                )

    def test_topic_selection_prefers_uncovered(self):
        """select_next_topic must return an uncovered topic from the matrix."""
        existing_posts = scan_existing_posts()
        topic, pillar = select_next_topic(existing_posts)
        self.assertIsNotNone(topic)
        self.assertIn(pillar, TOPIC_MATRIX)
        # Verify the chosen topic is not already covered
        covered = is_topic_covered(topic, existing_posts, threshold=0.40)
        self.assertFalse(covered, f"Topic '{topic}' was selected but is already considered covered!")

    def test_algorithmic_fallback_generator(self):
        """generate_algorithmic_topic must produce a valid topic and recognized pillar."""
        existing_posts = scan_existing_posts()
        topic, pillar = generate_algorithmic_topic(existing_posts)
        self.assertIsNotNone(topic)
        self.assertGreater(len(topic), 20)
        self.assertIn(pillar, TOPIC_MATRIX)


if __name__ == "__main__":
    unittest.main()
