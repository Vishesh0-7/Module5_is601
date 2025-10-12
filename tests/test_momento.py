import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation


class TestCalculatorMemento:
    """Test suite for CalculatorMemento class."""

    def test_memento_creation_empty_history(self):
        """Test creating a memento with empty history."""
        memento = CalculatorMemento(history=[])
        assert memento.history == []
        assert isinstance(memento.timestamp, datetime)

    def test_memento_creation_with_history(self):
        """Test creating a memento with calculation history."""
        calc1 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
        calc2 = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("2"))
        
        memento = CalculatorMemento(history=[calc1, calc2])
        
        assert len(memento.history) == 2
        assert memento.history[0] == calc1
        assert memento.history[1] == calc2
        assert isinstance(memento.timestamp, datetime)

    def test_memento_custom_timestamp(self):
        """Test creating a memento with a custom timestamp."""
        custom_time = datetime(2024, 1, 15, 10, 30, 0)
        memento = CalculatorMemento(history=[], timestamp=custom_time)
        
        assert memento.timestamp == custom_time

    def test_memento_default_timestamp_is_recent(self):
        """Test that default timestamp is set to current time."""
        before = datetime.now()
        memento = CalculatorMemento(history=[])
        after = datetime.now()
        
        assert before <= memento.timestamp <= after

    def test_to_dict_empty_history(self):
        """Test converting memento with empty history to dictionary."""
        memento = CalculatorMemento(history=[])
        result = memento.to_dict()
        
        assert result['history'] == []
        assert 'timestamp' in result
        assert isinstance(result['timestamp'], str)

    def test_to_dict_with_history(self):
        """Test converting memento with history to dictionary."""
        calc1 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
        calc2 = Calculation(operation="Multiplication", operand1=Decimal("4"), operand2=Decimal("5"))
        
        memento = CalculatorMemento(history=[calc1, calc2])
        result = memento.to_dict()
        
        assert len(result['history']) == 2
        assert result['history'][0]['operation'] == "Addition"
        assert result['history'][0]['result'] == "5"
        assert result['history'][1]['operation'] == "Multiplication"
        assert result['history'][1]['result'] == "20"
        assert isinstance(result['timestamp'], str)

    def test_to_dict_timestamp_format(self):
        """Test that timestamp is properly formatted in ISO format."""
        custom_time = datetime(2024, 1, 15, 10, 30, 45, 123456)
        memento = CalculatorMemento(history=[], timestamp=custom_time)
        result = memento.to_dict()
        
        assert result['timestamp'] == custom_time.isoformat()

    def test_from_dict_empty_history(self):
        """Test creating memento from dictionary with empty history."""
        data = {
            'history': [],
            'timestamp': datetime.now().isoformat()
        }
        
        memento = CalculatorMemento.from_dict(data)
        
        assert memento.history == []
        assert isinstance(memento.timestamp, datetime)

    def test_from_dict_with_history(self):
        """Test creating memento from dictionary with calculation history."""
        data = {
            'history': [
                {
                    'operation': 'Addition',
                    'operand1': '2',
                    'operand2': '3',
                    'result': '5',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'operation': 'Division',
                    'operand1': '10',
                    'operand2': '2',
                    'result': '5',
                    'timestamp': datetime.now().isoformat()
                }
            ],
            'timestamp': datetime(2024, 1, 15, 10, 30, 0).isoformat()
        }
        
        memento = CalculatorMemento.from_dict(data)
        
        assert len(memento.history) == 2
        assert memento.history[0].operation == 'Addition'
        assert memento.history[0].result == Decimal('5')
        assert memento.history[1].operation == 'Division'
        assert memento.history[1].result == Decimal('5')
        assert memento.timestamp == datetime(2024, 1, 15, 10, 30, 0)

    def test_from_dict_preserves_timestamp(self):
        """Test that from_dict correctly parses and preserves timestamp."""
        original_time = datetime(2024, 3, 20, 14, 25, 30, 500000)
        data = {
            'history': [],
            'timestamp': original_time.isoformat()
        }
        
        memento = CalculatorMemento.from_dict(data)
        
        assert memento.timestamp == original_time

    def test_round_trip_serialization_empty(self):
        """Test that serialization and deserialization preserves empty memento."""
        original = CalculatorMemento(history=[], timestamp=datetime(2024, 1, 1, 12, 0, 0))
        
        # Serialize to dict
        data = original.to_dict()
        
        # Deserialize back to memento
        restored = CalculatorMemento.from_dict(data)
        
        assert len(restored.history) == len(original.history)
        assert restored.timestamp == original.timestamp

    def test_round_trip_serialization_with_history(self):
        """Test that serialization and deserialization preserves memento with history."""
        calc1 = Calculation(operation="Addition", operand1=Decimal("10"), operand2=Decimal("20"))
        calc2 = Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("3"))
        calc3 = Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("2"))
        
        original = CalculatorMemento(
            history=[calc1, calc2, calc3],
            timestamp=datetime(2024, 6, 15, 9, 30, 0)
        )
        
        # Serialize to dict
        data = original.to_dict()
        
        # Deserialize back to memento
        restored = CalculatorMemento.from_dict(data)
        
        assert len(restored.history) == 3
        assert restored.history[0].operation == "Addition"
        assert restored.history[0].result == Decimal("30")
        assert restored.history[1].operation == "Power"
        assert restored.history[1].result == Decimal("8")
        assert restored.history[2].operation == "Root"
        assert restored.history[2].result == Decimal("4")
        assert restored.timestamp == original.timestamp

    def test_memento_with_multiple_operations(self):
        """Test memento with various calculation operations."""
        calculations = [
            Calculation(operation="Addition", operand1=Decimal("1"), operand2=Decimal("2")),
            Calculation(operation="Subtraction", operand1=Decimal("10"), operand2=Decimal("3")),
            Calculation(operation="Multiplication", operand1=Decimal("4"), operand2=Decimal("5")),
            Calculation(operation="Division", operand1=Decimal("20"), operand2=Decimal("4")),
            Calculation(operation="Power", operand1=Decimal("3"), operand2=Decimal("2")),
            Calculation(operation="Root", operand1=Decimal("25"), operand2=Decimal("2"))
        ]
        
        memento = CalculatorMemento(history=calculations)
        
        assert len(memento.history) == 6
        assert memento.history[0].result == Decimal("3")
        assert memento.history[1].result == Decimal("7")
        assert memento.history[2].result == Decimal("20")
        assert memento.history[3].result == Decimal("5")
        assert memento.history[4].result == Decimal("9")
        assert memento.history[5].result == Decimal("5")

    def test_to_dict_structure(self):
        """Test that to_dict returns correct structure."""
        calc = Calculation(operation="Addition", operand1=Decimal("5"), operand2=Decimal("5"))
        memento = CalculatorMemento(history=[calc])
        result = memento.to_dict()
        
        assert isinstance(result, dict)
        assert 'history' in result
        assert 'timestamp' in result
        assert isinstance(result['history'], list)
        assert len(result['history']) == 1
        assert isinstance(result['history'][0], dict)

    def test_from_dict_with_different_timestamp_formats(self):
        """Test from_dict handles ISO format timestamp correctly."""
        # Test with microseconds
        data1 = {
            'history': [],
            'timestamp': '2024-01-15T10:30:45.123456'
        }
        memento1 = CalculatorMemento.from_dict(data1)
        assert memento1.timestamp.microsecond == 123456
        
        # Test without microseconds
        data2 = {
            'history': [],
            'timestamp': '2024-01-15T10:30:45'
        }
        memento2 = CalculatorMemento.from_dict(data2)
        assert memento2.timestamp.microsecond == 0

    def test_memento_history_is_list_of_calculations(self):
        """Test that memento history contains Calculation instances."""
        calc1 = Calculation(operation="Addition", operand1=Decimal("1"), operand2=Decimal("1"))
        calc2 = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
        
        memento = CalculatorMemento(history=[calc1, calc2])
        
        for calc in memento.history:
            assert isinstance(calc, Calculation)

    def test_large_history(self):
        """Test memento with a large number of calculations."""
        calculations = [
            Calculation(operation="Addition", operand1=Decimal(str(i)), operand2=Decimal("1"))
            for i in range(100)
        ]
        
        memento = CalculatorMemento(history=calculations)
        
        assert len(memento.history) == 100
        
        # Test serialization with large history
        data = memento.to_dict()
        assert len(data['history']) == 100
        
        # Test deserialization
        restored = CalculatorMemento.from_dict(data)
        assert len(restored.history) == 100