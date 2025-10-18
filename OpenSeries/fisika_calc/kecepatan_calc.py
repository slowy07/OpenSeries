from abc import ABC, abstractmethod
from typing import Union

from OpenSeries.util.error import ErrorDibagiNol, ErrorTipeData, Error
import numpy as np


class Validator:
    @staticmethod
    def validasi_numerik(
        nilai: Union[float, int], nama_parameter: str = "nilai"
    ) -> Union[float, int]:
        if not isinstance(nilai, (int, float, np.integer, np.floating)):
            raise ErrorTipeData(
                tipe_diharapkan=["int", "float"],
                tipe_sebenarnya=type(nilai).__name__,
                nama_parameter=nama_parameter,
            )
        return float(nilai) if isinstance(nilai, (int, np.integer)) else nilai

    @staticmethod
    def validasi_list_numerik(
        daftar_nilai: Union[list[Union[float, int]], np.ndarray],
        nama_parameter: str = "daftar_nilai",
    ) -> list[Union[float, int]]:
        if not isinstance(daftar_nilai, (list, np.ndarray)):
            raise ErrorTipeData(
                tipe_diharapkan=["list", "numpy.ndarray"],
                tipe_sebenarnya=type(daftar_nilai).__name__,
                nama_parameter=nama_parameter,
            )

        hasil_validasi = []
        for i, item in enumerate(daftar_nilai):
            try:
                hasil_validasi.append(
                    Validator.validasi_numerik(item, f"{nama_parameter}[{i}]")
                )
            except ErrorTipeData as e:
                raise e

        return hasil_validasi


class Kecepatan(ABC):
    @abstractmethod
    def hitung_kecepatan(
        self, jarak: Union[float, int], waktu: Union[float, int]
    ) -> float:
        pass


class KecepatanImpl(Kecepatan):
    def hitung_kecepatan(
        self, jarak: Union[float, int], waktu: Union[float, int]
    ) -> float:
        jarak = Validator.validasi_numerik(jarak, "jarak")
        waktu = Validator.validasi_numerik(waktu, "waktu")

        if waktu == 0:
            raise ErrorDibagiNol(operasi="kecepatan", dividend=jarak)

        return jarak / waktu


class KecepatanNumpy(Kecepatan):
    def hitung_kecepatan(
        self, jarak: Union[float, int], waktu: Union[float, int]
    ) -> float:
        jarak = Validator.validasi_numerik(jarak, "jarak")
        waktu = Validator.validasi_numerik(waktu, "waktu")

        if waktu == 0:
            raise ErrorDibagiNol(operasi="kecepatan", dividend=jarak)

        return np.divide(jarak, waktu)


class KecepatanProcessor:
    """
    Kelas utama untuk memproses berbagai operasi terkait perhitungan kecepatan.

    Mendukung berbagai tipe data input dan menyediakan berbagai metode pemrosesan.
    """

    def __init__(self, use_numpy: bool = False):
        """
        Inisialisasi processor kecepatan.

        Args:
            use_numpy (bool): Jika True, gunakan implementasi NumPy untuk performa lebih baik.
        """
        self.calculator = KecepatanNumpy() if use_numpy else KecepatanImpl()
        self.use_numpy = use_numpy

    def hitung_single(
        self, jarak: Union[float, int], waktu: Union[float, int]
    ) -> Union[float, ErrorDibagiNol, ErrorTipeData, Error]:
        """
        Menghitung kecepatan untuk satu pasang jarak dan waktu.

        Args:
            jarak: Jarak tempuh.
            waktu: Waktu tempuh.

        Returns:
            Union[float, ErrorDibagiNol, ErrorTipeData, ErrorNilai]:
                Hasil perhitungan atau error jika terjadi kesalahan.
        """
        try:
            hasil = self.calculator.hitung_kecepatan(jarak, waktu)
            return hasil
        except (ErrorDibagiNol, ErrorTipeData, Error) as e:
            return e

    def hitung_multiple(
        self,
        daftar_jarak: Union[list[Union[float, int]], np.ndarray],
        daftar_waktu: Union[list[Union[float, int]], np.ndarray],
    ) -> Union[list[Union[float, ErrorDibagiNol, ErrorTipeData, Error]], ErrorTipeData]:
        """
        Menghitung kecepatan untuk banyak pasang jarak dan waktu.

        Args:
            daftar_jarak: List atau array jarak tempuh.
            daftar_waktu: List atau array waktu tempuh.

        Returns:
            Union[List[Union[float, ErrorDibagiNol, ErrorTipeData, ErrorNilai]], ErrorTipeData]:
                List hasil perhitungan atau error jika terjadi kesalahan.
        """
        try:
            jarak_valid = Validator.validasi_list_numerik(daftar_jarak, "daftar_jarak")
            waktu_valid = Validator.validasi_list_numerik(daftar_waktu, "daftar_waktu")

            if len(jarak_valid) != len(waktu_valid):
                raise Error("Panjang daftar jarak dan waktu harus sama")

            hasil = []
            if (
                self.use_numpy
                and isinstance(daftar_jarak, np.ndarray)
                and isinstance(daftar_waktu, np.ndarray)
            ):
                hasil = self._hitung_vectorized_numpy(daftar_jarak, daftar_waktu)
            else:
                for j, w in zip(jarak_valid, waktu_valid):
                    hasil.append(self.hitung_single(j, w))

            return hasil

        except (ErrorTipeData, Error) as e:
            raise e

    def _hitung_vectorized_numpy(
        self, array_jarak: np.ndarray, array_waktu: np.ndarray
    ) -> list[Union[float, ErrorDibagiNol, ErrorTipeData, Error]]:
        """
        Menghitung kecepatan secara vectorized menggunakan NumPy.

        Args:
            array_jarak: Array NumPy jarak tempuh.
            array_waktu: Array NumPy waktu tempuh.

        Returns:
            List[Union[float, ErrorDibagiNol, ErrorTipeData, ErrorNilai]]: List hasil perhitungan.
        """
        hasil = []
        for j, w in zip(array_jarak, array_waktu):
            try:
                kecepatan = np.divide(float(j), float(w))
                hasil.append(kecepatan)
            except ZeroDivisionError:
                hasil.append(ErrorDibagiNol(operasi="kecepatan", dividend=float(j)))
            except Exception as e:
                hasil.append(ErrorTipeData(["float", "int"], type(e).__name__))

        return hasil

    def hitung_rata_rata(
        self, daftar_jarak, daftar_waktu
    ) -> Union[float, ErrorTipeData, Error]:
        """
        Menghitung kecepatan rata-rata dari banyak pasang jarak dan waktu.

        Args:
            daftar_jarak: List atau array jarak tempuh.
            daftar_waktu: List atau array waktu tempuh.

        Returns:
            Union[float, ErrorTipeData, ErrorKustom]: Kecepatan rata-rata atau error.
        """
        try:
            hasil_perhitungan = self.hitung_multiple(daftar_jarak, daftar_waktu)

            if isinstance(hasil_perhitungan, list):
                # Filter hanya hasil numerik
                hasil_numerik = [
                    h
                    for h in hasil_perhitungan
                    if isinstance(h, (int, float, np.number))
                ]

                if not hasil_numerik:
                    return Error("Tidak ada hasil perhitungan yang valid")

                if self.use_numpy:
                    return float(np.mean(hasil_numerik))
                else:
                    return sum(hasil_numerik) / len(hasil_numerik)
            else:
                return hasil_perhitungan

        except Exception as e:
            return Error(f"Error dalam perhitungan rata-rata: {str(e)}")

    def toggle_numpy(self, use_numpy: bool) -> None:
        """
        Mengganti implementasi calculator antara NumPy dan implementasi dasar.

        Args:
            use_numpy (bool): Jika True, gunakan NumPy; jika False, gunakan implementasi dasar.
        """
        self.calculator = KecepatanNumpy() if use_numpy else KecepatanImpl()
        self.use_numpy = use_numpy


class KecepatanFactory:
    """Factory class untuk membuat instance KecepatanProcessor."""

    @staticmethod
    def create_processor(use_numpy: bool = False) -> KecepatanProcessor:
        """
        Membuat instance KecepatanProcessor.

        Args:
            use_numpy (bool): Jika True, gunakan implementasi NumPy.

        Returns:
            KecepatanProcessor: Instance processor yang siap digunakan.
        """
        return KecepatanProcessor(use_numpy=use_numpy)

    @staticmethod
    def create_default() -> KecepatanProcessor:
        """
        Membuat instance KecepatanProcessor dengan konfigurasi default.

        Returns:
            KecepatanProcessor: Instance processor dengan konfigurasi default.
        """
        return KecepatanProcessor(use_numpy=False)


class KecepatanService:
    """Singleton service untuk operasi kecepatan."""

    _instance = None

    @classmethod
    def get_instance(cls) -> KecepatanProcessor:
        """
        Mendapatkan instance singleton dari KecepatanProcessor.

        Returns:
            KecepatanProcessor: Instance processor singleton.
        """
        if cls._instance is None:
            cls._instance = KecepatanFactory.create_default()
        return cls._instance
