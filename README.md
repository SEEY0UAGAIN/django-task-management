# django-task-management # ระบบบริหารจัดการข้อมูลการเพาะปลูกแปลงใหญ่ข้าวอินทรีย์ตลุกกลางทุ่ง 🌾

โปรเจกต์นี้เป็นระบบ Web Application ที่พัฒนาด้วย Django Framework เพื่อช่วยเกษตรกรบริหารจัดการการเพาะปลูกข้าวอินทรีย์ โดยเฉพาะกลุ่มแปลงใหญ่ตลุกกลางทุ่ง จังหวัดตาก ซึ่งมีสมาชิกจำนวนมากและทรัพยากรทางการเกษตรที่จำกัด

## 🎯 วัตถุประสงค์ของระบบ

- เพื่อให้เกษตรกรสามารถจองการใช้ทรัพยากรที่เป็นของส่วนกลางได้ง่าย
- เพื่อลดปัญหาการจองทรัพยากรซ้ำซ้อนในช่วงฤดูเก็บเกี่ยว
- เพื่อเปลี่ยนกระบวนการทำเกษตรแบบดั้งเดิมให้เป็นระบบดิจิทัลที่เข้าถึงง่ายและง่ายต่อการติดตามของหัวหน้ากลุ่ม

## 🚜 ฟีเจอร์เด่นของระบบ

- ระบบจองล่วงหน้าเครื่องมือ/อุปกรณ์การเกษตร
- ระบบบริหารจัดการช่วงเวลาการใช้งาน
- ระบบจัดเก็บประวัติการจองของแต่ละเกษตรกร
- ระบบจะช่วยให้หัวหน้ากลุ่มติดตามขั้นตอนการเพาะปลูก: เตรียมดิน → เพาะปลูก → ดูแล → เก็บเกี่ยว 
- ออกแบบให้ใช้งานง่ายบนโทรศัพท์ (Responsive Design)

## 🛠 เทคโนโลยีที่ใช้

- Backend: Django (Python)
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Database: SQLite

## 🖥 วิธีการติดตั้ง (สำหรับนักพัฒนา)

```bash
# clone โปรเจกต์
git clone https://github.com/SEEY0UAGAIN/django-task-management.git
cd django-task-management

# สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # หรือ venv\Scripts\activate สำหรับ Windows

# ติดตั้ง dependencies
pip install -r requirements.txt

# สร้าง database และรันเซิร์ฟเวอร์
python manage.py migrate
python manage.py runserver
