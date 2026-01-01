import pytest
import random
from vector import Vector

@pytest.fixture
def oVec():
    return Vector()

def test_push_back(oVec):
    oVec.push_back(10)
    assert oVec.size() == 1

def test_push_back_stores_values(oVec):
    oVec.push_back(10)
    oVec.push_back(20)
    oVec.push_back(-5)
    assert oVec[0] == 10
    assert oVec[1] == 20
    assert oVec[2] == -5

def test_resize(oVec):
    oVec.resize(5, 0)
    assert oVec.size() == 5

def test_resize_grow_fills(oVec):
    oVec.push_back(7)
    oVec.resize(4, 0)
    assert oVec.size() == 4
    assert oVec.to_list() == [7, 0, 0, 0]

def test_resize_shrink(oVec):
    oVec.resize(5, 1)
    oVec[2] = 99
    oVec.resize(2)
    assert oVec.size() == 2
    assert oVec.to_list() == [1, 1]

def test_resize_to_zero(oVec):
    oVec.resize(5, 3)
    oVec.resize(0)
    assert oVec.size() == 0

def test_erase_shifts_left(oVec):
    for x in [10, 20, 30, 40]:
        oVec.push_back(x)
    oVec.erase(1)
    assert oVec.to_list() == [10, 30, 40]

def test_erase_first(oVec):
    oVec.resize(3, 0)
    oVec[0], oVec[1], oVec[2] = 1, 2, 3
    oVec.erase(0)
    assert oVec.to_list() == [2, 3]

def test_erase_last(oVec):
    for x in [1, 2, 3]:
        oVec.push_back(x)
    oVec.erase(2)
    assert oVec.to_list() == [1, 2]
    
def test_erase_range_middle(oVec):
    for x in [1, 2, 3, 4, 5, 6]:
        oVec.push_back(x)
    oVec.erase_range(2, 5)
    assert oVec.to_list() == [1, 2, 6]

def test_erase_range_no_change(oVec):
    for x in [1, 2, 3]:
        oVec.push_back(x)
    oVec.erase_range(1, 1)
    assert oVec.to_list() == [1, 2, 3]

def test_erase_range_all(oVec):
    oVec.resize(5, 8)
    oVec.erase_range(0, 5)
    assert oVec.size() == 0

def test_setitem_overwrites(oVec):
    oVec.push_back(1)
    oVec.push_back(2)
    oVec[1] = 99
    assert oVec[0] == 1
    assert oVec[1] == 99

def test_cap_doubles(oVec):
    caps = []
    for i in range(10):
        oVec.push_back(i)
        caps.append(oVec.capacity())
    assert all(caps[i] <= caps[i + 1] for i in range(len(caps) - 1))
    assert oVec.capacity() in (16, 32)

def test_buffer_address_changes_on_reallocation(oVec):
    prev = oVec.buffer_address()
    for i in range(100):
        oVec.push_back(i)
        curr = oVec.buffer_address()
        if curr != prev:
            return
    pytest.fail("Expected at least one reallocation but didn't see any")

def test_getitem_out_of_range_raises(oVec):
    with pytest.raises(IndexError):
        _ = oVec[0]

def test_setitem_out_of_range_raises(oVec):
    with pytest.raises(IndexError):
        oVec[0] = 5

def test_erase_out_of_range_raises(oVec):
    with pytest.raises(IndexError):
        oVec.erase(0)

def test_erase_range_invalid_raises(oVec):
    oVec.resize(3, 0)
    with pytest.raises(IndexError):
        oVec.erase_range(2, 5)
    with pytest.raises(IndexError):
        oVec.erase_range(-1, 2)
    with pytest.raises(IndexError):
        oVec.erase_range(2, 1)

def test_random_operations_match_list(oVec):
    ref = []
    random.seed(0)

    for _ in range(200):
        op = random.choice(["push", "set", "erase", "erase_range", "resize"])
        if op == "push":
            x = random.randint(-10, 10)
            oVec.push_back(x)
            ref.append(x)

        elif op == "set" and ref:
            i = random.randrange(len(ref))
            x = random.randint(-10, 10)
            oVec[i] = x
            ref[i] = x

        elif op == "erase" and ref:
            i = random.randrange(len(ref))
            oVec.erase(i)
            ref.pop(i)

        elif op == "erase_range" and ref:
            a = random.randrange(len(ref)+1)
            b = random.randrange(a, len(ref)+1)
            oVec.erase_range(a, b)
            del ref[a:b]

        elif op == "resize":
            new_n = random.randrange(0, 20)
            fill = random.randint(-2, 2)
            oVec.resize(new_n, fill)
            if new_n < len(ref):
                ref = ref[:new_n]
            else:
                ref.extend([fill] * (new_n - len(ref)))

        assert oVec.to_list() == ref