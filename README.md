# Welcome to SIPERPUS 👋

<p>SIPERPUS Merupakan aplikasi Sistem Informasi Perpustakaan Pusat (Polnep) yang berguuna untuk mengelola data buku TUGAS AKHIR yang ada diperpustakaan</p>

<hr>

**Instruksi untuk menginstall dan setup aplikasi**

Pastikan Python dan Node.js sudah terinstall di device/perangkat kalian masing masing
Setelah kalian mengclone project ini kalian jalankan perintah dibawah ini

```bash

python -m venv venv
venv/Scripts/activate
python -m pip install django
python -m pip install -U pip

```

Install beberapa lib tambahan terlebih dahulu

```bash

pip install django-cors-headers
pip install djangorestframework

```

Setelah itu arahkan / masuk ke dalam folder cd siperpus

Jalankan perintah berikut untuk menginstall Django-Tailwind

```bash

python -m pip install 'django-tailwind[reload]'
python manage.py tailwind init
python manage.py tailwind install
npm i -D daisyui@latest

```

Jika terjadi error seperti 'theme already exist' hiraukan saja
Setela itu jalankan server dan jalankan tailwind css di split terminal Visual Studio Code

```bash

python manage.py runserver
python manage.py tailwind start

```
