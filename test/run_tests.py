#!/usr/bin/env python3
#
# Trilobite AppHub:
# author: Michael Gene Brockus (Dreamer)
# Gmail: <mail: michaelbrockus@gmail.com>
#
from code.program import greet

#
# Test cases for this project.
#
class TestFixture:
    def test_basic_assert_works(self):
        assert True
    # end of case

    def test_greet_not_none(self):
        assert greet() is not None
    # end of case

# end of fixture
