# gui.py

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os
import calendar
from utils import setup_locale

SAVE_FILE = "last_result.json"
from budgeting import BudgetCalculator

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

class BudgetGUI:
    def __init__(self, root):
        setup_locale()
        self.root = root
        self.root.title("Budgeting Transportasi Profesional")
        self.root.geometry("1000x700")
        self._build_gui()
        self._load_last()

    def _build_gui(self):
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill='both', expand=True)

        control = ttk.Frame(container)
        control.pack(fill='x', pady=(0,20))

        ttk.Label(control, text="Tahun:").grid(row=0, column=0, sticky='w')
        today = datetime.today()
        yrs = [str(y) for y in range(today.year, today.year+6)]
        self.year_cb = ttk.Combobox(control, values=yrs, state="readonly", width=6)
        self.year_cb.current(0)
        self.year_cb.grid(row=0, column=1, padx=5)
        self.year_cb.bind("<<ComboboxSelected>>", self._update_months)

        ttk.Label(control, text="Bulan:").grid(row=0, column=2, sticky='w')
        self.month_cb = ttk.Combobox(control, state="readonly", width=6)
        self.month_cb.grid(row=0, column=3, padx=5)
        self._update_months()

        ttk.Label(control, text="Saldo KMT:").grid(row=0, column=4, sticky='w')
        self.saldo_var = tk.IntVar(value=0)
        ttk.Entry(control, textvariable=self.saldo_var, width=10).grid(row=0, column=5, padx=5)

        ttk.Button(control, text="Generate", command=self._on_generate).grid(row=0, column=6, padx=20)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill='both', expand=True)

        self.summary_tab = ttk.Frame(self.notebook)
        self.details_tab = ttk.Frame(self.notebook)
        self.chart_tab   = ttk.Frame(self.notebook)

        self.notebook.add(self.summary_tab, text='Summary')
        self.notebook.add(self.details_tab, text='Details')
        self.notebook.add(self.chart_tab,   text='Charts')

        cards = ttk.Frame(self.summary_tab)
        cards.pack(fill='x', pady=10)
        self.card_total = ttk.Label(cards, text='Total: -', font=('Helvetica',16,'bold'))
        self.card_final = ttk.Label(cards, text='Setelah Saldo: -', font=('Helvetica',14))
        self.card_krl   = ttk.Label(cards, text='KRL: -',   font=('Helvetica',14))
        self.card_krd   = ttk.Label(cards, text='KRD: -',   font=('Helvetica',14))
        for w in (self.card_total, self.card_final, self.card_krl, self.card_krd):
            w.pack(side='left', expand=True, padx=10)

        self.gen_label = ttk.Label(self.summary_tab, text='')
        self.gen_label.pack(pady=(0,10))

        cols = ('Date','Day','KRL','KRD','Total')
        self.tree = ttk.Treeview(self.details_tab, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor='center')
        vsb = ttk.Scrollbar(self.details_tab, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        if HAS_MPL:
            # Only use Figure if matplotlib is available
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            fig = Figure(figsize=(6,4), dpi=100)
            self.ax1 = fig.add_subplot(211)
            self.ax2 = fig.add_subplot(212)
            self.canvas = FigureCanvasTkAgg(fig, master=self.chart_tab)
            self.canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            ttk.Label(self.chart_tab, text="Matplotlib tidak terpasang\nCharts disabled", anchor='center').pack(expand=True)

    def _update_months(self, event=None):
        year = int(self.year_cb.get())
        today = datetime.today()
        start_m = 1 if year > today.year else today.month
        vals = [str(m) for m in range(start_m,13)]
        self.month_cb['values'] = vals
        self.month_cb.current(0)

    def _on_generate(self):
        yr    = int(self.year_cb.get())
        mo    = int(self.month_cb.get())
        saldo = self.saldo_var.get()
        last  = calendar.monthrange(yr,mo)[1]
        day0  = 29 if last>=29 else last
        start = datetime(yr, mo, day0)
        end   = datetime(yr + (mo==12), (mo%12)+1, 28)
        calc  = BudgetCalculator(start, end)
        calc.calculate()
        gen_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        self._update_summary(calc, saldo, gen_time)
        self._update_details(calc)
        if HAS_MPL:
            self._update_charts(calc)
        self.notebook.select(self.summary_tab)
        self._save_last(calc, saldo, yr, mo, gen_time)

    def _update_summary(self, calc, saldo=0, gen_time=None):
        final = calc.total - saldo
        if final < 0:
            final = 0
        self.card_total.config(text=f"Total: Rp{calc.total:,}")
        self.card_final.config(text=f"Setelah Saldo: Rp{final:,}")
        self.card_krl.config(text=f"KRL: Rp{calc.total_krl:,}")
        self.card_krd.config(text=f"KRD: Rp{calc.total_krd:,}")
        if gen_time:
            self.gen_label.config(text=f"Dibuat: {gen_time}")

    def _update_details(self, calc):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for date,day,krl,krd in calc.daily_logs:
            tot = krl+krd
            self.tree.insert('', 'end', values=(
                date.strftime('%d-%m-%Y'),
                day.capitalize(),
                f"Rp{krl:,}",
                f"Rp{krd:,}",
                f"Rp{tot:,}"
            ))

    def _update_charts(self, calc):
        dates  = [d.strftime('%d-%b') for d,_,_,_ in calc.daily_logs]
        totals = [k+kr for _,_,k,kr in calc.daily_logs]
        self.ax1.clear()
        self.ax1.bar(dates, totals)
        self.ax1.set_title('Biaya Harian')
        self.ax1.tick_params(axis='x', rotation=45)
        self.ax2.clear()
        self.ax2.pie([calc.total_krl, calc.total_krd],
                     labels=['KRL','KRD'], autopct='%1.1f%%')
        self.ax2.set_title('Distribusi KRL vs KRD')
        self.canvas.draw()

    def _save_last(self, calc, saldo, year, month, gen_time):
        data = {
            'year': year,
            'month': month,
            'saldo': saldo,
            'generated_at': gen_time,
            'total_krl': calc.total_krl,
            'total_krd': calc.total_krd,
            'daily_logs': [
                (d.strftime('%Y-%m-%d'), day, krl, krd)
                for d, day, krl, krd in calc.daily_logs
            ]
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)

    def _load_last(self):
        if not os.path.exists(SAVE_FILE):
            return
        with open(SAVE_FILE) as f:
            data = json.load(f)

        self.year_cb.set(str(data['year']))
        self._update_months()
        self.month_cb.set(str(data['month']))
        self.saldo_var.set(data.get('saldo', 0))

        class Calc:
            def __init__(self, d):
                self.total_krl = d['total_krl']
                self.total_krd = d['total_krd']
                self.daily_logs = [
                    (datetime.strptime(dt, '%Y-%m-%d'), day, krl, krd)
                    for dt, day, krl, krd in d['daily_logs']
                ]

            @property
            def total(self):
                return self.total_krl + self.total_krd

        calc = Calc(data)
        gen_time = data.get('generated_at')
        self._update_summary(calc, data.get('saldo', 0), gen_time)
        self._update_details(calc)
        if HAS_MPL:
            self._update_charts(calc)

