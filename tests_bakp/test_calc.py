import pytest
from app.calculation import add, subtract, multiply, divide, BankAccount

#@pytest.mark.parametrize("num1,num2,results", [])
def test_add():
    assert add(5,3) == 8

def test_Sub():
    assert subtract(9,4) == 5

def test_bank_set_ini_amt():
    Bank_AC =  BankAccount(50)
    assert Bank_AC.balance == 50


 