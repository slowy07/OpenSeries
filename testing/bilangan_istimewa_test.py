from OpenSeries.bilangan_istimewa import angka_armstrong


class TestAngkaArmstrong:
    def test_armstrong_3_digit(self):
        """Test bilangan Armstrong 3 digit"""
        assert angka_armstrong(153) == "angka armstrong"
        assert angka_armstrong(371) == "angka armstrong"
        assert angka_armstrong(407) == "angka armstrong"

    def test_armstrong_4_digit(self):
        """Test bilangan Armstrong 4 digit"""
        assert angka_armstrong(9474) == "angka armstrong"
        assert angka_armstrong(1634) == "angka armstrong"

    def test_armstrong_5_digit(self):
        """Test bilangan Armstrong 5 digit"""
        assert angka_armstrong(54748) == "angka armstrong"

    def test_armstrong_6_digit(self):
        """Test bilangan Armstrong 6 digit"""
        assert angka_armstrong(548834) == "angka armstrong"

    def test_satu_digit(self):
        """Semua angka 0-9 adalah Armstrong (n^1 = n)"""
        for i in range(10):
            assert angka_armstrong(i) == "angka armstrong"

    def test_nol(self):
        """0 adalah angka Armstrong"""
        assert angka_armstrong(0) == "angka armstrong"

    def test_bilangan_besar(self):
        assert angka_armstrong(123456789) == "bukan angka armstrong"
