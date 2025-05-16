
from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# إعداد قاعدة البيانات (ملف على القرص لأجل الاحتفاظ بالبيانات)
conn = sqlite3.connect('simple.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY, type TEXT, amount REAL, commission REAL,
              account TEXT, wallet TEXT, date TEXT, notes TEXT)''')
conn.commit()
conn.close()

HTML_TEMPLATE = '''
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>فودا كاش - نسخة مبسطة</title>
</head>
<body>
  <h2>إضافة عملية</h2>
  <form method="POST">
    النوع:
    <select name="type">
      <option value="سحب">سحب</option>
      <option value="إيداع">إيداع</option>
    </select><br>
    المبلغ: <input name="amount" type="number" step="0.01" required><br>
    العمولة %: <input name="commission" type="number" step="0.01" required><br>
    الحساب: <input name="account" required><br>
    المحفظة: <input name="wallet" required><br>
    التاريخ: <input name="date" type="date" required><br>
    ملاحظات: <input name="notes"><br>
    <button type="submit">إضافة</button>
  </form>

  <h3>العمليات</h3>
  <table border="1" cellspacing="0" cellpadding="5">
    <tr><th>النوع</th><th>المبلغ</th><th>العمولة</th><th>الحساب</th><th>المحفظة</th><th>التاريخ</th><th>ملاحظات</th></tr>
    {% for row in transactions %}
      <tr>
        <td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}%</td>
        <td>{{ row[4] }}</td><td>{{ row[5] }}</td><td>{{ row[6] }}</td><td>{{ row[7] }}</td>
      </tr>
    {% endfor %}
  </table>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = sqlite3.connect('simple.db')
        c = conn.cursor()
        c.execute("INSERT INTO transactions (type, amount, commission, account, wallet, date, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (request.form['type'], request.form['amount'], request.form['commission'],
                   request.form['account'], request.form['wallet'], request.form['date'], request.form['notes']))
        conn.commit()
        conn.close()
        return redirect('/')

    conn = sqlite3.connect('simple.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
