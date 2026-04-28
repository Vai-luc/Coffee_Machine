import pytest
from controllers.order_controller import process_order


def test_process_order_exact_payment():
    result = process_order('latte', amount_paid=3.25, size='tall', quantity=1)
    assert result['status'] == 'success'
    assert result['change'] == 0
    assert result['total'] == 3.25


def test_process_order_overpayment_returns_change():
    result = process_order('espresso', amount_paid=5.0, size='tall', quantity=1)
    assert result['status'] == 'success'
    assert result['change'] == pytest.approx(2.75)


def test_process_order_underpayment_returns_error():
    result = process_order('cappuccino', amount_paid=1.0, size='tall', quantity=1)
    assert result['status'] == 'error'
    assert 'amount_due' in result
    assert result['amount_due'] == pytest.approx(2.75)


def test_process_order_invalid_size_returns_error():
    result = process_order('latte', amount_paid=10.0, size='mega', quantity=1)
    assert result['status'] == 'error'
    assert result['message'] == 'Invalid size selection.'
