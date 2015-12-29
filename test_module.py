from help_function import due_date_info_summary, calculate_profit, calculate_cost_2
# DATA数据包含4个字段，分别表示是否是自己做交易，1表示是自己做交易，0表示其他做市商做交易
DATA_1 = [[1, '2015/10/01', 100, 10], [1, '2015/11/01', 200, 16], [1, '2015/11/01', -100, 18]]
DATA_2 = [[1, '2015/11/18', 1, 100], [0, '2015/11/18', 1, 101], [1, '2015/11/18', 1, 101], [1, '2015/11/18', -1, 101]]
DATA_3 = [[1, '2015/01/01', 1000, 5], [1, '2015/10/01', 200, 10], [1, '2015/11/01', 300, 12], [1, '2015/11/18', -300, 15], [1, '2015/11/19', -200, 12], [1, '2015/11/19', 100, 10]]
DATA_4 = [[1, '2015/11/20', 1000, 5]  ]
# print(calculate_profit(DATA_3))


def test_script():
    assert due_date_info_summary(DATA_1, '2015/10/01') == (100, 1000, 100)
    assert due_date_info_summary(DATA_1, '2015/11/01') == (300, 4200, 200)
    # assert calculate_profit(DATA_2) == (0.25, 0.25)
    assert calculate_profit(DATA_3)[0] - (4491 + 2.0/3) < 0.1e-8
    assert calculate_profit(DATA_3)[1] - (986 + 2.0/3) < 0.1e-8
    assert calculate_profit(DATA_3, '2015/11/18')[0] - (48393 + 1/3) < 01e-8
    assert calculate_profit(DATA_3, '2015/11/18')[1] - 2380 < 01e-8
    print("Test passed")

test_script()

def test_calculate_cost_2():
    assert calculate_cost_2()