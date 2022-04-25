#!/bin/python3


from pptrees.prefix_graph import prefix_node as node
from pptrees.adder_tree import adder_tree as tree
from pptrees.util import lg

n = 8

g = tree(n)
# assert(g._checkLF(7,7)==(g[7,7],g[6,6],[g[7,5]],[g[6,4]]))
# assert(g._checkLT(7,7)==(g[7,7],g[6,6]))
# assert(g._checkLT(3)==(g[3,3],g[2,2]))
# assert(g._checkLF(2,2)==(g[2,2],g[1,1],[g[2,1]],[g[1,0]]))
# assert(g._checkLT(2)==(None,None))

# assert(g._checkFT(7)==(None,None,None,None))
# assert(g._checkTF(7)==(None,None))
# assert(g._checkFL(7,7)==(g[7,7],g[6,7]))
# assert(g._checkTL(7)==(None,None))

# assert(len(g)==7)
# g.trim_layer()
# assert(len(g)==7)


def sklansky():
    # Start from ripple-carry
    # Reduce layer by layer
    # From a total of n layers
    # To a total of lg(n) layers
    for a in range(1, n):
        if a & (a - 1) == 0:
            continue
        g.batch_transform("LF", a, n)
        g.png("{0}.png".format(a - lg(n)))
    g.png("sklansky.png")


def koggestone():
    # Start from ripple-carry
    # Reduce 1st layer
    g.LT(7)

    # Reduce 2nd layer
    g.LT(6)
    g.LT(7)

    # Reduce 3rd layer
    g.LT(5)
    g.LT(6)
    g.LT(7)

    # Reduce 4th layer
    g.LT(3)
    g.LT(4)
    g.LT(5)
    g.LT(6)
    g.LT(7)
    g.png("koggestone.png")


def brentkung():
    # Start from Sklansky
    sklansky()

    g.harris_step("FL", 2)

    g.png("brentkung.png")


def ladnerfischer():
    # Start from Sklansky
    sklansky()

    g.harris_step("FL", 1)

    g.png("ladnerfischer.png")


def knowles():
    # Start from Sklansky
    sklansky()
    g.FT(4)
    g.FT(4)
    g.FT(5)
    g.FT(5)
    g.png("knowles.png")


#    g.TF(5)
#    g.png('4.png')


def koggestone():
    # Start from Knowles
    knowles()
    g.FT(2)
    g.FT(4)
    g.FT(6)
    g.FT(4)
    g.FT(6)
    g.png("koggestone.png")


def demo():
    g = tree(8)
    g.png("00.png")
    g.png("01.png")
    g.png("02.png")
    g.png("03.png")
    g.png("04.png")
    g.LF(7)
    g.compress()
    g.png("05.png")
    g.LF(5)
    g.compress()
    g.png("06.png")
    g.LF(3)
    g.compress()
    g.png("07.png")
    g.LF(7)
    g.png("08.png")
    g.trim_layer()
    g.trim_layer()
    g.png("09.png")
    g.shift_node(g[4, 3], g.bot)
    g.shift_node(g[4, 4], g.bot)
    g.shift_node(g[6, 4], g.bot)
    g.shift_node(g[5, 3], g.bot)
    g.shift_node(g[2, 2], g.bot)
    g.shift_node(g[2, 3], g.bot)
    g.shift_node(g[2, 4], g.bot)
    g.png("10.png")
    g.png("11.png")
    g.png("12.png")
    g.png("13.png")
    g.png("14.png")
    g.LF(6)
    g.png("15.png")
    g.compress()
    g.png("16.png")
    g.png("17.png")
    g.png("18.png")
    g.png("19.png")
    g.png("20.png")
    g.FT(7)
    g.png("21.png")
    g.FT(6)
    g.png("22.png")
    g.FT(7, 2)
    g.png("23.png")
    g.FT(5, 2)
    g.png("24.png")
    g.FT(3, 2)
    g.png("25.png")
    g.FT(7)
    g.png("26.png")
    g.FT(5)
    g.png("27.png")
    g.png("28.png")
    g.png("29.png")
    g.png("30.png")
    g.png("31.png")
    g.TF(7, 3)
    g.png("32.png")
    g.TF(5, 3)
    g.png("33.png")
    g.TF(7, 2)
    g.remove_node(g[6, 1])
    g.add_node(node(6, 1, "buffer_node"))
    g.png("34.png")
    g.TF(5, 2)
    g.remove_node(g[4, 1])
    g.add_node(node(4, 1, "buffer_node"))
    g.png("35.png")
    g.TF(3, 2)
    g.remove_node(g[2, 1])
    g.add_node(node(2, 1, "buffer_node"))
    g.png("36.png")
    g.png("37.png")
    g.png("38.png")
    g.png("39.png")
    g.png("40.png")


def LFT():
    g = tree(4)
    g.png("L.png")
    g.LF(3)
    g.png("F.png")
    g.FT(2)
    g.png("T.png")


def paper_review():
    n = 64
    g = tree(n)
    g.harris_step("FL", 1)
    g.harris_step("FL", 1)
    g.harris_step("FL", 1)
    g.harris_step("FL", 1)
    g.harris_step("FL", 1)
    print("hi")
    g.LF(47)
    g.LF(51)
    g.LF(53)
    g.LF(54)
    g.LF(51)
    g.LF(53)
    g.LF(54)
    g.png("1.png")

    print("hi")
    g.LF(51)
    g.LF(54)

    print("hi")
    g.LF(54)
    g.png("2.png")
    print("hi")
    g.png("3.png")
    print("hi")
    g.FT(47)
    g.png("4.png")
    # Re-calculate the tree
    pre_processing = g.node_list[0]
    for n in pre_processing:
        g.walk_downstream(n, fun=g._recalc_pg)

    # Check that tree remains valid
    post_processing = g.node_list[-1]
    for i in range(len(post_processing)):
        assert all(post_processing[i].pg[: i + 1])
        assert post_processing[i].m in ["post_node"]
    g.hdl("hdl64/brent_kung_mod.v")


def sk_bk(n, hybrid=False):
    g = tree(n, "sklansky")
    #    g.hdl('hdl{0}/pure_sklansky.v'.format(n))
    g.png("1.png")
    if hybrid:
        g.harris_step("FL", lg(n), top_bit=n // 2)
        g.png("3.png")
    #        g.hdl('hdl{0}/sklanksy_brentkung.v'.format(n))
    else:
        g.harris_step("FL", lg(n))
        g.png("2.png")
    #        g.hdl('hdl{0}/pure_brentkung.v'.format(n))
    g.check_tree()


def test(n):
    g = tree(n, "sklansky")
    g.harris_step("FL", top_bit=4)
    g.harris_step("FL", top_bit=8)
    g.harris_step("FL", top_bit=16)
    # Ladner-Fischer
    g.png("1.png")

    g.FT(9, 4)
    g.FT(9, 4)
    g.FT(11, 4)
    g.FT(11, 4)

    g.FT(5, 3)
    g.FT(9, 3)
    g.FT(13, 3)
    # Harris
    g.png("2.png")

    #    g.harris_step('FL',top_bit=16)
    #    g.FL(5)
    #    # Ladner-Fischer
    #    g.png('2.png')
    #    g.FT(11,4)
    #    # Han-Carlson
    #    g.png('4.png')

    #    g.harris_step('FL',top_bit=16)
    #    print('hi')
    #    g.png('3.png')
    #    g.harris_step('LF',top_bit=16)
    #    print('hi')
    #    g.png('4.png')

    #    g.harris_step('FL',lg(n)-1)
    g.check_tree()
    g.recalc_weights()
    g.add_best_blocks()
    g.png("3.png")
    g.hdl("16b_harris_good.v")


def test2(n):
    g = tree(n, "kogge-stone")
    g.png("1.png")
    g.TF(4, 3)
    g.TF(6, 3)
    g.png("2.png")
    g.TF(2)
    g.FL(2)
    g.FL(4)
    g.TF(4, 4)
    g.FL(6)
    g.TF(6, 4)
    g.FL(2)
    g.LF(2)
    g.FT(6, 4)
    g.LF(6)
    g.FT(4, 4)
    g.LF(4)
    g.LF(2)
    g.FT(2, 2)
    g.FT(4, 2)
    g.FT(6, 2)
    g.png("3.png")
    g.FT(4, 3)
    g.FT(4, 3)
    g.FT(5, 3)
    g.FT(5, 3)
    g.FT(4, 2)
    g.FT(4, 3)
    g.FT(6, 3)
    g.png("4.png")
    g.check_tree()


def hdl_test():
    g = tree(8, "sklansky")
    g.png("1.png")
    #    g.add_block(g[0,0],g[1,1],g[3,2],g[4,3])
    g.add_best_blocks()
    g.png("2.png")
    g.hdl("test.v")


def test3_bk(n):
    g = tree(n, "sklansky")
    g.harris_step("FL", top_bit=4)
    g.harris_step("FL", top_bit=8)
    g.harris_step("FL", top_bit=16)
    g.harris_step("FL", top_bit=32)
    g.harris_step("FL", 5, top_bit=64)
    #    g.hdl('{0}b_brent-kung_flat.v'.format(n))
    #    exit()
    g.hdl("{0}b_brent-kung_unflat.v".format(n))
    g = tree(n, "sklansky")
    g.harris_step("FL", top_bit=4)
    g.harris_step("FL", top_bit=8)
    g.harris_step("FL", top_bit=16)
    g.harris_step("FL", top_bit=32)
    g.harris_step("FL", 5, top_bit=64)
    g.png("1.png")
    g.recalc_weights()
    g.add_best_blocks()
    g.png("2.png")
    g.hdl("{0}b_brent-kung_good.v".format(n))


def test3_sk(n):
    g = tree(n, "sklansky")
    # g.hdl('{0}b_sklansky_flat.v'.format(n))
    # exit()
    g.hdl("{0}b_sklansky_unflat.v".format(n))
    g = tree(n, "sklansky")
    g.png("1.png")
    g.recalc_weights()
    g.add_best_blocks()
    g.png("2.png")
    g.hdl("{0}b_sklansky_good.v".format(n))


def test3_ks(n):
    g = tree(n, "kogge-stone")
    # g.hdl('{0}b_kogge-stone_flat.v'.format(n))
    # exit()
    g.hdl("{0}b_kogge-stone_unflat.v".format(n))
    g = tree(n, "kogge-stone")
    g.png("1.png")
    g.recalc_weights()
    g.add_best_blocks()
    g.png("2.png")


# LFT()
# knowles()
# koggestone()
# ladnerfischer()
# brentkung()
# sklansky()
test(16)
# test2(8)
# test3_ks(64)
# hdl_test()

# sk_bk(32,False)
# sk_bk(64,False)
# sk_bk(128,False)
# sk_bk(32,True)
# sk_bk(64,True)
# sk_bk(128,True)

g.check_tree()
